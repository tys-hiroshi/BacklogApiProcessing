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

jp = pytz.timezone('Asia/Tokyo')
updated_since = '2018-10-01'
updated_until = '2018-10-31'
project_id = client.get_project_id("FFIS_SMAPHOSYS")
issue_type_id = '197980'
MAX_COUNT = 100

issueUtil = issue_util.IssueUtil(HOST, API_KEY, project_id, MAX_COUNT)
issue_keys = issueUtil.get_updated_issue_keys(client, project_id, issue_type_id, updated_since, updated_until)
print(issue_keys)
print(len(issue_keys))