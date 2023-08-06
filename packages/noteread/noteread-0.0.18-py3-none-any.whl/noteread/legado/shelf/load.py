import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(process)d-%(processName)s - %(filename)s-%(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    #datefmt='%Y-%m-%d %H:%M:%S',
    # filename='notejob.log',
    # filemode='a'
)

from notetool.log import logger

logger.info("msg")
from tqdm import tqdm
from noteread.legado.shelf.base import BookSource, BookSourceCorrect
import requests
import json



def check_contain_unusual(s):
    """包含汉字的返回TRUE"""
    if s is None:
        return False
    for c in s:
        if c in (' ', '\u011f'):
            return True
        # if (c < '\u4e00' or c > '\u9fa5') and c not in ('\u2603', ' ', '\u0e05'):
        #    return True
    return False


def check_contain_chinese(s):
    """包含汉字的返回TRUE"""
    if s is None:
        return False
    for c in s:
        if '\u4e00' <= c <= '\u9fa5':
            return True
    return False


class SourceDetail:
    def __init__(self, data):
        self.data = json.loads(data, encoding='utf-8')
        self.valid = True
        self.check()
        if self.valid:
            self.handle()
            print(self.data)
            print(self.data.get('bookSourceGroup', ''), self.data.get('bookSourceComment', ''))

    def check(self):
        if check_contain_unusual(self.data.get('bookSourceGroup')):
            self.valid = False
            return self.valid

    def handle(self):
        if 'bookSourceComment' in self.data.keys() and len(self.data['bookSourceComment']) > 10:
            self.data['bookSourceComment'] = '默认'


def load_source(urls=None, cate1='1'):
    if urls is None:
        urls = [
            "https://cdn.jsdelivr.net/gh/bushixuanqi/book-source/%E4%B9%A6%E6%BA%90%E5%90%88%E9%9B%86.json",

            "https://guaner001125.coding.net/p/coding-code-guide/d/booksources/git/raw/master/sources/guaner.json",
            "https://haxc.coding.net/p/booksrc/d/booksrc/git/raw/master/Book3.0Source.json",

            "https://namofree.gitee.io/yuedu3/legado3_booksource_by_Namo.json",
            "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/syhj.json",
            "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/yshj.json",

            "http://shuyuan.miaogongzi.net/shuyuan/1624832786.json",
            "https://shuyuan.miaogongzi.net/shuyuan/1630342495.json",
            "http://shuyuan.miaogongzi.net/shuyuan/1623355431.json",

            "https://tangguochaotian.coding.net/p/tangguoshuyuan1015/d/tangguo/git/raw/master/exportBookSource.json",
            "https://tianyuzhange.coding.net/p/booksource/d/shuyuan/git/raw/master/2.0shuyuan.json",
        ]

    book = BookSource(lanzou_fid=4103875)
    print(book.db_path)
    for url in tqdm(urls):
        try:
            text = requests.get(url).text
            for line in json.loads(text):
                book.add_json(json.dumps(line), cate1=cate1)
        except Exception as e:
            logger.error(e)
    # book.db_save()


def correct_source():
    book = BookSourceCorrect(lanzou_fid=4103875)
    print(book.db_path)
    for shelf in book.select_all():
        source = SourceDetail(data=shelf['jsons'])
        if not source.valid:
            continue
        book.add_json(json.dumps(source.data),
                      md5=shelf['md5'],
                      cate1=shelf['cate1'],
                      cate2=shelf['cate2'],
                      cate3=shelf['cate3'])

    # book.db_save()


load_source()
correct_source()

book = BookSource(lanzou_fid=4103875)
print(book.db_save())
