import logging

def setup_logger():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    return logging.getLogger("TelegramBotLogger")

# Initialize the logger
logger = setup_logger()
