import requests
import json
import jmespath
from datetime import datetime, timedelta, timezone

class WikiUtil():
    def __init__(self, client):
        self.client = client

    def get_wiki_page(wiki_id):
        wiki_page = client.wiki(wiki_id)
        return wiki_page