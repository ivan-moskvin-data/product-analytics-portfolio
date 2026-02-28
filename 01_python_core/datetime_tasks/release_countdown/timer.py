from datetime import datetime
from typing import Final

# Константы вынесены в начало и помечены как Final для защиты от изменений
DAY_DECLENSIONS: Final = ("день", "дня", "дней")
HOUR_DECLENSIONS: Final = ("час", "часа", "часов")
MINUTE_DECLENSIONS: Final = ("минута", "минуты", "минут")
RELEASE_DATE: Final = datetime(year=2022, month=11, day=8, hour=12)
DATE_FORMAT: Final = "%d.%m.%Y %H:%M"

def get_plural_form(amount: int, declensions: tuple[str, str, str]) -> str:
    """
    Вычисляет правильное склонение слова на основе числа (алгоритм O(1)).
    """
    amount = abs(amount)
    remainder_10 = amount % 10
    remainder_100 = amount % 100

    # Правила склонения в русском языке
    if 11 <= remainder_100 <= 19:
        word = declensions[2]
    elif remainder_10 == 1:
        word = declensions[0]
    elif 2 <= remainder_10 <= 4:
        word = declensions[1]
    else:
        word = declensions[2]
        
    return f"{amount} {word}"

def format_time_remaining(current_date: datetime, release_date: datetime) -> str:
    """
    Рассчитывает разницу во времени и формирует читаемую строку.
    """
    if current_date >= release_date:
        return "Игра уже вышла!"

    timer = release_date - current_date
    days = timer.days
    hours = timer.seconds // 3600
    minutes = (timer.seconds % 3600) // 60

    # Собираем только значимые части времени
    parts = []
    if days > 0:
        parts.append(get_plural_form(days, DAY_DECLENSIONS))
    if hours > 0:
        parts.append(get_plural_form(hours, HOUR_DECLENSIONS))
    # Минуты выводим только если нет дней и они больше нуля
    if days == 0 and minutes > 0:
        parts.append(get_plural_form(minutes, MINUTE_DECLENSIONS))

    # Красивая склейка через 'и' для двух элементов
    if len(parts) > 1:
        return f"До выхода игры осталось: {parts[0]} и {parts[1]}"
    elif len(parts) == 1:
        return f"До выхода игры осталось: {parts[0]}"
    
    return "Игра выходит прямо сейчас!"

def main() -> None:
    """
    Точка входа: обработка ввода и запуск логики.
    """
    user_input = input(f"Введите дату ({DATE_FORMAT}): ")
    try:
        current_date = datetime.strptime(user_input, DATE_FORMAT)
        print(format_time_remaining(current_date, RELEASE_DATE))
    except ValueError:
        print(f"Ошибка: Неверный формат даты.")

if __name__ == "__main__":
    main()