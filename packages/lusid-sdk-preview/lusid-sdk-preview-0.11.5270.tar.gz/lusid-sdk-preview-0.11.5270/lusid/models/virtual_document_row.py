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


class VirtualDocumentRow(object):
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
        'row_id': 'dict(str, str)',
        'row_data': 'GroupedResultOfAddressKey'
    }

    attribute_map = {
        'row_id': 'rowId',
        'row_data': 'rowData'
    }

    required_map = {
        'row_id': 'optional',
        'row_data': 'optional'
    }

    def __init__(self, row_id=None, row_data=None, local_vars_configuration=None):  # noqa: E501
        """VirtualDocumentRow - a model defined in OpenAPI"
        
        :param row_id:  The identifier for the row. This is keyed by address keys, and values obtained through applying the data map to the documents.
        :type row_id: dict(str, str)
        :param row_data: 
        :type row_data: lusid.GroupedResultOfAddressKey

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._row_id = None
        self._row_data = None
        self.discriminator = None

        self.row_id = row_id
        if row_data is not None:
            self.row_data = row_data

    @property
    def row_id(self):
        """Gets the row_id of this VirtualDocumentRow.  # noqa: E501

        The identifier for the row. This is keyed by address keys, and values obtained through applying the data map to the documents.  # noqa: E501

        :return: The row_id of this VirtualDocumentRow.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._row_id

    @row_id.setter
    def row_id(self, row_id):
        """Sets the row_id of this VirtualDocumentRow.

        The identifier for the row. This is keyed by address keys, and values obtained through applying the data map to the documents.  # noqa: E501

        :param row_id: The row_id of this VirtualDocumentRow.  # noqa: E501
        :type row_id: dict(str, str)
        """

        self._row_id = row_id

    @property
    def row_data(self):
        """Gets the row_data of this VirtualDocumentRow.  # noqa: E501


        :return: The row_data of this VirtualDocumentRow.  # noqa: E501
        :rtype: lusid.GroupedResultOfAddressKey
        """
        return self._row_data

    @row_data.setter
    def row_data(self, row_data):
        """Sets the row_data of this VirtualDocumentRow.


        :param row_data: The row_data of this VirtualDocumentRow.  # noqa: E501
        :type row_data: lusid.GroupedResultOfAddressKey
        """

        self._row_data = row_data

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
        if not isinstance(other, VirtualDocumentRow):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, VirtualDocumentRow):
            return True

        return self.to_dict() != other.to_dict()
