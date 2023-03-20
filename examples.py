import datetime

from decorators import memoize, log_execution, timing_decorator, retry, email_on_failure
from time import sleep
import logging


@timing_decorator
def count_function_timing(limit_number, step=1):
    counter = 0
    while counter < limit_number:
        counter += step
        sleep(counter)
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


@email_on_failure(sender_email="christos.karvouniaris247@gmail.com",
                  password="<an app password here for gmail>",
                  recipient_email="christos.karvouniaris247@gmail.com")
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
    print(e)

# print("\n")
# logging.info("Calling function count_function_email_exception")
# try:
#     count_function_email_exception(10, step=2)
# except ValueError as e:
#     print(e)

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
