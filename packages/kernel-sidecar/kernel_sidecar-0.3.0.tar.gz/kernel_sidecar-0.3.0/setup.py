# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kernel_sidecar', 'kernel_sidecar.models']

package_data = \
{'': ['*']}

install_requires = \
['jupyter-client>=7.3.4', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'kernel-sidecar',
    'version': '0.3.0',
    'description': 'A sidecar ',
    'long_description': '<p align="center">\nKernel Sidecar\n</p>\n\n<p align="center">\n<img alt="Pypi" src="https://img.shields.io/pypi/v/kernel-sidecar">\n<a href="https://github.com/kafonek/kernel-sidecar/actions/workflows/tests.yaml">\n    <img src="https://github.com/kafonek/kernel-sidecar/actions/workflows/tests.yaml/badge.svg" alt="Tests" />\n</a>\n<img alt="Python versions" src="https://img.shields.io/pypi/pyversions/kernel-sidecar">\n</p>\n\n# Kernel-Sidecar\n\nThis package offers the building blocks for creating a "Kernel Sidecar" Jupyter framework. In normal Jupyter Notebook architecture, one or many frontends manage the document model (code cells, outputs, metadata, etc) and send requests to a single Kernel. Each frontend observes responses on different ZMQ channels (`iopub`, `shell`, etc) but may end up with some inconsistency based on the Kernel only sending certain responses to the client that made the request.\n\nIn a `kernel-sidecar` architecture, all frontend clients talk to the `kernel-sidecar` client, and only the `kernel-sidecar` client communicates with the Kernel over ZMQ. That pattern offers several potential features:\n - Keep a document model within `kernel-sidecar` or the backend architecture\n - Add "extension"-esque capabilities on the backend such as auto-linting code on execute\n - Eliminate inconsistencies in what messages individual frontends receive because of Kernel replies\n - Model all requests, replies, and the Notebook document with Pydantic\n\n## Installation\n\n```bash\npip install kernel-sidecar\n```\n\n# Key Concepts\n## KernelSidecarClient\n\nA manager that uses `jupyter_client` under the hood to create ZMQ connections and watch for messages coming in over different ZMQ channels (`iopub`, `shell`, etc. An important assumption here is that `kernel-sidecar` is the only client talking to the Kernel, which means every message observed coming from the Kernel should be a reply (based on `parent_header_msg.msg_id`) to a request sent from this client.\n\nWhen the `KernelSidecarClient` send a request to the Kernel, it is wrapped in an `KernelAction` class. Every message received from the Kernel is delegated to the requesting Action and triggers callbacks attached to the Action class.\n\n## Actions\n\nActions in `kernel-sidecar` encompass a request-reply cycle, including an `await action` syntax, where the Action is complete when the Kernel has reported its status returning to `idle` and optionally emitted a reply appropriate for the request. For instance, an `execute_request` is "done" when the `status` has been reported as `idle` *and* the Kernel has emitted an `execute_reply`, both with the `parent_header_msg.msg_id` the same as the `execute_request` `header.msg_id`.\n\nIn a nutshell, an `actions.KernelAction` takes in a `requests.Request` and zero-to-many `handlers.Handler` subclasses (or just `async functions`) and creates an `awaitable` instance. `kernel.send(action)` submits the Request over ZMQ, and registers the Action so that all observed messages get routed to that Action to be handled by the Handlers/callbacks.\n\nMost of the time, you should be able to just use convience functions in the `KernelSidecarClient` class to create the actions. See `tests/test_actions.py` for many examples of using Actions and Handlers.\n\n## Models\n\n`kernel-sidecar` has Pydantic models for:\n - The Jupyter Notebook document (`models/notebook.py`), which should be consistent with `nbformat` parsing / structure\n - Request messages sent to the Kernel over ZMQ (`models/requests.py`)\n - Messages received over ZMQ from the Kernel (`models/messages.py`)\n\n\n\n',
    'author': 'Matt Kafonek',
    'author_email': 'matt.kafonek@noteable.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kafonek/kernel-sidecar',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
