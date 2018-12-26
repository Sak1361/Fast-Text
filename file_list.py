import os
import sys

def print_list(list):
    for item in list:
        print(item)

def get_files(path,file_list):
    for file in os.listdir(path):
        full_path = path + file
        if os.path.isfile(full_path):
            file_list.append(full_path)
        elif os.path.isdir(full_path):
            get_files(full_path + "/",file_list)

def main(argv):
    path = argv[0]
    file_list = []
    get_files(path,file_list)
    print_list(file_list)

if __name__ == '__main__':
    main(sys.argv[1:])