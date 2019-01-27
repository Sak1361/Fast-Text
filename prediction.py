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
    estimate_name = classifier.predict([words], k=3)    #k=表示件数
    estimate = classifier.predict_proba([words], k=3)
    print(estimate_name[0]) #label名
    print(estimate[0])  # スコア

if __name__ == '__main__':
    model = sys.argv[1]
    word = sys.argv[2]

    word = Content(word)
    scoring(word,model)