#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils.WikiBase import WikiBase

'''
サマリーページのtableの種: 一番最初に手書きで用意しておくべきもの

|プロジェクト名|プロジェクトキー|
|:--|:--|
|実績期間合計| |
==========ここから上はコメントを書かないでください==========

- 表
  row = 3, column = 2
  見出しの文言は、上と同じものを書くこと
  最後のrowの最後のcolumnに、spaceが必要
- セパレータ
  上と全く同じものを書くこと
  セパレータがない場合は、手書きのコメントは保持されず、上書きされて消えてしまう
'''

class Summary(WikiBase):
    Separator = u'==========ここから上はコメントを書かないでください=========='
    ProjectNameLabel = u'プロジェクト名'
    ProjectKeyLabel = u'プロジェクトキー'
    ProjectNameLine = ':--'
    ProjectKeyLine = ':--'
    AmountLabel = u'実績期間合計'

    def __init__(self, wikiId, client):
        super().__init__(wikiId, client)
        content = self.wikiPage['content']
        content = content.split(self.Separator)
        self.bottomHalf = content[1] if len(content) > 1 else ''
        self.table = content[0].split(self.WikiLineSep)
        for i in range(len(self.table)):
            row = self.table[i]
            row = row.strip('|').split('|')
            if len(row) < 2: # 2カラムないrowがあれば削除する
                self.table.pop(i) # ToDo: popすると長さが変ってしまう
            else:
                self.table[i] = row

        if not self.isValidTable():
            raise Exception(f'it has invalid table structure: wikiId = {wikiId}')

    # private
    def isValidTable(self):
        if self.table[0][0] != self.ProjectNameLabel or self.table[0][1] != self.ProjectKeyLabel:
            return False

        if self.table[1][0] != self.ProjectNameLine or self.table[1][1] != self.ProjectKeyLine:
            return False

        if self.table[-1][0] != self.AmountLabel:
            return False

        return True

    # private
    def getProjectKeys(self):
        return {self.table[i][1] for i in range(2, len(self.table)-1)}

    def addRecord(self, period, record):
        if period in self.table[0]:
            index = self.table[0].index(period)
            self.replaceRecord(index, record)
        else:
            self.appendRecord(period, record)
        return self

    # private
    def replaceRecord(self, index, record):
        # 既存のrowを置き換える
        for i in range(2, len(self.table)-1):
            projectKey = self.table[i][1]
            if projectKey in record:
                self.table[i][index] = record[projectKey][0]

        # 新規のrowを追加する
        numOfColumns = len(self.table[0]) # 現状のcolumn数
        addedKeys = list(set(record.keys()) - self.getProjectKeys()) # 元々存在しない(つまり、新規に追加された)ProjectKeyを求める
        for key in addedKeys:
            name = record[key][1]
            row = [name, key] + [str(0.0)] * (numOfColumns-2-1) + [str(record[key][0])]
            self.table.insert(-1, row)

        # 合計のrowを置き換える
        amount = sum([record[row][0] for row in record])
        self.table[-1][index] = str(amount)

    # private
    def appendRecord(self, period, record):
        self.table[0].append(period)
        self.table[1].append('--:')

        # 既存のrowに追加する
        for i in range(2, len(self.table)-1):
            row = self.table[i]
            projectKey = row[1]
            if projectKey in record:
                row.append(str(record[projectKey][0]))
            else:
                row.append(str(0))
            self.table[i] = row

        # 新規のrowを追加する
        numOfColumns = len(self.table[0]) # 追加した後の新しいcolumn数
        addedKeys = list(set(record.keys()) - self.getProjectKeys()) # 元々存在しない(つまり、新規に追加された)ProjectKeyを求める
        for key in addedKeys:
            name = record[key][1]
            row = [name, key] + [str(0.0)] * (numOfColumns-2-1) + [str(record[key][0])]
            self.table.insert(-1, row)

        # 合計のrowを追加する
        amount = sum([record[row][0] for row in record])
        self.table[-1].append(str(amount))

    def printRecords(self):
        table = ''
        for row in self.table:
            table += '|'
            for column in row:
                table += f'{column}|'
            table += f'{self.WikiLineSep}'
        content = table + self.Separator + self.bottomHalf
        self.writeWikiPage(content, False)

if __name__ == '__main__':
    pass
