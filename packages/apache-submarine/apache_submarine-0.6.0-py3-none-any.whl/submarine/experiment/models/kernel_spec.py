# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Submarine Experiment API

    The Submarine REST API allows you to create, list, and get experiments. The API is hosted under the /v1/experiment route on the Submarine server. For example, to list experiments on a server hosted at http://localhost:8080, access http://localhost:8080/api/v1/experiment/  # noqa: E501

    The version of the OpenAPI document: 0.6.0
    Contact: dev@submarine.apache.org
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from submarine.experiment.configuration import Configuration


class KernelSpec(object):
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
    openapi_types = {"name": "str", "channels": "list[str]", "dependencies": "list[str]"}

    attribute_map = {"name": "name", "channels": "channels", "dependencies": "dependencies"}

    def __init__(
        self, name=None, channels=None, dependencies=None, local_vars_configuration=None
    ):  # noqa: E501
        """KernelSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._channels = None
        self._dependencies = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if channels is not None:
            self.channels = channels
        if dependencies is not None:
            self.dependencies = dependencies

    @property
    def name(self):
        """Gets the name of this KernelSpec.  # noqa: E501


        :return: The name of this KernelSpec.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this KernelSpec.


        :param name: The name of this KernelSpec.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def channels(self):
        """Gets the channels of this KernelSpec.  # noqa: E501


        :return: The channels of this KernelSpec.  # noqa: E501
        :rtype: list[str]
        """
        return self._channels

    @channels.setter
    def channels(self, channels):
        """Sets the channels of this KernelSpec.


        :param channels: The channels of this KernelSpec.  # noqa: E501
        :type: list[str]
        """

        self._channels = channels

    @property
    def dependencies(self):
        """Gets the dependencies of this KernelSpec.  # noqa: E501


        :return: The dependencies of this KernelSpec.  # noqa: E501
        :rtype: list[str]
        """
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies):
        """Sets the dependencies of this KernelSpec.


        :param dependencies: The dependencies of this KernelSpec.  # noqa: E501
        :type: list[str]
        """

        self._dependencies = dependencies

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
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
        if not isinstance(other, KernelSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, KernelSpec):
            return True

        return self.to_dict() != other.to_dict()
