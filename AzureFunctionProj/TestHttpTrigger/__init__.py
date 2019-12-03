import logging

import azure.functions as func
from backlogapiprocessmodule import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('-------Python HTTP trigger function processed a request.')
    configFilePath = '/home/site/wwwroot/BacklogApiTimerTrigger/config.yml'
    loggingConfigFilePath = '/home/site/wwwroot/BacklogApiTimerTrigger/logging_debug.conf'
    backlogapiprocess.run(configFilePath, loggingConfigFilePath)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
