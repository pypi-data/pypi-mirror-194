# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.5270
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class CreateRelationshipRequest(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'source_entity_id': 'dict(str, str)',
        'target_entity_id': 'dict(str, str)',
        'effective_from': 'str',
        'effective_until': 'str'
    }

    attribute_map = {
        'source_entity_id': 'sourceEntityId',
        'target_entity_id': 'targetEntityId',
        'effective_from': 'effectiveFrom',
        'effective_until': 'effectiveUntil'
    }

    required_map = {
        'source_entity_id': 'required',
        'target_entity_id': 'required',
        'effective_from': 'optional',
        'effective_until': 'optional'
    }

    def __init__(self, source_entity_id=None, target_entity_id=None, effective_from=None, effective_until=None, local_vars_configuration=None):  # noqa: E501
        """CreateRelationshipRequest - a model defined in OpenAPI"
        
        :param source_entity_id:  The identifier of the source entity. (required)
        :type source_entity_id: dict(str, str)
        :param target_entity_id:  The identifier of the target entity. (required)
        :type target_entity_id: dict(str, str)
        :param effective_from:  The effective date of the relationship to be created
        :type effective_from: str
        :param effective_until:  The effective datetime until which the relationship is valid. If not supplied this will be valid indefinitely.
        :type effective_until: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._source_entity_id = None
        self._target_entity_id = None
        self._effective_from = None
        self._effective_until = None
        self.discriminator = None

        self.source_entity_id = source_entity_id
        self.target_entity_id = target_entity_id
        self.effective_from = effective_from
        self.effective_until = effective_until

    @property
    def source_entity_id(self):
        """Gets the source_entity_id of this CreateRelationshipRequest.  # noqa: E501

        The identifier of the source entity.  # noqa: E501

        :return: The source_entity_id of this CreateRelationshipRequest.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._source_entity_id

    @source_entity_id.setter
    def source_entity_id(self, source_entity_id):
        """Sets the source_entity_id of this CreateRelationshipRequest.

        The identifier of the source entity.  # noqa: E501

        :param source_entity_id: The source_entity_id of this CreateRelationshipRequest.  # noqa: E501
        :type source_entity_id: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and source_entity_id is None:  # noqa: E501
            raise ValueError("Invalid value for `source_entity_id`, must not be `None`")  # noqa: E501

        self._source_entity_id = source_entity_id

    @property
    def target_entity_id(self):
        """Gets the target_entity_id of this CreateRelationshipRequest.  # noqa: E501

        The identifier of the target entity.  # noqa: E501

        :return: The target_entity_id of this CreateRelationshipRequest.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._target_entity_id

    @target_entity_id.setter
    def target_entity_id(self, target_entity_id):
        """Sets the target_entity_id of this CreateRelationshipRequest.

        The identifier of the target entity.  # noqa: E501

        :param target_entity_id: The target_entity_id of this CreateRelationshipRequest.  # noqa: E501
        :type target_entity_id: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and target_entity_id is None:  # noqa: E501
            raise ValueError("Invalid value for `target_entity_id`, must not be `None`")  # noqa: E501

        self._target_entity_id = target_entity_id

    @property
    def effective_from(self):
        """Gets the effective_from of this CreateRelationshipRequest.  # noqa: E501

        The effective date of the relationship to be created  # noqa: E501

        :return: The effective_from of this CreateRelationshipRequest.  # noqa: E501
        :rtype: str
        """
        return self._effective_from

    @effective_from.setter
    def effective_from(self, effective_from):
        """Sets the effective_from of this CreateRelationshipRequest.

        The effective date of the relationship to be created  # noqa: E501

        :param effective_from: The effective_from of this CreateRelationshipRequest.  # noqa: E501
        :type effective_from: str
        """
        if (self.local_vars_configuration.client_side_validation and
                effective_from is not None and len(effective_from) > 256):
            raise ValueError("Invalid value for `effective_from`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                effective_from is not None and len(effective_from) < 0):
            raise ValueError("Invalid value for `effective_from`, length must be greater than or equal to `0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                effective_from is not None and not re.search(r'^[a-zA-Z0-9\-_\+:\.]+$', effective_from)):  # noqa: E501
            raise ValueError(r"Invalid value for `effective_from`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_\+:\.]+$/`")  # noqa: E501

        self._effective_from = effective_from

    @property
    def effective_until(self):
        """Gets the effective_until of this CreateRelationshipRequest.  # noqa: E501

        The effective datetime until which the relationship is valid. If not supplied this will be valid indefinitely.  # noqa: E501

        :return: The effective_until of this CreateRelationshipRequest.  # noqa: E501
        :rtype: str
        """
        return self._effective_until

    @effective_until.setter
    def effective_until(self, effective_until):
        """Sets the effective_until of this CreateRelationshipRequest.

        The effective datetime until which the relationship is valid. If not supplied this will be valid indefinitely.  # noqa: E501

        :param effective_until: The effective_until of this CreateRelationshipRequest.  # noqa: E501
        :type effective_until: str
        """
        if (self.local_vars_configuration.client_side_validation and
                effective_until is not None and len(effective_until) > 256):
            raise ValueError("Invalid value for `effective_until`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                effective_until is not None and len(effective_until) < 0):
            raise ValueError("Invalid value for `effective_until`, length must be greater than or equal to `0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                effective_until is not None and not re.search(r'^[a-zA-Z0-9\-_\+:\.]+$', effective_until)):  # noqa: E501
            raise ValueError(r"Invalid value for `effective_until`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_\+:\.]+$/`")  # noqa: E501

        self._effective_until = effective_until

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateRelationshipRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateRelationshipRequest):
            return True

        return self.to_dict() != other.to_dict()
