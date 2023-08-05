#!/usr/bin/env python
from objectionloltotxt import objectiontotxt
import argparse
import os
import sys


def main():
    commandline_interface = argparse.ArgumentParser(prog='objtotxt', description='Convert .objection files to txt')
    mutually_exclusive_arguments = commandline_interface.add_mutually_exclusive_group(required=True)
    mutually_exclusive_arguments.add_argument('--filename', metavar="file", type=str, nargs='+',
                                              help="Filename of the .objection file")
    mutually_exclusive_arguments.add_argument('-d', metavar="directory", type=str,
                                              help='convert the .objection files in a directory to readable text file')
    args = commandline_interface.parse_args()
    input_filename = args.filename
    input_directory = args.d
    if input_filename is not None:
        for file in input_filename:
            if not os.path.isfile(file):
                print("That file doesn't exist")
                sys.exit()

    if input_directory is not None and not os.path.isdir(input_directory):
        print("that directory doesn't exist")
        sys.exit()
    if input_directory is not None:
        list_of_file = os.listdir(input_directory)
        for file in list_of_file:
            if file.endswith(".objection"):
                full_path = os.path.join(input_directory, file)
                objectiontotxt.convert_base64objection_to_readable_text_file(full_path)

    else:
        for file in input_filename:
            if file.endswith(".objection"):
                objectiontotxt.convert_base64objection_to_readable_text_file(file)

if __name__ == "__main__":
    main()
