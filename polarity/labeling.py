import urllib.request, os, mojimoji
from bs4 import BeautifulSoup

def pn_wago():
    if os.path.exists("pn_wago.csv"):
        with open("pn_wago.csv",'r') as f:
            soup = f.read()
        return soup
    pn = 'http://www.cl.ecei.tohoku.ac.jp/resources/sent_lex/wago.121808.pn'
    pn_file = urllib.request.urlopen(pn)
    soup = BeautifulSoup(pn_file,'html.parser')
    soup = str(soup)
    ###毎回呼ぶの面倒だからファイル作る
    with open("pn_wago.csv","w") as f:
        f.write(soup)
    return soup

def pn_vocab():
    with open("pn_word.csv") as f:
        word = f.read()
    return word

def labeling(word):
    nega = ''
    posi = ''
    even = ''
    word = word.split('\n')
    for line in word:
        line = line.split('\t')
        if len(line) == 2:
            if line[0]=='ネガ（経験）' or line[0]=='ネガ（評価）':
                nega += "__label__Disagree, " + line[1] + '\n'
            else:
                posi += "__label__Agree, " + line[1] + '\n'
        elif len(line) == 3:
            if line[1]=='n':
                nega += "__label__Disagree, " + line[0] + '\n'
            elif line[1]=='p':
                posi += "__label__Agree, " + line[0] + '\n'
            elif line[1]=='e':
                even += "__label__even, " + line[0] + '\n'
    label = posi + nega + even
    return label
if __name__ == "__main__":
    wago = pn_wago()
    vocab = pn_vocab()

    labels = labeling(wago)
    labels += labeling(vocab)
    with open('polarity_pros-cons.csv','w')as f:
        f.write(labels)