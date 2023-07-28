import os
import pytest
from utils.utils import load_data, get_filtered_data, get_sorted_data, get_formatted_data


@pytest.fixture()
def testing_data():
    temp_data = os.path.join(os.path.dirname(__file__), "test_data_file.json")
    return temp_data


def test_load_data(testing_data):
    """ Тест на корректность загрузки файла """
    loaded_data = load_data(testing_data)
    assert loaded_data == [
        {"id": 1, "name": "Mary", "state": "EXECUTED"},
        {"id": 2, "name": "Jerry", "state": "CANCELED"},
        {},
        {"id": 3, "name": "Piter", "state": "EXECUTED"}
    ]


@pytest.mark.parametrize('testing_data, expected', [
    ([
        {"id": 1, "name": "Mary", "state": "EXECUTED"},
        {"id": 2, "name": "Jerry", "state": "CANCELED"},
        {},
        {"id": 3, "name": "Piter", "state": "EXECUTED"}
        ],
        [
        {"id": 1, "name": "Mary", "state": "EXECUTED"},
        {"id": 3, "name": "Piter", "state": "EXECUTED"}
    ])
])
def test_get_filtered_data(testing_data, expected):
    """ Тест на фильтрацию данных """
    filtered_data = get_filtered_data(testing_data)
    assert filtered_data == expected


@pytest.mark.parametrize('testing_data, expected', [
    ([
        {"id": 1, "name": "Mary", "state": "EXECUTED"},
        {"id": 2, "name": "Jerry"}],
        KeyError)
])
def test_get_filtered_dataKeyError(testing_data, expected):
    """ Тест на ошибку по ключу """
    with pytest.raises(expected):
        get_filtered_data(testing_data)


@pytest.mark.parametrize('testing_data, expected', [
    ([{'date': 3}, {'date': 1}, {'date': 2}, {'date': 7}, {'date': 12}, {'date': 71}, {'date': 20}],
        [{'date': 71}, {'date': 20}, {'date': 12}, {'date': 7}, {'date': 3}]),
    ([{'date': 5}, {'date': 2}, {'date': 8}], [{'date': 8}, {'date': 5}, {'date': 2}])
])
def test_get_sorted_data(testing_data, expected):
    """ Тест на проверку корректности сортировки данных по ключу и порядку"""
    assert get_sorted_data(testing_data) == expected


@pytest.mark.parametrize('example_data, expected_result', [
    ([
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "to": "Счет 35383033474447895560"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        }
    ], [
        f"""
        26.08.2019 Перевод организации
        Maestro 1596 83** **** 5199 -> Счет **9589
        31957.58 руб.
        """,
        f"""
        03.07.2019 Перевод организации
          -> Счет **5560
        8221.37 USD
        """,
        f"""
        19.08.2018 Перевод с карты на карту
        Visa Classic 6831 98** **** 7658 -> Visa Platinum 8990 92** **** 5229
        56883.54 USD
        """,
        f"""
        30.06.2018 Перевод организации
        Счет **6952 -> Счет **6702
        9824.07 USD
        """
        ])])
def test_get_formatted_data(example_data, expected_result):
    """ Тест на корректность форматирования данных """
    assert get_formatted_data(example_data) == expected_result