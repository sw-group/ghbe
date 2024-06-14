# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.comment_author import CommentAuthor  # noqa: F401,E501
from swagger_server import util


class Comment(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, author: CommentAuthor=None, message: str=None, created_at: datetime=None, updated_at: datetime=None):  # noqa: E501
        """Comment - a model defined in Swagger

        :param author: The author of this Comment.  # noqa: E501
        :type author: CommentAuthor
        :param message: The message of this Comment.  # noqa: E501
        :type message: str
        :param created_at: The created_at of this Comment.  # noqa: E501
        :type created_at: datetime
        :param updated_at: The updated_at of this Comment.  # noqa: E501
        :type updated_at: datetime
        """
        self.swagger_types = {
            'author': CommentAuthor,
            'message': str,
            'created_at': datetime,
            'updated_at': datetime
        }

        self.attribute_map = {
            'author': 'author',
            'message': 'message',
            'created_at': 'created_at',
            'updated_at': 'updated_at'
        }
        self._author = author
        self._message = message
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def from_dict(cls, dikt) -> 'Comment':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Comment of this Comment.  # noqa: E501
        :rtype: Comment
        """
        return util.deserialize_model(dikt, cls)

    @property
    def author(self) -> CommentAuthor:
        """Gets the author of this Comment.


        :return: The author of this Comment.
        :rtype: CommentAuthor
        """
        return self._author

    @author.setter
    def author(self, author: CommentAuthor):
        """Sets the author of this Comment.


        :param author: The author of this Comment.
        :type author: CommentAuthor
        """

        self._author = author

    @property
    def message(self) -> str:
        """Gets the message of this Comment.


        :return: The message of this Comment.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this Comment.


        :param message: The message of this Comment.
        :type message: str
        """

        self._message = message

    @property
    def created_at(self) -> datetime:
        """Gets the created_at of this Comment.


        :return: The created_at of this Comment.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        """Sets the created_at of this Comment.


        :param created_at: The created_at of this Comment.
        :type created_at: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self) -> datetime:
        """Gets the updated_at of this Comment.


        :return: The updated_at of this Comment.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        """Sets the updated_at of this Comment.


        :param updated_at: The updated_at of this Comment.
        :type updated_at: datetime
        """

        self._updated_at = updated_at