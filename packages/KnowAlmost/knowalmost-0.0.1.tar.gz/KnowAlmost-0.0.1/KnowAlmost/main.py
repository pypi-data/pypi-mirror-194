import requests
import time
import sys

from loguru import logger

from KnowAlmost.utils.error import (
    BadRequest, Forbidden, HTTPException, NotFound, TooManyRequests,
    KnowAlmostException, Unauthorized, KnowAlmostServerError
)
from KnowAlmost.utils.util import get_x96
from setting import LIST_PARAMS, LIST_HEADERS
from urllib.parse import urlencode


class API:
    """KnowAlmost API v1.0.1 Interface
    """

    def __init__(
        self, *, host='www.zhihu.com',
        proxy=None, retry_count=0, retry_delay=0, retry_errors=None,
        timeout=60,
        wait_on_rate_limit=False
    ):
        self.host = host
        self.proxy = {}
        if proxy is not None:
            self.proxy['https'] = proxy

        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.timeout = timeout

        self.wait_on_rate_limit = wait_on_rate_limit

        self.session = requests.Session()

    def request(
        self, endpoint_parameters=(), params=None, query="", token="",
        headers=None, offset=0, search_source="Normal",
        **kwargs
    ):
        if headers is None:
            headers = LIST_HEADERS
        headers["Cookie"] = f"d_c0={token};"

        # Build the request URL
        path = '/api/v4/search_v3'
        url = 'https://' + self.host + path

        if params is None:
            params = LIST_PARAMS
        params['q'] = query
        params['offset'] = offset
        params['search_source'] = search_source

        for k, arg in kwargs.items():
            if arg is None:
                continue
            if k not in endpoint_parameters + (
                "gk_version", "t", "correction", "filter_fields", "lc_idx", "show_all_topics", "limit"
            ):
                logger.warning(f'Unexpected parameter: {k}')
            else:
                params[k] = str(arg)

            if k in (
                    "user-agent", "x-api-version", "x-zse-93"
            ):
                headers[k] = str(arg)
        xzse_96 = get_x96(token=token, search_api=path+'?'+urlencode(params))
        headers["x-zse-96"] = xzse_96
        logger.info(f"PARAMS: {params}")
        logger.info(f"HEADERS: {headers}")

        remaining_calls = None
        reset_time = None

        try:
            # Continue attempting request until successful
            retries_performed = 0
            while retries_performed <= self.retry_count:
                if (self.wait_on_rate_limit and
                        reset_time is not None and remaining_calls is not None and remaining_calls < 1):
                    # Handle running out of API calls
                    sleep_time = reset_time - int(time.time())
                    if sleep_time > 0:
                        logger.warning(f"Rate limit reached. Sleeping for: {sleep_time}")
                        time.sleep(sleep_time + 1)  # Sleep for extra sec

                # Execute request
                try:
                    resp = self.session.request(
                        "GET", url, params=params, headers=headers,
                        timeout=self.timeout, proxies=self.proxy
                    )

                except Exception as e:
                    raise KnowAlmostException(f'Failed to send request: {e}').with_traceback(sys.exc_info()[2])

                if 200 <= resp.status_code < 300:
                    break

                retry_delay = self.retry_delay
                if resp.status_code in (420, 429) and self.wait_on_rate_limit:
                    if remaining_calls == 0:
                        # If ran out of calls before waiting switching retry last call
                        continue
                    if 'retry-after' in resp.headers:
                        retry_delay = float(resp.headers['retry-after'])
                elif self.retry_errors and resp.status_code not in self.retry_errors:
                    # Exit request loop if non-retry error code
                    break

                # Sleep before retrying request again
                time.sleep(retry_delay)
                retries_performed += 1

            # If an error was returned, throw an exception
            self.last_response = resp
            if resp.status_code == 400:
                raise BadRequest(resp)
            if resp.status_code == 401:
                raise Unauthorized(resp)
            if resp.status_code == 403:
                raise Forbidden(resp)
            if resp.status_code == 404:
                raise NotFound(resp)
            if resp.status_code == 429:
                raise TooManyRequests(resp)
            if resp.status_code >= 500:
                raise KnowAlmostServerError(resp)
            if resp.status_code and not 200 <= resp.status_code < 300:
                raise HTTPException(resp)

            # Parse the response payload
            return self.last_response
        finally:
            self.session.close()

api = API()
token = 'APAdAlwbIBWPThzJMZJuMEoPksQPWXxgiTc=|1655711908'

print(api.request(query="高启强", token=token).content)