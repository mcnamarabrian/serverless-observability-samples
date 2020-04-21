import logging
import random

import aws_lambda_logging


log = logging.getLogger()

def handler(event, context):
    aws_lambda_logging.setup(level='DEBUG',
                             aws_request_id=context.aws_request_id)
    
    random_number = random.randrange(100) + 1
    
    log.info({"Number": random_number})
    return(random_number)
