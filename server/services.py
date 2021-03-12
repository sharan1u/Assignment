import random
from datetime import datetime
import requests
from requests.exceptions import RetryError
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from itertools import takewhile

http_netloc = 'http://'


class CustomRetry(Retry):

    def __init__(self, *args, **kwargs):
        super(CustomRetry, self).__init__(*args, **kwargs)

    def get_backoff_value(self, attempts):
        """
        generating an exponential value for multiple attempts
        """
        return self.backoff_factor * (10 ** (attempts - 1))

    def get_backoff_time(self):
        """ Formula for computing the current backoff
        :rtype: float
        """
        print(f'attempting to connect to the server {datetime.now().time()}')
        attempts = len(
            list(
                takewhile(lambda x: x.redirect_location is None, reversed(self.history))
            )
        )
        if attempts <= 1:
            return 0
        backoff_value = self.get_backoff_value(attempts)
        backoff_value_with_jitter = random.randrange(0, min(self.BACKOFF_MAX, backoff_value))
        return backoff_value_with_jitter


def make_request(url, retries):
    """
    utility method to initiate the incoming request
    """
    try:
        session_obj = requests.Session()
        session_obj.mount(http_netloc, HTTPAdapter(max_retries=retries))
        session_obj.get(url)
    except RetryError as e:
        raise RetryError




