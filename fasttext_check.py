import fasttext as ft
import MeCab
import sys

def get_score(result,label_dict):
    scores = []
    for item in result:
        scores.append(label_dict[item[0]]+':'+str(item[1]))
    return scores

def get_label_dict(dict_name):
    dictionay = {}
    with open(dict_name, 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            category_name, category_number = line.split(':')
            dictionay['__label__'+category_number.strip()] = category_name
            line = f.readline()
    return dictionay

def get_token(content):
    tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('')
    node = tagger.parse(content)

    return node

def main(argv):
    model_name = argv[0]
    dict_name = argv[1]
    content = argv[2]
    label_dict = get_label_dict(dict_name)
    classifier = ft.load_model(model_name)
    tokens = get_token(content)
    estimate = classifier.predict_proba(tokens, k=3)
    scores = get_score(estimate[0],label_dict)
    print(scores)

if __name__ == '__main__':
    main(sys.argv[1:])