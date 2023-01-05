from functools import wraps
import ormar

from controllers.utils.entity_not_found import entity_not_found

def delete_controller(modelo: ormar.Model):
    def inner(func):
        @entity_not_found
        @wraps(func)
        async def wrapper(id: int, **kwargs):
            entidade = await modelo.objects.get(id=id)
            return await entidade.delete()
        return wrapper
    return inner