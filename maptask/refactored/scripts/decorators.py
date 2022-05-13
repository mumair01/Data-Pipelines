# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-12 13:57:28
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-12 19:38:48

import time


def print_component_decorator(func):
    """
    Print details about the current component
    """

    def time_func(*args, **kwargs):
        print("*" * 30)
        print("Running pipeline component: {}".format(func.__name__))
        # storing time before function execution
        begin = time.time()
        func(*args, **kwargs)
        # storing time after function execution
        print("Total time taken in : {} {} seconds".format(
            func.__name__, time.time() - begin))
        print("*" * 30)
    return time_func
