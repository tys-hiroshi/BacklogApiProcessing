#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils.Issue import Issue

class Project(object):
    ''' projectを抽象化するクラス
    '''
    def __init__(self, projectKey, client, logger):
        self.project = None
        projects = client.projects()
        for project in projects:
            if project['projectKey'] == projectKey:
                self.project = project
                break
        if self.project is None:
            raise Exception(f'project not found: projectKey = {projectKey}')

        self.client = client
        self.logger = logger
        self.issues = None

    # private
    def getIssueTypeId(self, issueTypeName):
        issueTypes = self.client.project_issue_types(self.project['id'])

        issueTypeId = None
        for issueType in issueTypes:

            if not 'name' in issueType:
                continue

            name = issueType['name']
            if name != issueTypeName:
                continue

            issueTypeId = issueType['id']
            break

        return issueTypeId

    # private
    def getIssueKeys(self, issueTypeId, beginDate, endDate, operationType, maxCount):
        params = {
            'projectId[]': [self.project['id']],
            'issueTypeId[]': [issueTypeId],
            'sort': 'updated',
            'order': 'desc'
        }
        # maxCountが負の値の場合は、'count' を明示的に指定しない
        if maxCount >= 0:
            params['count'] = maxCount
        params[f'{operationType}Since'] = beginDate
        params[f'{operationType}Until'] = endDate
        issues = self.client.issues(params)

        issueKeys = []
        for issue in issues:
            issueKeys += [issue['issueKey']]

        return issueKeys

    def collectIssues(self, issueTypeName, beginDate, endDate, maxCount=-1):
        issueTypeId = self.getIssueTypeId(issueTypeName)
        if not issueTypeId: # 指定されたissue typeがこのprojectに存在しない
            return

        createdIssueKeys = self.getIssueKeys(issueTypeId, beginDate, endDate, 'created', maxCount)
        updatedIssueKeys = self.getIssueKeys(issueTypeId, beginDate, endDate, 'updated', maxCount)
        issueKeys = createdIssueKeys + updatedIssueKeys
        issueKeys = list(set(issueKeys))
        issueKeys.sort()

        issues = []
        for issueKey in issueKeys:
            issues += [Issue(issueKey, self.client, self.logger, beginDate, endDate)]
        self.issues = issues

    def getSummaryRecord(self, maxComments):
        if self.issues is None:
            raise Exception('issues have not been collected yet, call collectIssues() first')

        hours = 0.0
        for issue in self.issues:
            actualHours = issue.getActualHours(maxComments)
            self.logger.debug(f'actualHours: {actualHours}')
            hours += actualHours[1]
        return (self.project['name'], self.project['projectKey'], hours)

    def getDetailRecords(self, maxComments):
        if self.issues is None:
            raise Exception('issues have not been collected yet, call collectIssues() first')

        records = []
        for issue in self.issues:
            actualHours = issue.getActualHours(maxComments)
            self.logger.debug(f'actualHours: {actualHours}')
            records.append(actualHours)
        return (self.project['name'], self.project['projectKey'], records)

if __name__ == '__main__':
    pass
