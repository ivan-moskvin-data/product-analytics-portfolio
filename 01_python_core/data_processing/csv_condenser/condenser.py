import csv

def condense_csv(filename, id_name="XXX"):
    with open(filename, encoding="utf-8") as sf, open ("condensed.csv", "w", encoding="utf-8") as ef:
        l = list(csv.reader(sf))
        colunms = [id_name]
        for c in l:
            if c[1] not in colunms:
                colunms.append(c[1])
        nl = []
        for i in range(0, len(l), len(colunms) - 1):
            d = {id_name:l[i][0]}
            for j in range(len(colunms) - 1):
                d[l[i + j][1]] = l[i + j][2]
            nl.append(d)
        write = csv.DictWriter(ef, fieldnames=colunms)
        write.writeheader()
        write.writerows(nl)