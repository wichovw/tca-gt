import logging

logger = logging.getLogger('TCA')
logger.setLevel(logging.DEBUG)

#Create file handler

handler = logging.FileHandler('tca.log', mode='w')
handler.setLevel(logging.DEBUG)

#Set up logging format
formatter = logging.Formatter('%(asctime)s %(levelname)5s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)