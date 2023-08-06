"""
    Main module that defines interaction commands and overhaul project comportament
"""

import os
import sys
import click

from trace_feature.core.features.gherkin_parser import read_all_bdds
from trace_feature.core.ruby.read_methods import (read_methods, send_all_methods,
                                                  install_excellent_gem, analyse_methods)
from trace_feature.core.ruby.ruby_execution import RubyExecution
from trace_feature.core.ruby.ruby_config import RubyConfig

@click.command()
@click.option(
    '--scenario',
    '-s',
    default=0,
    help='This is the scenario\'s correponding line that can be found at the feature file.'
)
@click.option(
    '--feature',
    '-f',
    default='',
    help='This is the file\'s name where the feature is.'
)
@click.option(
    '--project',
    '-p',
    default='.',
    help='This is the name of the project to be analyzed. Default: current folder.'
)
@click.option(
    '--lista',
    '-l',
    is_flag=True,
    help='This option list all features into this project.'
)
@click.option(
    '--spec',
    '-t',
    is_flag=True,
    help='This option execute spec files tests into this project.'
)
@click.option(
    '--methods',
    '-m',
    is_flag=True,
    help='This option read all methods into this project.'
)
@click.option(
    '--analyse',
    '-a',
    is_flag=True,
    help='This option analyse all methods into this project.'
)
@click.option(
    '--url',
    '-u',
    default='http://localhost:8000',
    help='This option specify the target server url'
)


def trace(analyse, methods, spec, lista, project, feature, scenario, url):
    """
        This command ables you to run the traces generator's tool by running every BDD feature.
        None of the arguments are required.
    """

    project_path = os.path.abspath(project)

    if lista:
        features = read_all_bdds(project_path)
        for existing_feature in features:
            print(existing_feature)
        print('-----------------------------------')
        print('Number of Features: ', len(features))
    else:

        if methods:
            project_methods = read_methods(project_path)
            install_excellent_gem()
            project_methods.methods = analyse_methods(project_methods.methods)
            send_all_methods(project_methods, url)
            for method in project_methods.methods:
                print('Name: ', method.method_name)
                print('Path: ', method.class_path)
            print(len(project_methods.methods))
        elif analyse:
            project_methods = read_methods(project_path)
            install_excellent_gem()
            project_methods.methods = analyse_methods(project_methods.methods)
        else:
            #  TO DO: language = find_language(path)
            language = 'Ruby'

            if language == 'Ruby':
                execution = RubyExecution()
                config = RubyConfig()
                if config.config() is False:
                    print('Error!')
                    sys.exit()
                elif spec:
                    # project_methods = read_methods(project_path)
                    # install_excellent_gem()
                    # project_methods.methods = analyse_methods(project_methods.methods)
                    # send_all_methods(project_methods)
                    execution.execute_specs(project_path, url)
                else:
                    # print('Read methods..')
                    # project_methods = read_methods(project_path)
                    # install_excellent_gem()
                    # project_methods.methods = analyse_methods(project_methods.methods)
                    # send_all_methods(project_methods)
                    if feature and scenario:
                        print('feature and scenario')
                        execution.prepare_scenario(feature, int(scenario), url)
                    elif feature != '':
                        print('feature')
                        execution.execute_feature(project_path, feature, url)
                    else:
                        print('Full Execution!')
                        execution.execute(project_path, url)
