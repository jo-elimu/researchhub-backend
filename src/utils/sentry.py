import traceback

from sentry_sdk import capture_exception, capture_message, configure_scope


def log_error(e, base_error=None, message=None, json_data=None):
    """Captures an exception with the sentry sdk.

    Arguments:
        e (Exception)
        base_error (Exception) -- Exception that triggered e
        message (str) -- Optional message for additional info
        json_data (dict) -- Optional json data to send with the error
    """
    from researchhub.settings import PRODUCTION

    if not PRODUCTION:
        if isinstance(e, Exception):
            print(e, base_error, message)
            try:
                traceback.print_exception(e)
            except:
                pass
        else:
            print(e, base_error, message)

    with configure_scope() as scope:
        if base_error is not None:
            scope.set_extra("base_error", message)
        if message is not None:
            scope.set_extra("message", message)
        if json_data is not None:
            for k, v in json_data.items():
                if isinstance(v, dict):
                    for k2, v2 in v.items():
                        scope.set_extra(f"{k}_{k2}", v2)
                elif v is not None:
                    scope.set_extra(k, v)
        capture_exception(e)


def log_request_error(response, message, extra=None):
    from researchhub.settings import PRODUCTION

    if not PRODUCTION:
        print(response, message, extra)

    with configure_scope() as scope:
        if extra:
            for k in extra:
                scope.set_extra(k, extra[k])
        scope.set_extra("req_error", response.reason)
        capture_exception(message)


def log_info(message, error=None):
    """Captures a message with the sentry sdk.

    Arguments:
        message (str)
        error (obj) -- Optional error to send with the message
    """
    from researchhub.settings import PRODUCTION

    if not PRODUCTION:
        print(message, error)

    with configure_scope() as scope:
        if error is not None:
            scope.set_extra("error", error)
        capture_message(message)
