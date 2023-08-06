import logging

_level = logging.INFO
_logger = None


def setlevel(level=None):

    global _level, _logger

    if level:
        _level = level

    if _logger == None:
        # create logger
        _logger = logging.getLogger()

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(_level)

        # create formatter
        formatter = logging.Formatter(" %(levelname)s\t%(message)s")

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        _logger.addHandler(ch)

    for h in _logger.handlers:
        h.setLevel(_level)

    _logger.setLevel(_level)


def setdebug():
    setlevel(logging.DEBUG)


setlevel()


def _flat(args):
    fs = map(lambda x: str(x), args)
    return " ".join(fs)


def _log(level, args):
    if _logger.isEnabledFor(level):
        _logger.log(level, _flat(args))


def log(*args):
    _log(logging.INFO, args)


def print_t(*args):
    _log(logging.DEBUG, args)


def print_e(*args):
    _log(logging.CRITICAL, args)
