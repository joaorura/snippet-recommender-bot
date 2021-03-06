from code_recommender.src.sqlconnector import MySqlOperator
import json


class UserMethod:
    def __init__(self, method_name, number_parameters, parameter_types, return_type):
        self.method_name = method_name
        self.number_parameters = number_parameters
        self.parameter_types = parameter_types
        self.return_type = return_type


class RecommendationMethod:
    def __init__(self, method_name, code, number_parameters, parameter_types, return_type):
        self.method_name = method_name
        self.code = code
        self.number_parameters = number_parameters
        self.parameter_types = parameter_types
        self.return_type = return_type
        self.points = 0


def rank_methods(user_method, recommendation_method_list):
    for method in recommendation_method_list:

        # Return types points
        return_type_points = 0
        if user_method.return_type == method.return_type:
            return_type_points = 1
        # Number parameters points
        if user_method.number_parameters >= method.number_parameters:
            number_parameters_points = user_method.number_parameters / method.number_parameters
        else:
            if user_method.number_parameters == 0 and method.number_parameters == 0:
                number_parameters_points = 1
            elif user_method.number_parameters == 0 and method.number_parameters != 0:
                number_parameters_points = 1
            else:
                number_parameters_points = method.number_parameters / user_method.number_parameters

        # Parameter types points
        if len(user_method.parameter_types) > len(method.parameter_types):
            bigger = user_method.parameter_types
            smaller = method.parameter_types
        else:
            bigger = method.parameter_types
            smaller = user_method.parameter_types
        can_match = []
        match = 0
        for i in bigger:
            for j in smaller:
                if i == j and can_match[j] is not False:
                    match += 1
                    can_match[j] = False
        parameter_type_points = match/len(bigger) * 2
        method.points = return_type_points + number_parameters_points + parameter_type_points
        print("######## CODE ###########")
    return recommendation_method_list


def generate_methods_to_recommender(method_name):
    similar_methods = list()
    get = MySqlOperator().select_method(method_name)
    print(len(get))
    for data in get:
        object = RecommendationMethod(data[2], data[3], data[4], data[5], data[6])
        similar_methods.append(object)
    return similar_methods


def recommender(method_name, number_parameters, parameter_types, return_type):
    user_method = UserMethod(method_name, number_parameters, parameter_types, return_type)
    recommendation_method_list = generate_methods_to_recommender(method_name)
    recommendation_method_list = rank_methods(user_method, recommendation_method_list)
    recommendation_method_list.sort(key=lambda x: x.points, reverse=True)
    method_name_list = []
    method_code_list = []
    method_points_list = []
    num_codes = len(recommendation_method_list)
    for i in recommendation_method_list:
        method_name_list.append(i.method_name)
        method_code_list.append(i.code)
        method_points_list.append(i.points)
    print(method_name_list)
    method_dict = {'method_name': method_name_list, 'method_code': method_code_list, 'method_points': method_points_list, 'num_codes': num_codes}
    return method_dict

