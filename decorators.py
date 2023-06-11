from time import sleep
from functools import wraps
import logging
logging.basicConfig(level=logging.INFO)
import smtplib
import traceback
from email.mime.text import MIMEText
import asyncio
from datetime import datetime


# retry decorator function
def retry_upon_exceptions(exceptions, max_retries=3, delay_seconds=1):
    def decorator_retry(func):
        @wraps(func)
        def wrapper_retry(*args, **kwargs):
            tries = 0
            while tries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as exception:
                    logging.warning(f"Function {func.__name__} failed with an "
                                    f"exception {exception.__class__.__name__}, "
                                    f"retrying in {delay_seconds} seconds")
                    tries += 1
                    if tries == max_retries:
                        raise exception
                    sleep(delay_seconds)
        return wrapper_retry
    return decorator_retry


# manual cache decorator function
def custom_cache(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result
    return wrapper


# timing decorator function
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.utcnow()
        result = func(*args, **kwargs)
        end_time = datetime.utcnow()
        logging.info(f"Function {func.__name__} took "
                     f"{round((end_time - start_time).total_seconds(), 3)} seconds to run.")
        return result
    return wrapper


def async_timing_decorator(func):
    async def process(func, *args, **params):
        if asyncio.iscoroutinefunction(func):
            logging.info("This is a coroutine")
            return await func(*args, **params)
        else:
            logging.info("This is a function")
            return func(*args, **params)

    async def wrapper(*args, **params):
        start_time = datetime.utcnow()
        result = await process(func, *args, **params)
        end_time = datetime.utcnow()
        logging.info(f"Function {func.__name__} took {round((end_time - start_time).total_seconds(), 3)} seconds to run.")
        return result

    return wrapper


# log execution decorator function
def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__} with positional arguments "
                     f"{[arg for arg in args]} and keyword arguments {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"Finished executing {func.__name__}")
        return result
    return wrapper


#  email on failure decorator
def email_on_failure(sender_email, password, recipient_email):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # format the error message and traceback
                logging.error(f"Exception caught, "
                              f"sending an email to {recipient_email} "
                              f"via account {sender_email}")
                err_msg = f"Error: {str(e)}\n\nT" \
                          f"raceback:\n{traceback.format_exc()}"

                # create the email message
                message = MIMEText(err_msg)
                message['Subject'] = f"{func.__name__} failed"
                message['From'] = sender_email
                message['To'] = recipient_email

                # send the email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(sender_email, password)
                    smtp.sendmail(sender_email, recipient_email, message.as_string())
                # re-raise the exception
                raise
        return wrapper
    return decorator


def call_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        result = func(*args, **kwargs)
        logging.info(f'{func.__name__} has been called {wrapper.count} times')
        return result
    wrapper.count = 0
    return wrapper
