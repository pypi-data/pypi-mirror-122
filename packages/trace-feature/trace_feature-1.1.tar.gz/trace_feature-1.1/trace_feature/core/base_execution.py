"""
    Base execution for ABC method
"""

from abc import ABC, abstractmethod


class BaseExecution(ABC):
    """
        BaseExecution class
    """

    @abstractmethod
    def execute(self, path, url):
        """
            BaseExecution execute self
        """

    # this method will execute only a specific feature
    @abstractmethod
    def execute_feature(self, project, feature_name, url):
        """
            BaseExecution execute for specific feature
        """

    # this method will execute a specific scenario into a specific feature
    # filename: refer to the .feature file
    # scenario_ref: refer to the line or the name of a specific scenario
    @abstractmethod
    def execute_scenario(self, feature_name, scenario):
        """
            BaseExecution execute for specific scenario into a specific feature
        """
