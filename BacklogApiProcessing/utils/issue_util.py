import requests
import json
import jmespath

class IssueUtil():
    def __init__(self, host, api_key, project_id):
        self.project_id = project_id
        self.host = host
        self.api_params = {'apiKey': api_key}
        
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

    def get_issue_comment(self):
        issueIdOrKey = 'FFIS_SMAPHOSYS-489'
        commentId = '39332511'
        url = '{host}/api/v2/issues/{issueIdOrKey}/comments/{commentId}'.format(**{'host': HOST, 'issueIdOrKey': issueIdOrKey, 'commentId': commentId})
        print(url)
        r = requests.get(url, params=self.api_params)
        data = r.json()
        print(r.json())
        print(json.dumps(r.json(), indent=2))
        print(data)
        print(jmespath.search("changeLog[?field=='actualHours'].newValue", data))
        print(jmespath.search("changeLog[?field=='actualHours']", data))