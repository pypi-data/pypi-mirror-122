from distutils.core import setup

setup(

      name='trace_feature',
      packages = ['trace_feature'],
      version='0.1',
      description='A lib to trace bdd features.',
      url='https://github.com/vitorbribas/trace_feature',
      download_url = 'https://github.com/vitorbribas/trace_feature/archive/refs/tags/v_02.tar.gz',
      author='Rafael Fazzolino',
      author_email='fazzolino29@gmail.com',
      license='MIT',
      keywords = ['BDD', 'Trace'],
      py_modules=['trace_feature'],
      install_requires=[
            'Click',
      ]
)