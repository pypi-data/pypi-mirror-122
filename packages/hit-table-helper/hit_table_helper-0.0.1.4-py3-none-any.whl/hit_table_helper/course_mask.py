# -*- coding: utf-8 -*-
import numpy
import numpy as np


class CourseMask:

    def __init__(self, d=0):
        self.__mask = numpy.int64(d)

    @staticmethod
    def _timeToNum(time: str):
        return int(time[1:2]) // 2

    @staticmethod
    def _mapTime(a, b):
        return int((a - 1) * 6 + b)

    @staticmethod
    def _maskPositionFrom(weekday, time):
        if isinstance(weekday, str):
            weekday = int(weekday)
        if isinstance(time, str):
            time = CourseMask._timeToNum(time)
        return CourseMask._mapTime(weekday, time)

    @staticmethod
    def _courseToNum(course):
        time = course['上课时间']
        weekday = course['星期']
        return CourseMask._maskPositionFrom(weekday, time)

    @staticmethod
    def fromCourseSet(s):
        res = CourseMask()
        for _, course in s.course_table.iterrows():
            res.setCourseOccupied(course)
        return res

    def setCourseOccupied(self, course):
        self.__mask |= (1 << CourseMask._courseToNum(course))

    def __str__(self):
        s = np.zeros((6, 7))
        for i in range(1, 8):
            for j in range(0, 6):
                if self.__mask & (1 << CourseMask._mapTime(i, j)):
                    s[j][i - 1] = 1
        return str(s)

    def checkCourse(self, course):
        return bool(self.__mask & (1 << CourseMask._courseToNum(course)))

    def __or__(self, other):
        return CourseMask(self.__mask | other.__mask)

    def __and__(self, other):
        return CourseMask(self.__mask & other.__mask)

    def __xor__(self, other):
        return CourseMask(self.__mask ^ other.__mask)

    def __invert__(self):
        return CourseMask(~self.__mask)
