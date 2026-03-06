import json, csv
from datetime import datetime

with open("exam_results.csv", "r", encoding="utf-8") as file:
    dr = list(csv.DictReader(file))

for i in dr:
    i["date_and_time"] = datetime.fromisoformat(i["date_and_time"])
    i["score"] = int(i["score"])

ms = set("-".join((i["name"], i["surname"])) for i in dr)

l = []
for s in ms:
    s = s.split("-")
    ls = list(filter(lambda x: x["name"] == s[0] and x["surname"] == s[1], dr))
    ls = sorted(ls, key=lambda x: (x["score"], x["date_and_time"]))
    l.append(ls[-1])

for i in l:
    i["date_and_time"] = datetime.strftime(i["date_and_time"], "%Y-%m-%d %H:%M:%S")
    i["best_score"] = i.pop("score")

l = sorted(l, key=lambda x: x["email"])

with open("best_scores.json", "w", encoding="utf-8") as file:
    json.dump(l, file, indent=3)