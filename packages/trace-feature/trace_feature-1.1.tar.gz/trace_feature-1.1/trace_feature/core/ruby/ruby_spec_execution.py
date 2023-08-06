# Criar métodos para ler estaticamente todos os "its" presentes no projeto analisado.

# Com o array de "its" disponível e todos seus dados preenchidos, podemos executar 1 por 1 e
# registrar os métodos executados, assim como é feito com o BDD. A diferença é que o BDD executa
# um cenário, aqui vamos executar 1 it de cada vez e salvar a execução.

"""
    Module responsable for executing spec files on target project
"""

import os

from trace_feature.core.ruby.spec_models import It


def read_specs(path):
    """
        Get all IT declarations from the project looping through each of the spec files
    """

    specs = []
    for root, _, files in os.walk(path + '/spec/'):
        for file in files:
            if file.endswith(".rb"):
                file_path = os.path.join(root, file)
                its = get_its(file_path)
                specs += its
    return specs


def get_its(file_path):
    """
        Get each IT declaration from a spec file
    """

    with open(file_path) as file:
        file.seek(0)
        its = []
        for number_line, line in enumerate(file):
            if "it " in line and line[-3:] == "do\n":
                line = line.split('it ')
                line = line[1][1:-5]
                spec = It()
                spec.description = line
                spec.line = number_line
                spec.file = file_path
                spec.executed_methods = []
                its.append(spec)
    return its
