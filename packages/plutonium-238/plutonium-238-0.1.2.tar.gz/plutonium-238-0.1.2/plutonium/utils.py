import subprocess
import logging
import os
import sys
import shutil
import requests
import plutonium.config as config

# log format
formatter = logging.Formatter(config.LOG_FORMAT)
logger = logging.getLogger(__name__)

# file logger
file_handler = logging.FileHandler(config.LOG_FILENAME)
file_handler.setFormatter(formatter)

# console logger
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# init logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(config.LOG_LEVEL)

def filter_ignored_dirs(dirs):
    """
    Method to filter directory list to remove ignored directories
    :param dirs: Directories to ignore
    :return: Filtered directory list
    """
    [
        dirs.remove(d)
        for d in list(dirs)
        if d.lower() in config.ignore_directories or d.startswith(".")
    ]
    return dirs

def find_python_reqfiles(path):
    """
    Method to find python requirements files

    Args:
      path Project dir
    Returns:
      List of python requirement files
    """
    result = []
    req_files = [
        "requirements.txt",
        "Pipfile",
        "poetry.lock",
        "Pipfile.lock",
        "conda.yml",
    ]
    for root, dirs, files in os.walk(path):
        filter_ignored_dirs(dirs)
        for name in req_files:
            if name in files:
                result.append(os.path.join(root, name))
    return result

def is_binary_string(content):
    """
    Method to check if the given content is a binary string
    """
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F})
    return bool(content.translate(None, textchars))

def is_exe(src):
    """Detect if the source is a binary file
    :param src: Source path
    :return True if binary file. False otherwise.
    """
    if os.path.isfile(src):
        try:
            return is_binary_string(open(src, "rb").read(1024))
        except Exception:
            return False
    return False

def find_files(src, src_ext_name, quick=False, filter=True):
    """
    Method to find files with given extenstion
    """
    result = []
    for root, dirs, files in os.walk(src):
        if filter:
            filter_ignored_dirs(dirs)
        for file in files:
            if file == src_ext_name or file.endswith(src_ext_name):
                result.append(os.path.join(root, file))
                if quick:
                    return result
    return result

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def exec_tool(args, cwd=None, stdout=subprocess.PIPE):
    """
    Convenience method to invoke cli tools

    Args:
      args cli command and args
    """
    try:
        logger.debug('Executing "{}"'.format(" ".join(args)))
        if os.environ.get("FETCH_LICENSE"):
            logger.debug(
                "License information would be fetched from the registry. This would take several minutes ..."
            )
        cp = subprocess.run(
            args,
            stdout=stdout,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            env=os.environ.copy(),
            check=False,
            shell=False,
            encoding="utf-8",
        )
        logger.debug(cp.stdout)
    except Exception as e:
        logger.exception(e)

def detect_language_type(src_dir):
    """Detect project type by looking for certain files

    :param src_dir: Source directory

    :return List of detected types
    """
    # container image support
    if (
        "docker.io" in src_dir
        or "quay.io" in src_dir
        or ":latest" in src_dir
        or "@sha256" in src_dir
        or src_dir.endswith(".tar")
        or src_dir.endswith(".tar.gz")
    ):
        return ["docker"]
    # Check if the source is an exe file. Assume go for all binaries for now
    if is_exe(src_dir):
        return ["go", "binary"]
    project_types = []
    if find_python_reqfiles(src_dir):
        project_types.append("python")
    if find_files(src_dir, "pom.xml", quick=True) or find_files(
        src_dir, ".gradle", quick=True
    ):
        project_types.append("java")
    if find_files(src_dir, ".gradle.kts", quick=True):
        project_types.append("kotlin")
    if find_files(src_dir, "build.sbt", quick=True):
        project_types.append("scala")
    if (
        find_files(src_dir, "package.json", quick=True)
        or find_files(src_dir, "yarn.lock", quick=True)
        or find_files(src_dir, "rush.json", quick=True)
    ):
        project_types.append("nodejs")
    if find_files(src_dir, "go.sum", quick=True) or find_files(
        src_dir, "Gopkg.lock", quick=True
    ):
        project_types.append("go")
    if find_files(src_dir, "Cargo.lock", quick=True):
        project_types.append("rust")
    if find_files(src_dir, "composer.json", quick=True):
        project_types.append("php")
    if find_files(src_dir, ".csproj", quick=True):
        project_types.append("dotnet")
    if find_files(src_dir, "Gemfile", quick=True) or find_files(
        src_dir, "Gemfile.lock", quick=True
    ):
        project_types.append("ruby")
    if find_files(src_dir, "deps.edn", quick=True) or find_files(
        src_dir, "project.clj", quick=True
    ):
        project_types.append("clojure")
    if find_files(src_dir, "conan.lock", quick=True) or find_files(
        src_dir, "conanfile.txt", quick=True
    ):
        project_types.append("cpp")
    if find_files(src_dir, "pubspec.lock", quick=True) or find_files(
        src_dir, "pubspec.yaml", quick=True
    ):
        project_types.append("dart")
    if find_files(src_dir, "cabal.project.freeze", quick=True):
        project_types.append("haskell")
    if find_files(src_dir, "mix.lock", quick=True):
        project_types.append("elixir")
    if find_files(
        os.path.join(src_dir, ".github", "workflows"), ".yml", quick=True, filter=False
    ):
        project_types.append("github")
    # jars
    if "java" not in project_types and find_files(src_dir, ".jar", quick=True):
        project_types.append("jar")
    # Jenkins plugins or plain old jars
    if "java" not in project_types and find_files(src_dir, ".hpi", quick=True):
        project_types.append("jenkins")
    if find_files(src_dir, ".yml", quick=True) or find_files(
        src_dir, ".yaml", quick=True
    ):
        project_types.append("yaml-manifest")
    return project_types


