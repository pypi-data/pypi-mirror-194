# -*- coding: utf-8 -*-

#from typing import Any
from .api import Params, session
from typing import Union
from .color_cmdline import cprint, COLORS
from . import diff

import time, re, datetime

EXISTS = True
NOT_EXISTS = False
UNKNOWN = None

class Page:
    """wiki page class
    ~~~~~~~~~~~~~~~~~~
    """

    def __init__(self, session: session):
        #self.__root_path = session.url
        #"""root path (Absolute path)"""
        #self.__api_path = session.url
        #"""api path (Absolute path)"""

        self.title = ""
        self.origin: str = ''
        self._cont = "\0"
        self.__session = session
        """wiki session"""

        self.exists = UNKNOWN
        """ page exist

            exists: UNKNOWN, NOT_EXISTS, EXISTS
        """

    def __lshift__(self, title):
        self.set(title)
        return self

    def set(self, title: str):
        """init page object"""
        self.cont = ""
        self.title = title
        self.info = {}
        self.exists = UNKNOWN
        return self

            
    def get(self):
        """페이지 내용 얻기"""

        data: dict = self.__session.get({
            "action": "query",
            "prop": "revisions",
            "rvprop": "content|ids|user|timestamp|size",
            "titles": self.title,
        })["query"]["pages"][0]

        if "missing" in data:
            self.exists = NOT_EXISTS
        else:
            self.exists = EXISTS
            self.info = data.pop("revisions")[0]
            self.info["ns"] = data.pop("ns")
            self.info["title"] = data.pop("title")
            self.info["pageid"] = data.pop("pageid")

            self.origin = self._cont = self.info["content"]

        time.sleep(0.5)

    @property
    def cont(self) -> str:
        """page content"""

        if self.exists == UNKNOWN:
            self.get()

        return self._cont

    @property
    def rev_id(self) -> int:
        """int"""

        if self.exists == UNKNOWN:
            self.get()

        return self.info["revid"]

    @property
    def parent_id(self) -> int:
        """int"""

        if self.exists == UNKNOWN:
            self.get()

        return self.info["parentid"]

    @cont.setter
    def cont(self, content: str):
        if type(content) == str:
            self._cont = content
        else:
            Exception("type of page_content is str!")

    def get_revisions(self,
        start: Union[time.struct_time, None],
        end: Union[time.struct_time, None],
        dir = "older", prop: list = []) -> list:
        """ 판 목록 반환

        Args:
            start (time.struct_time, optional): _description_. Defaults to None.

            end (time.struct_time, optional): _description_. Defaults to None.

            dir (str, optional): sorting direction. "older" or "newer" are available.

                "older" is "newer to older". "newer" is "older to newer".

            prop (list, optional): revision property.

        Returns:
            list: revisions
        """

        params = {
            "action": "query",
            "titles": self.title,
            "prop": "revisions",
            "rvprop": '|'.join(prop),
            "rvslots": "*",
            "rvdir": dir
        }

        if start is not None:
            params['rvstart'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', start)

        if end is not None:
            params['rvend'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', end)

        localtime = time.time()

        data = self.__session.get(params)["query"]["pages"][0]

        if "missing" in data:
            self.new_page = True
            return []
        else:
            revs = data["revisions"]
            return revs


    def print(self):
        """페이지 텍스트 출력"""

        print(self)

    def printtitle(self):
        """페이지 텍스트 출력"""
        print(self.title)

    def __repr__(self) -> str:
        """페이지 객체 내용물 출력"""
        self.get()
        return f'''
__________________________________________________________
제목 = {self.title}
마지막 편집 = {self.info["timestamp"]}
----------------------------------------------------------
{self.cont}'''

    def remove(self, toremove: str) -> object:
        """텍스트 삭제

        Args:
            toremove (str): text to remove

        Returns:
            object: page object"""
        self.cont = self.cont.replace(toremove, "")
        return self

    def remove_re(self, pattern: str) -> object:
        """정규식 텍스트 삭제
        pattern: 정규식"""
        self.cont = re.sub(pattern, "", self.cont)
        return self

    def replace(self, toreplace: str, repl: str) -> object:
        """텍스트 대체
        pattern: 문자열
        repl: 대체할 문자열"""
        self.cont = self.cont.replace(toreplace, repl)
        return self

    def replace_re(self, pattern: str, repl: str) -> object:
        """정규식 텍스트 대체
        pattern: 정규식
        repl: 대체할 문자열"""
        self.cont = re.sub(pattern, repl, self.cont)
        return self

    def last_line(self) -> str:
        """last_line

        _extended_summary_

        Returns:
            str: _description_
        """
        return self.cont.rsplit("\n", 1)[1]

    def pop_last_line(self) -> str:

        return self.cont.rsplit("\n", 1)[0]

    def extract(self, start: str, end: str) -> str:

        cont = self.cont
        return f"{cont[ (cont.find(start) + len(start)) : (cont.find(end) ) ]}"

    def find_put_cont(self, start, toput: str, end):

        cont = self.cont
        self.cont = f"{cont[:cont.find(start)]}{start}\n{toput}{cont[cont.find(end):]}"

    def add_category(self, category: str, sortkey: str = "") -> str:
        """분류 추가
        category: 분류
        sortkey: 정렬키"""
        if sortkey == "":
            category = f"\n[[분류:{category}]]"
        else:
            category = f"\n[[분류:{category}|{sortkey}]]"

        if self.cont.find(category) == -1:
            self.append(category)

        return self.cont

    def append(self, string: str, dup: bool = True) -> str:
        """문서 끝에 문자열 추가
        dup = True 중복 허용(기본값)
        dup = False 중복 없음"""

        if dup is True or (dup is False and self.cont.find(string) == -1 ):
            self.cont = self.cont + string

        return self.cont

    def prepend(self, string: str, dup: bool = True) -> str:
        """문서 앞에 문자열 추가
        dup = True 중복 허용(기본값)
        dup = False 중복 없음"""

        if dup is True or (dup is False and self.cont.find(string) == -1 ):
            self.cont = string + self.cont

        return self.cont

    def save(self,
             summary: str = '',
             nocreate=None,
             minor=None,
             delay: float = 0,
             ):
        """save

        save page

        Args:
            summary (str, optional): edit summary
            nocreate (_type_, optional): dont create (only edit)
            minor (_type_, optional): is minor edit?
            delay (float, optional): presave delay

        Returns:
            _type_: _description_
        """

        time.sleep(delay)
        print(self.title + " 편집", end=' ')
        params = {
            "action": "edit",
            "title": self.title,
            "text": self.cont,
            "summary": summary,
            "bot": "true",
            "nocreate": nocreate,
            "minor": minor,
        }

        json = self.__session.post(params)
        if "edit" in json:
            if "nochange" in json["edit"]:
                cprint("변경 없음", COLORS.MINOR)
            else:
                diff.view(self.origin, self.cont)

                if "title" in json["edit"]:
                    print(f"제목 : {json['edit']['title']}")
                if "contentmodel" in json["edit"]:
                    print(f"콘텐츠 모델 : {json['edit']['contentmodel']}")
  
        else:
            print(json)
        # print(json)
        return json

    def move (
        self,
        new_title: str,
        reason: str = "",
        redirect: bool = False,
        movesubpages: bool = False,
    ) -> None:
        """move wikipage

        Args:
            new_title (str): _description_
            reason (str, optional): _description_. Defaults to "".
            redirect (bool, optional): _description_. Defaults to False.
            movesubpages (bool, optional): _description_. Defaults to False.
        """

        params = {
            "action": "move",
            "from": self.title, "to": new_title,
            "reason": reason,
            "movetalk": 1,
        }

        if redirect is False:
            params["noredirect"] = 1
        if movesubpages is True:
            params["movesubpages"] = 1

        data = self.__session.post(params)
        print(data)
