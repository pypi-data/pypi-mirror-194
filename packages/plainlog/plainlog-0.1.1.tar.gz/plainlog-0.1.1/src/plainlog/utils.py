def log_catch(
    logger,
    exception=Exception,
    *,
    level="ERROR",
    reraise=False,
    onerror=None,
    exclude=None,
    default=None,
    message="An error has been caught in function '{record[function]}', "
    "process '{record[process].name}' ({record[process].id}), "
    "thread '{record[thread].name}' ({record[thread].id}):"
):
    """Return a decorator to automatically log possibly caught error in wrapped function.
    This is useful to ensure unexpected exceptions are logged, the entire program can be
    wrapped by this method. This is also very useful to decorate |Thread.run| methods while
    using threads to propagate errors to the main logger thread.
    Note that the visibility of variables values (which uses the great |better_exceptions|_
    library from `@Qix-`_) depends on the ``diagnose`` option of each configured sink.
    The returned object can also be used as a context manager.
    Parameters
    ----------
    exception : |Exception|, optional
        The type of exception to intercept. If several types should be caught, a tuple of
        exceptions can be used too.
    level : |str| or |int|, optional
        The level name or severity with which the message should be logged.
    reraise : |bool|, optional
        Whether the exception should be raised again and hence propagated to the caller.
    onerror : |callable|_, optional
        A function that will be called if an error occurs, once the message has been logged.
        It should accept the exception instance as it sole argument.
    exclude : |Exception|, optional
        A type of exception (or a tuple of types) that will be purposely ignored and hence
        propagated to the caller without being logged.
    default : |Any|, optional
        The value to be returned by the decorated function if an error occurred without being
        re-raised.
    message : |str|, optional
        The message that will be automatically logged if an exception occurs. Note that it will
        be formatted with the ``record`` attribute.
    Returns
    -------
    :term:`decorator` / :term:`context manager`
        An object that can be used to decorate a function or as a context manager to log
        exceptions possibly caught.
    Examples
    --------
    >>> @logger.catch
    ... def f(x):
    ...     100 / x
    ...
    >>> def g():
    ...     f(10)
    ...     f(0)
    ...
    >>> g()
    ERROR - An error has been caught in function 'g', process 'Main' (367), thread 'ch1' (1398):
    Traceback (most recent call last):
    File "program.py", line 12, in <module>
        g()
        └ <function g at 0x7f225fe2bc80>
    > File "program.py", line 10, in g
        f(0)
        └ <function f at 0x7f225fe2b9d8>
    File "program.py", line 6, in f
        100 / x
            └ 0
    ZeroDivisionError: division by zero
    >>> with logger.catch(message="Because we never know..."):
    ...    main()  # No exception, no logs
    >>> # Use 'onerror' to prevent the program exit code to be 0 (if 'reraise=False') while
    >>> # also avoiding the stacktrace to be duplicated on stderr (if 'reraise=True').
    >>> @logger.catch(onerror=lambda _: sys.exit(1))
    ... def main():
    ...     1 / 0
    """
    if callable(exception) and (not isclass(exception) or not issubclass(exception, BaseException)):
        return self.catch()(exception)

    class Catcher:
        def __init__(self, from_decorator):
            self._from_decorator = from_decorator

        def __enter__(self):
            return None

        def __exit__(self, type_, value, traceback_):
            if type_ is None:
                return

            if not issubclass(type_, exception):
                return False

            if exclude is not None and issubclass(type_, exclude):
                return False

            from_decorator = self._from_decorator
            _, depth, _, *options = logger._options

            if from_decorator:
                depth += 1

            catch_options = [(type_, value, traceback_), depth, True] + options
            logger._log(level, from_decorator, catch_options, message, (), {})

            if onerror is not None:
                onerror(value)

            return not reraise

        def __call__(self, function):
            if isclass(function):
                raise TypeError(
                    "Invalid object decorated with 'catch()', it must be a function, "
                    "not a class (tried to wrap '%s')" % function.__name__
                )

            catcher = Catcher(True)

            if iscoroutinefunction(function):

                async def catch_wrapper(*args, **kwargs):
                    with catcher:
                        return await function(*args, **kwargs)
                    return default

            elif isgeneratorfunction(function):

                def catch_wrapper(*args, **kwargs):
                    with catcher:
                        return (yield from function(*args, **kwargs))
                    return default

            else:

                def catch_wrapper(*args, **kwargs):
                    with catcher:
                        return function(*args, **kwargs)
                    return default

            functools.update_wrapper(catch_wrapper, function)
            return catch_wrapper

    return Catcher(False)
