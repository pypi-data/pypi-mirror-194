import logging
import os
import sys

class Log(object):

    """
        %(levelno)s	    print log level value
        %(levelname)s	print log level name
        %(pathname)s	print the path of the currently executing program, which is actually sys.argv[0
        %(filename)s	print the name of the currently executing program
        %(funcName)s	print the current function of log
        %(lineno)d	    print the current line number of the log
        %(asctime)s	    print time of the print log
        %(thread)d	    print thread id
        %(threadName)s	print the name of the thread
        %(process)d	    print process id
        %(message)s	    print log information

        LOG LEVEL       CRITICAL > ERROR > WARNING > INFO > DEBUG
    """


    def __init__(self, file_name=None, log_name=None):
        self.logger = logging.getLogger(file_name)  # Add logger
        self.logger.setLevel(level=logging.INFO)  # Set log level
        self.console_format = logging.Formatter(fmt='[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s')  # set the log format
        self.file_format = logging.Formatter(fmt='[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s')  # set the log format
        self.log_dir = os.path.join(sys.path[0], 'logs', log_name)  # log file name

        if not self.logger.handlers:
            # Add a console handler
            ch = logging.StreamHandler()  # Add console handler
            ch.setLevel(level=logging.INFO)  # Set the log level of the processor
            ch.setFormatter(self.console_format)  # Processor Add Format
            self.logger.addHandler(ch)  # Logger add handler

            # Add a file handler
            fh = logging.FileHandler(filename=self.log_dir, encoding='utf-8')  # Add file handler
            fh.setLevel(level=logging.INFO)  # Set the log level of the processor
            fh.setFormatter(self.file_format)   # Processor Add Format
            self.logger.addHandler(fh)  # Logger add handler

    def init_logger(self):
        return self.logger


if __name__ == '__main__':

    logger = Log(file_name=None, log_name='test.log').init_logger() # Instantiate the log class and call the get_logger method

    logger.info('======[INFO TEST]======')
    logger.debug('======[DEBUG TEST]======')
    logger.warning('======[WARNING TEST]======')
    logger.error('======[ERROR TEST]======')
    logger.critical('======[CRITICAL TEST]======')
