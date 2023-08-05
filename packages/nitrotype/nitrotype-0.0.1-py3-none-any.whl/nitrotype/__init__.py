import requests
import random


class RaiseError(Exception):
    pass


class Client:
    def __init__(this, token: str):
        this._session = requests.Session()
        this._auth = token
        this._headers = {
            "authority": "www.nitrotype.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "cache-control": "no-cache",
            "authorization": this._auth,
            "origin": "https://www.nitrotype.com",
            "pragma": "no-cache",
            "referer": "https://www.nitrotype.com/",
            "sec-ch-ua": '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56",
        }
        this._api = {
            "profile": "https://www.nitrotype.com/api/v2/settings/profile",
            "register": "https://www.nitrotype.com/api/v2/auth/register/username",
            "daily": "https://www.nitrotype.com/api/v2/rewards/daily",
            "social": "https://www.nitrotype.com/api/v2/settings/social",
            "account": "https://www.nitrotype.com/api/v2/settings/account",
        }

    def account(
        this, 
        firstname: str, 
        lastname: str, 
        email: str, 
        contact: 1, 
        password=None
    ):
        if password == None:
            password = None
        password = password

        r = this._session.post(
            this._api["account"],
            headers=this._headers,
            json={
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "contact": contact,
                "password": password,
            },
        )
        if "restrict access" in r.text:
            raise RaiseError("Cloudflare denied your access.")
        return r.json()

    def social(this, status: bool, allowFriendRequests: bool, lookingForTeam: bool):
        if status == True:
            offline = 0
        else:
            offline = 1

        if allowFriendRequests == True:
            friends = 1
        else:
            friends = 0

        if lookingForTeam == True:
            team = 1
        else:
            team = 0
        r = this._session.post(
            this._api["social"],
            headers=this._headers,
            json={
                "offline": offline,
                "allowFriendRequests": friends,
                "lookingForTeam": team,
            },
        )
        if "restrict access" in r.text:
            raise RaiseError("Cloudflare denied your access.")
        return r.json()

    def daily(this):
        r = this._session.get(this._api["daily"], headers=this._headers)
        if "restrict access" in r.text:
            raise RaiseError("Cloudflare denied your access.")
        return r.json()

    def create(
        this, 
        username: str, 
        password: str, 
        wpm: int, 
        accuracy: int, 
        tz=None, 
        email=None
    ):
        if len(username) < 6:
            raise RaiseError("Display names must be between 6 and 20 characters.")

        if tz == None:
            tz = "America/New_Jersey"
        tz = tz

        if email == None:
            email = "%s@lasagna.email" % "".join(
                random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=10)
            )
        email = email

        this._session.headers["authorization"] = None
        r = this._session.post(
            this._api["register"],
            headers=this._headers,
            json={
                "username": username,
                "password": password,
                "email": email,
                "acceptPolicy": "on",
                "receiveContact": "",
                "tz": tz,
                "qualifying": 1,
                "avgSpeed": wpm,
                "avgAcc": accuracy,
                "carID": 9,
                "raceSounds": "only_fx",
            },
        )
        if "restrict access" in r.text:
            raise RaiseError("Cloudflare denied your access.")
        return r.json()

    def change_user(this, username: str):
        if len(username) < 6:
            raise RaiseError("Display names must be between 6 and 20 characters.")
        r = this._session.post(
            this._api["profile"],
            headers=this._headers,
            json={"displayName": username},
        )
        if "restrict access" in r.text:
            raise RaiseError("Cloudflare denied your access.")
        return r.json()
