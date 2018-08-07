from setuptools import setup
import toxbot.app as app


version = app.__version__ + '.0'


setup(name='ToxBotPlatform',
      version=version,
      description='Tox Bot Platform',
      long_description='Tox bot platform provides easy way to create bots for Tox messenger',
      url='https://github.com/toxygen-project/bot-platform',
      keywords='tox messenger bot platform',
      author='Ingvar',
      maintainer='Ingvar',
      license='GPL3',
      packages=[
          'toxbot', 'toxbot.core', 'toxbot.wrapper', 'toxbot.middleware', 'toxbot.core.bootstrap',
          'toxbot.core.bot_data', 'toxbot.core.commands', 'toxbot.core.file_transfers', 'toxbot.core.common'
      ],
      include_package_data=True,
      package_data={'toxbot.core.bootstrap': ['nodes.json']},
      classifiers=[
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      entry_points={
          'console_scripts': ['toxbot=toxbot.app:main'],
      })
