def should_raise_error(block, error_type):
    try:
        block()
    except Exception as e:
        if not isinstance(e, error_type):
            raise AssertionError

        return

    raise AssertionError


def should_not_contains(value, substr):
    if substr in value:
        raise AssertionError


def should_contains(value, substr):
    if substr not in value:
        raise AssertionError
