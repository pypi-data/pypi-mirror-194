"""connect with wiki api"""

from json import JSONDecodeError
from typing_extensions import override
from requests import Session as S
from .color_cmdline import cprint, COLORS

HEADER = S().headers
USER_AGENT = 'ceruleanwikibot/0.0.1'
HEADER['User-Agent'] = USER_AGENT

class Params(dict):
    """create preseted params

    Args:
        data (dict): json data
            without "formatversion", "utf8" and "format", These are preset
    """
    def __init__(self, data: dict):
        super().__init__(data)
        self.update({"formatversion": "latest", "utf8": 1, "format": "json"})

    def add(self, key: str, value: object) -> object:
        self[key] = value
        return self

def error_handle(res, params):
    try:
      # 서버 응답은 정상, json 오류
        if 'error' in res.json():
            cprint("api error", COLORS.ERROR)
            print(res.json()['error'])
            return {}
        return res.json()
    except JSONDecodeError:  # 404, 500 등의 오류
        cprint("server error", COLORS.ERROR)
        print(f"request: {params}")
        print(f"response: {res}")
        return {}

class session(S):
    class __str:
        def __init__(self, string):
            self.string = string

        def print(self):
            print(self.string)

# --------------------
# Method
# --------------------
    @override
    def get(self, params: dict) -> dict:
        """
        overriden GET Method for wiki

        Args:
            params (dict): json data
                without "formatversion", "utf8" and "format"!
                These are preset

        Raises:
            Exception: remote error

        Returns:
            Response
        """
        params = Params(params)
        response = super().get(url=self.url, params=params)

        return error_handle(response, params)

    def get_by_url(self, url: str):
        """
        GET Method by url

        Args:
            url (str): url with query string

        """
        return super().get(url=url)

    @override
    def post(self, data: dict, files= None):
        """
        overriden POST Method for wiki

        Args:
            data (dict): api param data
            files: only used to upload files
        """
        params = Params(data)

        if params['action'] != 'login':
            params.update({
                "token": self.csrftoken, "bot": int(self.bot_flag)
            })
        
        response = super().post(url=self.url, data=params, files=files)

        return error_handle(response, params)


    def __init__(self, api_path):
        super().__init__()
        self.headers = HEADER

        self.url = api_path
        """remote url"""

        self.login_status = False
        """ 로그인 상태 """
        self.login_result: str = "login result"
        """ 로그인 결과: 에러 메시지 등 """
        
        self.__csrftoken = False
        self.__bot_flag = False

        self.ret: object

    def get_userinfo(self, attrlist: list = ['editcount']):
        uiprops = '|'.join(attrlist)

        return self.get({
            'action': 'query',
            'meta': 'userinfo',
            'uiprop': uiprops
        })["query"]["userinfo"]

    def login(self, username: str, password: str):
        """사이트에 로그인

        로그인하지 않으면 편집 기록에 ip 주소가 노출됩니다.

        봇 계정도 가능하지만 봇을 이용하려면 봇 비밀번호 설정을 권장합니다, 형식 : username@passwd
        사이트 위키 특수문서에서 발급 가능.
        """
        
        data = self.get({'action': 'query', 'meta': 'tokens', 'type': 'login'})
        # get login token

        data = self.post({
            'action': 'login',
            'lgname': username,
            'lgpassword': password,
            'lgtoken': data["query"]["tokens"]["logintoken"]
        })
        # login

        self.result = data["login"]["result"]
        if self.result in ("Success", "success"):
            self.ret = self.__str(data)
            self.login_status = True
            self.username = username
            cprint("로그인됨", COLORS.SUCCESS)
            print(":", self.username)
        else:
            self.ret = self.__str(data)
            cprint("로그인 실패", COLORS.WARNING)
            print(data)

    def logout(self):
        if self.login_status is False:
            print("already logouted")
        else:
            data = self.post({"action": "logout"})
            if "error" in data:
                print("로그아웃 에러")
                raise Exception(data['error'])
                
            else:
                self.login_status = False
                cprint("로그아웃", COLORS.SUCCESS)
                print(": " + self.username)

    @property
    def csrftoken(self):
        """csrf token"""
        if self.__csrftoken is False:
            data = self.get({"action": "query", "meta": "tokens"})
            if data is None:
                data = self.get({"action": "query", "meta": "tokens"})  # retry
                if data is None:
                    return

            self.__csrftoken = data["query"]["tokens"]["csrftoken"]

        return self.__csrftoken

    @property
    def bot_flag(self):
        """bot flag"""
        return self.__bot_flag

    @bot_flag.setter
    def bot_flag(self, flag: bool):
        if flag is True or flag is False:
            self.__bot_flag = flag

    def __repr__(self) -> str:
        """view user info"""
        return f"Url = {self.url.api}\n사용자 = {self.username}"
