# https://backlog.com/developer/applications/

from datetime import datetime
import requests
import json
import jmespath

BACKLOG_HOST_GLOBAL = 'https://toyoko.backlog.jp'
BACKLOG_HOST_IP = 'https://toyoko-ip.backlog.com'
BACKLOG_API_KEY_GLOBAL = ''
BACKLOG_API_KEY_IP = ''

params = {'apiKey': BACKLOG_API_KEY_GLOBAL}
issueIdOrKey = 'FFIS_SMAPHOSYS-489'
commentId = '39332511'
url = BACKLOG_HOST_GLOBAL + '/api/v2/issues/' + issueIdOrKey + "/comments/" + commentId
print(url)
r = requests.get(url, params=params)
data = r.json()
print(r.json())
print(json.dumps(r.json(), indent=2))
print(data)
#print(jmespath.search('changeLog[?feild==`actualHours`]', data))
#machines[?state=='running'].name
print(jmespath.search("changeLog[?field=='actualHours'].newValue", data))
print(jmespath.search("changeLog[?field=='actualHours']", data))
print(jmespath.search("changeLog[].f", data))
#data = json.loads(r.json())
#print(json.dumps(data, indent=2))