from QS_Crawlers import lambda_modules  # type: ignore


def lambda_handler(event, context, *args, **kwargs):
    lambda_modules.step_function_log(event)
