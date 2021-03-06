import MeCab, re, urllib.request, codecs , time, sys, os, json, mojimoji
from bs4 import BeautifulSoup

class Mecab:
    def __init__(self):
        self.s = 0
        self.e = 200000
        self.stops = 2000000
        self.tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        self.All = 0

    def re_def(self,filepass):
        with codecs.open(filepass, 'r', encoding='utf-8', errors='ignore')as f:
        #with open(filepass, 'r')as f:
            l = ""
            re_half = re.compile(r'[!-~]')  # 半角記号,数字,英字
            re_full = re.compile(r'[︰-＠]')  # 全角記号
            re_full2 = re.compile(r'[、・’〜：＜＞＿｜「」｛｝【】『』〈〉“”○〇〔〕…――――─◇]')  # 全角で取り除けなかったやつ 
            re_comma = re.compile(r'[。]')  # 全角で取り除けなかったやつ
            re_url = re.compile(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+')
            re_tag = re.compile(r"<[^>]*?>")    #HTMLタグ
            re_n = re.compile(r'\n')  # 改行文字
            re_space = re.compile(r'[\s+]')  #１以上の空白文字
            re_num = re.compile(r"[0-9]")
            pattern = "(.*)　(.*)"
            i = 0
            for line in f:
                if re_num.match(line):  #半角数字は全角数字にする
                    line = mojimoji.han_to_zen(line, ascii=False)
                if line.find('○',0,10) == 0:
                    if i:
                        yield l
                        l = ""
                    sep = re.search(pattern,line)
                    line = line.replace(sep.group(1),"")
                    i = 1
                line = re_half.sub("", line)
                line = re_full.sub("", line)
                line = re_url.sub("", line)
                line = re_tag.sub("",line)
                line = re_n.sub("", line)
                line = re_space.sub("", line)
                line = re_full2.sub(" ", line)
                line = re_comma.sub("\n",line)
                l += line

    def sloth_words(self):    #slothwordのlist化
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
        soup = BeautifulSoup(slothl_file, 'lxml')
        soup = str(soup).split()  # soupは文字列じゃないので注意
        soup.pop(0) #htmlタグを殲滅せよ
        soup.pop()
        mydict = ['君','先','いわば','拍手','登壇','する','者','あり']
        soup.extend(mydict)
        ###sloth_singleword###
        sloth_1 = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/OneLetterJp.txt'
        slothl_file2 = urllib.request.urlopen(sloth_1)
        soup2 = BeautifulSoup(slothl_file2, 'lxml')
        soup2 = str(soup2).split()  # soupは文字列じゃないので注意
        soup2.pop(0)
        soup2.pop()
        soup.extend(soup2)  #1つにまとめる
        
        ###毎回呼ぶの面倒だからファイル作る
        with open("sloth_words.txt","w") as f:
            text_dic = json.dumps(soup,ensure_ascii=False, indent=2 )
            f.write(text_dic)
        return soup

    def owakati(self,all_words):
        wakatifile = []
        while True:
            w = all_words[self.s:self.e]
            wakatifile.extend(self.tagger.parse(w).split("\n"))
            if self.e > self.stops or self.e > len(all_words) : 
                break
            else:
                self.s = self.e
                self.e += 200000
        return wakatifile

    def counting(self,all_words):
        wakati_list = ""
        tmp_list = []
        #ALL = 0 #単語のカウント
        mem = 0 #一定単語以上か判別
        sloths = self.sloth_words()  #slothのlist
        if len(all_words) > 2000000:    #単語数オーバーなら再帰
            mem = 1
        while True:
            wakati = self.owakati(all_words)  #分かち書きアンド形態素解析
            for addlist in wakati:
                #tmp_list.extend(re.split('[\t,]', addlist))  # 空白と","で分割
                tmp_list = re.split('[ ,]', addlist)  # 空白と","で分割
                for addword in tmp_list:    #ストップワードを取り除く
                    if addword in sloths:
                        pass
                    else:
                        wakati_list += addword + ' '    #空白で区切る
            ###語数オーバーの時###
            if mem:
                if len(all_words) < self.stops:
                    break
                else:
                    print("{}万字まで終わったよ".format(self.stops/10000))
                    self.stops += 2000000
                    self.s = self.e
                    self.e += 200000
            else:
                break
        return wakati_list

if __name__ == '__main__':
    input_f = sys.argv[1]
    out_f = sys.argv[2]
    mecab = Mecab()
    c = ""
    label = input("label name?:")
    for text in mecab.re_def(input_f):
        c += "__label__" + label + ', '
        c += mecab.counting(text) + '\n'
    with open(out_f, "w") as f:
        f.write(c)