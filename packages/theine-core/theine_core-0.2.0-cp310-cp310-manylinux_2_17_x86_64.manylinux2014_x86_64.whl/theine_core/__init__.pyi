from typing import Optional

class TlfuCore:
    def __init__(self, size: int): ...
    def set(self, key: str, expire: int) -> Optional[str]: ...
    def remove(self, key: str): ...
    def access(self, key: str): ...
    def advance(self, now: int, cache: dict, kh: dict, hk: dict): ...

class LruCore:
    def __init__(self, size: int): ...
    def set(self, key: str, expire: int) -> Optional[str]: ...
    def remove(self, key: str): ...
    def access(self, key: str): ...
    def advance(self, now: int, cache: dict, kh: dict, hk: dict): ...

class BloomFilter:
    def put(self, key: str): ...
    def contains(self, key: str) -> bool: ...
