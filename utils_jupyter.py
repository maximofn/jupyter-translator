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

def write_dict_to_file(file, dictionary, indentation):
    file.write("{\n")
    indentation += 1
    for i, key in enumerate(dictionary.keys()):
        file.write(((" ")*2*indentation)+f"\"{key}\": \"{dictionary[key]}\"")
        if type(dictionary[key]) == dict:
            write_dict_to_file(file, dictionary[key], indentation)
        elif type(dictionary[key]) == list:
            pass
            # write_list_to_file(file, dictionary[key], indentation)
            # file.write(((" ")*2*indentation)+"[")
            # for item in dictionary[key]:
            #     file.write("\""+item+"\",")
            # file.write("]")
        elif type(dictionary[key]) == str:
            pass
            # write_str_to_file(file, dictionary[key], indentation)
        else:
            pass
            # write_rest_to_file(file, dictionary[key], indentation)
        if i == len(dictionary.keys())-1:
            file.write("\n")
        else:
            file.write(",\n")
    indentation -= 1
    file.write(((" ")*2*indentation)+"}")    
    return indentation

def dict_to_ipynb(notebook, filename):
    # new_notebook = open_notebook("new_notebook.txt")
    new_notebook = open_notebook("new_notebook.ipynb")
    # new_notebook = open_notebook(filename)

    indentation = 0
    new_notebook.write(((" ")*2*indentation)+"{\n")
    indentation += 1

    notebook_keys = list(notebook.keys())
    for k, key in enumerate(notebook_keys):
        if type(notebook[key]) == dict:
            print(f"Key {key} is a dict")
            new_notebook.write(((" ")*2*indentation)+"\""+key+"\": {\n")
            indentation += 1
            dict_keys = list(notebook[key].keys())
            for dk, dict_key in enumerate(dict_keys):
                new_notebook.write(((" ")*2*indentation)+"\""+dict_key+"\": {\n")
                indentation += 1
                if type(notebook[key][dict_key]) == str:
                    new_notebook.write(((" ")*2*indentation)+"\""+notebook[key][dict_key]+"\"")
                elif type(notebook[key][dict_key]) == list:
                    new_notebook.write(((" ")*2*indentation)+"[")
                    for item in notebook[key][dict_key]:
                        new_notebook.write("\""+item+"\",")
                    new_notebook.write("]")
                elif type(notebook[key][dict_key]) == dict:
                    for sk, subkey in enumerate(notebook[key][dict_key].keys()):
                        new_notebook.write(((" ")*2*indentation)+"\""+subkey+"\": ")
                        if type(notebook[key][dict_key][subkey]) == str:
                            new_notebook.write("\""+notebook[key][dict_key][subkey]+"\"")
                        elif type(notebook[key][dict_key][subkey]) == list:
                            new_notebook.write("[")
                            for item in notebook[key][dict_key][subkey]:
                                new_notebook.write(((" ")*2*indentation)+"\""+item+"\",")
                            new_notebook.write(((" ")*2*indentation)+"]")
                        elif type(notebook[key][dict_key][subkey]) == dict:
                            print(f"Key {subkey} is a dict")
                            indentation = write_dict_to_file(new_notebook, notebook[key][dict_key][subkey], indentation)
                            # new_notebook.write("{\n")
                            # indentation += 1
                            # for ssk, subsubkey in enumerate(notebook[key][dict_key][subkey].keys()):
                            #     new_notebook.write(((" ")*2*indentation)+"\""+subsubkey+"\": \""+str(notebook[key][dict_key][subkey][subsubkey])+"\"")
                            #     if ssk == len(notebook[key][dict_key][subkey].keys())-1:
                            #         new_notebook.write("\n")
                            #     else:
                            #         new_notebook.write(",\n")
                            # indentation -= 1
                            # new_notebook.write(((" ")*2*indentation)+"}")
                        else:
                            new_notebook.write(str(notebook[key][dict_key][subkey]).lower())
                        if sk == len(notebook[key][dict_key].keys())-1:
                            new_notebook.write("\n")
                        else:
                            new_notebook.write(",\n")
                else:
                    new_notebook.write(((" ")*2*indentation)+str(notebook[key][dict_key])+"")
                indentation -= 1
                if dk == len(dict_keys)-1:
                    new_notebook.write(((" ")*2*indentation)+"}\n")
                else:
                    new_notebook.write(((" ")*2*indentation)+"},\n")
                # new_notebook.write(((" ")*2*indentation)+"},\n")
            indentation -= 1
            if k == len(notebook_keys)-1:
                new_notebook.write(((" ")*2*indentation)+"}\n")
            else:
                new_notebook.write(((" ")*2*indentation)+"},\n")
        elif type(notebook[key]) == list:
            print(f"Key {key} is a list")
            pass
            # new_notebook.write(((" ")*2*indentation)+"\""+key+"\": [\n")
            # indentation += 1
            # for i, item in enumerate(notebook[key]):
            #     if i > 1:
            #         break
            #     new_notebook.write(((" ")*2*indentation)+"{\n")
            #     indentation += 1
            #     if type(item) == dict:
            #         for ik, item_key in enumerate(item.keys()):
            #             new_notebook.write(((" ")*2*indentation)+"\""+item_key+"\": ")
            #             if type(item[item_key]) == str:
            #                 new_notebook.write("\""+item[item_key]+"\"")
            #             elif type(item[item_key]) == list:
            #                 new_notebook.write("[")
            #                 indentation += 1
            #                 for ii, item_item in enumerate(item[item_key]):
            #                     if type(item_item) == str:
            #                         new_notebook.write(((" ")*2*indentation)+"\""+item_item+"\"")
            #                     elif type(item_item) == dict:
            #                         new_notebook.write(((" ")*2*indentation)+"{\n")
            #                         indentation += 1
            #                         for iii, item_item_item in enumerate(item_item.keys()):
            #                             new_notebook.write(((" ")*2*indentation)+"\""+item_item_item+"\": \""+item_item[item_item_item]+"\"")
            #                             if iii == len(item_item.keys())-1:
            #                                 new_notebook.write("\n")
            #                             else:
            #                                 new_notebook.write(",\n")
            #                         indentation -= 1
            #                         new_notebook.write(((" ")*2*indentation)+"}")
            #                     else:
            #                         new_notebook.write(((" ")*2*indentation)+str(item_item))
            #                     if ii == len(item[item_key])-1:
            #                         new_notebook.write("\n")
            #                     else:
            #                         new_notebook.write(",\n")
            #                 indentation -= 1
            #                 new_notebook.write("]")
            #             elif type(item[item_key]) == dict:
            #                 new_notebook.write("{\n")
            #                 indentation += 1
            #                 for iik, item_item_key in enumerate(item[item_key].keys()):
            #                     new_notebook.write(((" ")*2*indentation)+"\""+item_item_key+"\": \""+str(item[item_key][item_item_key])+"\"")
            #                     if iik == len(item[item_key].keys())-1:
            #                         new_notebook.write("\n")
            #                     else:
            #                         new_notebook.write(",\n")
            #                 indentation -= 1
            #                 new_notebook.write(((" ")*2*indentation)+"}")
            #             else:
            #                 new_notebook.write(str(item[item_key]).lower())
            #             if ik == len(item.keys())-1:
            #                 new_notebook.write("\n")
            #             else:
            #                 new_notebook.write(",\n")
            #     indentation -= 1
            #     if i == len(notebook[key])-1:
            #         new_notebook.write(((" ")*2*indentation)+"}\n")
            #     else:
            #         new_notebook.write(((" ")*2*indentation)+"},\n")
            # indentation -= 1
            # if k == len(notebook_keys)-1:
            #     new_notebook.write(((" ")*2*indentation)+"]\n")
            # else:
            #     new_notebook.write(((" ")*2*indentation)+"],\n")
        else:
            new_notebook.write(((" ")*2*indentation)+"\""+key+"\": "+str(notebook[key]))
            if k == len(notebook_keys)-1:
                new_notebook.write("\n")
            else:
                new_notebook.write(",\n")
    indentation -= 1
    new_notebook.write(((" ")*2*indentation)+"}\n")

    close_notebook(new_notebook)