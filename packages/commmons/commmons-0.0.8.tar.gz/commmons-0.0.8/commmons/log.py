import logging

__all__ = [
    "get_prefixed_logger"
]


def get_prefixed_logger(parent_logger, prefix) -> logging.Logger:
    class CustomAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            return '[%s] %s' % (self.extra['prefix'], msg), kwargs

    return CustomAdapter(parent_logger, {'prefix': prefix})
