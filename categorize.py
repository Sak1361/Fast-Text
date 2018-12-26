import sys

def get_content(file_name):
    contexts = []
    with open(file_name, 'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            contexts.append(line.strip())
            line = file.readline()
    return ''.join(contexts)

def put_content(file_name,content):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)

def make_categorized_data(file_list, text_path):
    keyword_dict = {
            'Politics':['政治','国会','選挙','政党','行政','司法','警察','財政','外交','在日外国人','旧日本領土','軍事'],
            'Economy':['経済','金融','株式','貿易','為替','産業','企業','農林','水産','鉱業','工業','運輸','通信','土木','建築','商業'],
            'Society':['社会','厚生','医事','衛生','公害','地球','環境','生活','料理','住生活','婦人','子供','青少年','趣味','娯楽','観光','旅行','行事','祝祭','世相','風俗'],
            }
    file_num = {
            'Politics':'0',
            'Economy':'0',
            'Society':'0',
            }
    for file_name in file_list:
        content = get_content(file_name)
        flag = -1
        for category in keyword_dict.keys():
            for keyword in keyword_dict[category]:
                flag = content.find(keyword)
                if flag > -1:
                    break
            if flag > -1:
                full_path_file_name = text_path+category+'/'+category+file_num[category]
                put_content(full_path_file_name,content)
                file_num[category] = str( int(file_num[category]) + 1 )

def get_file_list(file_name):
    file_list = []
    with open(file_name, 'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            file_list.append(line.strip())
            line = file.readline()
    return file_list

def main(argv):
    file_name = argv[0]
    text_path = argv[1]
    file_list = get_file_list(file_name)
    make_categorized_data(file_list, text_path)

if __name__ == '__main__':
    main(sys.argv[1:])