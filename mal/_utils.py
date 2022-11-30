import json
import secrets
from mal._basic import _BasicReq, _secondaryApiUrl

def get_new_code_verifier() -> str: #para generar codigos
    token = secrets.token_urlsafe(100)
    return token[:128]

class _MalToken():

    def __init__(self, tokenType: str,accessToken: str,refreshToken: str,expiresIn: int | None):
        self.token_type: str = tokenType
        self.expires_in: int | None = expiresIn
        self.access_token: str = accessToken
        self.refresh_token: str = refreshToken

    def fromJsonObj(obj: dict["token_type": str,"access_token": str,"refresh_token": str, "expires_in": int | None]): 
        """Get MalToken From Token JSON Object"""
        try:
            return _MalToken(
                obj["token_type"],
                obj["access_token"],
                obj["refresh_token"],
                obj["expires_in"]
            )
        except:
            return obj

    def fromJsonString(string: str):
        """Get MalToken From Token JSON String"""
        obj = dict[
            "token_type": str,
            "access_token": str,
            "refresh_token": str,
            "expires_in": int | None,
        ] = json.loads(string)
        try:
            return _MalToken(
                obj["token_type"],
                obj["access_token"],
                obj["refresh_token"],
                obj["expires_in"]
            )
        except:
            return obj

    async def fromCredential(clientId: str,username: str,password: str):
        """
        **Unstable!**
        Get MalToken From Login And Password
        """
        DATA = {
            "client_id": clientId,
            "grant_type": "password",
            "username": username,
            "password": password
        }
        REQ = _BasicReq()
        res = REQ._post("auth/token",data=DATA)
        try:
            return _MalToken(
                res["token_type"],
                res["access_token"],
                res["refresh_token"],
                res["expires_in"]
            )
        except:
            return res

    async def fromRefreshToken(clientId: str, refreshToken: str):
        """Get MalToken From Refresh Token"""
        DATA = {
            "client_id": clientId,
            "refresh_token": refreshToken,
            "grant_type": "refresh_token",
        }
        REQ = REQ = _BasicReq()
        res = REQ._postApiV1("oauth2/token",data=DATA)
        try:
            return _MalToken(
                res["token_type"],
                res["access_token"],
                res["refresh_token"],
                res["expires_in"]
            )
        except:
            return res

    async def fromAuthorizationCode(clientId: str,code: str,codeVerifier: str): 
        """Get _MalToken From PKCE Authorization Code"""
        DATA = {
            "client_id": clientId,
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": codeVerifier,
        }
        REQ = REQ = _BasicReq()
        res = REQ._postApiV1("oauth2/token",data=DATA)
        try:
            return _MalToken(
                res["token_type"],
                res["access_token"],
                res["refresh_token"],
                res["expires_in"]
            )
        except:
            return res

class _MalAccount():

    def __init__(self, clientId: str, malToken: _MalToken | None = None):
        self.__clientId: str = clientId
        self.__malToken: _MalToken = malToken
        # DONT USE REFERENCE CIRCULAR TO IMPORT NO VALID
        # self.user: MalUser = MalUser(self)
        # self.anime:MalAnime = MalAnime(self)
        # self.manga: MalManga = MalManga(self)
        # self.forum: MalForum = MalForum(self)

    async def refreshToken(self):
        if (self.__malToken is None):
            self.__malToken = await _MalToken.fromRefreshToken(
                self.__clientId,
                self.__malToken.refresh_token
            )
        return self

    def getHttpHeaders(self):
        HEADERS: dict[str, str] = {
            'Content-Type': 'application/json',
            "Authorization": None,
            "X-MAL-CLIENT-ID": self.__clientId
        }
        print(type(self.__malToken))
        if (self.__malToken is None):
            HEADERS["Authorization"] = "Bearer %s" %(self.__malToken["access_token"])
        return HEADERS

    def stringifyToken(self) -> str:
        if (self.__malToken is None):
            return json.dumps(self.__malToken)
        else:
            return None

class Auth():
    
    def __init__(self,clientId: str = "6114d00ca681b7701d1e15fe11a4987e"):
        self.__clientId = clientId

    def loadToken(self, token: _MalToken):
        return _MalAccount(self.__clientId, token)

    def getOAuthUrl(self,codeChallenge: str) -> str:
        BASE = _secondaryApiUrl
        return  "%soauth2/authorize?response_type=code&client_id=%s&code_challenge_method=plain&code_challenge=%s" %(BASE,self.__clientId,codeChallenge)

    async def authorizeWithRefreshToken(self,refreshToken: str) -> _MalAccount: 
        MALTOKEN = await _MalToken.fromRefreshToken(self.__clientId,refreshToken)
        return _MalAccount(self.__clientId, MALTOKEN)

    async def authorizeWithCode(self, code: str,codeChallenge: str) -> _MalAccount:
        """It is actually a `code_verifier` but mal accepts code_challenge here instead"""
        MALTOKEN = await _MalToken.fromAuthorizationCode(self.__clientId,code,codeChallenge)
        return _MalAccount(self.__clientId, MALTOKEN)

    # *** UNSTABLE FOR NO USE PRODUCTION ***
    # async def guestLogin(self) -> _MalAccount:
    #     return _MalAccount(self.__clientId, None)

    async def unstableLogin(self,username: str, password: str) -> _MalAccount:
        """### Login to API using login and password `(Unstable!)`"""
        MALTOKEN = await _MalToken.fromCredential(self.__clientId,username,password)
        print(self.__clientId)
        return _MalAccount(self.__clientId, MALTOKEN)