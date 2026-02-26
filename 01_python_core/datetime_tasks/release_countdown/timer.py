from datetime import datetime, timedelta

def cp(amount, declensions): 
  suf2 = ["0"] + [str(i) for i in range(5, 20)]
  n = str(amount)
  if n[-2:] in suf2 or n[-1] in suf2:
    return f"{amount} {declensions[2]}"
  elif n[-1] == "1":
    return f"{amount} {declensions[0]}"
  else:
    return f"{amount} {declensions[1]}"

dtup = ("день", "дня", "дней")
htup = ("час", "часа", "часов")
mtup = ("минута", "минуты", "минут")

pat = "%d.%m.%Y %H:%M"
d = datetime.strptime(input(), pat)

kurse = datetime(year=2022, month=11, day=8, hour=12)

if d >= kurse:
  print("Игра уже вышла!")
else:
    timer = kurse - d
    l = [timer.days, int(timer.seconds // 3600), int(timer.seconds % 3600 // 60)]
    if l[0] != 0:
        if l[1] != 0:
            print(f"До выхода игры осталось: {cp(l[0], dtup)} и {cp(l[1], htup)}")
        else:
            print(f"До выхода игры осталось: {cp(l[0], dtup)}")
    else:
        if l[1] != 0 and l[2] != 0:
            print(f"До выхода игры осталось: {cp(l[1], htup)} и {cp(l[2], mtup)}")
        elif l[2] == 0:
            print(f"До выхода игры осталось: {cp(l[1], htup)}")
        else:
            print(f"До выхода игры осталось: {cp(l[2], mtup)}")