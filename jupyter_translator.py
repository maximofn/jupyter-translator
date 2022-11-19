#!/usr/bin/env python3

import argparse
import sys
import os
from languages import target_lang
# sys.path.append('../jupyter-to-html')
import utils_jupyter as uj
import utils_deepl as ud


def path_name_ext_from_file(file):
    path, name = os.path.split(file)
    name, extension = os.path.splitext(name)
    simplex_name = name[11:].replace("-", " ")
    return path, name, extension, simplex_name


def parse_arguments():
    parser = argparse.ArgumentParser(description='Jupyter notebook translator')
    # parser.add_argument('-f', '--file', help='The notebook to translate', required=True)
    parser.add_argument('-f', '--file', help='The notebook to translate', default="2021-02-11-Introducción-a-Python.ipynb")
    parser.add_argument('-t', '--target', help='The target language, can be a list of languajes', default=['EN', 'PT-BR'])
    
    args = parser.parse_args()
    if args.file:
        _, name, extension, _ = path_name_ext_from_file(args.file)
        if extension == '.ipynb':
            for lang in args.target:
                if lang not in target_lang.keys() and lang not in target_lang.values():
                    print(f"Target language {lang} is not supported")
                    sys.exit(1)
                if lang in target_lang.keys():
                    print(f"Translate {name}{extension} to {name}_{target_lang[lang]}{extension}")
                else:
                    print(f"Translate {name}{extension} to {name}_{lang}{extension}")
        else:
            print(f"File {args.file} is not a Jupyter notebook")
            sys.exit(1)
    else:
        print('No file specified')
        sys.exit(1)
    
    return parser.parse_args()



def main():
    args = parse_arguments()

    # Open notebook and get text as a dict
    notebook = uj.get_notebook_as_dict(args.file)  # Open the notebook as a dictionary

    # Get name and extension of the notebook
    _, name, extension, _ = path_name_ext_from_file(args.file)

    # Create new dictionary with the translated text
    notebooks_translated = []
    for lang in args.target:
        if lang in target_lang.keys():
            lang = target_lang[lang]
        notebooks_translated.append(notebook)

    # Get cells of the notebook
    cells = notebook['cells']   # Get only with the cells

    # Initialize the translator
    translator = ud.init_deepl()

    # Translate only markdown cells
    for c, cell in enumerate(cells):
        if c == 2:
            break;
        if cell['cell_type'] == 'markdown':
            # print(f"Cell {c}: {cell['source']}")
            for i, lang in enumerate(args.target):
                if lang in target_lang.keys():
                    lang = target_lang[lang]
                if type(cell['source']) == str:
                    notebooks_translated[i]['cells'][c]['source'] = ud.translate_text(cell['source'], lang, translator)
                elif type(cell['source']) == list:
                    for j, line in enumerate(cell['source']):
                        pass
                        # notebooks_translated[i]['cells'][c]['source'][j] = ud.translate_text(line, lang, translator)
                # print(f"Translated to {lang}: {notebooks_translated[i]['cells'][c]['source']}")
            # print()
    
    # Save the translated notebooks
    # for i, lang in enumerate(args.target):
    #     if lang in target_lang.keys():
    #         lang = target_lang[lang]
    #     with uj.open_notebook(f"{name}_{lang}{extension}", "w") as f:
    #         print(f"Saving {name}_{lang}{extension}")
    uj.dict_to_ipynb(notebook, "new_notebook.ipynb")

if __name__ == '__main__':
    main()