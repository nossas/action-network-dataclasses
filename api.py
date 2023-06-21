import re
import requests

from typing import Any, TypeVar, Generic

from base import Page, Campaign
from parsers import json_to_obj


A = TypeVar("A")
B = TypeVar("B")



class BaseActionNetwork(Generic[A, B]):
    DetailClass = None
    ListClass = None
    urls = {
        "list": "/campaigns",
        "get": "/campaigns/[uuid:str]/"
    }

    def __init__(self):
        self.base_url = "https://actionnetwork.org/api/v2"
        self.headers = {
            "OSDI-API-Token": "xxx"
        }
    
    def _get_url(self, method, **kwargs):
        endpoint = self.urls.get(method)
        routes = []
        subpath = endpoint.split("/")
        
        for path in subpath:
            pattern = re.compile(r"[\w]+").findall(path)
            if len(pattern) > 1:
                param = kwargs.get(pattern[0], None)
                if not param:
                    raise Exception(f"should be pass '{path}'")
                
                routes.append(param if pattern[1] == 'str' else str(param))
            else:
                routes.append(path)
               
        return self.base_url + "/".join(routes)

    def __make_request(self, url, Class, method="get", **kwargs) -> Any:
        response = getattr(requests, method)(url, headers=self.headers)
        
        if response.status_code == 200:
            # Fixed values like action_network:campaigns
            data = response.json()
            if data.get("_embedded", False):
                data["_embedded"]["data"] = data["_embedded"].pop("action_network:campaigns")
            
            return json_to_obj(Class, data)
        else:
            raise Exception(response.status_code, response.json())

    def list(self) -> A:
        uri = self._get_url("list")
        
        return self.__make_request(uri, self.ListClass)



    def get(self, uuid: str) -> B:
        uri = self._get_url("get", uuid=uuid)
        
        return self.__make_request(uri, self.DetailClass)

        # response = requests.get(self.base_url + self.path, headers=self.headers)
        # if response.status_code == 200:
        #     # Fixed values like action_network:campaigns
        #     data = response.json()
        #     if data.get("_embedded", False):
        #         data["_embedded"]["data"] = data["_embedded"].pop("action_network:campaigns")
            
        #     return json_to_obj(T, data)
        # else:
        #     raise Exception(response.status_code, response.json())



class CampaignAPI(BaseActionNetwork[Page, Campaign]):
    DetailClass = Campaign
    ListClass = Page