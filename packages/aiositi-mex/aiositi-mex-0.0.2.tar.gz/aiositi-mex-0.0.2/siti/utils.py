import re


def to_snake_case(camel_case: str):
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case).lower()


def to_camel_case(snake_case: str):
    # https://stackoverflow.com/questions/19053707/converting-snake-case-to-lower-camel-case-lowercamelcase
    components = snake_case.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def dict_to_snake_case(camel_case_dict: dict):
    transformed_dict = dict()
    for k, v in camel_case_dict.items():
        if isinstance(v, dict):
            transformed_dict[to_snake_case(k)] = dict_to_snake_case(v)
        elif isinstance(v, list):
            transformed_dict[to_snake_case(k)] = list_to_snake_case(v)
        else:
            transformed_dict[to_snake_case(k)] = v
    return transformed_dict


def list_to_snake_case(camel_case_list: list):
    transformed_list = []
    for e in camel_case_list:
        if isinstance(e, dict):
            transformed_list.append(dict_to_snake_case(e))
        elif isinstance(e, list):
            transformed_list.append(list_to_snake_case(e))
        else:
            transformed_list.append(e)
    return transformed_list


def dict_to_camel_case(snake_case_dict: dict):
    transformed_dict = dict()
    for k, v in snake_case_dict.items():
        if isinstance(v, dict):
            transformed_dict[to_camel_case(k)] = dict_to_camel_case(v)
        elif isinstance(v, list):
            transformed_dict[to_camel_case(k)] = list_to_camel_case(v)
        else:
            transformed_dict[to_camel_case(k)] = v
    return transformed_dict


def list_to_camel_case(snake_case_list: list):
    transformed_list = []
    for e in snake_case_list:
        if isinstance(e, dict):
            transformed_list.append(dict_to_camel_case(e))
        elif isinstance(e, list):
            transformed_list.append(list_to_camel_case(e))
        else:
            transformed_list.append(e)
    return transformed_list
