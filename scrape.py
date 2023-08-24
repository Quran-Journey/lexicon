import requests
from bs4 import BeautifulSoup
from main_translate import *

# Most successful so far


def acceptable(text):
    accept = ['[', 'a.', '', 'b.', 'c.', 'd.', 'e.', '(', 'ac.', ')']
    for every in accept:
        if every in text:
            return True
    return False


def split_def(sen: str):
    split = [". a..", ". c.", ". d.", ". e."]
    splitted = []
    for i in split:
        if i in sen:
            # print(f"splitted: {splitted}")
            sen = sen.split(i)
            # print(f"sen is:{sen}")
            splitted.append(sen.pop(0))
            sen = "".join(sen)
    # print(sen)
    splitted.append(sen)
    return splitted


def remove_aft(i: str, j: str):
    i = i.split(j)
    return i[0]


dictionary = {}
url = 'http://arabiclexico.com/habib-anthony-salmone-an-advanced-learners-arabic-english-dictionary/'
html = requests.get(url)

soup = BeautifulSoup(html.content, 'html.parser')
results = soup.find(id='container')
all_words = results.find_all('a', class_="letter-nav-post-link")

# Get all links from the html
links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))
# len of all links on page
# print(len(links)) = 6362

# Get all <a> tags
# print(str(all_words))

# To get all links of books
lst = []
for i in links[:6343]:
    if 'book' in i:
        # print(i)
        lst.append(str(i))
# Number of words = 6335
# print(len(lst))

# I only did it to 10 o we can reduce amount of requests made
for each in lst[:10]:
    new_html = requests.get(each)
    new_soup = BeautifulSoup(new_html.content, 'html.parser')
    new_result = new_soup.find('div', class_="definition")

    # First key of dictionary
    header = new_result.find('h2').text

    # Number of breakpoints
    # defi = len(new_result.find_all("br"))

    if header in dictionary:
        print(1)
    else:
        dictionary[header] = {}
        # print(f"Dictionary is: {dictionary}")

    new_parse = new_result.text.split(' ')
    index = 0
    lang = get_lang(new_parse[index])
    """
    Need to fix case where 
    1. the root word is 4 letter word
    2. the first index in new_parse is of form (ي)
    3. the first index in new_parse has len = 1
    4. Look at case jeem raa raa
    5. Look at case Jeem Zaa Hamza
    6. Look at case Jeem seen Daal
    7. Jeem Seen Meem
    8. Jeem Noon Yaa
    9. Jeem Haa Raa
    10. Haa Meem Laam
    11. Khaa Seen Faa
    12. "خَنْجَر"
    13. "دَحَا"
    14. Daal Alif Meem
    15. Raa Hamza Faa
    16. 
    """
    if lang == 'Arabic' or lang == 'Neither':
        # print(new_parse)
        while index != len(new_parse):
            sentences = []
            sentence = ''
            if ")" in new_parse[index]:
                index += 1
                while index < len(new_parse) and (get_lang(new_parse[index]) == 'English' or
                                            (acceptable(new_parse[index]) and get_lang(new_parse[index]) == 'Neither')):
                    sentence += " " + new_parse[index]
                    index += 1
                    # print(sentence)
                #print(sentence)
                #print(index)
                sentences = split_def(sentence)
                # print(new_parse[1], 111)
                if "(" in new_parse[1]:
                    define = remove_aft(new_parse[1], "(")
                else:
                    define = new_parse[1]
                dictionary[new_parse[0]][define] = sentences
                # print(sentences)
            if len(sentences) >= 1:
                # print(sentences)
                break
            index += 1


root = dictionary.keys()
for i in root:
    words = dictionary[i].keys()
    for j in words:
        print(i, j, dictionary[i][j])

print(f"Dictionary is: {dictionary}")
