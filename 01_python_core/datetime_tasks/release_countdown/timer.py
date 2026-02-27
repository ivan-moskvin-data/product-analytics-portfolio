from datetime import datetime

DAY_DECLENSIONS = ("день", "дня", "дней")
HOUR_DECLENSIONS = ("час", "часа", "часов")
MINUTE_DECLENSIONS = ("минута", "минуты", "минут")
RELEASE_DATE = datetime(year=2022, month=11, day=8, hour=12)
DATE_FORMAT = "%d.%m.%Y %H:%M"

def get_plural_form(amount, declensions):
    amount = abs(amount)
    remainder_10 = amount % 10
    remainder_100 = amount % 100

    if 11 <= remainder_100 <= 19:
        word = declensions[2]
    elif remainder_10 == 1:
        word = declensions[0]
    elif 2 <= remainder_10 <= 4:
        word = declensions[1]
    else:
        word = declensions[2]
        
    return f"{amount} {word}"

def format_time_remaining(current_date, release_date):
    if current_date >= release_date:
        return "Игра уже вышла!"

    timer = release_date - current_date
    days = timer.days
    hours = timer.seconds // 3600
    minutes = (timer.seconds % 3600) // 60

    parts = []
    if days > 0:
        parts.append(get_plural_form(days, DAY_DECLENSIONS))
    if hours > 0:
        parts.append(get_plural_form(hours, HOUR_DECLENSIONS))
    if days == 0 and minutes > 0:
        parts.append(get_plural_form(minutes, MINUTE_DECLENSIONS))

    if len(parts) > 1:
        return f"До выхода игры осталось: {parts[0]} и {parts[1]}"
    elif len(parts) == 1:
        return f"До выхода игры осталось: {parts[0]}"
    
    return "Игра выходит прямо сейчас!"

def main():
    user_input = input(f"Введите дату ({DATE_FORMAT}): ")
    try:
        current_date = datetime.strptime(user_input, DATE_FORMAT)
        print(format_time_remaining(current_date, RELEASE_DATE))
    except ValueError:
        print(f"Ошибка: Неверный формат.")

if __name__ == "__main__":
    main()