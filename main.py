import os
from utils.utils import load_data, get_filtered_data, get_sorted_data, get_formatted_data


def main():
    filename = os.path.join('.', 'operations.json')
    data = load_data(filename)
    filtered_data = get_filtered_data(data)
    sorted_data = get_sorted_data(filtered_data)
    formatted_data = get_formatted_data(sorted_data)
    operations = ''.join(formatted_data)
    print(operations)


if __name__ == '__main__':
    main()