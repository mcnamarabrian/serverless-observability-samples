import random

from aws_embedded_metrics import metric_scope


@metric_scope
def handler(event, context, metrics):    
    random_number = random.randrange(100) + 1
    random_winner = random.choice(['Svetlana', 'Brian', 'George', 'Sam', 'Adam', 'Roberto'])

    metrics.set_namespace('Lottery')
    metrics.put_dimensions({'service':'payout_service'})
    metrics.put_metric('PayoutAmount', random_number, 'Sum')
    metrics.set_property('Player', random_winner)
    metrics.set_property('RequestId', context.aws_request_id)

    payload = {'winner': random_winner, 'payout': random_number}
    return(payload)
