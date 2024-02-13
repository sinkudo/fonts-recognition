import glob
import os
from keras.models import load_model

import enum

from main import ROOT_DIR

char_pool = dict(
    rus_eng=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
             'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
             'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
             'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
             'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', '.', ',', '/', ':', ';', '<', '=', '>', '?',
             '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '©', '™'],
    rus_eng_no_reg_diff=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                         'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э',
                         'ю', 'я', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"', '#', '$', '%', '&', "'",
                         '(', ')', '*', '+', '-', '.', ',', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
                         '_', '`', '{', '|', '}', '~', '©', '™'],
    rus=['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
         'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й',
         'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю',
         'Я', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*',
         '+', '-', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|',
         '}', '~', '©', '™'],
    rus_no_reg_diff=['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
                     'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', '0', '1', '2', '3', '4', '5', '6', '7',
                     '8', '9', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', ',', '.', '/', ':', ';', '<',
                     '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '©', '™'],
    eng=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
         'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
         'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!',
         '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@',
         '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '©', '™'],
    eng_no_reg_diff=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"', '#', '$',
                     '%', '&', "'", '(', ')', '*', '+', '-', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[',
                     '\\', ']', '^', '_', '`', '{', '|', '}', '~', '©', '™']
)

other = dict(
    bottom_align=[',', '.', '_'],
    dont_aug=[",", "dot", "\\", "`", "_", "-", "=", ";", ":", "quotedbl", "colon", "backslash", ")", "(", "[", "]" "<",
              ">", "~", "+", "'"]
)
convert = dict(
    convert_chars_to_rus={"a": "а", "b": "в", 'c': 'с', 'd': 'д', 'e': 'е', "h": "н", 'k': 'к', 'm': 'м', 'o': 'о',
                          'p': 'р', 'r': 'г', 'y': 'у', "t": "т", "u": "и", 'x': 'х', },
    convert_chars_to_eng={"а": "a"}
)

folders = dict(
    # fonts_folder="data/fonts/fonts",
    fonts_folder=os.path.join(ROOT_DIR, "data/fonts/fonts"),
    # images_folder="data/datasets/images",
    images_folder=os.path.join(ROOT_DIR, "data/datasets/test2"),
    output_train=os.path.join(ROOT_DIR, "data/datasets/images/output"),
    extracted_data_folder=os.path.join(ROOT_DIR, "data/pdfdata"),
    extracted_fonts_folder=os.path.join(ROOT_DIR, "data/pdfdata/extracted_fonts"),
    extracted_glyphs_folder=os.path.join(ROOT_DIR, "data/pdfdata/glyph_images"),
    default_models_folder=os.path.join(ROOT_DIR, "data/default_models"),
    custom_models_folder=os.path.join(ROOT_DIR, "data/models_and_classnames"),
    # default_models_folder="data/default_models",
    # custom_models_folder="data/models_and_classnames",
)

default_models = [i.split('\\')[-1].split('.')[0] for i in
                  glob.glob(os.path.join(folders.get('default_models_folder'), "*.h5"))]
default_models_and_labels = {i: {"model_name": i + ".h5", "labels": sorted([str(ord(c)) for c in char_pool.get(i)])} for
                             i in default_models}


def chars_to_code(char_list: list):
    return [ord(i) for i in char_list]


# class Language(enum.Enum):
#     Russian_and_English = chars_to_code(char_pool['rus_eng_no_reg_diff'])
#     Russian = chars_to_code(char_pool['rus_no_reg_diff'])
#     English = chars_to_code(char_pool['eng_no_reg_diff'])

class Language(enum.Enum):
    Russian_and_English_no_reg_diff = char_pool['rus_eng_no_reg_diff']
    Russian_no_reg_diff = char_pool['rus_no_reg_diff']
    English_no_reg_diff = char_pool['eng_no_reg_diff']
    Russian_and_English = char_pool['rus_eng']
    Russian = char_pool['rus']
    English = char_pool['eng']


class DefaultModel(enum.Enum):
    Russian_and_English = {'model': load_model(os.path.join(folders['default_models_folder'], 'rus_eng.h5')),
                           'labels': Language.Russian_and_English_no_reg_diff.value}
    Russian = {'model': load_model(os.path.join(folders['default_models_folder'], 'rus.h5')),
               'labels': Language.Russian_no_reg_diff.value}
    English = {'model': load_model(os.path.join(folders['default_models_folder'], 'eng.h5')),
               'labels': Language.English_no_reg_diff.value}
