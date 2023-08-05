# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hades',
 'hades.data_loading',
 'hades.plots',
 'hades.summaries',
 'hades.topic_analysis',
 'hades.topic_modeling',
 'hades.topic_modeling.model_optimizer',
 'hades_app',
 'hades_app.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=2.6.0,<3.0.0',
 'bert-extractive-summarizer>=0.10.1,<0.11.0',
 'black>=22.6.0,<23.0.0',
 'click>=8.1.3,<9.0.0',
 'contextualized-topic-models>=2.4.2,<3.0.0',
 'en-core-web-lg @ '
 'https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.3.0/en_core_web_lg-3.3.0-py3-none-any.whl',
 'en-core-web-sm @ '
 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.3.0/en_core_web_sm-3.3.0-py3-none-any.whl',
 'gensim>=4.2.0,<5.0.0',
 'hdbscan>=0.8.28,<0.9.0',
 'llvmlite==0.39.1',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.23.1,<2.0.0',
 'openai>=0.23.0,<0.24.0',
 'pandas>=1.4.3,<2.0.0',
 'plotly>=5.9.0,<6.0.0',
 'pyLDAvis>=3.3.1,<4.0.0',
 'pycountry>=22.3.5,<23.0.0',
 'scipy>=1.8.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'spacy>=3.3.1,<4.0.0',
 'st-annotated-text>=3.0.0,<4.0.0',
 'statsmodels>=0.13.2,<0.14.0',
 'streamlit==1.16.0',
 'swifter>=1.2.0,<2.0.0',
 'umap-learn>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['hades = hades_app.run_app:cli']}

setup_kwargs = {
    'name': 'hades-nlp',
    'version': '0.1.0',
    'description': 'Homologous Automated Document Exploration and Summarization - A powerful tool for comparing similarly structured documents',
    'long_description': '# HADES: Homologous Automated Document Exploration and Summarization\nA powerful tool for comparing similarly structured documents\n\n[![PyPI version](https://badge.fury.io/py/hades-nlp.svg)](https://pypi.org/project/hades-nlp/)\n[![Downloads](https://static.pepy.tech/badge/hades-nlp)](https://pepy.tech/project/hades-nlp)\n\n## Overview\n`HADES` is a **Python** package for comparing similarly structured documents. HADES is designed to streamline the work of professionals dealing with large volumes of documents, such as policy documents, legal acts, and scientific papers. The tool employs a multi-step pipeline that begins with processing PDF documents using topic modeling, summarization, and analysis of the most important words for each topic. The process concludes with an interactive web app with visualizations that facilitate the comparison of the documents. HADES has the potential to significantly improve the productivity of professionals dealing with high volumes of documents, reducing the time and effort required to complete tasks related to comparative document analysis.\n\n## Installation\nLatest released version of the `HADES` package is available on [Python Package Index (PyPI)](https://pypi.org/project/hades-nlp/):\n\n```\npip install -U hades-nlp\n```\nThe source code and development version is currently hosted on [GitHub](https://github.com/MI2DataLab/HADES).\n## Usage\nThe `HADES` package is designed to be used in a Python environment. The package can be imported as follows:\n\n```python\nfrom hades.data_loading import load_processed_data\nfrom hades.topic_modeling import ModelOptimizer, save_data_for_app, set_openai_key\nfrom my_documents_data import PARAGRAPHS, COMMON_WORDS, STOPWORDS\n```\nThe `load_processed_data` function loads the documents to be processed. The `ModelOptimizer` class is used to optimize the topic modeling process. The `save_data_for_app` function saves the data for the interactive web app. The `set_openai_key` function sets the OpenAI API key.\n`my_documents_data` contains the informations about the documents to be processed. The `PARAGRAPHS` variable is a list of strings that represent the paragraphs of the documents. The `COMMON_WORDS` variable is a list of strings that represent the most common words in the documents. The `STOPWORDS` variable is a list of strings that represent the most common words in the documents that should be excluded from the analysis.\n\nFirst, the documents are loaded and processed:\n```python\nset_openai_key("my openai key")\ndata_path = "my/data/path"\nprocessed_df = load_processed_data(\n    data_path=data_path,\n    stop_words=STOPWORDS,\n    id_column=\'country\',\n    flattened_by_col=\'my_column\',\n)\n```\nAfter the documents are loaded, the topic modeling process is optimized for each paragraph:\n```python\nmodel_optimizers = []\nfor paragraph in PARAGRAPHS:\n    filter_dict = {\'paragraph\': paragraph}\n    model_optimizer = ModelOptimizer(\n        processed_df,\n        \'country\',\n        \'section\',\n        filter_dict,\n        "lda",\n        COMMON_WORDS[paragraph],\n        (3,6),\n        alpha=100\n    )\n    model_optimizer.name_topics_automatically_gpt3()\n    model_optimizers.append(model_optimizer)\n\n```\nFor each paragraph, the `ModelOptimizer` class is used to optimize the topic modeling process. The `name_topics_automatically_gpt3` function automatically names the topics using the OpenAI GPT-3 API. User can also use the `name_topics_manually` function to manually name the topics.\n\nFinally, the data is saved for the interactive web app:\n```python\nsave_data_for_app(model_optimizers, path=\'path/to/results\', do_summaries=True)\n```\nThe `save_data_for_app` function saves the data for the interactive web app. The `do_summaries` parameter is set to `True` to generate summaries for each topic.\n\nWhen the data is saved, the interactive web app can be launched:\n```sh\nhades run-app --config path/to/results/config.json\n```\n\n***\n\n',
    'author': 'Artur Żółkowski',
    'author_email': 'artur.zolkowski@wp.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*, !=3.8.*, !=3.10.*, !=3.11.*',
}


setup(**setup_kwargs)
