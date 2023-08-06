import json

from noteread.legado.shelf.base import BookSource


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


class TransForm:
    def __init__(self):
        pass

    def run(self):
        # book = BookSource(lanzou_fid=4103875)
        book = BookSource()
        print(book.db_path)
        for shelf in book.select_all():
            source = SourceDetail(data=shelf['jsons'])
            # if source.valid:
            #     break


trans = TransForm()

trans.run()
