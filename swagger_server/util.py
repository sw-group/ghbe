import datetime
import enum

import six
import typing
from swagger_server import type_util



def _deserialize(data, klass):
    """Deserializes dict, list, str into an object.

    :param data: dict, list or str.
    :param klass: class literal, or string of class name.

    :return: object.
    """
    if data is None:
        return None

    if klass in six.integer_types or klass in (float, str, bool, bytearray):
        return _deserialize_primitive(data, klass)
    elif klass == object:
        return _deserialize_object(data)
    elif klass == datetime.date:
        return deserialize_date(data)
    elif klass == datetime.datetime:
        return deserialize_datetime(data)
    elif type_util.is_generic(klass):
        if type_util.is_list(klass):
            return _deserialize_list(data, klass.__args__[0])
        if type_util.is_dict(klass):
            return _deserialize_dict(data, klass.__args__[1])
    else:
        return deserialize_model(data, klass)


def _deserialize_primitive(data, klass):
    """Deserializes to primitive type.

    :param data: data to deserialize.
    :param klass: class literal.

    :return: int, long, float, str, bool.
    :rtype: int | long | float | str | bool
    """
    try:
        value = klass(data)
    except UnicodeEncodeError:
        value = six.u(data)
    except TypeError:
        value = data
    return value


def _deserialize_object(value):
    """Return an original value.

    :return: object.
    """
    return value


def deserialize_date(string):
    """Deserializes string to date.

    :param string: str.
    :type string: str
    :return: date.
    :rtype: date
    """
    try:
        from dateutil.parser import parse
        return parse(string).date()
    except ImportError:
        return string


def deserialize_datetime(string):
    """Deserializes string to datetime.

    The string should be in iso8601 datetime format.

    :param string: str.
    :type string: str
    :return: datetime.
    :rtype: datetime
    """
    try:
        from dateutil.parser import parse
        return parse(string)
    except ImportError:
        return string


def deserialize_model(data, klass):
    """Deserializes list or dict to model.

    :param data: dict, list.
    :type data: dict | list
    :param klass: class literal.
    :return: model object.
    """
    instance = klass()

    if not instance.swagger_types:
        return data

    for attr, attr_type in six.iteritems(instance.swagger_types):
        if data is not None \
                and instance.attribute_map[attr] in data \
                and isinstance(data, (list, dict)):
            value = data[instance.attribute_map[attr]]
            setattr(instance, attr, _deserialize(value, attr_type))

    return instance


def _deserialize_list(data, boxed_type):
    """Deserializes a list and its elements.

    :param data: list to deserialize.
    :type data: list
    :param boxed_type: class literal.

    :return: deserialized list.
    :rtype: list
    """
    return [_deserialize(sub_data, boxed_type)
            for sub_data in data]


def _deserialize_dict(data, boxed_type):
    """Deserializes a dict and its elements.

    :param data: dict to deserialize.
    :type data: dict
    :param boxed_type: class literal.

    :return: deserialized dict.
    :rtype: dict
    """
    return {k: _deserialize(v, boxed_type)
            for k, v in six.iteritems(data)}


## CUSTOM
def generate_date_count_map(issue_list):
    from collections import defaultdict
    from swagger_server.models import MapStringNumber
    from datetime import datetime
    date_count_map = defaultdict(int)

    for issue in issue_list:
        # Extract the date part from the created_at field
        created_date = issue['created_at'].date()
        # Convert the date to a string for dictionary keys
        created_date_str = created_date.isoformat()
        # Increment the count for the extracted date
        date_count_map[created_date_str] += 1

    return MapStringNumber.from_dict(date_count_map)


def __check_labels(issue_labels, labels, label_count_map):
    for label in labels:
        for issue_label in issue_labels:
            if label in issue_label["name"]:
                label_count_map[label] += 1
                return True
    return False


def __check_body_and_title(issue, labels, label_count_map):
    for label in labels:
        if label in issue["body"] or label in issue["title"]:
            label_count_map[label] += 1
            return


def generate_label_count_map(issues):
    from collections import defaultdict
    labels = ['bug', 'documentation', 'duplicate', 'enhancement', 'good first issue', 'help wanted', 'invalid',
              'question', 'wontfix']
    label_count_map = defaultdict(int)

    for issue in issues:
        if issue["labels"]:  # Ensure issue.labels is not empty or None
            if __check_labels(issue["labels"], labels, label_count_map):
                continue

        __check_body_and_title(issue, labels, label_count_map)

    return label_count_map


def generate_metrics_workflow_map(workflows):
    from collections import defaultdict
    label_count_map = defaultdict(float)
    # Filter workflows where "lines" is not None
    valid_workflows = [w for w in workflows if w["lines"] is not None]

    # Calculate the sum of lines and count of valid workflows
    total_lines = sum(w["lines"] for w in valid_workflows)

    # Calculate the sum of sizes in bytes and count of valid workflows
    total_size_bytes = sum(convert_size_to_bytes(w["size"]) for w in valid_workflows)

    count_valid_workflows = len(valid_workflows)

    # Calculate the mean
    if count_valid_workflows > 0:
        mean_lines = total_lines / count_valid_workflows
        mean_size_bytes = total_size_bytes / count_valid_workflows
    else:
        mean_lines = 0  # Handle case where there are no valid workflows with "lines" defined
        mean_size_bytes = 0

    label_count_map["lines"] = float(format(mean_lines, ".2f"))
    label_count_map["size"] = float(format(mean_size_bytes, ".2f"))
    return label_count_map

def convert_size_to_bytes(size_str):
    multipliers = {'Bytes': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3}
    size_str = size_str.strip()
    num, unit = size_str.split()
    return float(num) * multipliers[unit]


