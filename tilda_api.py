import requests

class TildaApi:
    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key
        self.base_url = 'https://api.tilda.cc'

    def _make_request(self, method, params=None):
        params = params or {}
        params.update({"public_key": self.public_key, "secret_key": self.secret_key})
        r = requests.get(f"{self.base_url}{method}/", params=params)
        return r.json()

    def create_post(self, title, description, text, images):
        project_id = self._make_request("getprojectslist")["result"][0]["id"]

        page = self._make_request("createpage", {"projectid": project_id, "title": title})
        if not page["result"]:
            return None

        page_id = page["result"]["id"]
        content = {
            "title": title,
            "descr": description,
            "text": text,
            "img": images[0] if images else "",
        }

        self._make_request("updatepage", {"pageid": page_id, "content": content})
        self._make_request("publishpage", {"pageid": page_id})

        return page_id

