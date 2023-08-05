from typing import Dict
from requests_html import HTMLSession
from functools import singledispatch
from .exception import NotEnglishWordException


def lazyproperty(func):
    name = "_lazy_" + func.__name__

    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value

    return lazy


class TransMeta(type):
    def __new__(cls, clsname, bases, attrs):
        if not clsname.endswith("Trans"):
            raise TypeError(f"Class name should end with Trans")
        if clsname != "Trans" and "translate" not in attrs:
            raise NotImplementedError(f"Class {clsname} should impl translate() method")
        return super().__new__(cls, clsname, bases, attrs)


class Trans(metaclass=TransMeta):
    def __init__(self, word, url):
        self.word = word
        self._url = url
        self._session = HTMLSession()

    @lazyproperty
    def r(self):
        return self._session.get(self._url)

    @property
    def pronounce(self):
        return self.translate()[0]

    @property
    def trans(self):
        return self.translate()[1]

    @property
    def sentences(self):
        return self.translate()[2]


class YoudaoTrans(Trans):
    def __init__(self, word):
        _url = f"http://dict.youdao.com/w/eng/{word}/"
        super(YoudaoTrans, self).__init__(word, _url)

    def translate(self):
        # pronounce
        pronounce = [
            "".join(p.xpath("//span//text()")).replace("\n", "").replace(" ", "")
            for p in self.r.html.xpath("//span[@class='pronounce']")
        ]
        # tranlation
        temp_trans = self.r.html.xpath(
            "(//div[@class='trans-container'])[1]/ul/li/text()"
        )
        trans = [
            {"cixing": t.split(".")[0], "tran": t.split(".")[1]}
            for t in temp_trans
            if len(t.split(".")) > 1
        ]

        # examples
        temp_sentences = self.r.html.xpath("//div[@id='bilingual']/ul/li")
        sentences = [
            {
                "en": "".join(example.xpath("(//p)[1]//text()")).strip("\n"),
                "cn": "".join(example.xpath("(//p)[2]//text()")).strip("\n"),
            }
            for example in temp_sentences
        ]
        return pronounce, trans, sentences


def trans(word: str, engine: str = "youdao") -> Dict:
    """trans word, default engine is youdao"""

    if len(word.split(" ")) > 1:
        raise NotEnglishWordException("Invalid word")

    engine = globals().get(f"{engine.title()}Trans", None)
    trans_result = engine(word) if engine else {}

    return {
        "name": word,
        "pronounce": trans_result.pronounce or [],
        "trans": trans_result.trans or [],
        "sentences": trans_result.sentences or {},
    }
