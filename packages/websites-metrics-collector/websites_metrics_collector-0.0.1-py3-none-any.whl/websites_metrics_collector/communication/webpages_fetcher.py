import aiohttp
import asyncio
import time
from websites_metrics_collector.helpers.regex_functions import check_patterns_in_webpage
from collections import namedtuple
from typing import Tuple, NamedTuple

WebCheck = namedtuple('WebCheck', ['url', 'http_status', 'elapsed_time', 'pattern_verified'])


async def fetch_url_and_check_pattern(session: aiohttp.client.ClientSession, url: str,
                                      patter_to_verify: list) -> NamedTuple:
    """
    This function fetches the given url and stores the HTML content as text, the HTTP status and
    checks if the given pattern_to_verify exists in the HTML content fetched.
    To track the elapsed time for each request time.monotonic() is used ( https://www.python.org/dev/peps/pep-0418/ )
    time.monotonic() method of the time module in Python is used to get the value of a monotonic clock.
    A monotonic clock is a clock that can not go backwards. Using a time.monotonic() avoid falling into issues that can
    arise with time.time(). In fact, time.time() looks at the system clock that can be changed by the user and can produce
    values that go forwards and backwards, resulting in unexpected behaviour.

    :param session: an already instantiated aiohttp.client.ClientSession
    :param url: http://cloudbased.me
    :param patter_to_verify: ['Antonio Di Mariano', 'Cloud']
    :return: a NamedTuple like WebCheck(url='http://cloudbased.me', http_status=200, elapsed_time=0.5274228749999998, pattern_verified=True)
    """
    try:
        start = time.monotonic()
        async with session.get(url) as response:
            elapsed_time = time.monotonic() - start
            html_content = await response.text()

            result = WebCheck(url=url, http_status=response.status, elapsed_time=elapsed_time,
                              pattern_verified=check_patterns_in_webpage(html_content, patterns=patter_to_verify))
            return result
    except Exception as error:
        print(f"HTTP error occurred: {error}")


async def fetch_all_urls(session: aiohttp.client.ClientSession, urls: list) -> Tuple:
    """
    This function processes the list of the given url and for each value in the tuple
    an asyncio Task is created to schedule coroutines concurrently.
    Two parameters are passed: url[0] is the url, and url[1] is a list of patterns to verify against the fetched HTML content.

    :param session: an already instantiated aiohttp.client.ClientSession
    :param urls: a list of tuple[('http://motoguzzi.com',['twitter','Antonio']),('http://ferrari.com',['ferrari','url'])]
    :return: a NamedTuple like [WebCheck(url='http://motoguzzi.com', http_status=200, elapsed_time=2.43176225, pattern_verified=False), WebCheck(url='http://ferrari.com', http_status=200, elapsed_time=1.416772042, pattern_verified=False)]
    """
    tasks = []
    for url in urls:
        # The asyncio.create_task() function to run coroutines concurrently as asyncio Tasks.
        # Tasks are used to schedule coroutines concurrently.
        # When a coroutine is wrapped into a Task with functions like asyncio.create_task() the coroutine
        # is automatically scheduled to run soon
        #
        # https://docs.python.org/3/library/asyncio-task.html#id4

        task = asyncio.create_task(fetch_url_and_check_pattern(session, url[0], url[1]))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def fetch_list_of_urls(list_of_urls: list) -> tuple:
    """
    This function use a Context manager to create/destroy a ClientSession
    with aiohttp.ClientSession()  does not perform I/O when entering the block,
    but at the end of it, it will ensure all remaining resources are closed correctly.

    https://docs.aiohttp.org/en/latest/http_request_lifecycle.html
    :param list_of_urls:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        results = await fetch_all_urls(session, list_of_urls)
        return results
