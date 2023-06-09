from datetime import datetime
import asyncio
import logging
from time import sleep
from random import randint

from decorators import custom_cache, log_execution, \
    timing_decorator, retry_upon_exceptions, \
    email_on_failure, async_timing_decorator


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


@retry_upon_exceptions(exceptions=(ValueError, TypeError),
                       max_retries=10, delay_seconds=1)
def raising_exception_func():
    random_num = randint(1, 50)
    if random_num % 2 == 0:
        raise ValueError("Dummy message on ValueError")
    elif random_num % 3 == 0:
        raise TypeError("Dummy message on TypeError")
    raise KeyError("Dummy message on KeyError")


@log_execution
def function_logging(limit_number, step, dummy_kwarg, dummy_kwarg_2):
    counter = 0
    while counter < limit_number:
        counter += step
        sleep(counter)
    return


@email_on_failure(sender_email="<sender gmail here>",
                  password="<an app password here for sender gmail>",
                  recipient_email="recipient gmail here")
def critical_function(limit_number, step=1):
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


@custom_cache
def fibonacci_w_cache(n):
    if n <= 1:
        return n
    else:
        return fibonacci_w_cache(n-1) + fibonacci_w_cache(n-2)


print("\n")
logging.info("Calling function count_function_timing")
count_function_timing(3, step=1)

print("\n")
logging.info("Calling function function_logging")
function_logging(4, 1, dummy_kwarg="some string", dummy_kwarg_2=3)

print("\n")
logging.info("Calling function raising_exception_func")
try:
    raising_exception_func()
except KeyError as exc:
    logging.warning(f"Caught exception after retry: {exc}")


print("\n")
logging.info(f"Calling function fibonacci_no_cache")
fibonacci_first_numbers = 50
start = datetime.utcnow()
result = fibonacci_no_cache(fibonacci_first_numbers)
end = datetime.utcnow()
logging.info(f"Calculation without cache for \n"
             f"{fibonacci_first_numbers}th fibonacci number took \n"
             f"{(end-start).total_seconds()} seconds,\n"
             f"result is {result}")

print("\n")
logging.info(f"Calling function fibonacci_w_cache")
start = datetime.utcnow()
result = fibonacci_w_cache(fibonacci_first_numbers)
end = datetime.utcnow()
logging.info(f"Calculation with cache for \n"
             f"{fibonacci_first_numbers}th fibonacci number took \n"
             f"{(end-start).total_seconds()} seconds, \n"
             f"result is {result}")

print("\n")
logging.info("Calling function count_function_timing")
count_function_timing(3, 1)


logging.info("Calling coroutine async_count_function_timing")
task = async_count_function_timing(3, 1)
asyncio.run(task)
