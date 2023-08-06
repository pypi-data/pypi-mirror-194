import json 
from pathlib import Path
import os
import enum

CONFIG_PATH = Path(__file__).parent.resolve() / 'user_config.json'


class Platform(enum.Enum):
    GOOGLE_APP_ENGINE = 'GOOGLE_APP_ENGINE'
    DETA = 'DETA'


def platforms():
    platforms = dict()
    for i, p in enumerate(Platform):
        platforms[f"{i}"] = p
    return platforms


def get_project_platform():
    for (_, _, filenames) in os.walk(os.curdir):
        for fn in filenames:
            if 'app.yaml' in fn:
                return Platform.GOOGLE_APP_ENGINE
    return Platform.DETA


def __fetch_config():
    with open(CONFIG_PATH, 'r') as j:
        return json.loads(j.read())


def set_project_key(project_key: str):
    conf = __fetch_config()
    conf['project_key'] = project_key 
    with open(CONFIG_PATH, 'w') as j:
        j.write(json.dumps(conf, indent=4))


def clear_project_key():
    set_project_key("")


def config(key: str or None = None):
    if key:
        return __fetch_config().get(key)
    return __fetch_config()


def run_server():
    server_cmd = "uvicorn main:app --reload"
    os.system(server_cmd)
