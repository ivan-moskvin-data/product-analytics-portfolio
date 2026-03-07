from zipfile import ZipFile

byte = ["B", "KB", "MB", "GB"]

with ZipFile("desktop.zip") as zf:
    for i in zf.infolist():
        fs = i.file_size
        cnt = 0
        while fs > 1024:
            fs = round(fs / 1024, 0)
            cnt += 1
        l = i.filename.split("/")
        if l[-1] == "":
            del l[-1]
        if fs > 0:
            print(f"{'  ' * (len(l) - 1)}{l[-1]} {int(fs)} {byte[cnt]}")
        else:
            print(f"{'  ' * (len(l) - 1)}{l[-1]}")