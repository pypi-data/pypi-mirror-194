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


class GlossaryUpdateParameters(object):
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
        'name': 'str',
        'project_ids': 'str',
        'space_ids': 'list[str]'
    }

    attribute_map = {
        'name': 'name',
        'project_ids': 'project_ids',
        'space_ids': 'space_ids'
    }

    def __init__(self, name=None, project_ids=None, space_ids=None, local_vars_configuration=None):  # noqa: E501
        """GlossaryUpdateParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._project_ids = None
        self._space_ids = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if project_ids is not None:
            self.project_ids = project_ids
        if space_ids is not None:
            self.space_ids = space_ids

    @property
    def name(self):
        """Gets the name of this GlossaryUpdateParameters.  # noqa: E501

        Name of the glossary  # noqa: E501

        :return: The name of this GlossaryUpdateParameters.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GlossaryUpdateParameters.

        Name of the glossary  # noqa: E501

        :param name: The name of this GlossaryUpdateParameters.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def project_ids(self):
        """Gets the project_ids of this GlossaryUpdateParameters.  # noqa: E501

        List of project ids the glossary should be assigned to.  # noqa: E501

        :return: The project_ids of this GlossaryUpdateParameters.  # noqa: E501
        :rtype: str
        """
        return self._project_ids

    @project_ids.setter
    def project_ids(self, project_ids):
        """Sets the project_ids of this GlossaryUpdateParameters.

        List of project ids the glossary should be assigned to.  # noqa: E501

        :param project_ids: The project_ids of this GlossaryUpdateParameters.  # noqa: E501
        :type: str
        """

        self._project_ids = project_ids

    @property
    def space_ids(self):
        """Gets the space_ids of this GlossaryUpdateParameters.  # noqa: E501

        List of space ids the glossary should be assigned to.  # noqa: E501

        :return: The space_ids of this GlossaryUpdateParameters.  # noqa: E501
        :rtype: list[str]
        """
        return self._space_ids

    @space_ids.setter
    def space_ids(self, space_ids):
        """Sets the space_ids of this GlossaryUpdateParameters.

        List of space ids the glossary should be assigned to.  # noqa: E501

        :param space_ids: The space_ids of this GlossaryUpdateParameters.  # noqa: E501
        :type: list[str]
        """

        self._space_ids = space_ids

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
        if not isinstance(other, GlossaryUpdateParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GlossaryUpdateParameters):
            return True

        return self.to_dict() != other.to_dict()
