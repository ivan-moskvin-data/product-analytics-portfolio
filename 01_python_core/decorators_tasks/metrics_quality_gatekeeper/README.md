# Строгая валидация продуктовых метрик (Data Quality Gatekeeper)

### 📝 Бизнес-задача
Наша дата-инженерная платформа собирает логи о платежах пользователей. Аналитики часто вызывают функции расчета метрик (например, LTV или Retention), куда передают `user_id` и `transactions_count`. Если в пайплайн случайно попадет строковый ID, `None` из-за ошибки джойна или отрицательное количество транзакций (возвраты, которые нужно обрабатывать иначе), дашборды "поедут" или упадут с ошибкой. Нам нужен строгий gatekeeper (декоратор), который не пропустит мусор и гарантирует, что все параметры бизнес-функции являются строго положительными целыми числами. Приоритет ошибок: неверный тип данных (`TypeError`) важнее неверного значения (`ValueError`).

### 💡 Решение и производительность
Изначально алгоритм проверки работал за $O(n)$ по времени и $O(n)$ по памяти (из-за распаковки всех аргументов в новый список и двойного прохода), но был оптимизирован до $O(n)$ по времени и $O(1)$ по памяти за счет использования ленивого генератора `itertools.chain` и объединения проверок в один цикл. 

Это обеспечивает:
* **Мгновенную обработку логов** без выделения дополнительной памяти, что критично при высоких нагрузках.
* **Абсолютную защиту от type-spoofing'a**, так как строгая проверка `type(arg) is not int` успешно отсекает булевы значения (`True` / `False`), которые стандартный `isinstance` пропустил бы как валидные `1` и `0`.
* **Защиту витрин данных** от загрязнения и предотвращение падения аналитических пайплайнов из-за аномалий.

### 🛠 Стек
* Python (Core)
* Концепции: Big O, Decorators (`functools.wraps`), Lazy Evaluation (`itertools.chain`), Unit Testing (`pytest`).

### 🚀 Как использовать
```python
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

# Пример вызова функции с тестовыми данными
@validate_positive_integers
def calculate_user_ltv(user_id, transactions_count, revenue):
    return f"LTV для пользователя {user_id} успешно рассчитан."

if __name__ == "__main__":
    # Успешный расчет
    result = calculate_user_ltv(1024, 5, revenue=5000)
    print(result)
    
    # TypeError: Строковый ID вместо числового
    # calculate_user_ltv("1024", 5, 5000)
    
    # ValueError: Отрицательная выручка
    # calculate_user_ltv(1024, 5, revenue=-100)
    ```