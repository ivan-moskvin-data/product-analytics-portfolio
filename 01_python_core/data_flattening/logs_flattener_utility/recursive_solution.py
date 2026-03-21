from typing import Any, Dict

def print_flattened_logs_recursive(raw_logs: Dict[str, Any]) -> None:
    """
    Рекурсивно преобразует многоуровневый JSON-лог в плоскую структуру.
    
    Идеально подходит для логов с небольшой и предсказуемой глубиной вложенности.
    Использует системный стек вызовов.
    
    Args:
        raw_logs (Dict[str, Any]): Исходный лог события пользователя.
    """
    # Базовая защита: если пришел не словарь или он пустой, ничего не делаем
    if not isinstance(raw_logs, dict) or not raw_logs:
        return

    flat_logs: Dict[str, Any] = {}

    # Внутренняя рекурсивная функция обхода
    def traverse_node(current_node: Dict[str, Any], prefix: str) -> None:
        for key, value in current_node.items():
            # Формируем составной ключ (например, session.device.os)
            current_key = f"{prefix}.{key}" if prefix else str(key)
            
            # Если значение — словарь, уходим в рекурсию (вглубь)
            if isinstance(value, dict):
                # Проверка на пустой словарь, чтобы не создавать "мертвые" ключи
                if value:
                    traverse_node(value, current_key)
            else:
                # Если дошли до конца, сохраняем в результат
                flat_logs[current_key] = value

    # Запускаем рекурсию с самого верхнего уровня (пустой префикс)
    traverse_node(raw_logs, "")

    # Сортировка по ключам обеспечивает лексикографический порядок
    for key in sorted(flat_logs.keys()):
        print(f"{key}: {flat_logs[key]}")


# Пример использования (тестовые данные)
if __name__ == "__main__":
    sample_event_log = {
        'user_id': 'user_123', 
        'transaction': {
            'amount': 1500, 
            'currency': 'RUB'
        },
        'device': {
            'os': 'iOS',
            'details': {
                'model': 'iPhone 14',
                'app_version': '1.0.5'
            }
        },
        'empty_data': {} # Этот пустой словарь будет безопасно проигнорирован
    }
    
    print("--- Рекурсивный вывод ---")
    print_flattened_logs_recursive(sample_event_log)