import os
import argparse
from plutonium.utils import logger, VoyagerDetect
from plutonium.config import (
    BOM_FILENAME,
    LOG_FILENAME,
    VOYAGER_SERVER,
    VOYAGER_USERNAME,
    VOYAGER_PASSWORD,
    VOYAGER_TOKEN,
    GOVERNANCE_TOKEN,
    LOGO
)

def init_data(data_dir):
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
        except Exception as e:
            logger.error(e)

def init_parse():

    parser = argparse.ArgumentParser(
        description="SCA Agent based on Cdxgen and internal project Voyager I, for application dependencies and risk discovery。"
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="type",
        required=True,
        help="project/image/package/project_file/image_file/package_file",
    )
    parser.add_argument(
        "--data-dir",
        default=os.path.join(os.getcwd(), "data"),
        dest="data_dir",
        help="Running data directory",
    )
    parser.add_argument(
        "-l",
        "--language",
        dest="language",
        default=None,
        help="project language",
    )
    parser.add_argument(
        "--target",
        dest="target",
        help="Source directory or container image or binary file",
    )
    parser.add_argument(
        "--no-error",
        action="store_true",
        default=False,
        dest="noerror",
        help="Continue on error to prevent build from breaking",
    )
    parser.add_argument(
        "--license",
        action="store_true",
        default=False,
        dest="license",
        help="Try to get license",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        default=False,
        dest="deep_scan",
        help="Perform deep scan by passing this --deep argument to cdxgen. Useful while scanning docker images and OS packages.",
    )
    parser.add_argument(
        "--voyager-server",
        default=VOYAGER_SERVER,
        dest="voyager_server",
        help="Voyager server url. Eg: https://api.voyager.com",
    )
    parser.add_argument(
        "--voyager-username",
        default=VOYAGER_USERNAME,
        dest="voyager_username",
        help="Voyager username",
    )
    parser.add_argument(
        "--voyager-password",
        default=VOYAGER_PASSWORD,
        dest="voyager_password",
        help="Voyager password",
    )
    parser.add_argument(
        "--voyager-token",
        default=VOYAGER_TOKEN,
        dest="voyager_token",
        help="Voyager token for token based submission",
    )
    parser.add_argument(
        "--governance-token",
        default=GOVERNANCE_TOKEN,
        dest="governance_token",
        help="Governance token for token based submission",
    )
    parser.add_argument(
        "--project_name",
        help="project name",
    )
    parser.add_argument(
        "--project_repository_url",
        help="project repository url",
    )
    parser.add_argument(
        "--project_user",
        help="project user",
    )
    # project branch
    parser.add_argument(
        "--project_branch",
        help="project branch",
    )
    parser.add_argument(
        "--project_file",
        help="project file",
    )
    parser.add_argument(
        "--project_pod",
        help="project pod",
    )
    parser.add_argument(
        "--project_service_name",
        help="project service name",
    )
    parser.add_argument(
        "--project_commit_id",
        help="project commit id",
    )

    parser.add_argument(
        "--depscan",
        action="store_true",
        default=False,
        dest="depscan",
        help="Try to scan vulnerabilities using depscan",
    )
    parser.add_argument(
        "--trivy",
        action="store_true",
        default=False,
        dest="trivy",
        help="Try to scan vulnerabilities using trivy",
    )

    # 镜像信息
    parser.add_argument(
        "--image_name",
        help="镜像名称",
    )
    parser.add_argument(
        "--image_file",
        help="镜像文件",
    )
    parser.add_argument(
        "--image_repository_url",
        help="镜像仓库地址",
    )
    parser.add_argument(
        "--internet_reachable",
        action="store_true",
        default=False,
        help="是否能够访问互联网",
    )
    parser.add_argument(
        "--core_application",
        action="store_true",
        default=False,
        help="是否是核心应用",
    )
    parser.add_argument(
        "--deploy_test_env",
        action="store_true",
        default=False,
        help="部署环境为测试环境",
    )
    parser.add_argument(
        "--deploy_pro_env",
        action="store_true",
        default=False,
        help="部署环境为正式环境",
    )

    parser.print_help()
    return parser.parse_args()


