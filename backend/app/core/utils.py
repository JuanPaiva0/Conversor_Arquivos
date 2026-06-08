import os

def ensure_output_dir():
    base_dir   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(base_dir, "outputs")

    os.makedirs(output_dir,  exist_ok=True)
    return output_dir

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
    
def get_output_path(file, output_dir, extension):
    safe_name = os.path.basename(file.filename)
    name, _ = os.path.splitext(safe_name)

    return os.path.join(output_dir, f"{name}.{extension}")

def get_input_path(file, output_dir):
    safe_name = os.path.basename(file.filename)
    
    return os.path.join(output_dir, safe_name)