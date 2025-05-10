import asyncio


async def run_async(func, *args, **kwargs):
    """
    Run a blocking function asynchronously.
    :param func: Blocking function
    :param args: Function arguments
    :param kwargs: Function keyword arguments
    :return: Result of the function
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


def safe_divide(a: float, b: float) -> float:
    """
    Safely divide two numbers without raising a ZeroDivisionError.
    :param a: Numerator
    :param b: Denominator
    :return: Division result or 0 if denominator is 0
    """
    return a / b if b != 0 else 0