def main():
    print(LOGO)
    args = init_parse()
    init_data(args.data_dir)
    target = args.target
    # Detect the project types and perform the right type of scan
    data = {
        'op_type': 'create_project_governance',
        'type': args.type,
        'governance_token': args.governance_token if args.governance_token else GOVERNANCE_TOKEN,
        # 项目信息
        'language': args.language,
        # 镜像类
        'image_name': args.image_name,
        'image_repository_url': args.image_repository_url,
        'internet_reachable': args.internet_reachable,
        'core_application': args.core_application,
        'deploy_test_env': args.deploy_test_env,
        'deploy_pro_env': args.deploy_pro_env,
        # 项目类
        'project_name': args.project_name,
        'project_branch': args.project_branch,
        'project_user': args.project_user,
        'project_commit_id': args.project_commit_id,
        'project_pod': args.project_pod,
        'project_service_name': args.project_service_name,
        'project_repository_url': args.project_repository_url,
        # 包类，暂时不用

    }
    attach_files = [
        # 提交的名称前缀需要与scan_log_detail的type一致
        # 项目文件
        # ('attach_file', ('2.md', open('./todo.md', 'rb'),)),
        # ('core_files_list', ('pom.xml', open('./todo.md', 'rb'), )),
        # ('core_files_list', ('package.json.lock', open('./todo.md', 'rb'), )),
        # ('sbom_files_list', ('sca_cdxgen.json', open('./voyager.json', 'rb'),)),
        # ('sbom_files_list', ('sca_dependency_tree.txt', open('./todo.md', 'rb'), )),
        # ('vul_files_list', ('vul_veinmind.json', open('./todo.md', 'rb'), )),
    ]
    # if args.project_file:
    #     try:
    #         attach_files.append(
    #             ('attach_file', (args.project_file.split('.')[0], open(args.project_file, 'rb'),)),
    #         )
    #     except Exception as e:
    #         logger.error(e)
    detector = VoyagerDetect(
        token=args.voyager_token if args.voyager_token else VOYAGER_TOKEN,
        url=args.voyager_server if args.voyager_server else VOYAGER_SERVER,
        username=args.voyager_username if args.voyager_username else VOYAGER_USERNAME,
        password=args.voyager_password if args.voyager_password else VOYAGER_PASSWORD,
    )
    if args.type in ['project', 'project_file']:
        sca_status = detector.sca_analysis(args.language, args.data_dir+'/'+BOM_FILENAME, target, args.deep_scan)
        if not sca_status:
            logger.debug("Bom file {} was not created successfully")
        try:
            attach_files.append(
                ('sbom_files_list', (BOM_FILENAME, open(args.data_dir+'/'+BOM_FILENAME, 'rb'),)),
            )
        except Exception as e:
            logger.error(e)
        # # 如果开启漏洞，执行漏洞扫描
        if args.depscan:
            logger.info('开始基于depscan进行漏洞扫描')
        if args.trivy:
            logger.info('开始基于trivy进行漏洞扫描')
        # 上传数据到后端
        print(data)
        # run_log进行上传
        # 将run.log进行复制
        try:
            attach_files.append(
                ('core_files_list', (LOG_FILENAME, open(LOG_FILENAME, 'rb'),)),
            )
        except Exception as e:
            logger.error(e)
        scan_status = detector.scan(data, attach_files)
        print(scan_status)
    elif args.type in ['image', 'image_file']:
        print(data)
        if args.image_file:
            try:
                attach_files.append(
                    ('attach_file', (args.image_file.split('/')[-1].split('.')[0], open(args.image_file, 'rb'),)),
                )
            except Exception as e:
                logger.error(e)
        print(data)
        print(attach_files)
        # run_log进行上传
        try:
            attach_files.append(
                ('core_files_list', (LOG_FILENAME, open(LOG_FILENAME, 'rb'),)),
            )
        except Exception as e:
            logger.error(e)
        scan_status = detector.scan(data, attach_files)
        print(scan_status)
    elif args.type in ['package','package_file']:
        pass
    else:
        pass
    # if scan_status['success']:
    #     print(scan_status['message'])
    # else:
    #     print(scan_status['message'])

if __name__ == '__main__':
    main()
