import functools
from typing import Callable, Any

def tag_metric_metadata(**metadata: Any) -> Callable:
    """
    Декоратор для обогащения функций расчета метрик бизнес-метаданными.
    Используется для построения каталога метрик и маршрутизации алертов.
    
    :param metadata: Произвольные именованные аргументы (теги метрики).
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Здесь можно добавить логирование запуска, если нужно,
            # но пока мы просто проксируем вызов оригинальной функции
            return func(*args, **kwargs)
        
        # Безопасно устанавливаем атрибуты через встроенный setattr, 
        # вместо прямого мутирования __dict__
        for key, value in metadata.items():
            setattr(wrapper, key, value)
            
        return wrapper
    return decorator


# --- Пример использования в продуктовой аналитике ---

@tag_metric_metadata(
    owner="product_growth_team", 
    data_source="clickhouse_events", 
    is_critical=True,
    sla_minutes=15
)
def calculate_retention_rate(cohort_id: str, day: int) -> float:
    """
    Рассчитывает Retention Rate для заданной когорты на указанный день.
    """
    # Имитация обращения к БД и расчета метрики
    if not cohort_id:
        raise ValueError("cohort_id не может быть пустым")
    
    # Заглушка: возвращаем условный Retention 7 дня в 25.5%
    return 25.5

# Проверка работы
if __name__ == "__main__":
    retention = calculate_retention_rate(cohort_id="2023-10-W1", day=7)
    
    print(f"Результат функции: {retention}%")
    print(f"Имя функции: {calculate_retention_rate.__name__}")
    print(f"Владелец метрики: {calculate_retention_rate.owner}")
    print(f"Источник данных: {calculate_retention_rate.data_source}")
    print(f"Критичность: {calculate_retention_rate.is_critical}")