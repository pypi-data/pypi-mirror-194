import json

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import GraphTraversalSource
from turbindo.configuration import TurbindoConfiguration


class Gremlin:
    GRAPH_NATIVE_TYPE_LIST = ["bool", "str", "int"]
    GRAPH_TYPE_SERIALIZERS = {
        "datetime": lambda dt: dt.timestamp(),
        "list": lambda lst: json.dumps(lst),
        "dict": lambda dct: json.dumps(dct),
        "EntryType": lambda et: int(et)
    }

    @classmethod
    @property
    def g(cls) -> GraphTraversalSource:
        config = TurbindoConfiguration().config
        return traversal().withRemote(DriverRemoteConnection(
            config.db.gremlin.url,
            config.db.gremlin.traversal_source
        ))
