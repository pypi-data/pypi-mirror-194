#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from typing import Iterable

from ..char import String
from ..classes import StaticClass
from ..exceptions import raise_exception

_empty = "\\s|\\u00a0|\\u0020|\\u3000"

_spec_all_re = re.compile(f"({_empty})*", re.U)
_spec_start_end_re = re.compile(f"^({_empty})*|({_empty})*$", re.U)
_spec_start = re.compile(f"^({_empty})*", re.U)
_spec_end = re.compile(f"({_empty})*$", re.U)


class StringUtils(metaclass=StaticClass):
    """
    string tools
    """

    @staticmethod
    def equals_trip(left: str, right: str) -> bool:
        """
        After removing the first and last white space characters, it is judged
        """
        if not issubclass(type(left), str) or not issubclass(type(right), str):
            return False
        return StringUtils.trip(left) == StringUtils.trip(right)

    @staticmethod
    def equals(left: str, right: str) -> bool:
        """
        Directly judge whether it is equal or not
        :param left:
        :param right:
        :return:
        """
        if not issubclass(type(left), str) or not issubclass(type(right), str):
            return False
        return left == right

    @staticmethod
    def equals_ignore_case(left: str, right: str) -> bool:
        """
        Determine whether it is equal, ignore case.
        """
        if not issubclass(type(left), str) or not isinstance(type(right), str):
            return False
        return left.upper() == right.upper()

    @staticmethod
    def equals_ignore_case_trip(left: str, right: str) -> bool:
        """
        Determine whether it is equal, ignore case and trip.
        """
        if not issubclass(type(left), str) or not isinstance(type(right), str):
            return False
        return StringUtils.trip(left.upper()) == StringUtils.trip(right.upper())

    @staticmethod
    def equals_any(src: str, targets: str) -> bool:
        """
        Any element of the original string and the target string number array are equal.
        """
        if not issubclass(type(src), str):
            return False
        for s in targets:
            if not issubclass(type(s), str):
                return False
            if src == s:
                return True
        return False

    @staticmethod
    def equals_all(src: str, targets: str) -> bool:
        """
        All elements of the original string and target string number arrays are equal.
        """
        if not issubclass(type(src), str):
            return False
        for s in targets:
            if not issubclass(type(s), str):
                return False
            if src != s:
                return False
        return True

    @staticmethod
    def equals_any_trip(src: str, targets: str) -> bool:
        """
        Any element of the original string and the target string number array are equal.
        will trip.
        """
        if not issubclass(type(src), str):
            return False
        for s in targets:
            if not issubclass(type(s), str):
                return False
            if StringUtils.trip(src) == StringUtils.trip(s):
                return True
        return False

    @staticmethod
    def equals_all_trip(src: str, targets: str) -> bool:
        """
        All elements of the original string and target string number arrays are equal.
        will trip.
        """
        if not issubclass(type(src), str):
            return False
        for s in targets:
            if not issubclass(type(s), str):
                return False
            if StringUtils.trip(src) != StringUtils.trip(s):
                return False
        return True

    @staticmethod
    def equals_any_ignore_case(src: str, targets: str) -> bool:
        """
        Any element of the original string and the target string number array are equal.
        ignore case.
        """
        if not issubclass(type(src), str):
            return False
        for s in targets:
            if not issubclass(type(s), str):
                return False
            if src.upper() == s.upper():
                return True
        return False

    @staticmethod
    def equals_all_ignore_case(src: str, targets: str) -> bool:
        """
        All elements of the original string and target string number arrays are equal.
        ignore case.
        """
        if not issubclass(type(src), str):
            return False
        for s in targets:
            if not issubclass(type(s), str):
                return False
            if src.upper() != s.upper():
                return False
        return True

    @staticmethod
    def equals_any_trip_ignore_case(src: str, targets: str) -> bool:
        """
        Any element of the original string and the target string number array are equal.
        ignore case and trip.
        """
        if not issubclass(type(src), str):
            return False
        for s in targets:
            if not issubclass(type(s), str):
                return False
            if StringUtils.trip(src.upper()) == StringUtils.trip(s.upper()):
                return True
        return False

    @staticmethod
    def equals_all_trip_ignore_case(src: str, targets: str) -> bool:
        """
        All elements of the original string and target string number arrays are equal.
        ignore case and trip.
        """
        if not issubclass(type(src), str):
            return False
        for s in targets:
            if not issubclass(type(s), str):
                return False
            if StringUtils.trip(src.upper()) != StringUtils.trip(s.upper()):
                return False
        return True

    @staticmethod
    def trip_start(value: str) -> String:
        if isinstance(value, str):
            return String(_spec_start.sub("", value))
        raise_exception(TypeError(f"expect is 'str', got a {type(value).__name__}"))

    @staticmethod
    def trip_end(value: str) -> String:
        if isinstance(value, str):
            return String(_spec_end.sub("", value))
        raise_exception(TypeError(f"expect is 'str', got a {type(value).__name__}"))

    @staticmethod
    def trip_all(value: str) -> String:
        """
        Clear all whitespace characters
        """
        if isinstance(value, str):
            return String(_spec_all_re.sub("", value))
        raise_exception(TypeError(f"expect is 'str', got a {type(value).__name__}"))

    @staticmethod
    def trip(value: str or bytes) -> String:
        """
        Clears the leading and trailing whitespace characters
        """
        if isinstance(value, str):
            return String(_spec_start_end_re.sub("", value))
        raise_exception(TypeError(f"expect is 'str', got a {type(value).__name__}"))

    @staticmethod
    def is_empty(value: str) -> bool:
        """
        Judge whether the string is empty
        """
        if issubclass(type(value), str):
            return len(value) == 0
        return False

    @staticmethod
    def is_not_empty(value: str) -> bool:
        """
        Judge whether the string is not empty
        """
        return not StringUtils.is_empty(value)

    @staticmethod
    def is_any_Empty(*strings):
        """
        Validates multiple strings at the same time, and returns True as long as one string is empty
        Usage:
            StringUtils.is_any_Empty("a", "b", "") => True
        """
        for s in strings:
            if StringUtils.is_empty(s):
                return True
        return False

    @staticmethod
    def is_all_Empty(*strings):
        """
        Validates multiple strings at the same time, and returns True as long as all string is empty
        Usage:
            StringUtils.is_any_Empty("a", "b", "") => True
        """
        for s in strings:
            if StringUtils.is_not_empty(s):
                return False
        return True

    @staticmethod
    def is_no_Empty(*strings):
        """
        Validates multiple strings at the same time, and returns True as long as all string is not empty
        Usage:
            StringUtils.is_any_Empty("a", "b", "") => True
        """
        for s in strings:
            if StringUtils.is_empty(s):
                return False
        return True

    @staticmethod
    def is_black(value: str) -> bool:
        """
        string is black, the first and last spaces will be removed before judgment
        """
        if isinstance(value, str):
            return len(value) == 0 or len(StringUtils.trip(value)) == 0
        return False

    @staticmethod
    def is_not_black(value: str) -> bool:
        """
        string isn't black,the first and last spaces will be removed before judgment
        """
        return not StringUtils.is_black(value)

    @staticmethod
    def is_any_Black(*strings):
        """
        Validates multiple strings at the same time, and returns True as long as one string is black
        Usage:
            StringUtils.is_any_Black("a", "b", " ") => True
        """
        for s in strings:
            if StringUtils.is_black(s):
                return True
        return False

    @staticmethod
    def is_all_Black(*strings):
        """
        Validates multiple strings at the same time, and returns True as long as all string is black
        Usage:
            StringUtils.is_any_Black("a", "b", " ") => True
        """
        for s in strings:
            if StringUtils.is_not_black(s):
                return False
        return True

    @staticmethod
    def is_no_Black(*strings):
        """
        Validates multiple strings at the same time, and returns True as long as all string is not black
        Usage:
            StringUtils.is_any_Black("a", "b", " ") => True
        """
        for s in strings:
            if StringUtils.is_black(s):
                return False
        return True

    @staticmethod
    def abbreviate(value, ellipsis_: str = "...", left_index: int = 0, right_index: int = -1) -> String:
        """
        Shorten the string
        """
        length = len(value)
        if left_index > length or right_index > length:
            return value
        if left_index > right_index:
            left_index, right_index = right_index, left_index
        new_value = value[left_index:right_index]
        if left_index > 0:
            new_value = ellipsis_ + new_value
        if right_index > 0:
            new_value += ellipsis_
        return String(new_value)

    @staticmethod
    def contains(src: str, target: str) -> bool:
        """
        src contains target
        """
        if isinstance(src, str) and isinstance(target, str):
            return target in src
        return False

    @staticmethod
    def not_contains(src: str, target: str) -> bool:
        """
        src not contains target
        """
        return not StringUtils.contains(src, target)

    @staticmethod
    def trip_contains(src: str, target: str) -> bool:
        """
        after removing the leading and trailing spaces, determine that src contains target
        """
        if isinstance(src, str) and isinstance(target, str):
            return StringUtils.trip(target) in StringUtils.trip(src)
        return False

    @staticmethod
    def trip_not_contains(src: str, target: str) -> bool:
        """
        after removing the leading and trailing spaces, determine that src not contains target
        """
        return not StringUtils.trip_contains(src, target)

    @staticmethod
    def trip_all_contains(src: str, target: str) -> bool:
        """
        Remove the "space" from anywhere in the string and make sure that src contain the destination string
        :param src: origin string
        :param target: The included string
        """
        if isinstance(src, str) and isinstance(target, str):
            return StringUtils.trip_all(target) in StringUtils.trip_all(src)
        return False

    @staticmethod
    def trip_all_not_contains(src: str, target: str) -> bool:
        """
        Remove the "space" from anywhere in the string and make sure that src does not contain the destination string
        :param src: origin string
        :param target: The included string
        """
        return not StringUtils.trip_all_contains(src, target)

    @staticmethod
    def to_bool(value: str, default: bool = False) -> bool:
        """
        Converts the string bool type to a true bool type.
        :param value: string bool type.
        :param default: If it is not of type string bool, the value returned by default.
        """
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            if value == "True" or value == "true":
                return True
            elif value == "False" or value == "false":
                return False
        return default

    @staticmethod
    def join(iterable: Iterable, sep: str = "") -> String:
        """
        You can receive elements for any type of iteration object for join operations.
        """
        return String(sep.join((str(i) for i in iterable)))

    @staticmethod
    def convert_to_camel(name: str) -> String:
        """snake to camel"""
        return String(re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name))

    @staticmethod
    def convert_to_pascal(name: str) -> String:
        """snake to pascal"""
        char = re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name)
        char_1 = char[:1].upper()
        char_rem = char[1:]
        return String(char_1 + char_rem)

    @staticmethod
    def convert_to_snake(name: str) -> String:
        """camel to snake"""
        if '_' not in name:
            name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
        else:
            raise ValueError(f"'{name}' contain underscores and cannot be converted")
        return String(name.lower())


__all__ = [StringUtils]
