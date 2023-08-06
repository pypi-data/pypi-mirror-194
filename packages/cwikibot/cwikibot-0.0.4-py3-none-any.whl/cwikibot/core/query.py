from .api import session
from . import date

import time
from typing import Union

from datetime import datetime, timedelta

def categorymembers(
    session: session,
    category_name: str,
    namespace="",
    pagetype="page",  # page | file | subcat
    sortmethod="title",  # timestamp
    startsortkey: Union[str, None] = None,
    endsortkey: Union[str, None] = None,
    sortdir = "desc"  # "desc | asc"
) -> list:

    if sortmethod == "timestamp": sortmethod = "touched"
    if sortdir == None:
        if sortmethod == "timestamp": sortdir = "desc"
        else: sortdir = "desc"
    members = []
    params = {
        "action": "query",
        "prop": "info",
        "generator": "categorymembers",
        "gcmnamespace": namespace,
        "gcmtitle": f"분류:{category_name}",
        "gcmprop": "title",
        "gcmtype": pagetype,
        "gcmlimit": "100",
        "gcmsort": "sortkey",
        "gcmdir": sortdir,
        "gcmcontinue": "",
    }
    while 1:
        data = session.get(params)
        members += data["query"]["pages"]
        if "continue" in data:
            params["gcmcontinue"] = data["continue"]["gcmcontinue"]
        else:
            break

    members = sorted(members, key=lambda item: item[sortmethod])

    if sortmethod == "touched":
        startdate = datetime.min
        enddate = datetime.min
        # when sortdir is "desc", startdate(2000) is later than enddate(1970)
        if startsortkey is None:
            startdate = datetime.now()
        else:
            startdate = date.parse(startsortkey)
        if endsortkey is None:
            enddate = datetime.min
        else:
            enddate = date.parse(endsortkey)
        members = [item["title"] for item in members
            if startdate < date.parse(item["touched"]) < enddate]
    
    else:
        if endsortkey == startsortkey is None:
            pass
        elif endsortkey is None:
            members = [item["title"] for item in members
                if startsortkey < item["title"]]
        elif startsortkey is None:
            members = [item["title"] for item in members
                if item["title"] < endsortkey]
        else:
            members = [item["title"] for item in members
                if startsortkey < item["title"] < endsortkey]
    return members


def recentchanges(
    session: session,
    days=0, minutes=0, hours=0, weeks=0,
    timestart = "", timeend = "",
    sortdir = "older",  # "older | newer"
    namespace = "",
    user = "",
    limit = 50,
    pagetype="page",  # page | file | subcat
    prefix = ""
    ) -> list:

    deltatime = timedelta(days=days, minutes=minutes, hours=hours, weeks=weeks)
    
    params = {
        "action": "query",
        "prop": "info",
        "list": "recentchanges",
        "rcnamespace": namespace,
        "rctype": "edit|new",
        "rclimit": limit,
        "rcdir": sortdir,
    }
    if user != "": params["rcuser"] = user

    if deltatime.total_seconds() != 0:
        timeend = date.now.utc
        timestart = timeend - deltatime
        print(f"timestart: {timestart}")
        print(f"timeend: {timeend}")
        params["rcstart"] = str(timeend)
        params["rcend"] = str(timestart)

    elif timeend == "" and timestart == "":
        pass

    else:
        if timeend == "":
            timeend = date.now.utc
        else:
            timeend = date.parse(timeend)

        timestart = date.parse(timestart)
        
        if sortdir == "older":
            params["rcstart"] = str(timeend)
            params["rcend"] = str(timestart)

        else:
            params["rcstart"] = str(timestart)
            params["rcend"] = str(timeend)

    data = session.get(params)
    members = data["query"]["recentchanges"]
    
    members = [item for item in members
        if item["title"].startswith(prefix) is True]

    #if "continue" in data:
    #    params["gcmcontinue"] = data["continue"]["gcmcontinue"]
    #else:
    #    break

    return members
