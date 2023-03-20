import time
from functools import wraps
import logging
logging.basicConfig(level=logging.INFO)
import smtplib
import traceback
from email.mime.text import MIMEText


# retry decorator function
def retry(max_tries=3, delay_seconds=1):
    def decorator_retry(func):
        @wraps(func)
        def wrapper_retry(*args, **kwargs):
            tries = 0
            while tries < max_tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"Function {func.__name__} failed with an exception, "
                                    f"retrying in {delay_seconds} seconds")
                    tries += 1
                    if tries == max_tries:
                        raise e
                    time.sleep(delay_seconds)
        return wrapper_retry
    return decorator_retry


# manual cache decorator function
def memoize(func):
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
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
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
                logging.error(f"Exception caught, sending an email to {recipient_email} via account {sender_email}")
                err_msg = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"

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
