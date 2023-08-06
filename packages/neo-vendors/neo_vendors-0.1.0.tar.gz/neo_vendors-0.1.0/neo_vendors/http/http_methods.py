from __future__ import annotations

import enum


class HttpMethodsEnum(enum.Enum):
    get = enum.auto()
    post = enum.auto()
    put = enum.auto()
    patch = enum.auto()
    options = enum.auto()
    delete = enum.auto()
    head = enum.auto()

    def has_request_body_support(self) -> bool:
        cls = self.__class__
        return self in (cls.post, cls.put, cls.patch)
