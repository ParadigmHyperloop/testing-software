""" logInit.py

This module contains helper functions for initializing loggers
for the various paradigm research/testing rigs. The purpose of
this module is to ensure log format consistency across all code """

import logging
import os
from datetime import date


def log_init(project, logger, formatStr=None, logFolderPath=None, logLevel=None):
    """ Initialize the root logger for the specified system 
    
    Args:
        project(str) - The name of the project (DTS, Stability, WindTunnel) 
        
        logger(Logger) - logger object, will generally be the root logger
        
        formatStr(str, optional) - The format log messages will be printed 
            default - "%(levelname)s - %(asctime)s - %(name)s - %(message)s"
            
        logFolderPath(str, optional) - The path to the folder to place the log files,
            (should end in /logs)
            default - "cwd/logs"
            
        logLevel(str) - The log level of the root logger. Can be one of
            [DEBUG, INFO, WARNING, ERROR, CRITICAL], any messages of lower
            criticality will not be logged by the root logger.
            default - DEBUG (All messages) 
    """
    if logLevel is None:
        logLevel = "DEBUG"
    
    if formatStr is None:
        formatStr = "%(levelname)s - %(asctime)s - %(name)s - %(message)s"
    formatter = logging.Formatter(formatStr)
    
    if logFolderPath is None:
        logFolderPath = os.path.join(os.getcwd(), "logs")
        
    fileName = f"{project}-{str(date.today())}.log"
    filePath = os.path.join(logFolderPath, fileName)
    
    if not os.path.exists(logFolderPath):
        os.makedirs(logFolderPath)

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    
    fileHandler = logging.FileHandler(filename=filePath)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    logger.setLevel(logLevel)
    logger.info(f"{project} ROOT LOGGER INITIALIZED, READY FOR USE")


if __name__ == "__main__":
    # Functional examples
    
    def default_root_log(msg):
        """ Test using default logger settings """
        logger = logging.getLogger()
        log_init("DTS", logger)
        logger.info(msg)
        
    def custom_root_log(msg):
        """ Test using custom log path, format string, and log level """
        logger = logging.getLogger()
        log_init("DTS", logger,  "%(levelname)s - %(message)s", "/mnt/c/logs", "INFO")
        logger.info(msg)
        
        
    default_root_log(f"Called init to setup root logger with default settings...")
    logger = logging.getLogger()
    
    for i in range(1,101):
        logger.info(f"Message #{i}")