#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils.WikiBase import WikiBase

'''
明細ページの種: 一番最初に手書きで用意しておくべきもの

***

- セパレータ
'''

# private
class Project(object):
    TaskLabel = u'タスク'
    HoursLabel = u'工数(時間)'
    TaskLine = ':--'
    HoursLine = '--:'

    def __init__(self, content=None):
        self.label = None
        self.records = []

        if content is None:
            return

        records = content.split(WikiBase.WikiLineSep)
        for record in records:
            if record.startswith('## '): # 見出し2
                self.label = record.replace('## ', '', 1)
            elif not record.startswith('|'):
                continue
            elif record != f'|{self.TaskLabel}|{self.HoursLabel}|' and record != f'|{self.TaskLine}|{self.HoursLine}|':
                record = record.strip('|').split('|')
                self.records.append((record[0], record[1]))

# private
class Section(object):
    def __init__(self, content=None):
        self.period = None
        self.projects = []

        if content is None:
            return

        records = content.split(WikiBase.WikiLineSep * 2) # 段落
        for record in records:
            if record.startswith('# '): # 見出し1 
                self.period = record.replace('# ', '', 1)
            elif record.startswith('## '):
                self.projects.append(Project(record))

class Detail(WikiBase):
    Separator = '***'

    def __init__(self, wikiId, client):
        super().__init__(wikiId, client)
        wikiPage = client.wiki(wikiId)
        content = self.wikiPage['content']
        sections = content.split(self.Separator)
        self.sections = []
        for section in sections:
            section = section.strip() # 末尾の改行を削除
            if not section: # 空のsectionはskip
                continue
            self.sections.append(Section(section))

    def addSection(self, period, projects):
        periods = [sec.period for sec in self.sections]
        if period in periods:
            index = periods.index(period)
            self.replaceSection(index, projects)
        else:
            self.appendSection(period, projects)
        return self

    # private
    def replaceSection(self, index, projects):
        newProjects = []
        for project in projects:
            newProject = Project()
            newProject.label = project
            for record in projects[project]:
                newProject.records.append(record)
            newProjects.append(newProject)
        self.sections[index].projects = newProjects

    # private
    def appendSection(self, period, projects):
        section = Section()
        section.period = period
        for project in projects:
            pj = Project()
            pj.label = project
            for record in projects[project]:
                pj.records.append(record)
            section.projects.append(pj)
        self.sections.append(section)

    def printSections(self):
        amountLabel = u'合計'
        content = ''
        for section in self.sections:
            content += f'# {section.period}{WikiBase.WikiLineSep}'
            for project in section.projects:
                content += f'{WikiBase.WikiLineSep}' # 段落
                content += f'## {project.label}{WikiBase.WikiLineSep}'
                if len(project.records) == 0:
                    content += f'- 該当タスクなし{WikiBase.WikiLineSep}'
                else:
                    content += f'|{Project.TaskLabel}|{Project.HoursLabel}|{WikiBase.WikiLineSep}'
                    content += f'|{Project.TaskLine}|{Project.HoursLine}|{WikiBase.WikiLineSep}'
                    amount = 0.0
                    for record in project.records:
                        if record[0] == amountLabel:
                            # 既に存在している合計のrecordをskip
                            continue
                        content += f'|{record[0]}|{record[1]}|{WikiBase.WikiLineSep}'
                        amount += float(record[1])
                    content += f'|{amountLabel}|{amount}|{WikiBase.WikiLineSep}'
            content += f'{self.Separator}{WikiBase.WikiLineSep}'
        self.writeWikiPage(content, False)

if __name__ == '__main__':
    pass
