# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acron']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=1.0.15,<2.0.0', 'pytz>=2021.1,<2022.0']

setup_kwargs = {
    'name': 'acron',
    'version': '0.1.5',
    'description': 'Lightweight scheduler',
    'long_description': 'Lightweight scheduler for python asyncio\n\nBased on croniter to support the crontab syntax.\n\n============\nInstallation\n============\n\nInstalling acron.\n\n.. code:: shell\n\n    $ pip install acron\n\n=====\nUsage\n=====\n\nTo get started you need a scheduler and at least one job.\nThe ``Scheduler`` class can be used as async context manager.\nCall ``scheduler.wait()`` to keep it running forever.\nTo submit jobs call ``scheduler.update_jobs(jobs)`` with the complete set of jobs.\n\nRunning a simple example running a function every hour...\n\n.. code:: python\n\n    import asyncio\n\n    from acron.scheduler import Scheduler, Job\n\n    async def do_the_thing():\n        print("Doing the thing")\n\n    async def run_jobs_forever():\n        do_thing = Job(\n            name="Do the thing",\n            schedule="0/1 * * * *",\n            func=do_the_thing,\n        )\n\n        async with Scheduler() as scheduler:\n            await scheduler.update_jobs({do_thing})\n            await scheduler.wait()\n\n    if __name__ == "__main__":\n        try:\n            asyncio.run(run_jobs_forever())\n        except KeyboardInterrupt:\n            print("Bye.")\n\n=================\nLocal development\n=================\n\nThe project uses poetry to run the test, the linter and to build the artifacts.\n\nThe easiest way to start working on acron is to use docker with the dockerfile\nincluded in the repository (manual usage of poetry is explained here:\nhttps://python-poetry.org/docs/ ).\n\nTo use docker, first generate the docker image. Run this command from the top\nlevel directory in the repository:\n\n.. code-block:: console\n\n   docker build -t acron-builder -f docker/Dockerfile .\n\nNow you can use it to build or run the linter/tests:\n\n.. code-block:: console\n\n    $ alias acron-builder="docker run --rm -it -v $PWD/dist:/build/dist acron-builder"\n\n    $ acron-builder run pytest tests\n    =============================================================================================== test session starts ================================================================================================\n    platform linux -- Python 3.9.7, pytest-5.4.3, py-1.10.0, pluggy-0.13.1\n    rootdir: /build\n    plugins: asyncio-0.15.1\n    collected 4 items\n    tests/test_acron.py ....                                                                                                                                                                                     [100%]\n    ================================================================================================ 4 passed in 0.04s =================================================================================================\n\n    $ acron-builder build\n    Building acron (0.1.0)\n      - Building sdist\n      - Built acron-0.1.0.tar.gz\n      - Building wheel\n      - Built acron-0.1.0-py3-none-any.whl\n\n    $ ls dist\n    acron-0.1.0-py3-none-any.whl  acron-0.1.0.tar.gz\n\n',
    'author': 'Aitor Iturri',
    'author_email': 'aitor.iturri@appgate.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/appgate/acron',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
