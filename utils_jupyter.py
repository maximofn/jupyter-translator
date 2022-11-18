import json

def get_notebook_as_dict(filename):
    with open(filename, 'r') as f:
        notebook = json.load(f)
    return notebook

def open_notebook(filename, type="w"):
    return open(f"{filename}", type)

def close_notebook(file):
    file.close()

def get_headers(cells):
    headers = []
    for cell in cells:
        if cell['cell_type'] == 'markdown' and cell['source'][0].startswith('#'):
            headers.append(cell['source'][0])
    return headers