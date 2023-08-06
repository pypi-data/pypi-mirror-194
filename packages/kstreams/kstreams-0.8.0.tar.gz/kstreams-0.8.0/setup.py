# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kstreams', 'kstreams.backends', 'kstreams.prometheus', 'kstreams.test_utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'aiokafka<1.0',
 'future>=0.18.2,<0.19.0',
 'prometheus-client<1.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'kstreams',
    'version': '0.8.0',
    'description': 'Build simple kafka streams applications',
    'long_description': '# Kstreams\n\n`kstreams` is a library/micro framework to use with `kafka`. It has simple kafka streams implementation that gives certain guarantees, see below.\n\n![Build status](https://github.com/kpn/kstreams/actions/workflows/pr-tests.yaml/badge.svg?branch=master)\n[![codecov](https://codecov.io/gh/kpn/kstreams/branch/master/graph/badge.svg?token=t7pxIPtphF)](https://codecov.io/gh/kpn/kstreams)\n![python version](https://img.shields.io/badge/python-3.8%2B-yellowgreen)\n\n---\n\n**Documentation**: https://kpn.github.io/kstreams/\n\n---\n\n## Installation\n\n```bash\npip install kstreams\n```\n\nYou will need a worker, we recommend [aiorun](https://github.com/cjrh/aiorun)\n\n```bash\npip install aiorun\n```\n\n## Usage\n\n```python\nimport aiorun\nfrom kstreams import create_engine, Stream\n\n\nstream_engine = create_engine(title="my-stream-engine")\n\n@stream_engine.stream("local--kstream")\nasync def consume(stream: Stream):\n    async for cr in stream:\n        print(f"Event consumed: headers: {cr.headers}, payload: {cr.value}")\n\n\nasync def produce():\n    payload = b\'{"message": "Hello world!"}\'\n\n    for i in range(5):\n        metadata = await create_engine.send("local--kstreams", value=payload)\n        print(f"Message sent: {metadata}")\n\n\nasync def start():\n    await stream_engine.start()\n    await produce()\n\n\nasync def shutdown(loop):\n    await stream_engine.stop()\n\n\nif __name__ == "__main__":\n    aiorun.run(start(), stop_on_unhandled_errors=True, shutdown_callback=shutdown)\n```\n\n## Features\n\n- [x] Produce events\n- [x] Consumer events with `Streams`\n- [x] `Prometheus` metrics and custom monitoring\n- [x] TestClient\n- [x] Custom Serialization and Deserialization\n- [x] Easy to integrate with any `async` framework. No tied to any library!!\n- [x] Yield events from streams\n- [ ] Store (kafka streams pattern)\n- [ ] Stream Join\n- [ ] Windowing\n\n## Development\n\nThis repo requires the use of [poetry](https://python-poetry.org/docs/basic-usage/) instead of pip.\n*Note*: If you want to have the `virtualenv` in the same path as the project first you should run `poetry config --local virtualenvs.in-project true`\n\nTo install the dependencies just execute:\n\n```bash\npoetry install\n```\n\nThen you can activate the `virtualenv` with\n\n```bash\npoetry shell\n```\n\nRun test:\n\n```bash\n./scripts/test\n```\n\nRun code formatting (`black` and `isort`)\n\n```bash\n./scripts/format\n```\n\n### Commit messages\n\nWe use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for the commit message.\n\nThe use of [commitizen](https://commitizen-tools.github.io/commitizen/) is recommended. Commitizen is part of the dev dependencies.\n\n```bash\ncz commit\n```\n',
    'author': 'Marcos Schroh',
    'author_email': 'marcos.schroh@kpn.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
