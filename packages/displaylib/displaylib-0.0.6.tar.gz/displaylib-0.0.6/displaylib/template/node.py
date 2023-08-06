from typing_extensions import Self
from ..math import Vec2
from .types import Engine


class Node:
    """Node base class

    Automatically keeps track of alive Node(s) by reference.
    An Engine subclass may access it's nodes through the `nodes` class attribute
    """
    __logical__ = True # logical means it won't have a position or existance in the "real world"

    root: Engine = None # set from a Engine subclass
    nodes = {} # all nodes that are alive
    _request_sort = False # requests Engine to sort
    _queued_nodes = set() # uses <Node>.queue_free() to ask Engine to delete them

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        instance = super().__new__(cls)
        Node.nodes[id(instance)] = instance
        return instance

    def __init__(self, parent: Self | None = None, *, force_sort: bool = True) -> None:
        self.parent = parent
        self.z_index = 0 # static
        if force_sort: # if True, requests sort every frame a new node is created
            Node._request_sort = True # otherwise, depent on a `z_index` change

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
    
    @property
    def name(self) -> str:
        return self.__class__.__name__

    def _update(self, delta: float) -> None:
        return
    
    def queue_free(self) -> None:
        Node._queued_nodes.add(self)


class Node2D(Node):
    """Node2D class with transform attributes
    """
    __logical__ = False

    def __init__(self, parent: Self | None = None, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        self.parent = parent
        self.position = Vec2(x, y)
        self._z_index = z_index
        self.visible = True
        if force_sort: # if True, requests sort every frame a new node is created
            Node._request_sort = True # otherwise, depend on a `z_index` change
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.position.x}, {self.position.y})"

    @property
    def z_index(self) -> int:
        return self._z_index

    @z_index.setter
    def z_index(self, value: int) -> None:
        if self._z_index != value:
            self._z_index = value
            Node._request_sort = True
    
    @property
    def global_position(self) -> Vec2:
        position = self.position
        node = self.parent
        while node != None:
            position += node.position
            node = node.parent
        return position
    
    @global_position.setter
    def global_position(self, position: Vec2) -> None:
        diff = position - self.global_position
        self.position += diff
