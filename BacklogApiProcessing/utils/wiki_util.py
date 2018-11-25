import requests
import json
import jmespath
from datetime import datetime, timedelta, timezone

class WikiUtil():
    def __init__(self, client):
        self.client = client

    def get_wiki_page(self, wiki_id):
        wiki_page = self.client.wiki(wiki_id)
        return wiki_page

    def add_actual_hours_to_content(self, wiki_content_table, actual_hours_list, year_month):
        wiki_content_row_list = wiki_content_table.split('\r\n')
        #wiki_content_row_list = wiki_content_row_list[2: len(wiki_content_row_list) + 1]
        add_last_row_list = [ year_month," ---- "]
        add_last_row_list.extend(list(map(str, actual_hours_list)))
        for i in range(len(wiki_content_row_list)):
            #wiki_content_row_list[i] = wiki_content_row_list[i] + " " + add_last_row_list[i] + " |"
            wiki_content_row_list[i] = wiki_content_row_list[i] + " " + add_last_row_list[i] + " |"

        return '\r\n'.join(wiki_content_row_list)

    def update_wiki_page(self, wiki_id, name, content, mail_notify):
        params = {"name" : name, "content" : content, "mailNotify" : str(mail_notify)}
        self.client.update_wiki(wiki_id, params)
