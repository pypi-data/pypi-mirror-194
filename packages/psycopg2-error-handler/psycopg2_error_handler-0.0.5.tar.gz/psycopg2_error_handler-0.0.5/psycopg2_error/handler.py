import asyncio
from functools import wraps

from psycopg2 import DatabaseError

from psycopg2_error.errors import sqlstate_errors


def psycopg2_error_handler(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except DatabaseError as err:
                catch(err)
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except DatabaseError as err:
                catch(err)
    return wrapper


def catch(err):
    pgorig = getattr(err, "orig")

    if pgorig:
        pgcode = getattr(pgorig, "pgcode")
        if pgcode:
            raise sqlstate_errors.get(pgcode, err.orig)(err.orig.pgerror)
    raise err
