"""
    Module responsable for parsing .feature files using Gherkin language
"""

import os
from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner
from trace_feature.core.models import Feature, SimpleScenario, StepBdd


def get_scenario(feature_path, line):
    """
    Read scenario from feature file
    :param feature_path: path of the file that contains the feature
    :return: None
    """
    with open(feature_path) as file:
        file.seek(0)
        parser = Parser()
        print(feature_path)
        feature_file = parser.parse(TokenScanner(file.read()))
        scenarios = get_scenarios(feature_file['feature']['children'])
        for each in scenarios:
            if each.line == line:
                return each
        return None

def read_all_bdds(project_path):
    """
    Read all feature files from project
    :param project_path: base path of the project
    :return: Array of Feature objects
    """
    features = []
    for root, _, files in os.walk(project_path + '/features/'):
        for file in files:
            if file.endswith(".feature"):
                file_path = os.path.join(root, file)
                feature = read_feature(file_path)

                features.append(feature)
    return features


def read_feature(feature_path):
    """
    Read a specific feature
    :param feature_path: path of the file that contains the feature
    :return: Feature object
    """
    feature = Feature()
    with open(feature_path) as file:
        file.seek(0)
        parser = Parser()
        print(feature_path)
        feature_file = parser.parse(TokenScanner(file.read()))

        feature.feature_name = feature_file['feature']['name']
        feature.language = feature_file['feature']['language']
        feature.path_name = feature_path
        feature.tags = feature_file['feature']['tags']
        feature.line = feature_file['feature']['location']['line']
        feature.scenarios = get_scenarios(feature_file['feature']['children'])

    return feature


def get_scenarios(childrens):
    """
    Read scenarios from feature childrens
    :param childres: path of the file that contains the feature
    :return: Array of SimpleScenario objects
    """
    scenarios = []
    for children in childrens:
        scenario = SimpleScenario()
        scenario.line = children['location']['line']
        scenario.scenario_title = children['name']
        scenario.steps = get_steps(children['steps'])

        scenarios.append(scenario)
    return scenarios


def get_steps(steps):
    """
    Instantiate Step objects from parsed steps data
    :param steps: parsed steps
    :return: Array of StepBdd objects
    """
    all_steps = []
    for each_step in steps:
        step = StepBdd()
        step.line = each_step['location']['line']
        step.keyword = each_step['keyword']
        step.text = each_step['text']

        all_steps.append(step)

    return all_steps
