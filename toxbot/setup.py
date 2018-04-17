from setuptools import setup
import app


version = app.__version__ + '.0'


setup(name='ToxBotPlatform',
      version=version,
      description='Tox Bot Platform',
      long_description='Tox bot platform provides easy way to create bots for Tox messenger',
      url='https://github.com/toxygen-project/ToxBotPlatform/',
      keywords='tox messenger bot platform',
      author='Ingvar',
      maintainer='Ingvar',
      license='GPL3',
      packages=[
          'core', 'wrapper', 'middleware', 'core.bootstrap', 'core.bot_data', 'core.commands', 'core.file_transfers'
      ],
      include_package_data=True,
      classifiers=[
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      entry_points={
          'console_scripts': ['toxbot=app:main'],
      })
