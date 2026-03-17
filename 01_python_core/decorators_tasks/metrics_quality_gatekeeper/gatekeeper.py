from functools import wraps
from itertools import chain

def validate_positive_integers(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        has_value_error = False
        
        for arg in chain(args, kwargs.values()):
            if type(arg) is not int:
                raise TypeError(f"Критическая ошибка: ожидался int, получен {type(arg).__name__} ({arg})")
            
            if arg <= 0:
                has_value_error = True
                
        if has_value_error:
            raise ValueError("Бизнес-ошибка: ID пользователей и метрики должны быть строго > 0")
            
        return func(*args, **kwargs)
        
    return wrapper

@validate_positive_integers
def calculate_user_ltv(user_id, transactions_count, revenue):
    return f"LTV для пользователя {user_id} успешно рассчитан."