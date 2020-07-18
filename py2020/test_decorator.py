from functools import wraps


''' useful doc: https://www.runoob.com/w3cnote/python-func-decorators.html '''

def logit(logfile='logit.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            with open(logfile, 'a') as opened_file:
                opened_file.write(log_string + '\n')
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator


@logit()
def myfunc1():
    pass


@logit(logfile='func2.log')
def myfunc2():
    pass


if __name__ == '__main__':
    myfunc1()
    myfunc2()