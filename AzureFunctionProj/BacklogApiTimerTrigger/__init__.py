import datetime
import logging

import azure.functions as func
from backlogapiprocessmodule import *

#BasePath = '/home/tashiro/projects/github/tys-hiroshi/BacklogApiProcessing_1/AzureFunctionProj/BacklogApiTimerTrigger/'

from chatworkpy.chatwork.rooms import Rooms
from chatworkpy.config import Config

BasePath = '/home/site/wwwroot/BacklogApiTimerTrigger/'
ConfigFilePath = BasePath + 'config.yml'
LoggingConfigFilePath = BasePath + 'logging_debug.conf'
#ConfigFilePath = '/home/site/wwwroot/BacklogApiTimerTrigger/config.yml'
#LoggingConfigFilePath = '/home/site/wwwroot/BacklogApiTimerTrigger/logging_debug.conf'

def main(mytimer: func.TimerRequest) -> None:
    try:
        utc_timestamp = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).isoformat()

        if mytimer.past_due:
            logging.info('The timer is past due!')

        logging.info('Python timer trigger function ran at %s', utc_timestamp)
        backlogapiprocess.run(ConfigFilePath, LoggingConfigFilePath)
    except Exception as e:
        chatwork_config = Config(ConfigFilePath).content["ALERT"]
        logging.info(f"ALERT IS {chatwork_config['IS_ENABLE']}")
        if not chatwork_config["IS_ENABLE"]:
            logging.error(e)
            return

        api_token = chatwork_config["CHATWORK_API_TOKEN"]
        room_id = chatwork_config["CHATWORK_ROOM_ID"]
        to_account_list = chatwork_config["CHATWORK_TO_ACCOUNT_LIST"]
        accounts_dict = []
        for account in to_account_list:
            accounts_dict.append({"account_id" : account["ID"], "name" : account["NAME"]})
        chatwork_rooms = Rooms(api_token, room_id)
        import traceback
        error_message = traceback.format_exc()  ##NOTE: get exception message
        chatwork_rooms.send_message(error_message, accounts_dict)