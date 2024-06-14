# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.map_string_number import MapStringNumber  # noqa: F401,E501
from swagger_server import util


class StatisticsPulls(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, daily_closed_progress: MapStringNumber=None, daily_opened_progress: MapStringNumber=None, merged: int=None):  # noqa: E501
        """StatisticsPulls - a model defined in Swagger

        :param daily_closed_progress: The daily_closed_progress of this StatisticsPulls.  # noqa: E501
        :type daily_closed_progress: MapStringNumber
        :param daily_opened_progress: The daily_opened_progress of this StatisticsPulls.  # noqa: E501
        :type daily_opened_progress: MapStringNumber
        :param merged: The merged of this StatisticsPulls.  # noqa: E501
        :type merged: int
        """
        self.swagger_types = {
            'daily_closed_progress': MapStringNumber,
            'daily_opened_progress': MapStringNumber,
            'merged': int
        }

        self.attribute_map = {
            'daily_closed_progress': 'dailyClosedProgress',
            'daily_opened_progress': 'dailyOpenedProgress',
            'merged': 'merged'
        }
        self._daily_closed_progress = daily_closed_progress
        self._daily_opened_progress = daily_opened_progress
        self._merged = merged

    @classmethod
    def from_dict(cls, dikt) -> 'StatisticsPulls':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Statistics_pulls of this StatisticsPulls.  # noqa: E501
        :rtype: StatisticsPulls
        """
        return util.deserialize_model(dikt, cls)

    @property
    def daily_closed_progress(self) -> MapStringNumber:
        """Gets the daily_closed_progress of this StatisticsPulls.


        :return: The daily_closed_progress of this StatisticsPulls.
        :rtype: MapStringNumber
        """
        return self._daily_closed_progress

    @daily_closed_progress.setter
    def daily_closed_progress(self, daily_closed_progress: MapStringNumber):
        """Sets the daily_closed_progress of this StatisticsPulls.


        :param daily_closed_progress: The daily_closed_progress of this StatisticsPulls.
        :type daily_closed_progress: MapStringNumber
        """

        self._daily_closed_progress = daily_closed_progress

    @property
    def daily_opened_progress(self) -> MapStringNumber:
        """Gets the daily_opened_progress of this StatisticsPulls.


        :return: The daily_opened_progress of this StatisticsPulls.
        :rtype: MapStringNumber
        """
        return self._daily_opened_progress

    @daily_opened_progress.setter
    def daily_opened_progress(self, daily_opened_progress: MapStringNumber):
        """Sets the daily_opened_progress of this StatisticsPulls.


        :param daily_opened_progress: The daily_opened_progress of this StatisticsPulls.
        :type daily_opened_progress: MapStringNumber
        """

        self._daily_opened_progress = daily_opened_progress

    @property
    def merged(self) -> int:
        """Gets the merged of this StatisticsPulls.


        :return: The merged of this StatisticsPulls.
        :rtype: int
        """
        return self._merged

    @merged.setter
    def merged(self, merged: int):
        """Sets the merged of this StatisticsPulls.


        :param merged: The merged of this StatisticsPulls.
        :type merged: int
        """

        self._merged = merged