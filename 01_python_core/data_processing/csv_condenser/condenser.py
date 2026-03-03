import csv

def get_unique_headers(filename):
    columns_seen = {}
    with open(filename, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                columns_seen[row[1]] = None
    return list(columns_seen.keys())

def condense_csv(filename, id_name="ID"):
    dynamic_headers = get_unique_headers(filename)
    fieldnames = [id_name] + dynamic_headers

    with open(filename, mode="r", encoding="utf-8") as sf, \
         open("condensed.csv", mode="w", encoding="utf-8", newline="") as ef:
        
        reader = csv.reader(sf)
        writer = csv.DictWriter(ef, fieldnames=fieldnames)
        writer.writeheader()

        current_id = None
        row_buffer = {}

        for row in reader:
            if len(row) != 3:
                continue
            
            obj_id, attr, value = row

            if obj_id != current_id:
                if current_id is not None:
                    writer.writerow(row_buffer)
                current_id = obj_id
                row_buffer = {id_name: obj_id}
            
            row_buffer[attr] = value

        if row_buffer:
            writer.writerow(row_buffer)