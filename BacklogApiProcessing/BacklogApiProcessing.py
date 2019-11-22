#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.Config import Config
from utils.Logger import Logger
from utils.AppManager import AppManager

ConfigFile = 'config.yml'
LogConfigFile = 'logging_debug.conf'

def run(argv=[]):
    def doProcessing(day, config, logger):
        beginDate = datetime(day.year, day.month, 1)
        endDate = datetime(day.year, day.month, 1) + relativedelta(months=1) - relativedelta(days=1)
        beginDate = beginDate.strftime('%Y-%m-%d')
        endDate = endDate.strftime('%Y-%m-%d')
        logger.info(f'start processing: beginDate = {beginDate}, endDate={endDate}')

        app = AppManager(config, logger)
        maxCount = 100 # backlog APIとしての上限が、現状はこの値らしい
        maxComments = 100 # backlog APIとしての上限が、現状はこの値らしい
        periodLabel = f'{beginDate} 〜 {endDate}'
        app.collectIssues(config['PROCESSING_ISSUE_TYPE_NAME'], beginDate, endDate, maxCount)
        app.reportSummary(config['PROCESSING_UPDATE_WIKI']['SUMMARY_WIKI_ID'], periodLabel, maxComments)
        app.reportDetail(config['PROCESSING_UPDATE_WIKI']['DETAIL_WIKI_ID'], periodLabel, maxComments)

    config = Config(ConfigFile).content
    logger = Logger(LogConfigFile)

    argc = len(argv)
    if argc > 1: # 引数が指定された場合
        days = [datetime.strptime(day, '%Y-%m') for day in argv[1:]]
    else:
        days = [datetime.today()]

    for day in days:
        doProcessing(day, config, logger)

if __name__ == '__main__':
    '''
    Usage: [python] BacklogApiProcessing.py [yyyy-mm [...]]
    '''
    import sys
    run(sys.argv)
