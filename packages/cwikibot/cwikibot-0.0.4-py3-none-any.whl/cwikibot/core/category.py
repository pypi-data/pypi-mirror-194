from typing import Union
from .api import session
import time

class Category:
    @staticmethod
    def members(
        session: session,
        category_name: str,
        namespace: str = "",
        type: str = "page",
        sortkey: str = "sortkey",
        startsortkey: Union[str, None] = None,
        endsortkey: Union[str, None] = None,
        ) -> list:

        members = []

        params = {
            "action": "query",
            "list": "categorymembers",
            "continue": "-||",
            "cmtitle": f"분류:{category_name}",
            "cmnamespace": namespace,
            "cmprop": "title|timestamp",
            "cmtype": type,
            "cmlimit": "100",
            "cmsort": sortkey,
            "cmstartsortkeyprefix": startsortkey,
            "cmendsortkeyprefix": endsortkey,
            }

        while 1:
            data = session.get(params)
            if data is None:
                continue

            data = data
            members.extend(data["query"]["categorymembers"])
            if "continue" in data:
                params["cmcontinue"] = data["continue"]["cmcontinue"]
            else:
                break
        #print(members)
        return members
        

    @staticmethod
    def members_sorted(
        session: session,
        category_name: str,
        namespace: str = "",
        type: str = "page",
        sortkey: str = "sortkey",
        startdate: Union[time.struct_time, None] = None,
        enddate: Union[time.struct_time, None] = None,
        ) -> list:

        if startdate is None:
            startdate = time.gmtime(0)
        else:
            startdate = time.strptime(str(startdate), "%Y-%m-%dT%H:%M:%SZ")
        if enddate is None:
            enddate = time.gmtime()
        else:
            enddate = time.strptime(str(enddate), "%Y-%m-%dT%H:%M:%SZ")

        members = []

        params = {
            "action": "query",
            "prop": "revisions",
           	"rvprop": "timestamp",
            "generator": "categorymembers",
            "gcmnamespace": namespace,
            "gcmtitle": f"분류:{category_name}",
            "gcmprop": "title",
            "gcmtype": type,
            "gcmlimit": "100",
            "gcmsort": sortkey,
            "gcmcontinue": "-||",
        }
        while 1:
            data = session.get(params)
            if data is None:
                continue

            data = data
            members.extend(data["query"]["pages"])
            if "continue" in data:
                params["gcmcontinue"] = data["continue"]["gcmcontinue"]
            else:
                break

        sorted_pages = sorted(
            members, key=lambda item: item["revisions"][0]["timestamp"])

        topushpages = []

        for v in sorted_pages:
            timestamp = v["revisions"][0]["timestamp"]
            timestamp = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
            if startdate < timestamp < enddate:
                topushpages.append(v["title"])

        #print(topushpages)
        return topushpages

