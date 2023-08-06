from typing import Union


def accesslog(flag: bool) -> Union[str, None]:
    """
    Enable / disable access log in Gunicorn depending on the flag.
    """

    if flag:
        return "-"
    return None