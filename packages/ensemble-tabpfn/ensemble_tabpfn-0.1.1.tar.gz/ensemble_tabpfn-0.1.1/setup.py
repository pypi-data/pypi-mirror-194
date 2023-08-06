# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ensemble_tabpfn', 'ensemble_tabpfn.samplers']

package_data = \
{'': ['*']}

install_requires = \
['lolP==0.0.4', 'tabpfn==0.1.8']

setup_kwargs = {
    'name': 'ensemble-tabpfn',
    'version': '0.1.1',
    'description': 'Adaptation of TabPFN to work with large tabular datasets.',
    'long_description': '# Ensemble TabPFN\n\nTabPFN is a transformer architecture prosposed by [Hollman et al](https://arxiv.org/abs/2207.01848) for classification on small tabular datasets. It is a Prior-Data Fitted Network that has been trained once and does not require fine tuning for new datasets. It works by approximating the distribution of new data to the prior synthetic data it has seen during training. In a machine learning pipeline, this network can be "fit" on a training dataset in under a second and can generate predictions for the test set in a single forward pass in the network. However there are limitations in the current architecture, namely, the training dataset can contain only upto 1000 inputs with upto 100 numerical features. In addition, the network can predict only upto 10 classes in a multi-class classification problem. With EnsembleTabPFN, we address two of these issues where we have extended the original model to work with datasets containing more than 1000 samples and 100 features.\nEnsembleTabPFN is fully compatible with Scikit-learn API and can be used in a modelling pipeline.\n\n\n# Installation\n\n## From source\n\n```bash\n\ngit clone https://github.com/ersilia-os/ensemble-tabpfn.git\ncd ensemble-tabpfn\npip install .\n```\n\n## From PyPI\n\n```python\npip install ensemble-tabpfn\n```\n\n## Using Poetry\n\n```python\n\ngit clone https://github.com/ersilia-os/ensemble-tabpfn.git\ncd ensemble-tabpfn\npoetry install --without dev,test,docs\n```\n\n# Usage\n\n```python\n\nfrom ensemble_tabpfn import EnsembleTabPFN\nfrom sklearn.metrics import accuracy_score\n\nclf = EnsembleTabPFN()\nclf.fit(X_train, y_train)\ny_hat = clf.predict(y_test)\nacc = accuracy_score(y_test, y_hat)\n```',
    'author': 'Ersilia Open Source Initiative',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ersilia-os/ensemble-tabpfn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
