# -*- coding: utf-8 -*-
import requests
import json
import jmespath
from datetime import datetime, timedelta, timezone

class IssueUtil():
    def __init__(self, host, api_key, project_id, MAX_COUNT = 20):
        self.project_id = project_id
        self.host = host
        self.api_params = {'apiKey': api_key}
        self.max_count = MAX_COUNT

    def get_issue_list(self, updated_since, updated_until):
        url = '{host}/api/v2/issues'.format(**{'host': self.host})
        print(url)
        api_params = self.api_params
        api_params['projectId[]'] = self.project_id
        api_params['updatedSince'] = updated_since
        api_params['updatedUntil'] = updated_until
        r = requests.get(url, params=api_params)
        data = r.json()
        print(r.json())
        print(json.dumps(r.json(), indent=2))
        print(data)

    def get_updated_issue_keys(self, client, project_id, issue_type_id, updated_since, updated_until, is_updated = True):
        issue_keys = []
        count  = 1
        while count > 0:
            params = {}
            if is_updated == True:
                params = {"projectId[]":[project_id], "issueTypeId[]": [issue_type_id] , "sort": "updated", "count": self.max_count, "updatedSince": updated_since, "updatedUntil": updated_until, "order": "desc"}
            else:
                params = {"projectId[]":[project_id], "issueTypeId[]": [issue_type_id] , "sort": "updated", "count": self.max_count, "createdSince": updated_since, "createdUntil": updated_until, "order": "desc"}
            issues = client.issues(params)  #TODO: updatedSince is UTC+0000?
            if len(issues) == 0:
                break
            _issue_keys = jmespath.search("[*].issueKey", issues)
            issue_keys.extend(_issue_keys)
            last_issue = issues[len(issues) - 1]
            last_issue_key = jmespath.search("issueKey", last_issue)
            last_updated = jmespath.search("updated", last_issue)
            last_updated_dt = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%SZ')
            #print(last_updated_dt.replace(tzinfo=jp))

            #print(last_issue_key)
            #print(last_updated)

            updated_until = last_updated_dt.strftime("%Y-%m-%d")
            count = len(issues)  #TODO:
            if count < self.max_count:
                break
        return issue_keys
