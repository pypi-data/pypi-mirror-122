# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['annhub_python',
 'annhub_python.core',
 'annhub_python.ml_lib',
 'annhub_python.model',
 'annhub_python.services']

package_data = \
{'': ['*']}

install_requires = \
['fastapi==0.68.1',
 'joblib==1.0.1',
 'loguru==0.4.0',
 'pydantic>=1.8.2,<2.0.0',
 'pytest==6.2.4',
 'requests==2.22.0',
 'uvicorn==0.11.1']

setup_kwargs = {
    'name': 'annhub-python',
    'version': '0.1.6',
    'description': 'Main backend module, which is used for developing web-app logic and deploying AI model.',
    'long_description': '# ANNHUB Python library\n\nMain backend module, which is used for developing web-app logic and deploying AI model by just a few lines of code.\n\n\n# Usage\n\nWe develop a RESTful web controller into a reusable library between many AI models. With these functionalities: **Input model**, **Define data input**, **logging**, **exception handler**.\n\n## Installing\nDelivering and versioning as a [PyPi](https://pypi.org/) package.\nInstall and update using [pip](https://pip.pypa.io/en/stable/getting-started/):\n\n```\n$ pip install annhub-python\n```\n## A simple example\n```python\nfrom annhub_python import PyAnn\n\napp = PyAnn()\n\n# Define the expected AI model\napp.set_model("D:\\ARI\\ANSCENTER\\TrainedModel_c++.ann")\n\n# Define which model ID will be used\napp.set_model_id(5122020)\n\n# Define the input corresponding to the choosen model\napp.set_input_length(4)\n\nif __name__ == "__main__":\n    app.run()\n\n```\n## API \nThe library will product two APIs: **health checking**, **predicting** as well as a [Swagger UI](https://swagger.io/) for API documentation.\n```\nGET: /api/v1/health\nPOST: /api/v1/predict\n```\n![Swagger UI](https://github.com/ans-ari/annhub-python/blob/master/figures/swagger.png?raw=true)\n\n## Detailed Example\n\n**Iris Prediction server**\n\nIn this example, we illustrate how to develop a server by using AI model powered by ANNHUB with only few steps. You can use this [link](https://github.com/ans-ari/annhub-python/tree/master/examples/iris) to access our code.\nThe procedure of using our library to server AI model is as follows:\n\n 1. Put a trained model into your project folder.\n 2. Create main.py file, where some key information will be determined such as model path, model id, input length,... \n 3. Create Dockerfile to containerize your application. (We recommend to reuse our [Dockerfile](examples/iris/Dockerfile)).\n 4. Create docker-compose.yml file, which will construct your docker container by a simple command line. (We also recommend to use as our [instruction](https://github.com/ans-ari/annhub-python/blob/master/examples/iris/docker-compose.yml))\n 5. Run your application be a simple command line: \n ```\n docker-compose up -d\n ``` \n 6. With default settings, your AI can be used at [http://localhost:8080](http://localhost:8080). You can access [http://localhost:8080/docs](http://localhost:8080/docs) to use your Swagger UI documentation. \n',
    'author': 'ARI Technology',
    'author_email': 'dung.ut@ari.com.vn',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ans-ari/annhub-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
