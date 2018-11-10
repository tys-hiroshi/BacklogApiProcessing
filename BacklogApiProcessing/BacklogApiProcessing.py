# https://backlog.com/developer/applications/

from datetime import datetime, timedelta, timezone
import pytz
from utils import config_util  # from [DirName] import [fileName]
from utils import issue_util  # from [DirName] import [fileName]
from utils import log_util  # from [DirName] import [fileName]
import requests
import json
import jmespath
import yaml
from pybacklog import BacklogClient

# Setting Configuration
configUtil = config_util.ConfigUtil()
config_data = configUtil.read_yaml_file('config.yml')

HOST = config_data['HOST']['GLOBAL']
API_KEY = config_data['API_KEY']['GLOBAL']

client = BacklogClient("toyoko", API_KEY)

# Log
logUtil = log_util.LogUtil()
logUtil.info("start")

# Get Issue List
# list issue
project_id = client.get_project_id("FFIS_SMAPHOSYS")
updated_since = '2018-10-01'
updated_until = '2018-10-31'
issue_type_id = '197980'
issues = client.issues({"projectId[]":[project_id], "issueTypeId[]": [issue_type_id] , "sort": "updated", "count": 100, "updatedSince": updated_since, "updatedUntil": updated_until, "order": "desc"})  #TODO: updatedSince is UTC+0000?
print(issues)
print(json.dumps(issues, indent=2))


first_issue = issues[0]
last_issue = issues[len(issues) - 1]
last_issue_key = jmespath.search("issueKey", last_issue)
last_updated = jmespath.search("updated", last_issue)
last_updated_dt = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%SZ')
jp = pytz.timezone('Asia/Tokyo')
print(last_updated_dt.replace(tzinfo=jp))

print(last_issue_key)
print(last_updated)

updated_until = last_updated_dt.strftime("%Y-%m-%d")
issues = client.issues({"projectId[]":[project_id], "issueTypeId[]": [issue_type_id] , "sort": "updated", "count": 100, "updatedSince": updated_since, "updatedUntil": updated_until})

