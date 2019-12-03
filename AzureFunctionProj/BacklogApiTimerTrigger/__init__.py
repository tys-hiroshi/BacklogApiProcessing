import datetime
import logging

import azure.functions as func
from backlogapiprocessmodule import *

#BasePath = '/home/tashiro/projects/github/tys-hiroshi/BacklogApiProcessing_1/AzureFunctionProj/BacklogApiTimerTrigger/'

BasePath = '/home/site/wwwroot/BacklogApiTimerTrigger/'
ConfigFilePath = BasePath + 'config.yml'
LoggingConfigFilePath = BasePath + 'logging_debug.conf'
#ConfigFilePath = '/home/site/wwwroot/BacklogApiTimerTrigger/config.yml'
#LoggingConfigFilePath = '/home/site/wwwroot/BacklogApiTimerTrigger/logging_debug.conf'

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    backlogapiprocess.run(ConfigFilePath, LoggingConfigFilePath)

