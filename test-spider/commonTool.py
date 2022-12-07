# commonTool
import json
from typing import List, Any


def to1D(arr_2d: List[List[Any]]) -> List[Any]:
  re_array: List[Any] = []
  for a in arr_2d:
    re_array.extend(a)
  return re_array


def loadJsonFile(path: str):
  with open(path, 'r') as f:
    return json.load(f)


##
assert [1, 2, 3, 4, 5] == to1D([[1], [2], [3, 4], [5]])
