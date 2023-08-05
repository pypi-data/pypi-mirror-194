#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from dataclasses import dataclass
from threading import RLock
from typing import Optional, Union, Any, Generic, TypeVar

from dataclasses_json import dataclass_json, Undefined
from . import Singleton

T = TypeVar("T")


class EntityType(Generic[T]):
    """
    All entities need to inherit the entire class.
    """

    @classmethod
    def init(cls: T):
        """
        get entity instance.
        """
        return _PropertiesManager().pull(cls, None)


class _PropertiesManager(metaclass=Singleton):
    __lock = RLock()

    def __init__(self):
        self.__cache = {}

    @property
    def cache(self) -> dict:
        return self.__cache

    def push(self, cls: T, instance: T):
        with self.__lock:
            self.__cache[cls] = instance

    def pull(self, cls: T, default: Any = None) -> T:
        with self.__lock:
            instance = self.__cache.get(cls)
            if instance:
                return instance
            return default


def Entity(init=True, repr=True, eq=True, order=False,
           unsafe_hash=False, frozen=False, match_args=True,
           kw_only=False, slots=False, letter_case=None,
           undefined: Optional[Union[str, Undefined]] = None):
    """
    Tag entity classes.

    If init is true, an __init__() method is added to the class. If
    repr is true, a __repr__() method is added. If order is true, rich
    comparison dunder methods are added. If unsafe_hash is true, a
    __hash__() method function is added. If frozen is true, fields may
    not be assigned to after instance creation. If match_args is true,
    the __match_args__ tuple is added. If kw_only is true, then by
    default all fields are keyword-only. If slots is true, an
    __slots__ attribute is added.

    Usage:
        @Entry()
        class Student(EntityType):
            name: str
            age: int
    """

    def __wrapper(cls):
        return dataclass_json(dataclass(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash,
                                        frozen=frozen, match_args=match_args, kw_only=kw_only, slots=slots),
                              letter_case=letter_case, undefined=undefined)

    return __wrapper


def Properties(path, coding: str = "utf-8"):
    """
    Ingress entity tags that automatically assemble attribute values.
    !!!!!!!Warning!!!!!!!
    Validation is not supported for properties.
    :param path:  file path
    :param coding:  file encoding
    Usage:
        @Entry()  # Tag sub-property type
        class Student(EntityType):
            name: str
            age: int

        @Properties("properties.json")  # property content file path.
        @Entry()  # Tag property object.
        class Class(EntityType):
            students: list[Student]
            teacher: str

        #  properties.json file content
        {"teacher": "Alice", "students": [{"name": "Tom", "age": 20}]}

        c: Class = Class.init()  # Entity create by init method.
        print(c.teacher)  # Alice
        print(c.students)  # [Student(name="Tom", age=20)]
        print(c.students[0].name)  # Tome
    """

    def __inner(cls):
        with open(path, "r", encoding=coding) as f:
            data = json.load(f)
            instance = cls.from_dict(data)
            _PropertiesManager().push(cls, instance)
        return cls

    return __inner


__all__ = ["Entity", "Properties"]
