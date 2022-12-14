#!/usr/bin/env python3

import argparse
import sys
import os
from languages import target_lang
import utils_jupyter as uj
import utils_deepl as ud
from tqdm import tqdm


def path_name_ext_from_file(file):
    path, name = os.path.split(file)
    name, extension = os.path.splitext(name)
    simplex_name = name[11:].replace("-", " ")
    return path, name, extension, simplex_name


def parse_arguments():
    parser = argparse.ArgumentParser(description='Jupyter notebook translator')
    parser.add_argument('-f', '--file', help='The notebook to translate', required=True)
    # parser.add_argument('-t', '--target', help='The target language, can be a list of languajes', default=['EN'])
    # parser.add_argument('-t', '--target', help='The target language, can be a list of languajes', default=['PT-BR'])
    parser.add_argument('-t', '--target', nargs='+', help='The target language, can be a list of languajes', required=True)
    
    args = parser.parse_args()
    if args.file:
        _, name, extension, _ = path_name_ext_from_file(args.file)
        if extension == '.ipynb':
            for lang in args.target:
                if lang not in target_lang.keys() and lang not in target_lang.values():
                    print(f"Target language {lang} is not supported")
                    sys.exit(1)
                # if lang in target_lang.keys():
                    # print(f"Translate {name}{extension} to {name}_{target_lang[lang]}{extension}")
                # else:
                    # print(f"Translate {name}{extension} to {name}_{lang}{extension}")
        else:
            print(f"File {args.file} is not a Jupyter notebook")
            sys.exit(1)
    else:
        print('No file specified')
        sys.exit(1)
    
    return parser.parse_args()



def main(file, target):
    # args = parse_arguments()

    # Open notebook and get text as a dict
    notebook = uj.get_notebook_as_dict(file)  # Open the notebook as a dictionary

    # Get name and extension of the notebook
    path, name, extension, _ = path_name_ext_from_file(file)

    # Create new dictionary with the translated text
    print("\tCreating new dictionary for new languages")
    notebooks_translated = []
    for lang in target:
        if lang in target_lang.keys():
            lang = target_lang[lang]
        notebooks_translated.append(uj.get_notebook_as_dict(file))

    # Get cells of the notebook
    print("\tGetting cells of the notebook")
    cells = notebook['cells']   # Get only with the cells

    # Initialize the translator
    print("\tInitializing the translator")
    translator = ud.init_deepl()

    # Translate only markdown cells
    print(f"\tTranslating {file} to {target}")
    bar = tqdm(cells, bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}')
    total_cells = len(cells)
    for c, cell in enumerate(bar):
        # if c == 4:
        #     break
        if cell['cell_type'] == 'markdown':
            for l, lang in enumerate(target):
                if lang in target_lang.keys():
                    lang = target_lang[lang]
                if type(cell['source']) == str:
                    notebooks_translated[l]['cells'][c]['source'] = ud.translate_text(cell['source'], lang, translator)
                elif type(cell['source']) == list:
                    for j, line in enumerate(cell['source']):
                        notebooks_translated[l]['cells'][c]['source'][j] = ud.translate_text(line, lang, translator)
        bar.set_description(f"\t\tCell {c}/{total_cells}")
    print(f"\tEnd of translation")

    # Add autimatic translation warning message
    for l, lang in enumerate(target):
        if lang in target_lang.keys():
            lang = target_lang[lang]
        if lang == 'EN' or lang == 'EN-GB' or lang == 'EN-US':
            warning_string = "This notebook has been automatically translated to make it accessible to more people, please let me know if you see any typos.\n"
            notebooks_translated[0]['cells'][2]['source'].insert(0, warning_string)
            notebooks_translated[0]['cells'][2]['source'].insert(1, "\n")
        elif lang == 'PT' or lang == 'PT-BR' or lang == 'PT-PT':
            warning_string = "Este caderno foi traduzido automaticamente para torn??-lo acess??vel a mais pessoas, por favor me avise se voc?? vir algum erro de digita????o..\n"
            notebooks_translated[1]['cells'][2]['source'].insert(0, warning_string)
            notebooks_translated[1]['cells'][2]['source'].insert(1, "\n")
        else:
            warning_string = "Este notebook ha sido traducido autom??ticamente para que sea accesible por m??s gente, por favor, si ves alguna errata h??zmelo saber"
            warning_string = ud.translate_text(warning_string, lang, translator)
            warning_string = warning_string + "\n"
            notebooks_translated[0]['cells'][2]['source'].insert(0, warning_string)
            notebooks_translated[0]['cells'][2]['source'].insert(1, "\n")

    # Save the translated notebooks
    output_paths = []
    for l, lang in enumerate(target):
        if lang in target_lang.keys():
            lang = target_lang[lang]
        output_path = f"{path}/notebooks_translated/{name}_{lang}{extension}"
        output_paths.append(output_path)
        uj.dict_to_ipynb(notebooks_translated[l], output_path)
    
    return output_paths

if __name__ == '__main__':
    args = parse_arguments()
    main(args.file, args.target)