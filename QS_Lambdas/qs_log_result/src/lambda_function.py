from QS_Crawlers import prod  # type: ignore


def lambda_handler(event, context, *args, **kwargs):
    prod.log_lambda(event)
