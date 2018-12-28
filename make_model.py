import fasttext as ft
import sys

def main(argv):
    input_file = argv[0]
    output_file = argv[1]
    ft.supervised(input_file, output_file, label_prefix='__label__',lr=0.01,dim=300,ws=15,epoch=50,thread=8)

if __name__ == '__main__':
    main(sys.argv[1:])