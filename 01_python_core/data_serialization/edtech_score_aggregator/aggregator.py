import csv
import json
from datetime import datetime

def extract_best_user_scores(input_csv_path, output_json_path):
    user_best_scores = {}

    with open(input_csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row["email"]
            score = int(row["score"])
            date = datetime.fromisoformat(row["date_and_time"])
            
            if email not in user_best_scores:
                user_best_scores[email] = {
                    "name": row["name"],
                    "surname": row["surname"],
                    "best_score": score,
                    "date_and_time": date,
                    "email": email
                }
            else:
                existing = user_best_scores[email]
                if score > existing["best_score"] or (score == existing["best_score"] and date > existing["date_and_time"]):
                    existing["best_score"] = score
                    existing["date_and_time"] = date

    final_results = []
    for email in sorted(user_best_scores.keys()):
        record = user_best_scores[email]
        record["date_and_time"] = record["date_and_time"].strftime("%Y-%m-%d %H:%M:%S")
        final_results.append(record)
        
    with open(output_json_path, mode="w", encoding="utf-8") as file:
        json.dump(final_results, file, indent=3, ensure_ascii=False)

extract_best_user_scores("exam_results.csv", "best_scores.json")