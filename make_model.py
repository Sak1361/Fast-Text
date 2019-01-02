import fasttext as ft
import sys

def main(argv):
    input_file = argv[0]
    output_file = argv[1]
    ft.supervised(input_file, output_file,lr=0.01,dim=300,ws=5,epoch=100)

if __name__ == '__main__':
    main(sys.argv[1:])