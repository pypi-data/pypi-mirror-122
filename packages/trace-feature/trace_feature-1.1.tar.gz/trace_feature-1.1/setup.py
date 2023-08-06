from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='trace_feature',
      packages=['trace_feature', 'trace_feature.core', 'trace_feature.core.ruby', 'trace_feature.core.features'],
      version='1.1',
      description='A lib to trace bdd features.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/vitorbribas/trace_feature',
      download_url = 'https://github.com/vitorbribas/trace_feature/archive/refs/tags/v_1.1.tar.gz',
      author='Rafael Fazzolino',
      author_email='fazzolino29@gmail.com',
      license='MIT',
      keywords = ['BDD', 'Trace'],
      py_modules=['trace_feature'],
      install_requires=[
            'Click==7.0',
            'gherkin-official==4.1.3',
            'requests==2.21.0',
            'ez-setup==0.9'
      ],
      entry_points='''
            [console_scripts]
            trace-feature=trace_feature.trace_feature:trace
      '''
)