# https://backlog.com/developer/applications/

from datetime import datetime
from utils import config_util  # from [DirName] import [fileName]
import requests
import json
import jmespath
import yaml
configUtil = config_util.ConfigUtil()
config_data = configUtil.read_yaml_file('config.yml')

HOST = config_data['HOST']['GLOBAL']
API_KEY = config_data['API_KEY']['GLOBAL']

params = {'apiKey': API_KEY}
issueIdOrKey = 'FFIS_SMAPHOSYS-489'
commentId = '39332511'
url = '{host}/api/v2/issues/{issueIdOrKey}/comments/{commentId}'.format(**{'host': HOST, 'issueIdOrKey': issueIdOrKey, 'commentId': commentId})
print(url)
r = requests.get(url, params=params)
data = r.json()
print(r.json())
print(json.dumps(r.json(), indent=2))
print(data)
print(jmespath.search("changeLog[?field=='actualHours'].newValue", data))
print(jmespath.search("changeLog[?field=='actualHours']", data))