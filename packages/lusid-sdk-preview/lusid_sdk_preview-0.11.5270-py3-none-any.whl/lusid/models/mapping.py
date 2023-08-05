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


class Mapping(object):
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
        'scope': 'str',
        'code': 'str',
        'name': 'str',
        'reconciliation_type': 'str',
        'rules': 'list[MappingRule]'
    }

    attribute_map = {
        'scope': 'scope',
        'code': 'code',
        'name': 'name',
        'reconciliation_type': 'reconciliationType',
        'rules': 'rules'
    }

    required_map = {
        'scope': 'required',
        'code': 'required',
        'name': 'required',
        'reconciliation_type': 'required',
        'rules': 'optional'
    }

    def __init__(self, scope=None, code=None, name=None, reconciliation_type=None, rules=None, local_vars_configuration=None):  # noqa: E501
        """Mapping - a model defined in OpenAPI"
        
        :param scope:  The scope for this mapping. (required)
        :type scope: str
        :param code:  The code for this mapping. (required)
        :type code: str
        :param name:  The mapping name (required)
        :type name: str
        :param reconciliation_type:  What type of reconciliation this mapping is for (required)
        :type reconciliation_type: str
        :param rules:  The rules in this mapping, keyed by the left field/property name
        :type rules: list[lusid.MappingRule]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._scope = None
        self._code = None
        self._name = None
        self._reconciliation_type = None
        self._rules = None
        self.discriminator = None

        self.scope = scope
        self.code = code
        self.name = name
        self.reconciliation_type = reconciliation_type
        self.rules = rules

    @property
    def scope(self):
        """Gets the scope of this Mapping.  # noqa: E501

        The scope for this mapping.  # noqa: E501

        :return: The scope of this Mapping.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this Mapping.

        The scope for this mapping.  # noqa: E501

        :param scope: The scope of this Mapping.  # noqa: E501
        :type scope: str
        """
        if self.local_vars_configuration.client_side_validation and scope is None:  # noqa: E501
            raise ValueError("Invalid value for `scope`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                scope is not None and len(scope) > 64):
            raise ValueError("Invalid value for `scope`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                scope is not None and len(scope) < 1):
            raise ValueError("Invalid value for `scope`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                scope is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', scope)):  # noqa: E501
            raise ValueError(r"Invalid value for `scope`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._scope = scope

    @property
    def code(self):
        """Gets the code of this Mapping.  # noqa: E501

        The code for this mapping.  # noqa: E501

        :return: The code of this Mapping.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this Mapping.

        The code for this mapping.  # noqa: E501

        :param code: The code of this Mapping.  # noqa: E501
        :type code: str
        """
        if self.local_vars_configuration.client_side_validation and code is None:  # noqa: E501
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) > 64):
            raise ValueError("Invalid value for `code`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) < 1):
            raise ValueError("Invalid value for `code`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', code)):  # noqa: E501
            raise ValueError(r"Invalid value for `code`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._code = code

    @property
    def name(self):
        """Gets the name of this Mapping.  # noqa: E501

        The mapping name  # noqa: E501

        :return: The name of this Mapping.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Mapping.

        The mapping name  # noqa: E501

        :param name: The name of this Mapping.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and not re.search(r'^[\s\S]*$', name)):  # noqa: E501
            raise ValueError(r"Invalid value for `name`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._name = name

    @property
    def reconciliation_type(self):
        """Gets the reconciliation_type of this Mapping.  # noqa: E501

        What type of reconciliation this mapping is for  # noqa: E501

        :return: The reconciliation_type of this Mapping.  # noqa: E501
        :rtype: str
        """
        return self._reconciliation_type

    @reconciliation_type.setter
    def reconciliation_type(self, reconciliation_type):
        """Sets the reconciliation_type of this Mapping.

        What type of reconciliation this mapping is for  # noqa: E501

        :param reconciliation_type: The reconciliation_type of this Mapping.  # noqa: E501
        :type reconciliation_type: str
        """
        if self.local_vars_configuration.client_side_validation and reconciliation_type is None:  # noqa: E501
            raise ValueError("Invalid value for `reconciliation_type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                reconciliation_type is not None and len(reconciliation_type) < 1):
            raise ValueError("Invalid value for `reconciliation_type`, length must be greater than or equal to `1`")  # noqa: E501

        self._reconciliation_type = reconciliation_type

    @property
    def rules(self):
        """Gets the rules of this Mapping.  # noqa: E501

        The rules in this mapping, keyed by the left field/property name  # noqa: E501

        :return: The rules of this Mapping.  # noqa: E501
        :rtype: list[lusid.MappingRule]
        """
        return self._rules

    @rules.setter
    def rules(self, rules):
        """Sets the rules of this Mapping.

        The rules in this mapping, keyed by the left field/property name  # noqa: E501

        :param rules: The rules of this Mapping.  # noqa: E501
        :type rules: list[lusid.MappingRule]
        """

        self._rules = rules

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
        if not isinstance(other, Mapping):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Mapping):
            return True

        return self.to_dict() != other.to_dict()
