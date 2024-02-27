import os
import logging
import logging.handlers
import yaml
from dotenv import find_dotenv, load_dotenv
from services import WebsiteExtractor

def init_app_version(project_dir):
    version = '0.0.0'
    try:
        file_path = project_dir + '/.gitlab-ci.yml'
        with open(file_path) as inFile:
            data = yaml.load(inFile, Loader=yaml.FullLoader)
            variables = data.get('variables', {})
            version = '{0}.{1}.{2}'.format(variables.get('VERSION_MAJOR', 0), variables.get('VERSION_MINOR', 0), variables.get('VERSION_BUILD', 0))
    except:
        pass
    os.environ['VERSION'] = version

def create_logger(project_dir):
    content_dir = os.path.join(project_dir, 'contents')
    os.makedirs(content_dir, exist_ok=True)

    ENV = os.getenv('ENV', 'UNKNOWN')
    SERVICE_NAME = os.getenv('SERVICE_NAME', 'UNKNOWN')
    VERSION = os.getenv('VERSION', '0.0.0')
    LOG_LEVEL = os.getenv('LOG_LEVEL',logging.INFO)

    logger = logging.getLogger('app')

    log_formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(levelname)s][{0}][{1}][{2}] %(message)s'.format(SERVICE_NAME, VERSION, ENV), '%Y-%m-%dT%H:%M:%S')
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    file_hander = logging.handlers.TimedRotatingFileHandler(os.path.join(content_dir, 'app.log'), 'h', 1, 48)
    file_hander.setFormatter(log_formatter)
    logger.addHandler(file_hander)

    logger.setLevel(LOG_LEVEL)
    return logger


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)

    load_dotenv(find_dotenv())

    init_app_version(project_dir)

    logger = create_logger(project_dir)
    logger.info('Start')

    url = os.getenv('WEBSITE_URL', None)
    if not url:
        logger.error('No Website url is provided')
        exit(-1)

    config = {
        'recursive_level_limit': int(os.getenv('RECURSIVE_LEVEL_LIMIT', 2)),
        'extract_page_sleep_sec': float(os.getenv('EXTRACT_PAGE_SLEEP_SEC', 0.1))
    }
    app = WebsiteExtractor(url, logger, config)
    app.extract()

    