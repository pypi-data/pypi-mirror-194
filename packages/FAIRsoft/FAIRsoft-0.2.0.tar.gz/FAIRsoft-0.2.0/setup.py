#!/usr/bin/env python3

from distutils.core import setup

setup(name='FAIRsoft',
      version='0.1.4',
      description='Library for the aggregation of Life Sciences software metadata and FAIR evaluation.',
      description_content_type='text/markdown',
      log_description='''FAIRsoft indicators are a set of FAIRness indicators for research software, specifically devised to be assesed automatically. 
      This package allows the user to gather metadata about research software specific to Life Sciences, harmonize and integrate it and then perform an evaluation of their compliance with FAIRsoft indicators.''',
      author='Eva Martin del Pico',
      author_email='eva.martin@bsc.es',
      license='AGLP-3.0',
      classifiers=['Development Status :: 4 - Beta'],
      install_requires = [
        'bidict',
        'matplotlib',
        'munch',
        'pymongo',
        'requests',
        'selenium',
        'simplejson',
        'webdriver_manager'],
      url='https://gitlab.bsc.es/inb/elixir/software-observatory/FAIRsoft_ETL/-/tree/master/FAIRsoft',
      packages=['FAIRsoft', 
                'FAIRsoft.importers',
                'FAIRsoft.importers.bioconductor_imp',
                  'FAIRsoft.importers.bioconda_imp',
                  'FAIRsoft.importers.bioconda_biotools_galaxy_imp',
                  'FAIRsoft.importers.toolshed_imp',
                  'FAIRsoft.importers.repositories_imp',
                  'FAIRsoft.importers.opeb_metrics_imp',
                  'FAIRsoft.importers.sourceforge_imp',
                'FAIRsoft.integration',
                'FAIRsoft.transformation',
                'FAIRsoft.indicators_evaluation'],
     )
