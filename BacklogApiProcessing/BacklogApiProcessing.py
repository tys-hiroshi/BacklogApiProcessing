# https://backlog.com/developer/applications/
# https://developer.nulab-inc.com/ja/docs/backlog/
# https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-comment-list/


from datetime import datetime, timedelta, timezone
import pytz
from utils import config_util  # from [DirName] import [fileName]
from utils import issue_util  # from [DirName] import [fileName]
from utils import log_util  # from [DirName] import [fileName]
from utils import count_actual_hours_util
from utils import issue_type_util
from utils import term_util
from utils import wiki_util
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

updated_start_date = config_data['PROCESSING_TERM']['START_DATE']
updated_end_date = config_data['PROCESSING_TERM']['END_DATE']
project_keys = config_data['PROCESSING_PROJECT_KEY']
issue_type_name = config_data['PROCESSING_ISSUE_TYPE_NAME']
person_hours_per_day = config_data['PERSON_HOURS_PER_DAY']
issueTypeUtil = issue_type_util.IssueTypeUtil(client)
termUtil = term_util.TermUtil()
MAX_COUNT = 100

projects_actual_hours_list = []
for project_key in project_keys:
    logUtil.info("start processing: " + project_key)
    project_id = client.get_project_id(project_key)
    issue_type_id = issueTypeUtil.select_issue_type_id(project_key, issue_type_name)
    if issue_type_id == '':
        projects_actual_hours_list.append(0)
    else:
        issueUtil = issue_util.IssueUtil(HOST, API_KEY, project_id, MAX_COUNT)
        issue_keys = issueUtil.get_updated_issue_keys(client, project_id, issue_type_id, updated_start_date, updated_end_date)
        print(issue_keys)
        print(len(issue_keys))

        updated_since = updated_start_date + ' 0:00:00'
        updated_until = termUtil.select_next_month_datetime(datetime.strptime(updated_end_date, '%Y-%m-%d')) + ' 0:00:00'

        countActualHoursUtil = count_actual_hours_util.CountActualHoursUtil(client, updated_since, updated_until, MAX_COUNT)
        actual_hours_list = []
        for issue_key in issue_keys:
            actual_hours = countActualHoursUtil.select_actual_hours(issue_key)
            actual_hours_list.append(actual_hours)

        print(actual_hours_list)
        logUtil.info("actual_hours")
        sum_actual_hours = sum(actual_hours_list)
        projects_actual_hours_list.append(sum_actual_hours)
        logUtil.info(sum_actual_hours)
        logUtil.info("person-days")
        logUtil.info(sum(actual_hours_list) / float(person_hours_per_day))

logUtil.info(projects_actual_hours_list)

wikiUtil = wiki_util.WikiUtil(client)
wiki_id = config_data['PROCESSING_UPDATE_WIKI_ID']
wiki_page = wikiUtil.get_wiki_page(wiki_id)
wiki_name = jmespath.search("name", wiki_page)
wiki_content_table = jmespath.search("content", wiki_page)
print(wiki_content_table.split('\r\n'))
head_row_name = updated_start_date + " to " + updated_end_date
added_content = wikiUtil.add_actual_hours_to_content(wiki_content_table, projects_actual_hours_list, head_row_name)
wikiUtil.update_wiki_page(wiki_id, wiki_name, added_content, False)