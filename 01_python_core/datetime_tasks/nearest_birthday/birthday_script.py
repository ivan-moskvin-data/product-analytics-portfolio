from datetime import datetime, timedelta
import sys

def get_next_birthday(birth_date, base_date):
    """
    Вычисляет дату ближайшего дня рождения относительно контрольной точки.
    Корректно обрабатывает перенос 29 февраля на 1 марта в невисокосные годы.
    """
    try:
        # Пытаемся просто подставить текущий год
        bday = birth_date.replace(year=base_date.year)
    except ValueError:
        # Если 29 февраля не существует в этом году, празднуем 1 марта
        bday = birth_date.replace(year=base_date.year, month=3, day=1)
        
    if bday <= base_date:
        # Если в этом году день рождения уже прошел, берем дату в следующем году
        try:
            bday = birth_date.replace(year=base_date.year + 1)
        except ValueError:
            # Снова проверка на 29 февраля для следующего года
            bday = birth_date.replace(year=base_date.year + 1, month=3, day=1)
            
    return bday

# Настройка формата и чтение начальных данных
date_format = "%d.%m.%Y"
base_date_input = sys.stdin.readline().strip()

if base_date_input:
    base_date = datetime.strptime(base_date_input, date_format)
    # Окно поиска: 7 дней, не считая текущего (используем строгое неравенство < 8 дней)
    end_date = base_date + timedelta(days=8)
    
    try:
        n = int(sys.stdin.readline().strip())
    except ValueError:
        n = 0

    # Переменные для отбора самых младших именинников
    youngest_birth_date = None
    result_names = []

    # Обработка данных в один проход для экономии памяти
    for _ in range(n):
        line = sys.stdin.readline().split()
        if len(line) < 3:
            continue
            
        first_name, last_name, date_str = line[0], line[1], line[2]
        birth_date = datetime.strptime(date_str, date_format)
        
        # Определяем дату предстоящего события
        next_bday = get_next_birthday(birth_date, base_date)
        
        # Проверка вхождения в 7-дневный интервал
        if base_date < next_bday < end_date:
            # Если это первый найденный или человек моложе предыдущих (дата рождения позже)
            if youngest_birth_date is None or birth_date > youngest_birth_date:
                youngest_birth_date = birth_date
                result_names = [f"{first_name} {last_name}"]
            # Если найден ровесник текущего самого младшего именинника
            elif birth_date == youngest_birth_date:
                result_names.append(f"{first_name} {last_name}")

    # Финальный вывод результатов
    if result_names:
        for name in result_names:
            print(name)
    else:
        print("Дни рождения не планируются")