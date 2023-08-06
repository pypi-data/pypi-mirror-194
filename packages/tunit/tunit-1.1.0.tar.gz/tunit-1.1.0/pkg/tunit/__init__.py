#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from tunit.tunit import *

__version__ = '1.1.0'

Nanoseconds = TimeUnit.UnitType(name='Nanoseconds', symbol='ns', conversionFactor=1)
Microseconds = TimeUnit.UnitType(name='Microseconds', symbol='us', conversionFactor=(1_000 * Nanoseconds.conversionFactor))
Milliseconds = TimeUnit.UnitType(name='Milliseconds', symbol='ms', conversionFactor=(1_000 * Microseconds.conversionFactor))
Seconds = TimeUnit.UnitType(name='Seconds', symbol='s', conversionFactor=(1_000 * Milliseconds.conversionFactor))
Minutes = TimeUnit.UnitType(name='Minutes', symbol='m', conversionFactor=(60 * Seconds.conversionFactor))
Hours = TimeUnit.UnitType(name='Hours', symbol='h', conversionFactor=(60 * Minutes.conversionFactor))
Days = TimeUnit.UnitType(name='Days', symbol='d', conversionFactor=(24 * Hours.conversionFactor))
Weeks = TimeUnit.UnitType(name='Weeks', symbol='w', conversionFactor=(7 * Days.conversionFactor))
