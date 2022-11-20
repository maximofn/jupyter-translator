import json

DEBUG = True

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

def write_end_of_line(file, i, N):
    if i == N-1:
        string = "\n"
        file.write(string)
        if DEBUG: print(string, end='')
    else:
        string = ",\n"
        file.write(string)
        if DEBUG: print(string, end='')

def write_dict_to_file(file, dictionary, indentation):
    string = "{\n"
    file.write(string)
    if DEBUG: print(string, end='')
    indentation += 1
    for i, key in enumerate(dictionary.keys()):
        string = ((" ")*2*indentation)+f"\"{key}\": "
        file.write(string)
        if DEBUG: print(string, end='')
        if type(dictionary[key]) == dict:
            write_dict_to_file(file, dictionary[key], indentation)
        elif type(dictionary[key]) == list:
            write_list_to_file(file, dictionary[key], indentation)
        elif type(dictionary[key]) == str:
            write_str_to_file(file, dictionary[key], indentation)
        else:
            write_rest_to_file(file, dictionary[key], indentation)
        write_end_of_line(file, i, len(dictionary.keys()))
    indentation -= 1
    string = ((" ")*2*indentation)+"}"
    file.write(string)
    if DEBUG: print(string, end='')
    return indentation

def write_list_to_file(file, list, indentation):
    if len(list) > 0:
        string = "[\n"+((" ")*2*indentation)
        file.write(string)
        if DEBUG: print(string, end='')
        indentation += 1
        for i, item in enumerate(list):
            if i > 0:
                break
            if type(item) == dict:
                write_dict_to_file(file, item, indentation)
            elif type(item) == list:
                write_list_to_file(file, item, indentation)
            elif type(item) == str:
                write_str_to_file(file, item, indentation)
            else:
                write_rest_to_file(file, item, indentation)
            write_end_of_line(file, i, len(list))
        indentation -= 1
        string = ((" ")*2*indentation)+"]"
        file.write(string)
        if DEBUG: print(string, end='')
    else:
        string = "[]"
        file.write(string)
        if DEBUG: print(string, end='')
    return indentation

def write_str_to_file(file, string, indentation):
    string = f"\"{string}\""
    file.write(string)
    if DEBUG: print(string, end='')
    return indentation

def write_rest_to_file(file, rest, indentation):
    string = f"\"{rest}\""
    file.write(string)
    if DEBUG: print(string, end='')
    return indentation

def dict_to_ipynb(notebook, filename):
    # new_notebook = open_notebook("new_notebook.txt")
    new_notebook = open_notebook("new_notebook.ipynb")
    # new_notebook = open_notebook(filename)

    indentation = 0
    new_notebook.write(((" ")*2*indentation)+"{\n")
    indentation += 1

    notebook_keys = list(notebook.keys())
    print(type(notebook_keys))
    for k, key in enumerate(notebook_keys):
        if type(notebook[key]) == dict:
            new_notebook.write(((" ")*2*indentation)+"\""+key+"\": ")
            indentation = write_dict_to_file(new_notebook, notebook[key], indentation)
            write_end_of_line(new_notebook, k, len(notebook_keys))
        elif type(notebook[key]) == list:
            new_notebook.write(((" ")*2*indentation)+"\""+key+"\": ")
            indentation = write_list_to_file(new_notebook, notebook[key], indentation)
            write_end_of_line(new_notebook, k, len(notebook_keys))
        elif type(notebook[key] == str):
            new_notebook.write(((" ")*2*indentation)+"\""+key+"\": ")
            indentation = write_str_to_file(new_notebook, notebook[key], indentation)
            write_end_of_line(new_notebook, k, len(notebook_keys))
        else:
            new_notebook.write(((" ")*2*indentation)+"\""+key+"\": ")
            indentation = write_rest_to_file(new_notebook, notebook[key], indentation)
            write_end_of_line(new_notebook, k, len(notebook_keys))
    indentation -= 1
    new_notebook.write(((" ")*2*indentation)+"}\n")

    close_notebook(new_notebook)