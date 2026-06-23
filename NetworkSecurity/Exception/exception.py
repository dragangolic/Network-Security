import sys
from NetworkSecurity.Logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_messagge, error_details:sys):
        self.error_message = error_messagge
        _,_,exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in script: [{0}] line number [{1}] error message[{2}]".format(
        self.file_name,self.lineno, str(self.error_message))

# for test only
'''
if __name__ == "__main__":
    try:
        logger.logging.info("Enter the try block")
        a=1/0
        print("This will not be printed",a)
    except Exception as e:
        raise NetwrokSecurityException(e, sys)
'''