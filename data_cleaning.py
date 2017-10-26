import os, re, time
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import ntpath


__REPL__ = ".\n"


def load_stop_words(stop_words_file):
    stop_words = set()
    with open(stop_words_file) as f:
            for line in f:
                word = line.strip()
                if word[0] != "#":
                    word = word.lower()
                    stop_words.add(word)
    return stop_words


__re_collapse_spaces__ = re.compile("\s+")
__re_remove_special_chars__ = re.compile("[;:\'\"\*/\),\(\|\s]+")


def collapse_spaces(s):
    return __re_collapse_spaces__.sub(" ", s).strip()


def clean_str(s):
    s = str(s).replace("'s"," ")
    s = s.replace("-", " ").replace("\\"," ")
    s = __re_remove_special_chars__.sub(" ",s).strip()
    return collapse_spaces(s)


def strip_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)


def pre_process_text(txt):
    txt = txt.replace("</li><li>", __REPL__).replace("<li>", __REPL__).replace("</li>", __REPL__)
    txt = txt.replace("<br>", __REPL__)
    txt = txt.replace("<br/>", __REPL__)
    txt = txt.replace("<br />", __REPL__)
    txt = txt.replace("<p>",  __REPL__)
    txt = txt.replace("<p/>",  __REPL__)
    txt = txt.replace("<p />",  __REPL__)
    txt = txt.replace("</p>", __REPL__)
    txt = txt.replace(". .",  __REPL__)
    txt = txt.replace("&nbsp;", " ")
    while ".." in txt:
        txt = txt.replace("..", ". ")
    while "  " in txt:
        txt = txt.replace("  ", " ")
    return txt


def if_visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', strip_non_ascii(element)):
        return False
    return True


def get_text(html):
    bs = BeautifulSoup(html,"html5lib")
    texts = bs.findAll(text=True)
    visible_texts = filter(if_visible, texts)
    return __REPL__.join(visible_texts)


def parsing_html(html):
    txt = get_text(pre_process_text(html))
    return txt


def split_into_sentences(txt):
    txt = strip_non_ascii(txt)
    sents = map(clean_str,sent_tokenize(txt))
    return filter(lambda s: len(s.strip()) > 5, sents)

ntpath.basename("a/b/c")


def get_file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

""" Process Files """


def process(documents_folder="", processed_documents_folder="", parse_html=True, minimum_file_size = 0):
    start = time.time()
    files = os.listdir(processed_documents_folder)
    if files:
        for file_path in files:
            os.remove(processed_documents_folder + file_path)

    files = os.listdir(documents_folder)
    for i, fpath in enumerate(files):
        with open(documents_folder + fpath) as f:
            contents = f.read()
            if len(contents) < minimum_file_size:
                continue
            if parse_html:
                contents = parsing_html(contents)
                if len(contents) < minimum_file_size:
                    continue
            sents = split_into_sentences(contents)
            doc = "\n".join(sents)
            file_name = get_file_name(fpath)
            fout_name = processed_documents_folder + "/" + file_name.split(".")[0] + "_proc.txt"
            with open(fout_name, "w+") as fout:
                fout.write(doc)
            if i % 1000 == 0 and i > 0:
                print("%i documents processsed" % i)
    end = time.time()
    print("Loading and processing documents took %s seconds" % str(end - start))
