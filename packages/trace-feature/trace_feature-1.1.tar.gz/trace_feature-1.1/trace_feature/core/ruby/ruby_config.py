"""
    Module which check and define Ruby configuration
"""

import os
import re
import subprocess

from trace_feature.core.base_config import BaseConfig

class RubyConfig(BaseConfig):
    """
        Class responsable for checking configuration on a Ruby target project
    """
    SIMPLECOV = '  gem \'simplecov-json\'\n'
    REQSIMCOV = 'require \'simplecov-json\'\n'
    START = 'SimpleCov.start \'rails\' do\n'
    EXCLUDE_FOLDERS = '    add_filter [\'migrations\', \'db\', \'.git\', \'features\', ' \
                      '\'log\', \'public\', \'script\', \'spec\',\'tmp\', \'vendor\', ' \
                      '\'lib\', \'docker\', \'db\', \'coverage\', \'config\']\nend \n'
    RESULT_DIR = 'SimpleCov.coverage_dir \'coverage/cucumber\'\n'

    def config(self):
        """
            This method checks the required configurations for Ruby target project
        """
        project_path = self.get_local_path()
        if self.is_rails_project(project_path):
            print('Rails project!')
            if (self.verify_requirements_on_gemfile(self, project_path) and
                    self.verify_requirements_on_env_file(self, project_path)):
                return True
            self.check_gemfile(project_path)
            subprocess.call(['bundle', 'install'], cwd=project_path)
            return self.check_environment(project_path)
        return False

    @classmethod
    def is_rails_project(cls, path):
        """
            Check if the target project is a Rails project
        """
        return os.path.exists(path + "/Gemfile")

    @classmethod
    def get_local_path(cls):
        """
            Return the project base path
        """
        return '.'

    @classmethod
    def verify_requirements_on_gemfile(cls, self, path):
        """
            This method verifies if SimpleCov Json gem is present on project requirements
        """
        with open(path+"/Gemfile", 'r') as file:
            if re.search(re.escape(self.SIMPLECOV), file.read(), flags=re.M) is None:
                return False
            return True

    @classmethod
    def verify_requirements_on_env_file(cls, self, path):
        """
            This method verifies if some SimpleCov requirements are present on env.rb target
            project file
        """
        with open(path + "/features/support/env.rb", 'r') as file:
            text_file = file.read()
            if (re.search(re.escape(self.REQSIMCOV), text_file, flags=re.M) is None or
                    re.search(re.escape(self.START), text_file, flags=re.M) is None or
                    re.search(re.escape(self.RESULT_DIR), text_file, flags=re.M) is None or
                    re.search(re.escape(self.EXCLUDE_FOLDERS), text_file, flags=re.M) is None):
                return False
            return True

    def check_gemfile(self, path):
        """
            This method verifies if SimpleCov Json gem is present on the test group of the Gemfile
            file. If it's not present, insert it there
        """
        output = []
        with open(path + '/Gemfile', 'r+') as file:
            has_simplecov = False
            is_on_test = False
            for line in file:
                tokens = line.split()
                if self.is_test_group(tokens):
                    is_on_test = True
                if is_on_test:
                    if not has_simplecov:
                        has_simplecov = self.simplecov_exists(tokens)
                    if tokens:
                        if tokens[0] == 'end':
                            if not has_simplecov:
                                simplecov_line = self.SIMPLECOV
                                output.append(simplecov_line)
                            is_on_test = False
                output.append(line)
            file.seek(0)
            file.writelines(output)

    @classmethod
    def is_test_group(cls, tokens):
        """
            This method verifies if the current Gemfile line is the beginning of the development
            and test group
        """
        if len(tokens) > 1:
            if tokens[0] == 'group' and tokens[1] == ':development,' and tokens[2] == ':test':
                return True
        return False

    @classmethod
    def simplecov_exists(cls, tokens):
        """
            This method verifies if SimpleCov Json gem is present on project requirements
        """
        if len(tokens) > 1:
            if tokens[0] == 'gem' and tokens[1] == '\'simplecov-json\'':
                return True
        return False

    def check_environment(self, path):
        """
            This method verifies if some SimpleCov requirements are present on env.rb target
            project file. If they are not present, insert them
        """
        output = []
        with open(path + '/features/support/env.rb', 'r+') as file:
            has_req = False
            has_start = False
            has_result_dir = False
            has_filter = False

            for line in file:
                tokens = line.split()
                if self.req_simple_cov(tokens):
                    has_req = True
                if self.simple_cov_start(tokens):
                    has_start = True
                if self.result_dir(tokens):
                    has_result_dir = True
                if self.simple_cov_exclude(tokens):
                    has_filter = True
                output.append(line)

            if not has_req:
                has_req_line = self.REQSIMCOV
                output.insert(6, has_req_line)
            if not has_result_dir:
                has_result_line = self.RESULT_DIR
                output.insert(7, has_result_line)
            if not has_start:
                has_start_line = self.START
                output.insert(8, has_start_line)
            if not has_filter:
                has_exclude_line = self.EXCLUDE_FOLDERS
                output.insert(9, has_exclude_line)

            file.seek(0)
            file.writelines(output)

    @classmethod
    def req_simple_cov(cls, tokens):
        """
            This method verifies if the current line being analized is a SimplecovJson require call
        """
        if len(tokens) > 1:
            if tokens[0] == 'require' and tokens[1] == '\'simplecov-json\'':
                return True
        return False

    @classmethod
    def simple_cov_start(cls, tokens):
        """
            This method verifies if the current line being analized is a SimplecovJson beggining
            block
        """
        if len(tokens) > 1:
            if tokens[0] == 'SimpleCov.start' and tokens[1] == '\'rails\'':
                return True
        return False

    @classmethod
    def simple_cov_exclude(cls, tokens):
        """
            This method verifies if the current line being analized in a SimplecovJson statement
            adding a filter block
        """
        if len(tokens) > 1:
            if tokens[0] == 'add_filter':
                return True
        return False

    @classmethod
    def result_dir(cls, tokens):
        """
            This method verifies if the current line being analized is a SimplecovJson statement
            for defining a result dir for coverage result
        """
        if len(tokens) > 1:
            if tokens[0] == 'SimpleCov.coverage_dir' and tokens[1] == '\'coverage/cucumber\'':
                return True
        return False
