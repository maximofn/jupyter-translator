#!/usr/bin/env python3

import argparse
import sys
import os
from languages import target_lang, source_lang
import utils_jupyter as uj
import deepl_class
from tqdm import tqdm
import anthropic
import pathlib


TRANSLATE = True


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
        _, _, extension, _ = path_name_ext_from_file(args.file)
        if extension == '.ipynb' or extension == '.md':
            for lang in args.target:
                if lang not in target_lang.keys() and lang not in target_lang.values():
                    print(f"Target language {lang} is not supported")
                    sys.exit(1)
        else:
            print(f"File {args.file} is not a Jupyter notebook")
            sys.exit(1)
    else:
        print('No file specified')
        sys.exit(1)
    
    return parser.parse_args()

def init_claude():
    claude_api_key = None
    api_env_file = pathlib.Path('../preparar_notebook/api.env')

    lines = api_env_file.read_text().splitlines()
    for line in lines:
        k, v = line.split('=')
        if 'CLAUDE_API_KEY' in k:
            claude_api_key = v.replace(' ', '').replace('"', '').replace("'", '')
    
    client = anthropic.Anthropic(api_key=claude_api_key)
    return client

def translate(client, text, lang):
    english_system_instruction="Eres un traductor experto de español a inglés de markdown. \
Te voy a pasar fragmentos de markdown y los tienes que traducir al inglés teniendo en cuenta que el texto traducido tiene que seguir siendo markdown.\
Contesta solo con la traducción, no contestes con nada más"
    portugesse_system_instruction="Eres un traductor experto de español a portugués de markdown. \
Te voy a pasar fragmentos de markdown y los tienes que traducir al portugués teniendo en cuenta que el texto traducido tiene que seguir siendo markdown.\
Contesta solo con la traducción, no contestes con nada más"
    model = "claude-3-5-sonnet-20240620"

    if 'en' in lang.lower():
        system_instruction = english_system_instruction
    elif 'pt' in lang.lower():
        system_instruction = portugesse_system_instruction
    else:
        KeyError(f"Language {lang} not supported")

    message = client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=0,
        system=system_instruction,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    )

    return message.content[0].text

def main(file, target):
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
    translated_cells = []
    for l, lang in enumerate(target):
        translated_cells.append(notebooks_translated[l]['cells'])
    print(f"\tNumber of cells: {len(cells)}")
    print(f"\tNumber of english translated cells: {len(translated_cells[0])}")
    print(f"\tNumber of portuguese translated cells: {len(translated_cells[1])}")

    # Initialize the translator
    print("\tInitializing the translator")
    # client = init_claude()
    translator = deepl_class.deepl_translator(source_lang["Spanish"])

    # Translate only markdown cells
    print(f"\tTranslating {file} to {target}")
    bar = tqdm(cells, bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}')
    total_cells = len(cells)
    for c, cell in enumerate(bar):
        # if c == 4:
            # break
        if cell['cell_type'] == 'markdown':
            for l, lang in enumerate(target):
                if lang in target_lang.keys():
                    lang = target_lang[lang]
                if type(cell['source']) == str:
                    if TRANSLATE:
                        translated_text = translator.translate(cell['source'], lang)
                        # translated_text = translate(client, cell['source'], lang)
                    else:
                        translated_text = cell['source']
                    if type(translated_text) != str:
                        raise Exception(f"Error: {translated_text}")
                    notebooks_translated[l]['cells'][c]['source'] = translated_text
                    print(notebooks_translated[l]['cells'][c]['source'])
                elif type(cell['source']) == list:
                    for j, line in enumerate(cell['source']):
                        if TRANSLATE:
                            translated_text = translator.translate(line, lang)
                            # translated_text = translate(client, line, lang)
                        else:
                            translated_text = line
                        if type(translated_text) != str:
                            raise Exception(f"Error: {translated_text}")
                        notebooks_translated[l]['cells'][c]['source'][j] = translated_text
        bar.set_description(f"\t\tCell {c}/{total_cells}")
    print(f"\tEnd of translation")

    # Add autimatic translation warning message
    for l, lang in enumerate(target):
        if lang in target_lang.keys():
            lang = target_lang[lang]
        if lang == 'EN' or lang == 'EN-GB' or lang == 'EN-US':
            warning_string_en = "This notebook has been automatically translated to make it accessible to more people, please let me know if you see any typos.\n"
            notebooks_translated[0]['cells'].insert(1, notebooks_translated[0]['cells'][1].copy())
            notebooks_translated[0]['cells'][1]['source'] = [warning_string_en]
        elif lang == 'PT' or lang == 'PT-BR' or lang == 'PT-PT':
            warning_string_pt = "Este caderno foi traduzido automaticamente para torná-lo acessível a mais pessoas, por favor me avise se você vir algum erro de digitação..\n"
            notebooks_translated[1]['cells'].insert(1, notebooks_translated[1]['cells'][1].copy())
            notebooks_translated[1]['cells'][1]['source'] = [warning_string_pt]
        else:
            warning_string = "Este notebook ha sido traducido automáticamente para que sea accesible por más gente, por favor, si ves alguna errata házmelo saber"
            warning_string = translator.translate(warning_string, lang)
            warning_string = warning_string + "\n"
            notebooks_translated[0]['cells'].insert(1, notebooks_translated[0]['cells'][1].copy())
            notebooks_translated[0]['cells'][1]['source'] = warning_string

    # Save the translated notebooks
    output_paths = []
    for l, lang in enumerate(target):
        if lang in target_lang.keys():
            lang = target_lang[lang]
        output_path = f"{path}/notebooks_translated/{name}_{lang}{extension}"
        if output_path[0] == "/":
            output_path = output_path[1:]
        print(f"\tSaving translated notebook to {output_path}")
        output_paths.append(output_path)
        uj.dict_to_ipynb(notebooks_translated[l], output_path)
    
    return output_paths

if __name__ == '__main__':
    args = parse_arguments()
    main(args.file, args.target)