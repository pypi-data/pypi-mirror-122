"""
    Module which declares some classes as models
"""

from abc import ABC, abstractmethod


class Project:
    """
        Project object
    """
    def __init__(self, name='', language='', repository='', methods=[]):
        self.name = name
        self.language = language
        self.repository = repository
        self.methods = methods

    def __str__(self):
        print('PROJETO:')
        print("\t name: " + self.name)
        print("\t language: " + self.language)
        print("\t Repository: " + str(self.repository))

        return ''

    def obj_dict(self):
        """ Return a dictionary or other mapping object. """
        return self.__dict__


class Feature:
    """
        Feature object
    """

    def __init__(self, path_name="", feature_name="", scenarios=[], language="", user_story="",
                 tags=[], line=None, background=None, project=""):
        self.path_name = path_name
        self.feature_name = feature_name
        self.scenarios = scenarios
        self.language = language
        self.user_story = user_story
        self.tags = tags
        self.line = line
        self.background = background
        self.project = project

    def __str__(self):
        return self.feature_name

    def obj_dict(self):
        """ Return a dictionary or other mapping object. """
        return self.__dict__


class Scenario(ABC):
    """ Scenario object """

    def __init__(self):
        self.steps = NotImplemented
        self.scenario_title = NotImplemented
        self.line = NotImplemented
        self.executed_methods = NotImplemented


    # @property
    # def steps(self):
    #     raise NotImplementedError

    # @property
    # def scenario_title(self):
    #     raise NotImplementedError

    # @property
    # def line(self):
    #     raise NotImplementedError

    @abstractmethod
    def execute(self):
        """ Execute scenario """

    @abstractmethod
    def set_line(self):
        """
            Set line
        """

class SimpleScenario(Scenario):
    """ Simple scenario object """

    def __init__(self, steps=[], scenario_title="", line=None, executed_methods=[]):
        super().__init__()
        self.steps = steps
        self.scenario_title = scenario_title
        self.line = line
        self.executed_methods = executed_methods

    def execute(self):
        pass

    def set_line(self):
        pass

    def __str__(self):
        print("SCENARIO:")
        print("\t title: " + self.scenario_title)
        print("\t line: " + str(self.line))
        print("\t steps: ")

        for step in self.steps:
            print("\t\t" + step.keyword + step.text)

        for method in self.executed_methods:
            print('\t\t', method)

        return ''


class StepBdd:
    """ BDD step object """

    def __init__(self, line=None, keyword='', text=''):
        self.line = line
        self.keyword = keyword
        self.text = text


class Method:
    """ Method object """

    def __init__(self, line=None, method_id="", method_name="", class_name="", class_path="",
                 abc_score=0, complexity=0, number_of_lines=0, content=""):
        self.line = line
        self.method_id = method_id
        self.method_name = method_name
        self.class_name = class_name
        self.class_path = class_path
        self.abc_score = abc_score
        self.complexity = complexity
        self.number_of_lines = number_of_lines
        self.content = content

    def __str__(self):
        print("METHOD:")
        print("\t\t\t name: " + self.method_name)
        print("\t\t\t classe: " + self.class_name)
        print("\t\t\t path: " + self.class_path)
        return ''

    def obj_dict(self):
        """ Return a dictionary or other mapping object. """
        return self.__dict__
