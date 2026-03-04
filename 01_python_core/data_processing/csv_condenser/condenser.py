import csv
from typing import List, Dict, Optional

def get_unique_headers(filename: str) -> List[str]:
    """
    Выполняет первый проход по файлу для сбора всех уникальных имен свойств.
    Использует словарь для сохранения порядка появления (Python 3.7+).
    """
    # Используем словарь как OrderedSet для O(1) поиска и сохранения порядка
    columns_seen: Dict[str, None] = {}
    
    with open(filename, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                # Название свойства находится во втором столбце
                attr_name = row[1]
                if attr_name not in columns_seen:
                    columns_seen[attr_name] = None
                    
    return list(columns_seen.keys())

def condense_csv(filename: str, id_name: str = "ID") -> None:
    """
    Преобразует EAV-структуру в классическую таблицу (Wide format).
    Оптимизировано для минимального потребления RAM через потоковую запись.
    """
    # Шаг 1: Получаем список всех будущих колонок
    dynamic_headers: List[str] = get_unique_headers(filename)
    fieldnames: List[str] = [id_name] + dynamic_headers

    # Шаг 2: Потоковое чтение и группировка
    with open(filename, mode="r", encoding="utf-8") as sf, \
         open("condensed.csv", mode="w", encoding="utf-8", newline="") as ef:
        
        reader = csv.reader(sf)
        writer = csv.DictWriter(ef, fieldnames=fieldnames)
        writer.writeheader()

        current_id: Optional[str] = None
        row_buffer: Dict[str, str] = {}

        for row in reader:
            if len(row) != 3:
                continue
            
            obj_id, attr, value = row

            # Если встречаем новый ID, значит данные предыдущего объекта полностью собраны
            if obj_id != current_id:
                if current_id is not None:
                    # Записываем накопленный объект в файл и освобождаем память
                    writer.writerow(row_buffer)
                
                # Инициализируем буфер для нового объекта
                current_id = obj_id
                row_buffer = {id_name: obj_id}
            
            # Наполняем буфер свойствами текущего объекта
            row_buffer[attr] = value

        # Не забываем записать последний объект после выхода из цикла
        if row_buffer:
            writer.writerow(row_buffer)