import logging

def get_logger(name):
    l = logging.getLogger(name)
    if not l.handlers:
        l.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s -%(message)s')
        
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        l.addHandler(file_handler)
        l.addHandler(console_handler)
    return l
logger = get_logger(__name__)

