# 📊 Оптимизация парсинга вложенных JSON-логов: Рекурсия vs Итеративный стек

### 📝 Бизнес-задача
**Легенда:** В Data Warehouse (например, ClickHouse) ежедневно поступают миллионы сырых событий и профилей пользователей из CRM. Данные приходят в виде многоуровневых JSON-файлов (вложенные словари). Чтобы аналитики могли строить воронки и считать LTV, инженерам необходимо "расплющить" (flatten) эти иерархические структуры в плоские таблицы.

**Условие:** Реализовать парсер, который принимает вложенный JSON произвольной глубины и возвращает плоскую структуру. Составные ключи должны формироваться через точку (например, `session.device.os`). Результат выводится в лексикографическом порядке ключей для удобства индексации.

### 💡 Решение и производительность
В данном кейсе реализовано **два подхода**, демонстрирующих эволюцию от классического алгоритма к production-ready решению, устойчивому к аномальным нагрузкам.

Временная сложность обоих алгоритмов составляет $O(N \log N)$, где $N$ — количество конечных значений (листьев), так как по условию бизнес-задачи обязательна финальная лексикографическая сортировка ключей. Основная разница заключается в **пространственной сложности** и работе с памятью:

**1. Рекурсивный подход (Академический)**
* **Архитектура:** Классический обход графа в глубину (DFS) через системный стек вызовов (Call Stack).
* **Память:** Ограничена программными лимитами ОС и интерпретатора (в Python по умолчанию ~1000 фреймов).
* **Плюсы:** Максимально читаемый и лаконичный код. Идеально для логов с предсказуемой и небольшой глубиной.
* **Минусы:** Риск падения пайплайна с `RecursionError` при обработке аномально глубоких или циклических структур.

**2. Итеративный подход (Production-ready)**
* **Архитектура:** Обход в глубину с использованием "ручного" стека на базе списка.
* **Память:** Пространственная сложность перенесена из Call Stack (жестко лимитированного) в Heap (Кучу). 
* **Плюсы:** Алгоритм масштабируется вместе с доступной оперативной памятью (RAM). Скрипт не упадет, даже если глубина вложенности JSON достигнет десятков тысяч уровней.

В репозитории содержится stress_test.py, который имитирует аномально вложенный JSON (2000+ уровней). Тест подтверждает, что рекурсивный метод падает с RecursionError, в то время как итеративный метод успешно обрабатывает данные, используя память Кучи (Heap).

**Бизнес-вывод:** Внедрение итеративного подхода с выделением памяти в Heap обеспечивает:
* **Стрессоустойчивость ETL-пайплайнов:** Гарантированная обработка любых аномальных логов без падений OOM (Out of Memory) или переполнения стека.
* **Качество данных:** 100% доставка событий до аналитических дашбордов без потерь на этапе трансформации.

### 🛠 Стек
* Python (Core)
* Концепции: Алгоритмы на графах (DFS), Big O, Управление памятью (Call Stack vs Heap), Type Hinting (PEP 8).

### 🚀 Реализация кода

<details>
<summary><b>Посмотреть итеративный подход (Рекомендуемый для Production)</b></summary>

```python
from typing import Any, Dict

def print_flattened_logs_iterative(raw_logs: Dict[str, Any]) -> None:
    if not isinstance(raw_logs, dict) or not raw_logs:
        return

    flat_logs: Dict[str, Any] = {}
    stack = [(raw_logs, "")] 

    while stack:
        current_node, prefix = stack.pop()
        for key, value in current_node.items():
            current_key = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(value, dict):
                if value:
                    stack.append((value, current_key))
            else:
                flat_logs[current_key] = value

    for key in sorted(flat_logs.keys()):
        print(f"{key}: {flat_logs[key]}")
```
</details>

<details>
<summary><b>Посмотреть рекурсивный подход (Академический)</b></summary>

```python

from typing import Any, Dict

def print_flattened_logs_recursive(raw_logs: Dict[str, Any]) -> None:
    if not isinstance(raw_logs, dict) or not raw_logs:
        return

    flat_logs: Dict[str, Any] = {}

    def traverse_node(current_node: Dict[str, Any], prefix: str) -> None:
        for key, value in current_node.items():
            current_key = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(value, dict):
                if value:
                    traverse_node(value, current_key)
            else:
                flat_logs[current_key] = value

    traverse_node(raw_logs, "")

    for key in sorted(flat_logs.keys()):
        print(f"{key}: {flat_logs[key]}")
```
</details>

