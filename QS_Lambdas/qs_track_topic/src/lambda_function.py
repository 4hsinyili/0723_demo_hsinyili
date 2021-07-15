from QS_Crawlers import prod  # type: ignore


def lambda_handler(event, context, *args, **kwargs):
    result = prod.track_topic_lambda(event)
    return result
