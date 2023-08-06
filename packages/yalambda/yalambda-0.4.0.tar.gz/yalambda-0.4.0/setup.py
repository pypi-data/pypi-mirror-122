# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yalambda']

package_data = \
{'': ['*']}

install_requires = \
['dataclass-factory>=2.11,<3.0']

setup_kwargs = {
    'name': 'yalambda',
    'version': '0.4.0',
    'description': 'Utility library for Yandex.Cloud',
    'long_description': '# `yalambda`\n\nYalambda lets you write Yanex.Cloud Functions with less boilerplate\n\nFeatures:\n- everything is type-annotated, so you\'ll get autocompletion in IDEs\n- base64 de/encoding and other details are handled for you\n\n\n# Echo server example\n\n```py\nfrom yalambda import function, YaRequest, YaResponse\n\n\n@function()\nasync def handler(req: YaRequest) -> YaResponse:\n    return YaResponse(200, req.body)\n```\n\n\n# Automatically parse dataclasses\n```py\nfrom dataclasses import dataclass\nfrom yalambda import function, YaResponse\n\n\n@dataclass\nclass Point:\n    x: float\n    y: float\n\n\n@function()\nasync def handler(point: Point) -> YaResponse:\n    dist = (point.x**2 + point.y**2)**0.5\n    return YaResponse(200, {"distance_to_origin": dist})\n```\n\nWe use the `dataclass-factory` package to parse the JSON request\n\n\n# Access both the dataclass and the request\n\n```py\nfrom dataclasses import dataclass\nfrom yalambda import function, YaRequest, YaResponse\n\n\n@dataclass\nclass Point:\n    x: float\n    y: float\n\n\n@function()\nasync def handler(point: Point, req: YaRequest) -> YaResponse:\n    if req.http_method != "POST":\n        return YaResponse(405, "Only POST requests are allowed")\n\n    dist = (point.x**2 + point.y**2)**0.5\n    return YaResponse(200, {"distance_to_origin": dist})\n```\n\n\n# Initialize something asynchronously on first call\n\n```py\nfrom yalambda import function, YaRequest, YaResponse\n\n\nasync def init():\n    global answer\n    answer = 42\n\n\n@function(init)\nasync def handler(req: YaRequest) -> YaResponse:\n    return YaResponse(200, "Answer:".format(answer))\n```',
    'author': 'decorator-factory',
    'author_email': '42166884+decorator-factory@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decorator-factory/yalambda',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
