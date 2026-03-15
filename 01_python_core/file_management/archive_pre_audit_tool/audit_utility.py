import zipfile
import math
from typing import List
import os 

# Константы вынесены наверх для удобства конфигурации
SIZE_UNITS = ["B", "KB", "MB", "GB", "TB"]

def format_file_size(size_in_bytes: int) -> str:
    """
    Конвертирует размер файла в байтах в человекочитаемый формат для отчетов.
    Использует логарифм вместо цикла для мгновенного $O(1)$ вычисления порядка.
    """
    if size_in_bytes == 0:
        return "0 B"
    
    # Вычисляем нужный индекс единицы измерения через логарифм по основанию 1024
    unit_index = int(math.log(size_in_bytes, 1024))
    
    # Ограничиваем индекс массивом доступных единиц, чтобы избежать IndexError на эксабайтах
    unit_index = min(unit_index, len(SIZE_UNITS) - 1)
    
    # Округляем до целых, как того требует бизнес-логика
    formatted_size = round(size_in_bytes / (1024 ** unit_index))
    
    return f"{formatted_size} {SIZE_UNITS[unit_index]}"

def audit_logs_archive(archive_path: str) -> None:
    """
    Анализирует архив с логами, выводя файловую структуру и объемы данных.
    Помогает валидировать полноту выгрузки перед загрузкой в DWH.
    """
    try:
        with zipfile.ZipFile(archive_path) as zf:
            for file_info in zf.infolist():
                # Очищаем путь от пустых строк, которые возникают из-за слэшей директорий
                path_parts = [part for part in file_info.filename.split('/') if part]
                
                if not path_parts:
                    continue
                    
                depth = len(path_parts) - 1
                indent = "  " * depth
                item_name = path_parts[-1]
                
                # Встроенный метод is_dir() надежнее ручной проверки пустых элементов массива
                if file_info.is_dir():
                    print(f"{indent}{item_name}")
                else:
                    size_str = format_file_size(file_info.file_size)
                    print(f"{indent}{item_name} {size_str}")

    except FileNotFoundError:
        print(f"Ошибка: Дамп '{archive_path}' не найден. Проверьте пайплайн выгрузки.")
    except zipfile.BadZipFile:
        print(f"Ошибка: Файл '{archive_path}' поврежден или не является ZIP-архивом.")

if __name__ == "__main__":
    # Определяем папку, в которой лежит сам файл .py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Склеиваем путь к папке и имя архива
    archive_path = os.path.join(current_dir, "analytics_export.zip")
    
    # Запускаем аудит
    audit_logs_archive(archive_path)