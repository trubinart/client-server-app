import datetime
from functools import wraps
import inspect
import logging

logging.basicConfig(level=logging.INFO)


def log(logger):
    def logggining(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            main_func = func(*args, **kwargs)
            end_time = datetime.datetime.now()
            performing_time = end_time - start_time
            func_name = func.__name__
            func_args = {'args': inspect.getargvalues(inspect.currentframe()).locals['args'],
                         'kwargs': inspect.getargvalues(inspect.currentframe()).locals['kwargs']}

            parent_name = inspect.currentframe().f_back.f_code.co_name
            # parent_args = inspect.getargvalues(inspect.currentframe().f_back).locals

            if parent_name != '<module>':
                logger.info(
                    f'Из parent_func: {parent_name} | отработала func: {func_name} '
                    f'| {func_args} | time: {performing_time}')
            else:
                logger.info(f'Отработала func: {func_name} '
                            f'| {func_args} | time: {performing_time}')
            return main_func

        return wrapper

    return logggining


if __name__ == "__main__":
    @log(logging)
    def func_z(a, b):
        a + b
        print('z function')


    @log(logging)
    def go(a, to):
        print(f'GO function {a * to}')


    def want(a, to):
        func_z(1, 5)
        print(f'WANT function {a * to}')


    go(4, to=5)
    want(4, to=40)
    func_z(1, 2)
