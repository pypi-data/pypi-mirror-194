from typing import Dict
from typing import Optional
from typing import Tuple

from flask import Request
from flask_login import UserMixin  # type: ignore

from jumonc import settings
from jumonc.authentication import scope_name
from jumonc.authentication import scopes
from jumonc.handlers import base
from jumonc.helpers.generateToken import generateToken


        
def parseUserToken(text: str) -> Tuple[str,int]:
    parts = text.split(":")
    return (parts[0], int(parts[1]))


tokens: Dict[str,int]= {}


def addToken(token:str, scope:int) -> None:
    tokens[token] = scope


def registerTokens() -> None:
    for user_token in settings.USER_DEFINED_TOKEN:
        (token, scope) = parseUserToken(user_token)
        tokens[token] = scope

    for scope in scopes.values():
        while True:
            token = generateToken()
            if token in tokens:
                pass
            break
        tokens[token] = scope

    for (token, scope) in tokens.items():
        print(scope_name[scope] + ": " + token)

class Authenticated(UserMixin):
    pass



@base.login_manager.user_loader
def user_loader(tokenScope: str) -> Optional[Authenticated]:
    if tokenScope not in tokens:
        return None

    auth = Authenticated()
    auth.id = tokenScope
    return auth


def getTokenScope(token: Optional[str]) -> Optional[Authenticated]:
    if token not in tokens:
        return None
    
    auth = Authenticated()
    auth.id = token
    
    #auth.is_authenticated = True
    
    return auth


@base.login_manager.request_loader
def request_loader(request: Request) -> Optional[Authenticated]:
    token = request.args.get('token', default = None, type = str)
    return getTokenScope(token)


@base.login_manager.unauthorized_handler
def unauthorized_handler() -> str:
    return 'Unauthorized'
