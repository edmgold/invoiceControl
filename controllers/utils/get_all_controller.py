import ormar
from functools import wraps


def get_all_controller(model: ormar.Model):
    def inner(func):
        @wraps(func)
        async def wrapper(**kwargs):
                return await model.objects.all()
        return wrapper
    return inner