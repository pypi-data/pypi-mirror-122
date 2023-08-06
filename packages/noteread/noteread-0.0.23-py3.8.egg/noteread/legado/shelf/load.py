import json
import logging

import requests
from noteread.legado.shelf.base import BookSource, BookSourceCorrect
from noteread.legado.shelf.libs.core import load_from_url
from noteread.legado.shelf.libs.correct import correct_source
from noteread.legado.shelf.libs.mumuceo import SHU_YUAN, load_from_mumuceo
from notetool.log import logger
from tqdm import tqdm

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


book = BookSource(lanzou_fid=4147049)
book_correct = BookSourceCorrect(lanzou_fid=4147049)

# load
load_from_url(urls=urls, book=book)
load_from_mumuceo(source=SHU_YUAN, book=book)

# correct
correct_source(book, book_correct)

# print
print(len(book.select_all()))
print(len(book_correct.select_all()))

# save
print(book.db_save())
