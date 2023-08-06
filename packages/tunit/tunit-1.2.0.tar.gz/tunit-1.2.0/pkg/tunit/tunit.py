#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from __future__ import annotations  # TODO: Remove when support dropped for: Python < 3.10

from dataclasses import dataclass
from enum import Enum, auto
from functools import total_ordering
from typing import Callable, Optional, Tuple, Type, Union

try:  # TODO: Remove when support dropped for: Python < 3.8
    from typing import get_args
except ImportError:
    def get_args(union: Union) -> Tuple[Type]:
        return union.__args__


class TimeUnitTypeError(TypeError):
    pass


@total_ordering
class TimeUnit:

    class _SupportedValueType:
        def __get__(self, instance, owner) -> Type[Union]:
            return Union[int, float, TimeUnit]

    class _ArithmeticOperation(Enum):
        Addition = auto()
        Subtraction = auto()
        Multiplication = auto()
        Division = auto()

    @dataclass(frozen=True)
    class _ArithmeticDetails:
        symbol: str
        name: str
        operation: Callable[[int, float], float]

    SupportedValue = _SupportedValueType()

    _ARITHMETIC = {
        _ArithmeticOperation.Addition: _ArithmeticDetails(symbol='+', name='addition', operation=lambda value, otherValue: value + otherValue),
        _ArithmeticOperation.Subtraction: _ArithmeticDetails(symbol='-', name='subtraction', operation=lambda value, otherValue: value - otherValue),
        _ArithmeticOperation.Multiplication: _ArithmeticDetails(symbol='*', name='multiplication', operation=lambda value, otherValue: value * otherValue),
        _ArithmeticOperation.Division: _ArithmeticDetails(symbol='/', name='division', operation=lambda value, otherValue: value / otherValue),
    }

    @dataclass(frozen=True)
    class UnitType:
        name: str
        symbol: str
        conversionFactor: int

        def __call__(self, value: Optional[TimeUnit.SupportedValue] = None) -> TimeUnit:
            return TimeUnit(unitType=self, value=value)

        def fromRawUnit(self, unit: TimeUnit.UnitType, value: Union[int, float]) -> TimeUnit:
            if unit.conversionFactor <= self.conversionFactor:
                return self(value=unit(value=value))

            multiplier = unit.conversionFactor / self.conversionFactor
            return self(value=(multiplier * value))

    def __init__(
        self,
        unitType: UnitType,
        value: Optional[SupportedValue] = None
    ) -> None:
        value = value if value is not None else 0

        self._unitType: TimeUnit.UnitType = unitType
        self._value: int = self._convertValue(value)

    def __str__(self) -> str:
        return f"{self._value}[{self.symbol}]"

    def __repr__(self) -> str:
        return f"{self.name}({self._value})"

    def __int__(self) -> int:
        return self._value

    def __float__(self) -> float:
        return float(self._value)

    def __add__(self, other: SupportedValue) -> TimeUnit:
        return self._arithmetic(operation=TimeUnit._ArithmeticOperation.Addition, other=other)

    def __sub__(self, other: SupportedValue) -> TimeUnit:
        return self._arithmetic(operation=TimeUnit._ArithmeticOperation.Subtraction, other=other)

    def __mul__(self, other: SupportedValue) -> TimeUnit:
        return self._arithmetic(operation=TimeUnit._ArithmeticOperation.Multiplication, other=other)

    def __truediv__(self, other: SupportedValue) -> TimeUnit:
        return self._arithmetic(operation=TimeUnit._ArithmeticOperation.Division, other=other)

    def __neg__(self) -> TimeUnit:
        return self._unitType(value=(-self._value))

    def __eq__(self, other: SupportedValue) -> bool:
        return self._value == self._convertValue(other)

    def __gt__(self, other: SupportedValue) -> bool:
        return self._value > self._convertValue(other)

    @property
    def name(self) -> str:
        return self._unitType.name

    @property
    def symbol(self) -> str:
        return self._unitType.symbol

    @property
    def conversionFactor(self) -> int:
        return self._unitType.conversionFactor

    @property
    def value(self) -> int:
        return self._value

    def toRawUnit(self, unit: TimeUnit.UnitType) -> float:
        if unit.conversionFactor <= self._unitType.conversionFactor:
            return float(unit(self))
        divider = unit.conversionFactor / self._unitType.conversionFactor
        return self._value / divider

    def _arithmetic(self, operation: _ArithmeticOperation, other: SupportedValue) -> TimeUnit:
        operationDetails = TimeUnit._ARITHMETIC[operation]

        if not self._isSupportedValueType(other=other):
            raise TimeUnitTypeError(f"Cannot perform {operationDetails.name} of types '{self.name}' and '{type(other).__name__}'!")

        if isinstance(other, TimeUnit) and self._unitType != other._unitType:
            raise TimeUnitTypeError(f"Cannot perform {operationDetails.name} between different time units! ({self.name} {operationDetails.symbol} {other.name})")

        otherValue = self._convertValue(other, skipValidation=True)
        return self._unitType(value=operationDetails.operation(self._value, otherValue))

    def _convertValue(self, other: SupportedValue, skipValidation: bool = False) -> int:
        if not skipValidation and not self._isSupportedValueType(other=other):
            raise TimeUnitTypeError(f"Cannot create '{self.name}' from '{type(other).__name__}'!")

        rawValue = other._value * other.conversionFactor / self.conversionFactor if isinstance(other, TimeUnit) \
            else other
        return int(rawValue)

    def _isSupportedValueType(self, other: SupportedValue) -> bool:
        return isinstance(other, get_args(self.SupportedValue))
