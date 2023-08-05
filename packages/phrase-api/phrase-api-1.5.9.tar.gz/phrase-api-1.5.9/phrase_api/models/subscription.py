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


class Subscription(object):
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
        'is_current': 'bool',
        'trial_expired': 'bool'
    }

    attribute_map = {
        'is_current': 'is_current',
        'trial_expired': 'trial_expired'
    }

    def __init__(self, is_current=None, trial_expired=None, local_vars_configuration=None):  # noqa: E501
        """Subscription - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._is_current = None
        self._trial_expired = None
        self.discriminator = None

        if is_current is not None:
            self.is_current = is_current
        if trial_expired is not None:
            self.trial_expired = trial_expired

    @property
    def is_current(self):
        """Gets the is_current of this Subscription.  # noqa: E501


        :return: The is_current of this Subscription.  # noqa: E501
        :rtype: bool
        """
        return self._is_current

    @is_current.setter
    def is_current(self, is_current):
        """Sets the is_current of this Subscription.


        :param is_current: The is_current of this Subscription.  # noqa: E501
        :type: bool
        """

        self._is_current = is_current

    @property
    def trial_expired(self):
        """Gets the trial_expired of this Subscription.  # noqa: E501


        :return: The trial_expired of this Subscription.  # noqa: E501
        :rtype: bool
        """
        return self._trial_expired

    @trial_expired.setter
    def trial_expired(self, trial_expired):
        """Sets the trial_expired of this Subscription.


        :param trial_expired: The trial_expired of this Subscription.  # noqa: E501
        :type: bool
        """

        self._trial_expired = trial_expired

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
        if not isinstance(other, Subscription):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Subscription):
            return True

        return self.to_dict() != other.to_dict()
