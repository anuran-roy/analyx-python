from .endpoints import Endpoint
from .flow import Flow, FlowNode, FlowLayer, FlowNodeType, FlowLayerType
from .settings import plugins
from typing import List
from .plugins import PluginType
from . import errors

class MetricsBase:
    def __init__(self):
        self._plugins: List = plugins
        for plg in self._plugins:
            globals()[lib] = __import__(plg)

    @property
    def plugins(self):
        return self._plugins
    
    # def addPlugin(self, plg: PluginType):
    #     if plg in self.plugins:
    #         raise errors.PluginAlreadyExists(which=plg._metadata["plugin"])

class Metrics(MetricsBase):
    def __init__(self, loc, **kwargs):
        super().__init__()
        self.id = loc
        self.endpoints: List = []
        self.db = kwargs["db"] if "db" in kwargs.keys() else None

    def add_to_analytics(self, func):
        functions = func() \
            if type(func) == type(lambda x: x) else func
        # print(f"\n\n{functions}\n\n")
        existing_endpoint_names = [x['id'] for x in self.endpoints]
        # new_endpoint_names = [x.__name__ for x in functions]

        for i in range(len(functions)):
            if functions[i].__name__ in existing_endpoint_names:
                loc = existing_endpoint_names.index(functions[i].__name__)
                self.endpoints[loc]["endpoint"].hits += 1
            else:
                new_endpoint = Endpoint(id=functions[i].__name__,
                                        endpoint=functions[i], hits=1)
                self.endpoints.append({
                    'id': functions[i].__name__,
                    'endpoint': new_endpoint})

    def display(self, **kwargs):

        # print(f"\n\n{self.id}\n\n")
        ep = None

        if 'id' in kwargs.keys():
            for i in self.endpoints:
                if i['id'] == kwargs['id']:
                    ep = [i]
                    break
        else:
            ep = self.endpoints

        print("\n\nId:\tHits\n")

        for i in ep:
            data = i['endpoint'].stats()

            for j in data.keys():
                print(f"{j}: {data[j]}", end="\t")

            print()