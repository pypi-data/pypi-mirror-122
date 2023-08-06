def user(message_):
    if message_ is not None:
        _user = message_.user
    else:
        _user = None
    return {"user": _user}


def message(message_):
    return {"message": message_}
