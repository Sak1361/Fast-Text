import sys
import fasttext as ft
import MeCab
import re

def Content(content):
    tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('')
    re_comma = re.compile(r'[、。]')
    content = re_comma.sub("",content)
    content = tagger.parse(content)
    return content

def scoring(words,model):
    classifier = ft.load_model(model)
    estimate_name = classifier.predict([words], k=2)
    estimate = classifier.predict_proba([words], k=2)
    print(estimate_name[0])
    print(estimate[0])
    """
    if estimate_name[0][0] == "__label__1,":
        print('ネガティブ',estimate[0][0][1],estimate[0])
    elif estimate_name[0][0] == "__label__2,":
        print('ポジティブ',estimate[0][0][1])
    """
if __name__ == '__main__':
    model = sys.argv[1]
    word = sys.argv[2]

    word = Content(word)
    scoring(word,model)