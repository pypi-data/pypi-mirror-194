from setuptools import setup

setup(name="byunlp",
      version="0.0.3",
      description="Automatic conjugation of Korean verbs",
      author='SungJoo Byun',
      author_email='byunsj@snu.ac.kr',
      keywords=['present','present_progressive', 'past', 'future', 'passive','causative', 'subj_honorific','sangdae_honorific','Korean verb','conjugation'],
      url=None,
      license='MIT',
      packages=['byunlp'],
      insall_requires=['soynlp']
     )
      