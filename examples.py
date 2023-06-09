import datetime

from decorators import memoize, log_execution, timing_decorator, retry, \
    email_on_failure, async_timing_decorator
from time import sleep
import logging
import asyncio


@timing_decorator
def count_function_timing(limit_number, step=1):
    counter = 0
    while counter < limit_number:
        counter += step
        sleep(step)
    return


@async_timing_decorator
async def async_count_function_timing(limit_number, step=1):
    counter = 0
    while counter < limit_number:
        counter += step
        sleep(step)
    return


@retry(max_tries=3, delay_seconds=1)
def count_function_retry(limit_number, step=1):
    counter = 0
    while counter < limit_number:
        counter += step
        sleep(counter)
    raise ValueError(f"Exceeded limit {limit_number}")


@log_execution
def count_function_logging(limit_number, step=1):
    counter = 0
    while counter < limit_number:
        counter += step
        sleep(counter)
    return


@email_on_failure(sender_email="<sender gmail here>",
                  password="<an app password here for sender gmail>",
                  recipient_email="recipient gmail here")
def count_function_email_exception(limit_number, step=1):
    counter = 0
    while counter < limit_number:
        counter += step
        sleep(counter)
    raise ValueError(f"Exceeded limit {limit_number}")


def fibonacci_no_cache(n):
    if n <= 1:
        return n
    else:
        return fibonacci_no_cache(n-1) + fibonacci_no_cache(n-2)


@memoize
def fibonacci_w_cache(n):
    if n <= 1:
        return n
    else:
        return fibonacci_w_cache(n-1) + fibonacci_w_cache(n-2)


print("\n")
logging.info("Calling function count_function_timing")
count_function_timing(3, step=1)

print("\n")
logging.info("Calling function count_function_logging")
count_function_logging(4, step=1)

print("\n")
logging.info("Calling function count_function_retry")
try:
    count_function_retry(5, step=1)
except ValueError as e:
    logging.info(e)


print("\n")
logging.info(f"Calling function fibonacci_no_cache")
fibonacci_first_numbers = 40
start = datetime.datetime.utcnow()
result = fibonacci_no_cache(fibonacci_first_numbers)
end = datetime.datetime.utcnow()
logging.info(f"Fibonacci without cache for first {fibonacci_first_numbers} took {(end-start).total_seconds()} seconds, "
             f"result is {result}")

print("\n")
logging.info(f"Calling function fibonacci_w_cache")
start = datetime.datetime.utcnow()
result = fibonacci_w_cache(fibonacci_first_numbers)
end = datetime.datetime.utcnow()
logging.info(f"Fibonacci with cache for first {fibonacci_first_numbers} took {(end-start).total_seconds()} seconds, "
             f"result is {result}")

print("\n")
logging.info("Calling function async_count_function_timing")
task = async_count_function_timing(3, 1)
asyncio.run(task)