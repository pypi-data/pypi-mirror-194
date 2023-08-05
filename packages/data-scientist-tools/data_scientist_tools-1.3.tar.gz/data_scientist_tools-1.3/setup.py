from setuptools import setup

setup(name='data_scientist_tools',
      version='1.3',
      description='Good-to-have tools for general Data Science tasks',
	long_description = '''Good-to-have tools for general Data Science tasks''',
      packages=['data_scientist_tools'],
      author_email='davidliu1007@gmail.com',
      zip_safe=False,
	install_requires=[
          'pandas',
          'seaborn',
          'numpy',
          'matplotlib',
          'scikit-learn',
          'pyautogui',
          'keyboard'
      ])
