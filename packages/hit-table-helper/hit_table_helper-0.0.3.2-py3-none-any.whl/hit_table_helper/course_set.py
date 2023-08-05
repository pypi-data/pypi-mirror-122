# -*- coding: utf-8 -*-
import copy
import re
from collections import Iterable
from json import JSONDecodeError

import pandas as pd

from hit_table_helper import constants
from hit_table_helper import hit_api_io
from hit_table_helper.course_mask import CourseMask


class CourseSet:
    cols = ['上课地点', '教师', '课程名', '周次', '上课时间', '星期']

    def __init__(self, courses, week=constants.default_week):
        """

        :param courses:
        :param week:
        """
        if not isinstance(courses, pd.DataFrame):
            courses = self.__week_courses_to_df(courses)
        self.__course_table = courses
        self.__course_table.drop_duplicates(inplace=True)
        self.__week = week

    @property
    def course_table(self):
        return self.__course_table

    @property
    def mask(self):
        return CourseMask.fromCourseSet(self)

    @staticmethod
    def __week_courses_to_df(interest) -> pd.DataFrame:
        """

        :param interest:
        :return:
        """
        res = pd.DataFrame(interest)
        col = ['上课地点', '教师', '课程名', '周次', '_', '上课时间', '星期', '__']
        try:
            res.columns = col
        except ValueError:
            res = pd.DataFrame(columns=col)
        res.drop(columns='_', inplace=True)
        res.drop(columns='__', inplace=True)
        return res

    @staticmethod
    def fromIteratorSearch(week: int = constants.default_week, course_name: str = None, it=None):
        """

        :param week:
        :param course_name:
        :param it:
        :return:
        """
        if it is None:
            def _generate_id():
                prefix = '120L'
                suffix = '01'
                for i in range(1, 5):
                    for j in range(1, 20):
                        yield prefix + str(i).zfill(2) + str(j).zfill(2) + suffix

            it = _generate_id()
        res = []
        for iter_result in hit_api_io.from_iterable(it, week):
            try:
                courses = iter_result.json()['module']['data']
                for course in courses:
                    name = str(course['kcmc'])
                    if course_name is None or name.find(course_name) != -1:
                        res.append(course)
            except JSONDecodeError:
                continue
                # 可能出现了本不应该出现的学号，应该跳过
        return CourseSet(res, week)

    def fromOtherSet(self, other):
        """

        :param other:
        :return:
        """
        if not isinstance(other, CourseSet):
            if isinstance(other, str):
                other_set = CourseSet.fromPerson(other, self.__week)
            elif isinstance(other, Iterable):
                other_set = CourseSet.fromIteratorSearch(self.__week, None, other)
            else:
                raise ValueError("Cannot subtract from this")
        else:
            other_set = other
        return other_set

    @staticmethod
    def fromPerson(hit_id, week: int = constants.default_week):
        return CourseSet.fromIteratorSearch(week, it=[hit_id])

    @staticmethod
    def fromPickle(io, week: int = constants.default_week):
        """

        :return:
        """
        data = pd.read_pickle(io)
        return CourseSet(data, week)

    @classmethod
    def fromEmpty(cls):
        return CourseSet(pd.DataFrame(columns=cls.cols))

    def toPickle(self, io):
        self.__course_table.to_pickle(io)

    def filterFromMask(self, mask: CourseMask, inplace=True):
        del_indexes = []
        if inplace:
            t = self.__course_table
        else:
            t = copy.deepcopy(self.__course_table)
        for index, course in self.__course_table.iterrows():
            if not mask.checkCourse(course):
                del_indexes.append(index)
        self.__course_table.drop(index=del_indexes, inplace=True)
        if not inplace:
            return CourseSet(t, self.__week)
        else:
            return self

    def toExcel(self, io):
        """

        :param io:
        :return:
        """
        self.__course_table.to_excel(io, index=False)

    @classmethod
    def fromExcel(cls, io):
        courses = pd.read_excel(io)
        return cls(courses)

    def filterFromStr(self, r, inplace=True):
        pattern = re.compile(r)
        indexes = []
        for index, course in self.__course_table.iterrows():
            indexes.append(index) if pattern.match(course['课程名']) else None
        if inplace:
            self.__course_table = self.__course_table.loc[indexes]
            return self
        else:
            p = copy.deepcopy(self.__course_table.loc[indexes])
            return CourseSet(p, self.__week)

    def __and__(self, other):
        """

        :param other:
        :return:
        """
        other_set = self.fromOtherSet(other)
        other_mask = CourseMask.fromCourseSet(other_set)
        return self.filterFromMask(other_mask, inplace=False)

    def __sub__(self, other):
        other_set = self.fromOtherSet(other)
        other_mask = CourseMask.fromCourseSet(other_set)
        return self.filterFromMask(~other_mask, inplace=False)

    def __str__(self):
        return str(self.__course_table)

    def __add__(self, other):
        other_set = self.fromOtherSet(other)
        return CourseSet(self.course_table.append(other_set.course_table, ignore_index=True))
