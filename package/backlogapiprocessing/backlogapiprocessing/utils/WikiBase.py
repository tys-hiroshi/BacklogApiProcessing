#!/usr/bin/env python3
# -*- coding:utf-8 -*-

class WikiBase(object):
    WikiLineSep = '\r\n'

    def __init__(self, wikiId, client):
        self.client = client
        self.wikiPage = client.wiki(wikiId)

    def writeWikiPage(self, content, mailNotify=False):
        wikiName = self.wikiPage['name']
        params = {
            'name': wikiName,
            'content': content,
            'mailNotify': str(mailNotify).lower()
        }
        self.client.update_wiki(self.wikiPage['id'], params)

if __name__ == '__main__':
    pass