class VoyagerDetect():

    def __init__(self, token=None, url=None, username=None, password=None):
        self.api_url = url
        self.api_token = token
        self.api_username = username
        self.api_password = password
        self.req = requests.Session()

    # 1.token生成，token有效期较长，失效后再进行重新生成
    def get_new_token(self):
        try:
            self.req.headers = {}
            res = self.req.post(self.api_url + 'api/member/get-auth-token/',
                                data={'username': self.api_username, 'password': self.api_password})
            token = res.json()['token']
            headers = {
                # 注意Token后有空格
                'Authorization': 'Token ' + token
            }
            self.req.headers = headers
            return token
        except Exception as e:
            logger.error(e)
            return None

    def check_token_valid(self):
        headers = {
            # 注意Token后有空格
            'Authorization': 'Token ' + self.api_token
        }
        self.req.headers = headers
        try:
            res = self.req.get(self.api_url + 'api/member/check-token/', )
            if res.status_code == 200 and res.json()['success']:
                return True
        except Exception as e:
            logger.error(e)
        return False

    # 登录认证
    def login(self):
        login_status = {
            'status': False,
            'message': '',
            'data': None
        }
        if self.api_token:
            if self.check_token_valid():
                login_status['status'] = True
                return login_status
            else:
                # token失效，使用账号密码登录
                login_status['message'] = 'token失效，使用账号密码登录'

        if self.api_username and self.api_password:
            # 获取认证token
            token = self.get_new_token()
            if token:
                self.api_token = token
                headers = {
                    # 注意Token后有空格
                    'Authorization': 'Token ' + self.api_token
                }
                self.req.headers = headers
                login_status['status'] = True
            else:
                login_status['message'] = '无法生成访问token，账号密码可能错误'
        else:
            login_status['message'] = '请提供API账号以及密码信息'
        logger.info(login_status['message'])
        return login_status

    # sca分析
    def sca_analysis(self, project_type, bom_file, src_dir=".", deep=False):
        """Method to create BOM file by executing cdxgen command

        :param project_type: Project type
        :param bom_file: BOM file
        :param src_dir: Source directory

        :returns True if the command was executed. False if the executable was not found.
        """
        cdxgen_cmd = os.environ.get("CDXGEN_CMD", "cdxgen")
        if not shutil.which(cdxgen_cmd):
            local_bin = resource_path(
                os.path.join(
                    "local_bin", "cdxgen.exe" if sys.platform == "win32" else "cdxgen"
                )
            )
            if not os.path.exists(local_bin):
                logger.warning(
                    "{} command not found. Please install using npm install @appthreat/cdxgen or set PATH variable".format(
                        cdxgen_cmd
                    )
                )
                return False
            try:
                cdxgen_cmd = local_bin
                # Set the plugins directory as an environment variable
                os.environ["CDXGEN_PLUGINS_DIR"] = resource_path("local_bin")
            except Exception as e:
                pass
        if project_type:
            if project_type in ("docker"):
                logger.info(
                    f"Generating Software Bill-of-Materials for container image {src_dir}. This might take a few mins ..."
                )
            sca_args = [cdxgen_cmd, "-r", "-t", project_type, "-o", bom_file]
            if deep or project_type in ("jar", "jenkins"):
                sca_args.append("--deep")
                logger.info("About to perform deep scan. This would take a while ...")
        else:
            sca_args = [cdxgen_cmd, "-o", bom_file]
        sca_args.append(src_dir)
        print(sca_args)
        exec_tool(['ls', '/app'],)
        exec_tool(sca_args,)
        return os.path.exists(bom_file)

    # 2.进行扫描
    def scan(self, data, files):
        login_status = self.login()
        if login_status['status']:
            if files:
                response = self.req.post(self.api_url + 'api/scan/detect/', data=data, files=files)
            else:
                response = self.req.post(self.api_url + 'api/scan/detect/', data=data, files=[ ('files', ('', None, )),])
            return response.json()
        else:
            return login_status


    # 3.获取扫描结果或报告
    def get_scan_result(self, task_id):
        login_status = self.login()
        if login_status['status']:
            response = self.req.get(self.api_url + 'api/scan/scan-log/?task_id={}'.format(task_id),)
            return response.json()
        else:
            return login_status
