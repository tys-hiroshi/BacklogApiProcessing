import azure.functions as func
import BacklogApiProcessing

def main(mytimer: func.TimerRequest) -> None:
    BacklogApiProcessing.run()
