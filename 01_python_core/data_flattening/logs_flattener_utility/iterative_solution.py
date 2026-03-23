from typing import Any, Dict

def print_flattened_logs_iterative(raw_logs: Dict[str, Any]) -> None:
    """
    Преобразует многоуровневый JSON-лог в плоскую структуру.
    
    Использует итеративный обход в глубину (DFS) через стек для предотвращения 
    ошибок переполнения стека вызовов (RecursionError) при глубокой вложенности.
    
    Args:
        raw_logs (Dict[str, Any]): Исходный лог события пользователя.
    """
    # Базовая защита: если пришел не словарь или он пустой, ничего не делаем
    if not isinstance(raw_logs, dict) or not raw_logs:
        return

    flat_logs: Dict[str, Any] = {}
    
    # Стек хранит кортежи: (текущий_словарь, префикс_составного_ключа)
    stack = [(raw_logs, "")]

    while stack:
        current_node, prefix = stack.pop()
        
        for key, value in current_node.items():
            # Формируем составной ключ (например, session.device.os)
            current_key = f"{prefix}.{key}" if prefix else str(key)
            
            # Если значение — словарь, кладем в стек для обхода
            if isinstance(value, dict):
                # Проверка на пустой словарь (избегаем мертвых ветвей)
                if value:
                    stack.append((value, current_key))
            else:
                # Если дошли до конца, сохраняем в результат
                flat_logs[current_key] = value

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
    
    print("--- Итеративный вывод ---")
    print_flattened_logs_iterative(sample_event_log)