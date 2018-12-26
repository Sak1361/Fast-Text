import MeCab
import os
import re
import sys

def get_content(file_name):
    contexts = []
    with open(file_name, 'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            contexts.append(line.strip())
            line = file.readline()
    return ''.join(contexts)

def get_token(content):
    tokens = []
    tagger = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologdx')
    tagger.parse('')
    node = tagger.parseToNode(content)
    while node:
        if node.feature.split(',')[0] == '名詞':
            tokens.append(node.surface)
        node = node.next
    return tokens

def get_file_name(path):
    return os.path.basename(path)

def get_label(path,label_dict):
    file_name = get_file_name(path)
    name, ext = os.path.splitext(file_name)
    category_name = re.sub(r'[0-9]+','',name)
    if category_name in label_dict.keys():
        label = label_dict[category_name]
    else:
        label = label_dict['category_number']
        label_dict[category_name] = label
        label_dict['category_number'] = str( int(label) + 1)
    return str(label)

def make_training_data(file_list,label_dict):
    for file_name in file_list:
        print_training_data(file_name,label_dict)

def format_content(content):
    content = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", content)
    return content

def print_training_data(path,label_dict):
    content = get_content(path)
    content = format_content(content)
    tokens = get_token(content)
    text = ' '.join(tokens)
    label = get_label(path,label_dict)
    print('__label__'+label+' '+text)

def get_file_list(file_name):
    file_list = []
    with open(file_name, 'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            file_list.append(line.strip())
            line = file.readline()
    return file_list

def output_dict(file_name, label_dict):
    with open(file_name, mode='w', encoding='utf-8') as file:
        for key, value in label_dict.items():
           file.write(key+':'+value+'\n')

def main(argv):
    #file_name = ""
    #dict_name = ""
    file_name = argv[0]
    dict_name = argv[1]
    label_dict = {'category_number':'0'}
    file_list = get_file_list(file_name)
    make_training_data(file_list,label_dict)
    output_dict(dict_name, label_dict)

if __name__ == '__main__':
    main(sys.argv[1:])