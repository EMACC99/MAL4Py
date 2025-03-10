from typing import Union, List, Dict
import requests

_api_url = "https://api.myanimelist.net/v2/"
_secondary_api_url = "https://myanimelist.net/v1/"


class _BasicReq:
    def __init__(self, headers: Union[Dict[str, str], None] = None):
        """
        Add params from API MAL GET and Headers from query
        """
        if headers is None:
            self.headers = {}
            self.headers["Content-Type"] = "application/x-www-form-urlencoded"
            self.headers["X-MAL-Client-ID"] = "6114d00ca681b7701d1e15fe11a4987e"
        else:
            self.headers = headers

    def _get(self, slug: str, params: Union[dict, None] = None) -> List[int, dict]:
        """Get request to https://api.myanimelist.net/v2/"""
        resp_get = requests.get(_api_url + slug, params=params, headers=self.headers)
        print(resp_get.url)
        return [resp_get.status_code, resp_get.json()]

    def _post(self, slug: str, data: Union[dict, None] = None) -> List[int, dict]:
        """Post request to https://api.myanimelist.net/v2/"""
        resp_post = requests.post(_api_url + slug, headers=self.headers, data=data)
        print(resp_post.url)
        return [resp_post.status_code, resp_post.json()]

    def _post_api_v1(
        self, slug: str, data: Union[dict, None] = None
    ) -> List[int, dict]:
        """Post request to https://myanimelist.net/v1/, usally for get token account"""
        resp_post = requests.post(
            _secondary_api_url + slug, headers=self.headers, data=data
        )
        print(resp_post.url)
        return [resp_post.status_code, resp_post.json()]

    def _patch(self, slug: str, data: Union[dict, None] = None) -> List[int, dict]:
        """Put request to https://api.myanimelist.net/v2/"""
        resp_patch = requests.patch(_api_url + slug, headers=self.headers, data=data)
        print(resp_patch.url)
        print(self.headers)
        return [resp_patch.status_code, resp_patch.json()]

    def _delete(self, slug: str, data: Union[dict, None] = None) -> List[int, dict]:
        """Delete request to https://api.myanimelist.net/v2/"""
        resp_del = requests.delete(_api_url + slug, headers=self.headers)
        print(resp_del.url)
        return [resp_del.status_code, resp_del.json()]
