# Разработка системы тегирования метрик (Metrics as Code)

### 📝 Бизнес-задача
Команде Data Engineering и Product Analytics требуется инструмент для ведения единого каталога метрик (Metric Store). Необходимо реализовать механизм, позволяющий прозрачно навешивать бизнес-теги (владелец, источник данных, критичность) на скрипты расчета продуктовых метрик (Retention, LTV и др.) без вмешательства в их математическую логику.

### 💡 Решение и производительность
Изначально алгоритм работал за O(K) при назначении K атрибутов, и был оптимизирован для промышленного использования с сохранением сложности O(1) в рантайме за счет применения безопасного встроенного метода `setattr` вместо прямой мутации `__dict__`, а также добавления строгой типизации. 

Это обеспечивает:
* Отсутствие накладных расходов при массовом расчете метрик (O(1) на вызов).
* Автоматическую сборку Data Catalog прямо из исходного кода аналитиков.
* Адресную маршрутизацию алертов в случае падения скриптов (оркестраторы знают `owner` метрики).

### 🛠 Стек
* Python (Core)
* Концепции: Metaprogramming, Decorators, Type Hinting, Data Governance

### 🚀 Как использовать
```python
# Импортируем декоратор обогащения метаданными
from metric_store import tag_metric_metadata

# Навешиваем продуктовые теги
@tag_metric_metadata(
    owner="product_growth_team", 
    data_source="clickhouse_events", 
    is_critical=True,
    sla_minutes=15
)
def calculate_retention_rate(cohort_id: str, day: int) -> float:
    """Расчет Retention Rate для заданной когорты"""
    # ... SQL/Pandas логика расчета ...
    return 25.5

# Пример вызова функции с тестовыми данными
result = calculate_retention_rate(cohort_id="2023-10-W1", day=7)
print(f"Результат: {result}%")

# Чтение метаданных генератором документации или Airflow
print(f"Владелец метрики: {calculate_retention_rate.owner}")
print(f"Источник: {calculate_retention_rate.data_source}")
```