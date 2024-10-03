# logger.py
import logging
import logging.config

def setup_logger(name):
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': f'{name}.log',
                'formatter': 'default',
            },
        },
        'loggers': {
            '': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        }
    })
    return logging.getLogger(name)

