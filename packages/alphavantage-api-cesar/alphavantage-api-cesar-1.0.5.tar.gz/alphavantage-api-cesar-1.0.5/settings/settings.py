from decouple import config
import logging as logger

APIKEY = config("APIKEY")
BASE_URL = config("BASE_URL", "https://www.alphavantage.co/query")
LOG_FILENAME = config("LOG_FILENAME","api.log")

log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'

logger.basicConfig(filename=LOG_FILENAME,
                   
                    filemode='w',
                    level=logger.DEBUG,
                    format=log_format)
log = logger.getLogger('root')
