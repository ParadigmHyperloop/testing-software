# Paradigm Python Logging Module
This module wraps some python logging functionality, ensuring python log format consistency across all of the paradigm-testing software. 

## Whats included in this package?
* `__init__.py`
* `logs/` - log folder containing a log file created using the module
* `loginit.py` - the module containing the log helper function(s), and some example usage
* `readme.md`

## log_init() Function

The log_init() function defined in the logInit.py module takes a project name and a logger object as the required arguements. The project name is used to name the log folder, and the function configures the logger object to write logs using a specific format to both stdout and a log file. This is achieved by creating a formatter object, attaching it to a stream and file handlers, and finally attaching the stream and file handlers to the logger object. The purpose of this function is to abstract the creation of formatters and handlers from the main code. 

The user can simply call `log_init(project, logger)` and the function will configure the logger with a default log format and a file / stream handler. The file is named {PROJECT-DATE}.log, and is placed in a `log/` folder in the cwd. 

The user can optionally specify a:
* formatStr - Format of logs (default="%(levelname)s - %(asctime)s - %(name)s - %(message)s")
* logFolderPath - Path to the log folder (default=cwd)
* logLevel - Log level to apply to the logger object (default=DEBUG)


## Usage
Import logging and the logInit module 
```
import logging 
from paralogging import logInit
```

Get root logger, and configure it with the log_init() function (docstring available) 
```
logger = logging.getLogger()
logInit.log_init("PROJECT", logger)
```
The primary purpose of log_init() is to configure the root logger of the system, and should only be called once. Any subsequent calls to logging.get_logger()
will return the same, already configured logger. Therefore, configuring the logger twice will result in all messages being printed twice (as the root logger 
will then have 4 total handlers)

Fianlly, use the configured logger to write logs when desired
```
logger.debug()
logger.info()
logger.warning()
logger.exception()
logger.error()
logger.critical()
```

The output log file will (by default) be of the form:  
INFO - 2020-05-01 20:21:16,705 - root - Message #1  
INFO - 2020-05-01 20:21:16,705 - root - Message #2  
INFO - 2020-05-01 20:21:16,705 - root - Message #3  
INFO - 2020-05-01 20:21:16,705 - root - Message #4  
INFO - 2020-05-01 20:21:16,705 - root - Message #5  
INFO - 2020-05-01 20:21:16,706 - root - Message #6  
INFO - 2020-05-01 20:21:16,706 - root - Message #7  
INFO - 2020-05-01 20:21:16,706 - root - Message #8  
INFO - 2020-05-01 20:21:16,706 - root - Message #9  

## Log Formatting Strings
The log_init() function takes an optional arguement for format string. This string decides the format of the logs as seen above. The default string used is:
```
 "%(levelname)s - %(asctime)s - %(name)s - %(message)s"
 ```

However, there are many more parameters available. The table below from the python docs (<https://docs.python.org/3/library/logging.html#logrecord-attributes>) contains all available parameters:

![Log Formatting Options Table](log-format-table.png)


