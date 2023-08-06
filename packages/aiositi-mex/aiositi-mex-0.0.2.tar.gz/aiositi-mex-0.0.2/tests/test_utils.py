import pytest

from siti.utils import (
    dict_to_camel_case,
    dict_to_snake_case,
    to_camel_case,
    to_snake_case,
)


@pytest.fixture
def snake_case_dict():
    return {
        'some_integer': 2,
        'some_float': 3.5,
        'some_str': 'some_str',
        'some_dict': {
            'inside_field': 'hehe',
        },
        'some_list': [1, 2, 3],
        'some_list_with_objects': [
            {'inside_field_again': '1', 'again_again': '2'},
            ['some', 'random', 'text'],
        ],
    }


@pytest.fixture
def camel_case_dict():
    return {
        'someInteger': 2,
        'someFloat': 3.5,
        'someStr': 'some_str',
        'someDict': {
            'insideField': 'hehe',
        },
        'someList': [1, 2, 3],
        'someListWithObjects': [
            {'insideFieldAgain': '1', 'againAgain': '2'},
            ['some', 'random', 'text'],
        ],
    }


def test_to_snake_case():
    assert to_snake_case('camelCase') == 'camel_case'
    assert to_snake_case('camel_case') == 'camel_case'


def test_to_camel_case():
    assert to_camel_case('snake_case') == 'snakeCase'
    assert to_camel_case('snakeCase') == 'snakeCase'


def test_dict_to_camel_case(snake_case_dict, camel_case_dict):
    assert dict_to_camel_case(snake_case_dict) == camel_case_dict


def test_dict_to_snake_case(snake_case_dict, camel_case_dict):
    assert dict_to_snake_case(camel_case_dict) == snake_case_dict
