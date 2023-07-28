import datetime
import json


def load_data(filename):
    """ Функция открывает и читает файл """
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def get_filtered_data(data):
    """ Функция фильтрует операции по выполненным и исключает пустые операции"""
    filtered_list = [operation for operation in data if operation and operation['state'] == 'EXECUTED']
    return filtered_list


def get_sorted_data(data):
    """ Функция принимает список, сортирует его по ключу в обратном порядке и возвращает 5 последних операций """
    sorted_list = sorted(data, key=lambda x: x['date'], reverse=True)
    sliced_list = sorted_list[:5]
    return sliced_list


def get_formatted_data(data):
    """ Функция форматирует данные и возвращает список в формате:
        [{ДД.ММ.ГГГГ} {description}
        {для карты} {формат XXXX XX** **** XXXX} -> {для счёта} {**XXXX} или  -> {счёт} {**XXXX} если не указан отправитель
        {transfer_amount} {currency}
        ' ']
        """
    formatted_data = []
    for item in data:
        data = datetime.datetime.strptime(item['date'],  "%Y-%m-%dT%H:%M:%S.%f").strftime('%d.%m.%Y')
        description = item['description']
        if 'from' in item:
            split_str = item['from'].split(' ')
            bill = split_str.pop()
            from_name = ' '.join(split_str)
            if len(bill) <= 16:
                sliced_bill = bill[:4] + ' ' + bill[4:6] + '** **** ' + bill[-4:]
            elif len(bill) > 16:
                sliced_bill = '**' + bill[-4:]
        else:
            sliced_bill, from_name = '', ''
        split_given_name = item['to'].split(' ')
        bill_given = split_given_name.pop()
        given_name = ' '.join(split_given_name)
        if len(bill_given) <= 16:
            sliced_giv_bill = bill_given[:4] + ' ' + bill_given[4:6] + '** **** ' + bill_given[-4:]
        elif len(bill_given) > 16:
            sliced_giv_bill = '**' + bill_given[-4:]
        transfer_amount = item['operationAmount']['amount']
        currency = item['operationAmount']['currency']['name']
        formatted_data.append(f"""
        {data} {description}
        {from_name} {sliced_bill} -> {given_name} {sliced_giv_bill}
        {transfer_amount} {currency}
        """)
    return formatted_data
