import csv
import json
from datetime import datetime
from typing import List, Dict, Any

def extract_best_user_scores(input_csv_path: str, output_json_path: str) -> None:
    """
    Анализирует логи тестирования пользователей и извлекает лучший балл для каждого.
    Использует email в качестве уникального идентификатора (Primary Key).
    
    Args:
        input_csv_path: Путь к сырым логам тестирования (CSV).
        output_json_path: Путь для сохранения агрегированных данных (JSON).
    """
    user_best_scores: Dict[str, Dict[str, Any]] = {}

    try:
        with open(input_csv_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                email = row.get("email")
                # Edge case: пропускаем битые логи без email
                if not email:
                    continue 
                
                try:
                    # Приведение типов с защитой от сломанных данных
                    current_score = int(row["score"])
                    current_date = datetime.fromisoformat(row["date_and_time"])
                except (ValueError, KeyError):
                    continue 
                
                # O(1) поиск в хеш-таблице
                if email not in user_best_scores:
                    user_best_scores[email] = {
                        "name": row["name"],
                        "surname": row["surname"],
                        "best_score": current_score,
                        "date_and_time": current_date,
                        "email": email
                    }
                else:
                    existing_record = user_best_scores[email]
                    
                    # Логика обновления: балл выше ИЛИ балл такой же, но дата свежее
                    is_score_higher = current_score > existing_record["best_score"]
                    is_same_score_but_newer = (
                        current_score == existing_record["best_score"] 
                        and current_date > existing_record["date_and_time"]
                    )
                    
                    if is_score_higher or is_same_score_but_newer:
                        existing_record["best_score"] = current_score
                        existing_record["date_and_time"] = current_date

        final_results: List[Dict[str, Any]] = []
        
        # Сортировка по email лексикографически
        for email in sorted(user_best_scores.keys()):
            record = user_best_scores[email]
            # Форматируем дату обратно в строку стандарта системы
            record["date_and_time"] = record["date_and_time"].strftime("%Y-%m-%d %H:%M:%S")
            final_results.append(record)
            
        with open(output_json_path, mode="w", encoding="utf-8") as file:
            json.dump(final_results, file, indent=3, ensure_ascii=False)
            
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_csv_path} не найден. Проверьте путь.")

# Пример вызова:
# extract_best_user_scores("exam_results.csv", "best_scores.json")