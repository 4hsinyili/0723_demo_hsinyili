from QS_Crawlers import lambda_modules  # type: ignore


def lambda_handler(event, context, *args, **kwargs):
    result = lambda_modules.get_topic()
    return result
