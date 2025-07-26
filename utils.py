
import shutil

def load_code_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"⚠️ Error reading file: {e}"

def save_fixed_code(code, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(code)
    except Exception as e:
        print(f"⚠️ Error saving file: {e}")

def backup_file(file_path):
    try:
        shutil.copy(file_path, file_path.replace(".py", "_BACKUP.py"))
    except Exception as e:
        print(f"⚠️ Error creating backup: {e}")
