from Logging import LoggerCore 

class LoggerTest:
    
    def __init__(self):
        self._logger = LoggerCore()
        if self._logger:
            self._logger._configure('file', 'loggerOutput.txt')
            self._logger._print('Test Print String')
            
            x = 0
            while x < 10:
                self._logger._print('Testing print: ' + str(x))
                x+=1
        self._logger = None
        
a = LoggerCore()
b = LoggerCore()     
