import azure.functions as func
from backlogapiprocessmodule import backlogapiprocess

def main(mytimer: func.TimerRequest) -> None:
    backlogapiprocess.run()
