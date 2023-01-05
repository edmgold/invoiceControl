import ormar
from functools import wraps

from controllers.utils.entity_not_found import entity_not_found


def get_controller(modelo: ormar.Model, select_related=[]):
    def inner(func):
        @entity_not_found
        @wraps(func)
        async def wrapper(id: int, **kwargs):
            consult = modelo.objects
            if len(select_related):
                consult = consult.select_related(select_related)
            entity = await consult.get(id=id)
            return entity
        return wrapper
    return inner