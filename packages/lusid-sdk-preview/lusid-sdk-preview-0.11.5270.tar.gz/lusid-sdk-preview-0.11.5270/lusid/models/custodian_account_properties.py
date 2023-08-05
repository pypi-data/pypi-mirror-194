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


class CustodianAccountProperties(object):
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
        'href': 'str',
        'properties': 'dict(str, ModelProperty)',
        'version': 'Version',
        'links': 'list[Link]'
    }

    attribute_map = {
        'href': 'href',
        'properties': 'properties',
        'version': 'version',
        'links': 'links'
    }

    required_map = {
        'href': 'optional',
        'properties': 'optional',
        'version': 'optional',
        'links': 'optional'
    }

    def __init__(self, href=None, properties=None, version=None, links=None, local_vars_configuration=None):  # noqa: E501
        """CustodianAccountProperties - a model defined in OpenAPI"
        
        :param href:  The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.
        :type href: str
        :param properties:  The Custodian Account properties. These will be from the 'CustodianAccount' domain.
        :type properties: dict[str, lusid.ModelProperty]
        :param version: 
        :type version: lusid.Version
        :param links: 
        :type links: list[lusid.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._href = None
        self._properties = None
        self._version = None
        self._links = None
        self.discriminator = None

        self.href = href
        self.properties = properties
        if version is not None:
            self.version = version
        self.links = links

    @property
    def href(self):
        """Gets the href of this CustodianAccountProperties.  # noqa: E501

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :return: The href of this CustodianAccountProperties.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this CustodianAccountProperties.

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :param href: The href of this CustodianAccountProperties.  # noqa: E501
        :type href: str
        """

        self._href = href

    @property
    def properties(self):
        """Gets the properties of this CustodianAccountProperties.  # noqa: E501

        The Custodian Account properties. These will be from the 'CustodianAccount' domain.  # noqa: E501

        :return: The properties of this CustodianAccountProperties.  # noqa: E501
        :rtype: dict[str, lusid.ModelProperty]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this CustodianAccountProperties.

        The Custodian Account properties. These will be from the 'CustodianAccount' domain.  # noqa: E501

        :param properties: The properties of this CustodianAccountProperties.  # noqa: E501
        :type properties: dict[str, lusid.ModelProperty]
        """

        self._properties = properties

    @property
    def version(self):
        """Gets the version of this CustodianAccountProperties.  # noqa: E501


        :return: The version of this CustodianAccountProperties.  # noqa: E501
        :rtype: lusid.Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this CustodianAccountProperties.


        :param version: The version of this CustodianAccountProperties.  # noqa: E501
        :type version: lusid.Version
        """

        self._version = version

    @property
    def links(self):
        """Gets the links of this CustodianAccountProperties.  # noqa: E501


        :return: The links of this CustodianAccountProperties.  # noqa: E501
        :rtype: list[lusid.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this CustodianAccountProperties.


        :param links: The links of this CustodianAccountProperties.  # noqa: E501
        :type links: list[lusid.Link]
        """

        self._links = links

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
        if not isinstance(other, CustodianAccountProperties):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CustodianAccountProperties):
            return True

        return self.to_dict() != other.to_dict()
