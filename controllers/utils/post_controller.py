import ormar
from functools import wraps

def post_controller (func):
    @wraps(func)
    async def wrapper(entity: ormar.Model, **kwargs):
            await entity.save()
            return entity
    return wrapper