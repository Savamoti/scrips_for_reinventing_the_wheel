#!/usr/bin/python3.7
"""
Arguments that was pass to the script will be translat(with google translate API)
into English or Russian(depending on what language the arguments),
result will be out in stdout.

For comfotable use it is better to create an alias for script in .bash_aliases,
for example:
    nano ~/.bash_aliases
    alias translate='/path/to/script/translate.py'

Using:
14:39 $ translate Hellow World

Привет, мир

requirements:
sudo apt-get install python3.7 python3-pip
pip3 install googletrans
"""

from sys import argv
from googletrans import Translator


def tr(sentence, lang):
    """
    Function translate sentence

    expect: 2 row
        sentence and destination languate('ru' or 'en')
    return: None
    """
    translator = Translator()
    print('\n' + translator.translate(sentence, dest=lang).text + '\n')

if __name__ == "__main__":
    sentence = ' '.join(argv[1:])
    en_alpabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b',
        'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
        'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # It little bit confusing, why lang='ru' if sentence have english words,
    # because lang is the destination language, into what language that will be translate
    lang = 'en' # default value
    for i in en_alpabet:
        if i in sentence:
            lang = 'ru'
            break
        else:
            pass
    tr(sentence, lang)