# -*- coding: utf-8 -*-
import json
import jmespath

class IssueTypeUtil():
    """description of class"""

    def __init__(self, client):
        self.client = client

    def select_issue_type_id(self, project_key, type_name):
        issue_types = self.client.project_issue_types(project_key)
        type_id_list = jmespath.search("[?name=='" + type_name + "'].id", issue_types)
        type_id = ''
        if len(type_id_list) > 0:
            type_id =  type_id_list[0]
        return type_id