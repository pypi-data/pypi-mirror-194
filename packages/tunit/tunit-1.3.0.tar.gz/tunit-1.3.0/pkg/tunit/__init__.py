#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from tunit.tunit import *

__version__ = '1.3.0'


class Nanoseconds(TimeUnit):
    unitInfo = staticmethod(lambda: TimeUnit.UnitInfo(name='Nanoseconds', symbol='ns', conversionFactor=1))


class Microseconds(TimeUnit):
    unitInfo = staticmethod(lambda: TimeUnit.UnitInfo(name='Microseconds', symbol='us', conversionFactor=(1_000 * Nanoseconds.conversionFactor)))


class Milliseconds(TimeUnit):
    unitInfo = staticmethod(lambda: TimeUnit.UnitInfo(name='Milliseconds', symbol='ms', conversionFactor=(1_000 * Microseconds.conversionFactor)))


class Seconds(TimeUnit):
    unitInfo = staticmethod(lambda: TimeUnit.UnitInfo(name='Seconds', symbol='s', conversionFactor=(1_000 * Milliseconds.conversionFactor)))


class Minutes(TimeUnit):
    unitInfo = staticmethod(lambda: TimeUnit.UnitInfo(name='Minutes', symbol='m', conversionFactor=(60 * Seconds.conversionFactor)))


class Hours(TimeUnit):
    unitInfo = staticmethod(lambda: TimeUnit.UnitInfo(name='Hours', symbol='h', conversionFactor=(60 * Minutes.conversionFactor)))


class Days(TimeUnit):
    unitInfo = staticmethod(lambda: TimeUnit.UnitInfo(name='Days', symbol='d', conversionFactor=(24 * Hours.conversionFactor)))


class Weeks(TimeUnit):
    unitInfo = staticmethod(lambda: TimeUnit.UnitInfo(name='Weeks', symbol='w', conversionFactor=(7 * Days.conversionFactor)))
