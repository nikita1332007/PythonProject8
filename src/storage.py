from abc import ABC,abstractmethod
import json,os
from typing import List,Dict
class BaseStorage(ABC):
    @abstractmethod
    def load(self)->List[Dict]: ...
    @abstractmethod
    def add(self, items:List[Dict])->None: ...
    @abstractmethod
    def remove(self, url:str)->None: ...
class JSONStorage(BaseStorage):
    def __init__(self,path:str="vacancies.json"): self._path=path
    def load(self)->List[Dict]:
        if not os.path.exists(self._path): return []
        with open(self._path,encoding="utf-8") as f: return json.load(f)
    def add(self, items:List[Dict])->None:
        data=self.load(); urls={d["url"] for d in data}
        data += [i for i in items if i["url"] not in urls]
        with open(self._path,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=2)
    def remove(self,url:str)->None:
        data=[d for d in self.load() if d.get("url")!=url]
        with open(self._path,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=2)