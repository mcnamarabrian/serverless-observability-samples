import random
import time

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all


patch_all()


def big_winner(name, payout):
    xray_recorder.begin_subsegment('## big_winner')
    subsegment = xray_recorder.current_subsegment()
    subsegment.put_metadata('name', name)
    subsegment.put_metadata('payout', payout)

    if payout > 70:
        status = True
        # Arbitrary sleep if payout > 70
        time.sleep(5)
        subsegment.put_annotation('BIG_WINNER', 'YES')
    else:
        status = False
        subsegment.put_annotation('BIG_WINNER', 'NO')
    
    xray_recorder.end_subsegment()

    return(status)


def handler(event, context):    
    random_number = random.randrange(100) + 1
    random_winner = random.choice(['Svetlana', 'Brian', 'George', 'Sam', 'Adam', 'Roberto'])

    winner_status = big_winner(random_winner, random_number)

    payload = {
        'winner': random_winner, 
        'payout': random_number,
        'big_winner': winner_status
    }

    return(payload)
