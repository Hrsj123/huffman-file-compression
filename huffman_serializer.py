from abc import ABC, abstractmethod
from functools import total_ordering
import heapq
from typing import List, Union, Dict
from bitarray import bitarray
import json

class HuffBaseNode(ABC):
    @abstractmethod
    def is_leaf() -> bool:
        pass
    
    @abstractmethod
    def weight() -> int:
        pass

class HuffLeafNode(HuffBaseNode):
    _element: str = ""
    _weight: int = 0

    def __init__(self, element: str, weight: int):
        self._element = element
        self._weight = weight

    def value(self) -> str:
        return self._element
    
    def weight(self) -> int:
        return self._weight
    
    def is_leaf(self) -> bool:
        return True
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self._element}, {self._weight})"

class HuffInternalNode(HuffBaseNode):
    _weight: int = 0
    _left: HuffBaseNode = None
    _right: HuffBaseNode = None

    def __init__(self, left: HuffBaseNode, right: HuffBaseNode, weight: int):
        self._weight = weight
        self._left = left
        self._right = right

    def left(self) -> HuffBaseNode:
        return self._left
    
    def right(self) -> HuffBaseNode:
        return self._right

    def weight(self) -> int:
        return self._weight

    def is_leaf(self) -> bool:
        return False
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self._weight})"


@total_ordering
class HuffTree:
    _root: HuffBaseNode = None
    _encoded_char_dict: Dict[str, str] = {}

    def __init__(self, wt: int, e1: str=None, l: HuffBaseNode=None, r: HuffBaseNode=None):
        if e1 is None and (l is None or r is None):
            raise ValueError("Either 'e1' must be provided or both 'l' and 'r' must be provided.")

        if e1 is not None:
            self._root = HuffLeafNode(e1, wt)
        elif not (l is None or r is None):
            self._root = HuffInternalNode(l, r, wt)

    def __lt__(self, other: 'HuffTree'):
        if isinstance(self.root(), HuffLeafNode) and isinstance(other.root(), HuffLeafNode):
            if self.weight() == other.weight():
                return self.root().value() < other.root().value()
            return self.weight() < other.weight()
        return self.weight() < other.weight()

    def __eq__(self, other: 'HuffTree'):
        if isinstance(self.root(), HuffLeafNode) and isinstance(other.root(), HuffLeafNode):
            return self.weight() == other.weight() and self.root().value() == other.root().value()
        return self.weight() == other.weight()

    def weight(self) -> int:
        return self._root.weight()

    def root(self) -> Union[HuffLeafNode, HuffInternalNode]:
        return self._root

    @classmethod
    def build_tree(cls, heap: List[HuffLeafNode]) -> 'HuffTree':
        heapq.heapify(heap)

        temp1: HuffTree = None
        temp2: HuffTree = None
        temp3: HuffTree = None

        while len(heap) > 1:
            temp1 = heapq.heappop(heap)
            temp2 = heapq.heappop(heap)

            combined_weight = temp1.weight() + temp2.weight()
            temp3 = HuffTree(
                l=temp1.root(), 
                r=temp2.root(), 
                wt=combined_weight
            )
            heapq.heappush(heap, temp3)
        return temp3
    
    def get_bytes_dict(self) -> bytes:
        return json.dumps(self._encoded_char_dict).encode("utf-8")
    
    def _encoder(self, root, seq=""):
        if root is not None:
            if isinstance(root, HuffLeafNode):
                self._encoded_char_dict[root.value()] = seq
            self._encoder(
                root.left() if not isinstance(root, HuffLeafNode) else None,
                seq=seq+"0"
            )
            self._encoder(
                root.right() if not isinstance(root, HuffLeafNode) else None,
                seq=seq+"1"
            )

    def encoder(self) -> Dict[str, str]:
        self._encoder(self.root())
        return self._encoded_char_dict

    def decoder(self, data: bitarray, d=None) -> str: 
        rev_dict = {v: k for k, v in (d or self._encoded_char_dict).items()}
        decoded_chars = []
        key = ""

        data_str = data.to01()

        for char in data_str:
            key += char
            if key in rev_dict:
                decoded_chars.append(rev_dict[key])
                key = ""
        
        if key:
            raise Exception("Failed to decode data......")
        

        return "".join(decoded_chars)
