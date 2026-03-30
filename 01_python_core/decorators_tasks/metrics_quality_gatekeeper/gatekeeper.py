from typing import Callable, Any
from functools import wraps
from itertools import chain

def validate_positive_integers(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Декоратор для строгой валидации продуктовых метрик.
    Гарантирует, что все аргументы (например, user_id, session_count)
    являются строго положительными целыми числами.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        has_value_error = False
        
        # Единый проход по всем значениям с помощью генератора (O(1) по памяти)
        for arg in chain(args, kwargs.values()):
            # Используем type() вместо isinstance(), чтобы отсеять bool 
            # (в Python isinstance(True, int) возвращает True)
            if type(arg) is not int:
                raise TypeError(f"Критическая ошибка: ожидался int, получен {type(arg).__name__} ({arg})")
            
            # Если тип корректный, но значение <= 0, помечаем флаг ошибки
            if arg <= 0:
                has_value_error = True
                
        # Если цикл завершился без TypeError, но были отрицательные числа/нули:
        if has_value_error:
            raise ValueError("Бизнес-ошибка: ID пользователей и метрики должны быть строго > 0")
            
        return func(*args, **kwargs)
        
    return wrapper

# --- Пример использования в продуктовом коде ---

@validate_positive_integers
def calculate_user_ltv(user_id: int, transactions_count: int, revenue: int) -> str:
    """Моковая функция расчета LTV пользователя."""
    return f"LTV для пользователя {user_id} успешно рассчитан."

# Пример вызова, который успешно отработает:
# print(calculate_user_ltv(1024, 5, revenue=5000))

# Пример вызова, который вызовет TypeError (строка вместо int):
# print(calculate_user_ltv(1024, "5", 5000))

# Пример вызова, который вызовет ValueError (отрицательная выручка):
# print(calculate_user_ltv(1024, 5, revenue=-100))