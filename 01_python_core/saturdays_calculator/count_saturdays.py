from datetime import date, timedelta

def count_saturdays_between_dates(start_date: date, end_date: date) -> int:
    """
    Вычисляет точное количество суббот между двумя датами включительно.
    
    Args:
        start_date (date): Начальная дата.
        end_date (date): Конечная дата.
        
    Returns:
        int: Количество суббот в заданном диапазоне.
        
    Raises:
        TypeError: Если переданы аргументы неверного типа.
    """
    # Валидация типов (Edge Case)
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        raise TypeError("Оба аргумента должны быть объектами datetime.date")

    # Гарантируем правильный хронологический порядок
    start, end = sorted([start_date, end_date])

    # Вычисляем количество дней до первой субботы в диапазоне
    # weekday(): Понедельник = 0, ..., Суббота = 5
    days_to_first_saturday = (5 - start.weekday()) % 7
    first_saturday = start + timedelta(days=days_to_first_saturday)

    # Если первая суббота выходит за рамки конечной даты, суббот нет
    if first_saturday > end:
        return 0

    # Считаем первую субботу (1) + количество полных недель до конца периода
    return 1 + (end - first_saturday).days // 7