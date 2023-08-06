# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentm']

package_data = \
{'': ['*']}

install_requires = \
['da-core-news-sm @ '
 'https://github.com/explosion/spacy-models/releases/download/da_core_news_sm-3.5.0/da_core_news_sm-3.5.0-py3-none-any.whl',
 'pandas>=1.5.2,<2.0.0',
 'spacy>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'sentm',
    'version': '0.1.0',
    'description': 'Lexical Sentiment Analysis in Danish',
    'long_description': '\n# senTM\n\nPronounced "sen-T-M". \n\nsenTM is a lexical approach to sentiment analysis in Danish. The approach is inspired by the [afinn](https://github.com/fnielsen/afinn) package, but using the [Danish Sentiment Lexicon version 0.2 (2022-12-20)](https://github.com/dsldk/danish-sentiment-lexicon). \n\nThe approach use the part-of-speech (POS) model from Spacy and then matches any tokens from the Danish Sentiment Lexicon. \n\nLicense: Same as [Danish Sentiment Lexicon version 0.2 (2022-12-20)](https://github.com/dsldk/danish-sentiment-lexicon): CC-BY-SA 4.0 International https://creativecommons.org/licenses/by-sa/4.0/',
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
