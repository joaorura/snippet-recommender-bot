import re
import pandas as pd


def print_method_lines(method_lines):
    for i in method_lines:
        print(i)


def pre_process_method(lines):
    lines = lines.split('\n')
    lines = filter(lambda x: not re.match(r'^\s*$', x), lines)  # remove whitespaces after line
    lines = filter(lambda x: not re.match(r'^[\t]*[ ]*//', x), lines)  # remove lines that only have comments
    lines = list(lines)
    for i in range(len(lines)):
        lines[i] = re.sub(r'[ ]*//.*', '', lines[i])  # remove comments like "line of code // comment"
        lines[i] = re.sub(r'[ ]+$', '', lines[i])  # remove spaces after each line
    return lines


def get_removable_line_indexes(method_lines):
    removable_indexes = []
    size = len(method_lines)
    for index in range(size):
        if re.search(r'[;][\s]*$', method_lines[index]) is not None:
            removable_indexes.append(index)
    return removable_indexes


def get_removable_indexes_variances(removable_indexes):
    removable_indexes_list = []  # list of list of removable indexes
    size = len(removable_indexes)
    variances_number = 5
    number_lines = int(size / variances_number)
    for i in range(1, variances_number):
        slicing = number_lines * i
        removable_indexes_list.append(removable_indexes[slicing:])
    return removable_indexes_list


def add_method_by_method_lines(methods, current_method, method_lines):
    method = ''
    for i in method_lines:
        method += i + '\n'
    current_method.at['codes'] = method
    methods = methods.append(current_method)
    return methods


def generate_incomplete_method(methods, current_method, method_lines, removable_indexes):
    new_method_lines = []
    method_lines_size = len(method_lines)
    for i in range(method_lines_size):
        if i not in removable_indexes:
            new_method_lines.append(method_lines[i])
    methods = add_method_by_method_lines(methods, current_method, new_method_lines)
    return methods


def main():
    df = pd.read_csv('./result.csv')
    methods = df
    methods = methods.drop('id', axis=1)
    for index, row in methods.iterrows():
        method = row['codes']
        method_lines = pre_process_method(method)
        removable_indexes = get_removable_line_indexes(method_lines)
        removable_indexes_list = get_removable_indexes_variances(removable_indexes)
        current_method = methods.loc[index]
        methods = methods.drop(index)
        methods = add_method_by_method_lines(methods, current_method, method_lines)
        print_method_lines(method_lines)
        for i in removable_indexes_list:
            methods = generate_incomplete_method(methods, current_method, method_lines, i)
    methods = methods.reset_index()
    methods = methods.drop('index', axis=1)
    methods.to_csv('./results_test.csv')


main()