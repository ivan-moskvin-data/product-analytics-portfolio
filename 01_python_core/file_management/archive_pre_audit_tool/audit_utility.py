import zipfile
import math
import os

SIZE_UNITS = ["B", "KB", "MB", "GB", "TB"]

def format_file_size(size_in_bytes):
    if size_in_bytes == 0:
        return "0 B"
    unit_index = min(int(math.log(size_in_bytes, 1024)), len(SIZE_UNITS) - 1)
    formatted_size = round(size_in_bytes / (1024 ** unit_index))
    return f"{formatted_size} {SIZE_UNITS[unit_index]}"

def audit_logs_archive(archive_path):
    try:
        with zipfile.ZipFile(archive_path) as zf:
            for file_info in zf.infolist():
                path_parts = [part for part in file_info.filename.split('/') if part]
                if not path_parts:
                    continue
                indent = "  " * (len(path_parts) - 1)
                item_name = path_parts[-1]
                if file_info.is_dir():
                    print(f"{indent}{item_name}")
                else:
                    size_str = format_file_size(file_info.file_size)
                    print(f"{indent}{item_name} {size_str}")
    except (FileNotFoundError, zipfile.BadZipFile):
        pass

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    archive_path = os.path.join(current_dir, "analytics_export.zip")
    audit_logs_archive(archive_path)