# coding: utf-8

"""
    Phrase Strings API Reference

    The version of the OpenAPI document: 2.0.0
    Contact: support@phrase.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from phrase_api.configuration import Configuration


class LocaleUserPreview(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'str',
        'username': 'str',
        'name': 'str',
        'role': 'str'
    }

    attribute_map = {
        'id': 'id',
        'username': 'username',
        'name': 'name',
        'role': 'role'
    }

    def __init__(self, id=None, username=None, name=None, role=None, local_vars_configuration=None):  # noqa: E501
        """LocaleUserPreview - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._username = None
        self._name = None
        self._role = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if username is not None:
            self.username = username
        if name is not None:
            self.name = name
        if role is not None:
            self.role = role

    @property
    def id(self):
        """Gets the id of this LocaleUserPreview.  # noqa: E501


        :return: The id of this LocaleUserPreview.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this LocaleUserPreview.


        :param id: The id of this LocaleUserPreview.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def username(self):
        """Gets the username of this LocaleUserPreview.  # noqa: E501


        :return: The username of this LocaleUserPreview.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this LocaleUserPreview.


        :param username: The username of this LocaleUserPreview.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def name(self):
        """Gets the name of this LocaleUserPreview.  # noqa: E501


        :return: The name of this LocaleUserPreview.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LocaleUserPreview.


        :param name: The name of this LocaleUserPreview.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def role(self):
        """Gets the role of this LocaleUserPreview.  # noqa: E501


        :return: The role of this LocaleUserPreview.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this LocaleUserPreview.


        :param role: The role of this LocaleUserPreview.  # noqa: E501
        :type: str
        """

        self._role = role

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, LocaleUserPreview):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LocaleUserPreview):
            return True

        return self.to_dict() != other.to_dict()
