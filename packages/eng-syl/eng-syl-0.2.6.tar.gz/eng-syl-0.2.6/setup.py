from setuptools import setup
import os


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(name='eng-syl',
      version='0.2.6',
      long_description=read_file('README.md'),
      long_description_content_type='text/markdown',
      url='https://github.com/ellipse-liu/eng-syl',
      author='ellipse-liu',
      author_email='timothys.new.email@gmail.comm',
      license='MIT',
      packages=['eng_syl'],
      pcakage_data={'eng_syl':['*.pkl', 'Segmenter2.0_bestweights.h5']},
      install_requires=[
          'tensorflow==2.6.0',
          'keras==2.6.0',
          'nltk',
          'numpy',
          'protobuf==3.20.0',
      ],
      keywords=['Syllable', 'NLP', 'psycholinguistics'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Intended Audience :: Developers',  # Define that your audience are developers
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',  # Again, pick a license
          'Programming Language :: Python :: 3.6',
      ],
      zip_safe=False)
