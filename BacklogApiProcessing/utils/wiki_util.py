# -*- coding: utf-8 -*-
import requests
import json
import jmespath
from datetime import datetime, timedelta, timezone
import re

class WikiUtil():
    def __init__(self, client):
        self.client = client

    def get_wiki_page(self, wiki_id):
        wiki_page = self.client.wiki(wiki_id)
        return wiki_page

    def add_actual_hours_to_content(self, wiki_content_table, actual_hours_list, head_row_name):
        wiki_content_row_list = wiki_content_table.split('\r\n')
        wiki_content_row_list_table = []
        wiki_content_row_list_out_of_table = []
        for i in range(len(wiki_content_row_list)):
            m = re.search(r'^\s?\|', wiki_content_row_list[i])
            if m is not None and len(m.group()) > 0:
                wiki_content_row_list_table.append(wiki_content_row_list[i])
            else:
                wiki_content_row_list_out_of_table.append(wiki_content_row_list[i])

        add_last_row_list = [head_row_name, "----"]
        add_last_row_list.extend(list(map(str, actual_hours_list)))
        sum_actual_hours_list = [sum(actual_hours_list)]
        add_last_row_list.extend(list(map(str, sum_actual_hours_list)))
        for i in range(len(wiki_content_row_list_table)):
            wiki_content_row_list_table[i] = wiki_content_row_list_table[i] + " " + add_last_row_list[i] + " |"
        wiki_content_table = '\r\n'.join(wiki_content_row_list_table)
        wiki_content_out_of_table = '\r\n\r\n\r\n'.join(wiki_content_row_list_out_of_table)
        return wiki_content_table + wiki_content_out_of_table

    def update_wiki_page(self, wiki_id, name, content, mail_notify):
        params = {"name" : name, "content" : content, "mailNotify" : str(mail_notify).lower().strip()}
        self.client.update_wiki(wiki_id, params)
