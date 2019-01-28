import sys,os,re,mojimoji,json, urllib.request
import MeCab
import fasttext as ft
from bs4 import BeautifulSoup

def sloth_words():    #slothwordのlist化
    if os.path.exists("sloth_words.txt"):
        text = ""
        with open("sloth_words.txt",'r') as f:
            for l in f:
                text += l
        soup = json.loads(text,encoding='utf-8')
        return soup
    ###sloth_words###
    sloth = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    slothl_file = urllib.request.urlopen(sloth)
    soup = BeautifulSoup(slothl_file, 'html.parser')
    soup = str(soup).split()
    ###sloth_singleword###
    sloth_2 = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/OneLetterJp.txt'
    slothl_file2 = urllib.request.urlopen(sloth_2)
    soup2 = BeautifulSoup(slothl_file2, 'html.parser')
    soup2 = str(soup2).split()
    soup.extend(soup2)  #1つにまとめる
    mydict = ['君','先','答弁','お尋ね','登壇']    #その他除外したいワード
    soup.extend(mydict)
    ###毎回呼ぶの面倒だからファイル作る
    with open("sloth_words.txt","w") as f:
        text_dic = json.dumps(soup,ensure_ascii=False, indent=2 )
        f.write(text_dic)
    return soup

def Content(content):
    sloth = sloth_words()
    tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('')
    re_comma = re.compile(r'[︰-＠!-~]')
    re_full = re.compile(r'[。、・’〜：＜＞＿｜「」｛｝【】『』〈〉“”○〔〕…――――◇]')  # 全角で取り除けなかったやつ
    content = re_comma.sub(" ",content)
    content = re_full.sub(" ",content)
    content = tagger.parse(content).strip()
    content = content.split()
    wakati = ''
    for word in content:
        if False:#word in sloth:
            pass
        else:
            wakati += word + ' '
    return wakati

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