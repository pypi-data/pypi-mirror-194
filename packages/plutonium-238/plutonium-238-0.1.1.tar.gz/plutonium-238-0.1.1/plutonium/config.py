import os
import logging

LOGO = r"""
   ,-------------------------------------------------------------------------------.
   |                                                                               |
   |                                                                               |
   |       ____  _       _              _                   ____  _____  ___       |
   |      |  _ \| |_   _| |_ ___  _ __ (_)_   _ _ __ ___   |___ \|___ / ( _ )      |
   |      | |_) | | | | | __/ _ \| '_ \| | | | | '_ ` _ \    __) | |_ \ / _ \      |
   |      |  __/| | |_| | || (_) | | | | | |_| | | | | | |  / __/ ___) | (_) |     |
   |      |_|   |_|\__,_|\__\___/|_| |_|_|\__,_|_| |_| |_| |_____|____/ \___/      |
   |                                                                               |
   |                                                                               |
   |                                                             version 0.1.1     |
   |                                                                               |
   |                 This is a SCA Agent, Copyright@OKX Security Team              |
   |                                                                               |
   |                                                                               |
   `-------------------------------------------------------------------------------'
"""
# 结果轮询最大时间
RESULT_CHECK_INTERVAL = 1
RESULT_CHECK_TIME_MAX = 1 * 10
# 结果轮询最大次数
RESULT_CHECK_COUNT = 20

# DATA_DIR = os.path.dirname(os.path.abspath(__file__)) +'/data/'
# System Env
VOYAGER_SERVER = os.getenv('VOYAGER_SERVER') if os.getenv('VOYAGER_SERVER') else 'http://localhost:9999/'
VOYAGER_USERNAME = os.getenv('VOYAGER_USERNAME') if os.getenv('VOYAGER_USERNAME') else 'dev'
VOYAGER_PASSWORD = os.getenv('VOYAGER_PASSWORD') if os.getenv('VOYAGER_PASSWORD') else 'dev'
VOYAGER_TOKEN = os.getenv('VOYAGER_TOKEN') if os.getenv('VOYAGER_TOKEN') else 'x'
GOVERNANCE_TOKEN = os.getenv('GOVERNANCE_TOKEN') if os.getenv('GOVERNANCE_TOKEN') else 'x'

# sca used cdxgen
BOM_FILENAME = 'sca_cdxgen.json'

# 默认忽略的目录
ignore_directories = [
    ".git",
    ".svn",
    ".mvn",
    ".idea",
    "dist",
    "bin",
    "obj",
    "backup",
    "docs",
    "tests",
    "test",
    "tmp",
    "report",
    "reports",
    "node_modules",
    ".terraform",
    ".serverless",
    "venv",
    "examples",
    "tutorials",
    "samples",
    "migrations",
    "db_migrations",
    "unittests",
    "unittests_legacy",
    "stubs",
    "mock",
    "mocks",
]

# 日志配置
if os.getenv("SCAN_MODE") == "debug":
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.DEBUG
    # LOG_LEVEL = logging.INFO
LOG_FILENAME = 'run.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s  - %(lineno)d - %(message)s'
