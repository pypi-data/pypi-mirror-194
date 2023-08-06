# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentm']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0', 'spacy>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'sentm',
    'version': '0.1.1',
    'description': 'Lexical Sentiment Analysis in Danish',
    'long_description': '\n# senTM\n\nPronounced "sen-T-M". \n\nsenTM is a lexical approach to sentiment analysis in Danish. The approach is inspired by the [afinn](https://github.com/fnielsen/afinn) package, but using the [Danish Sentiment Lexicon version 0.2 (2022-12-20)](https://github.com/dsldk/danish-sentiment-lexicon). \n\nThe approach use the part-of-speech (POS) model from Spacy and then matches any tokens from the Danish Sentiment Lexicon. \n\nLicense: Same as [Danish Sentiment Lexicon version 0.2 (2022-12-20)](https://github.com/dsldk/danish-sentiment-lexicon): CC-BY-SA 4.0 International https://creativecommons.org/licenses/by-sa/4.0/\n\n## Installation\n\nInstall from pip:\n```\npip install sentm\n```\n\n\n## Quickstart\n\nFirst initialize model. \n```\nfrom sentm.sentm import senTM\n\nsentm_model = senTM()\n```\n\nYou can both get sentiment score:\n```\nsentm_model.score(\'Du er en kæmpe idiot!\')\n```\n\nYou can also use it as a classifier. \nHere, the labels are determined by:\n* Score larger than 1: "positiv"\n* Score between -1 and 1: "neutral"\n* Score lower than -1: "negativ"\n```\nsentm_model.classify(\'Du er en kæmpe idiot!\')\n```',
    'author': 'MadsLang',
    'author_email': 'madslangs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MadsLang/senTM',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
