"""
    Module which declares auxiliary classes for readingtarget project methods
"""

import json
import linecache
import os
import re
import subprocess

import requests
import time
import random

from trace_feature.core.models import Method, Project
from trace_feature.core.ruby.ruby_execution import RubyExecution


def get_content(method, filename):
    """
        Get all method related content from a file
    """
    # We go through the file from the line containing the method definition
    # until its matching 'end' line. We need to keep track of the 'end'
    # keyword appearing in other contexts, e.g. closing other blocks of code.
    remaining_blocks = 1
    current_line = method

    block_tokens = ['do', 'case', 'for', 'begin', 'while']
    content = ""
    while remaining_blocks:
        line = linecache.getline(filename, current_line)
        content += line
        tokens = line.split()

        # If we have a line that requires a matching 'end', we increase the
        # number of blocks.

        if tokens:
            if any(token in tokens for token in block_tokens) or (tokens[0] in ['if', 'unless']):
                remaining_blocks += 1

        # Likewise, if we found an 'end', we decrease the number of blocks.
        # When it gets to zero, that means we have reached the end of the
        # method.

        if 'end' in tokens:
            remaining_blocks -= 1
        current_line += 1
    content += linecache.getline(filename, current_line)

    return content


def read_methods(path):
    """
        Read file methods and append all them to a project
    """

    ruby_exec = RubyExecution()
    project = ruby_exec.get_project_infos(path)

    exclude = ['migrations', 'db', '.git', 'log', 'public', 'script', 'spec', 'tmp',
               'vendor', 'docker', 'db', 'coverage', 'config', 'bin', 'features']
    for root, _, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file.endswith(".rb"):
                file_path = os.path.join(root, file)
                with open(file_path) as opened_file_path:
                    if ruby_exec.is_empty_class(opened_file_path):
                        pass
                    else:
                        ruby_exec.get_class_definition_line(opened_file_path)
                        methods_line = get_methods_line(opened_file_path, ruby_exec)
                        for method in methods_line:
                            # print('method: ', method)
                            if method is not None:
                                new_method = Method()
                                new_method.line = method
                                new_method.content = get_content(method, file_path)
                                new_method.method_name = ruby_exec.get_method_or_class_name(
                                    method,
                                    file_path
                                )
                                if ruby_exec.class_definition_line is None:
                                    new_method.class_name = 'None'
                                else:
                                    new_method.class_name = ruby_exec.get_method_or_class_name(
                                        ruby_exec.class_definition_line, file_path)
                                new_method.class_path = file_path
                                new_method.method_id = file_path + \
                                                       ruby_exec.get_method_or_class_name(
                                                           method,
                                                           file_path
                                                       ) + str(new_method.line)
                                project.methods.append(new_method)
                                print('Método: ')
                                print(new_method.method_name)
                                print(new_method.content)
                                # oi = input('oi')
    return project


def get_methods_line(file_path, ruby):
    """
        Interates ruby file and returns all methods lines
    """

    file_path.seek(0)
    methods = []
    for line_number, line in enumerate(file_path, 1):
        if ruby.is_method(line):
            methods.append(line_number)
    return methods


def send_all_methods(project, url):
    """
        Send creation requests to all methods from a project
    """

    json_string = json.dumps(project, default=Project.obj_dict)
    # file.write(json_string)
    for retry in range(1, 4):
        try:
            request = requests.post(url + "/createmethods", json=json_string)
            print(request.status_code, request.reason)
            return request.status_code
        except:
            print("Connection refused by the server... Waiting to try again")
            time.sleep(3**retry + random.uniform(0,1))
            print("Trying again for the " + str(retry) + "° time")
    else:
        print("Could not connect to server...exiting")

def install_excellent_gem():
    """
        Install excellent gem on target project
    """

    process = subprocess.Popen(["gem", "install", "excellent"], stdout=subprocess.PIPE)

    # Catches Tuple first element and decode it
    test_message = process.communicate()[0]
    test_message = test_message.decode('utf-8')
    # print(test_message)


def execute_excellent_gem(file):
    """
        Execute excellent gem on target project
    """

    process = subprocess.Popen(["excellent", file], stdout=subprocess.PIPE)

    # Catches Tuple first element and decode it
    test_message = process.communicate()[0]
    test_message = test_message.decode('utf-8')
    print(test_message)
    return test_message


def get_abc_score(result, method):
    """
        Get ABC score from a method
    """

    result = re.split(r'\* Line  |\* Line ', result)

    for line in result:
        if method.class_name + "#" in line:
            # print('ENTROU')
            name = line.split(method.class_name + "#")[1].split(' ')[0].replace(' ', '')
            # print('name: ', name)
            if name == method.method_name:
                if 'abc score of ' in line:
                    abc = line.split('abc score of ')[1]
                    abc = re.findall("\\d+\\.\\d+", abc)
                    if len(abc) > 0:
                        return float(abc[0])
    return 0


def get_cyclomatic_complexity(result, method):
    """
        Get cyclomatic complexity from a method
    """

    result = re.split(r'\* Line  |\* Line ', result)

    for line in result:
        if method.class_name + "#" in line:
            # print('ENTROU')
            name = line.split(method.class_name + "#")[1].split(' ')[0].replace(' ', '')
            # print('name: ', name)
            if name == method.method_name:
                if 'has cyclomatic complexity of ' in line:
                    complexity = line.split('has cyclomatic complexity of ')[1]
                    complexity = re.findall("\\d+", complexity)
                    if len(complexity) > 0:
                        return float(complexity[0])
    return 0


def get_number_of_lines(result, method):
    """
        Get number of lines from a method
    """

    result = re.split(r'\* Line  |\* Line ', result)

    for line in result:
        if method.class_name + "#" in line:
            # print('ENTROU')
            name = line.split(method.class_name + "#")[1].split(' ')[0].replace(' ', '')
            # print('name: ', name)
            if name == method.method_name:
                number_of_lines = re.findall("has \\d+ lines.", line)
                if len(number_of_lines) > 0:
                    return int(re.findall("\\d+", number_of_lines[0])[0])
    return 0


def analyse_methods(methods):
    """
        Get methods data from excellent gem execution
    """

    for method in methods:
        result = execute_excellent_gem(method.class_path)
        method.abc_score = get_abc_score(result, method)
        method.complexity = get_cyclomatic_complexity(result, method)
        method.number_of_lines = get_number_of_lines(result, method)

    return methods
