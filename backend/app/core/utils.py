import os

def ensure_output_dir():
    base_dir   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "outputs")

    os.makedirs(output_dir,  exist_ok=True)
    return output_dir
    
    