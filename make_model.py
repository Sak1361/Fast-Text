import fasttext as ft
import sys,logging

def main(argv):
    input_file = argv[0]
    output_file = argv[1]
    ft.supervised(input_file, output_file,lr=0.01,dim=400,ws=15)#,epoch=100)
    #ft.supervised(input_file, output_file,lr=0.01)

if __name__ == '__main__':
    main(sys.argv[1:])