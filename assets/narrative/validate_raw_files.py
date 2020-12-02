# Overview
# This is a script to be run from the terminal for checking validity and completeness of raw narrative files.
# It is expected to used by terminal-literate will run this script to check for errors when writing a writer's
# narrative into json files.  This script makes sure a given json file (or all in the directory) can be properly read
# and include translations for all phrases in the given language(s)
#
# Parameters
# The first parameter is the name of the json file to be checked. Only the name should be used, not the path or
# extension. Ex: 'section_1'. To check all files at once, you can use the word 'all'.
# After the file parameter, users can optionally include any number of languages as parameters. For each chosen
# language, it will be checked if every phrase has a translation into that language. If no language is chosen, all
# officially-supported languages will be checked.
# If no file or languages are specified, both will be assumed to be all.

import json
import os
import sys

RAW_NARRATIVE_DIR = 'raw'
OFFICIAL_LANGUAGES = [
                        'english'
                     ]

def main():
    file, languages = read_parameters()
    valid = True

    if file == 'all':
        for file_name in os.listdir(RAW_NARRATIVE_DIR):
            file_path = RAW_NARRATIVE_DIR + '/' + file_name
            valid = validate_file(file_path, languages) and valid
    else:
        file_path = RAW_NARRATIVE_DIR + '/' + file + '.json'
        valid = validate_file(file_path, languages)

    if valid:
        print('No errors detected')


# Read in parameters for files/languages to check from the system arguments
def read_parameters():
    args = sys.argv
    if len(args) == 1:
        return 'all', OFFICIAL_LANGUAGES
    elif len(args) == 2:
        return args[1], OFFICIAL_LANGUAGES
    else:
        return args[1], args[2:]


# Validate a single file
def validate_file(file_path, languages):
    valid = True

    if not os.path.exists(file_path):
        print('Error: file ' + file_path + ' does not exist')
        return False

    with open(file_path) as file:
        try:
            section = json.load(file)
        except json.JSONDecodeError:
            print('Error: file ' + file_path + ' is not a properly-formatted json file')
            return False

    for language in languages:
        for phrase in section.keys():
            if language not in section[phrase].keys():
                valid = False
                file_name = file_path.split('/')[1]
                print('Warning in ' + file_name + ': the phrase "' + phrase + '" is not translated into ' + language)
    return valid

if __name__ == '__main__':
    main()