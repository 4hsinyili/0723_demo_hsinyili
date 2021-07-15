from QS_Crawlers import prod


def lambda_handler(event, context, *args, **kwargs):
    result = prod.get_topic_lambda()
    return result
