

class DTHealth_StateMacine:
    
    def __init__(self, catchfrazeStart: str = [["anna", "hallo"], ["anna", "hello"]],  catchfrazeStop: str = ["anna", "danke"]):
        print("Inizalizise State Macine")
        self.CommandState = False
        self.NormalState = False
    
        self.catchfrazeStart = catchfrazeStart
        self.catchfrazeStop = catchfrazeStop

    def eval_st_sp_state(self, message:str) -> bool: #State Change
        if self.CommandState == False and self.eval_start_state(message):
            print("Stram Start")
            self.CommandState = True
        #Testet Keyword Start Stop
        elif self.CommandState == True and self.eval_stop_state(message):
            self.CommandState = False
        else:
            return False
        return True

    def eval_start_state(self, message: str)-> bool:
        message = message.lower()
        if all(x in message for x in self.catchfrazeStart[0]) or all(x in message for x in self.catchfrazeStart[1]):
            return True
        else:
            return False

    def eval_stop_state(self, message: str)-> bool:
        message = message.lower()
        if all(x in message for x in self.catchfrazeStop):
            return True
        else:
            return False

    def eval_custom_fraze(self, message: str, catchfraze: str)-> bool:
        message = message.lower()
        if all(x in message for x in catchfraze):
            return True
        else:
            return False