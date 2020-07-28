import argparse
import logging
import time
from os import environ
from pymemcache.client import base
from prometheus_client import Histogram, start_http_server

#args
# noinspection PyTypeChecker
parser = argparse.ArgumentParser(description="Tool to benchmark memcache speed and generate "
                                             "prom metrics."
                                             "\nParameters can be also specified via env vars.",
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-mp", "--metricsport", type=int, help="port for prom metrics",
                    default=environ.get('METRICSPORT', 8000))
parser.add_argument("-s", "--sleep", type=int, help="how long to sleep between mc requests",
                    default=environ.get('SLEEP', 1))
parser.add_argument("-m", "--memcacheaddress", type=str,
                    default=environ.get('MEMCACHEADDRESS', "127.0.0.1"))
parser.add_argument("-p", "--memcacheport", type=int,
                    default=environ.get('MEMCACHEPORT', 11211))
parser.add_argument("-mk", "--memcachekey", type=str,
                    default=environ.get('MEMCACHEKEY', 'memcache-mon'))
parser.add_argument("-mv", "--memcachevalue", type=str,
                    default=environ.get('MEMCACHEVALUE', "memcache-val"))
parser.add_argument("-v", "--verbose", action="store_true",
                    default=environ.get('MEMCACHEMONVERBOSE', False),
                    help="env: MEMCACHEMONVERBOSE")
args = parser.parse_args()

# vars
mp = args.metricsport
sleep_time = args.sleep
mc = args.memcacheaddress
p = args.memcacheport
mk = args.memcachekey
mv = args.memcachevalue

REQUEST_TIME_GET = Histogram('memcache_get_request_latency_seconds', 'Time in seconds a memcache '
                                                                     'get operation takes')

REQUEST_TIME_SET = Histogram('memcache_set_request_latency_seconds', 'Time in seconds a memcache '
                                                                     'set operation takes')

# Decorate function with metric.
@REQUEST_TIME_GET.time()
def process_get_request(key):
    """get value from memcache"""
    try:
        client.get(key)
    except Exception:
        logger.warning("Error on mc get")


# Decorate function with metric.
@REQUEST_TIME_SET.time()
def process_set_request(key, value):
    """set value to memcache"""
    try:
        client.set(key, value)
    except Exception:
        logger.warning("Error on mc set")

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

if __name__ == '__main__':

    # create logger
    logger = logging.getLogger("memcache-mon")
    logger.setLevel(logging.INFO)

    # create console handler with a higher log level
    ch = logging.StreamHandler()

    if args.verbose:
        ch.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)

    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)

    logger.info("Daemon started, starting metrics..")

    # Start up the server to expose the metrics.
    start_http_server(mp)

    logger.info("prom metrics started on port %s, configuring memcache", mp)

    # configure memcache
    client = base.Client((mc, p))

    logger.info("memcache configured ip: %s port: %s, starting benchmark queries.. "
                "sleep: %s seconds",
                mc, p, sleep_time)

    # Generate some requests.
    while True:
        logger.debug("mc set")
        process_set_request(mk, mv)
        logger.debug("mc get")
        process_get_request(mk)
        logger.debug("sleep..")
        time.sleep(sleep_time)
