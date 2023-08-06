# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scavenger', 'scavenger.internal', 'scavenger.model']

package_data = \
{'': ['*']}

install_requires = \
['apscheduler>=3.10.0,<4.0.0',
 'dataclass-builder>=1.2.0,<2.0.0',
 'grpcio>=1.51.1,<2.0.0',
 'path>=16.6.0,<17.0.0',
 'protobuf>=4.21.12,<5.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'scavenger-agent-python',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Scavenger Agent Python (BETA)\n\n*(본 Agent는 베타 버전으로 현재 개발 환경에서만의 사용을 권장하며 상용 환경에서의 사용을 권장하지 않습니다.)* Scavenger Agent의 Python 버전으로, Agent가 아닌 [Server Component](../doc/installation.md)는 사전에 준비되어야 합니다.\n\n## 개발 가이드\n\nScavenger Agent Python은 패키지 관리자로 [Poetry](https://python-poetry.org/)를 이용합니다.\n\n- 의존성 설치\n```sh\n$ poetry install\n```\n- 테스트\n```sh\n$ poetry run python -m unittest\n```\n- 빌드\n```sh\n$ poetry build\n```\n\n자세한 내용은 [Poetry Docs](https://python-poetry.org/docs/)를 참고해주세요.\n\n## 에이전트 설치 가이드\n\n### 전제조건\n\n`Python >= 3.7`\n\n### 설치\n\n```\n$ pip install scavenger-agent-python --save\n```\n### 설정\n\n설정은 설정 파일 `scavenger.conf`을 이용한 방식과 Config Instance를 직접 생성하는 두 가지 방식을 지원합니다.\n\n* Example of `scavenger.conf`\n```py\n# scavenger.conf\napiKey=eb99ff0f-aaaa-bbbb-cccc-5d1ec81f6183\nserverUrl=http://10.106.93.41:8081\nenvironment=dev\nappName=apiserver\npackages=views\ncodebase=.\n---\n# source\nconfig = Config.load_config()\nagent = Agent(config)\n```\n* Example of `Config()`\n```py\nconfig = Config(\n    api_key="eb99ff0f-aaaa-bbbb-cccc-5d1ec81f6183",\n    server_url="http://10.106.93.41:8081",\n    environment="dev",\n    app_name="apiserver",\n    packages=["views"],\n    codebase=["."],\n)\nagent = Agent(config)\n```\n\n### 에이전트 시작\nScavenger Agent Python은 Scavenger Agent Java와 달리, Agent 시작 코드를 직접 삽입하는 방식으로 동작합니다. 수집을 시작할 함수의 모듈이 import되기 전에 Agent가 동작해야 하므로 *반드시 프로그램의 시작점에 Agent 시작 코드가 삽입되어야 함을 유의하십시오.*\n```py\nfrom scavenger import Agent, Config\n\nconfig = Config.load_config()\nagent = Agent(config)\nagent.start()\n\n### your source code\nfrom ...\n```\n\n### 한계\n* Graceful Shutdown에 대한 구현은 기존 프레임워크와의 충돌 가능성으로 인해 자동으로 지원하지 않습니다. 대신 아래와 같은 `agent.shutdown()` 함수를 지원하므로 직접 등록하여서 사용하여야 합니다.\n```py\ndef shutdown_gracefully(*args):\n    # Shutdown your application/server first.\n    agent.shutdown()\n    sys.exit(0)\n\nsignal.signal(signal.SIGTERM, shutdown_gracefully)\nagent.start()\n```\n* Scavenger Python Agent는 현재 모듈/클래스의 레퍼런스를 대체하는 방식으로 동작하므로 레퍼런스를 사용하지 않고 함수를 호출하는 경우에는 동작하지 않습니다. 따라서 아래와 같이 Decorator를 이용해 함수의 레퍼런스만 따로 프레임워크에 저장해두는 경우, `def hello_world()`에는 동작하지 않습니다. 이는 추후 함수내 코드를 삽입하는 방식으로 변경되어 지원될 예정입니다.\n```py\nfrom flask import Flask\napp = Flask(__name__)\n\n@app.route(\'/\')\ndef hello_world():\n    return \'Hello World!\'\n```\n* 코드를 직접 읽어서 메서드를 탐색해야 하므로 pyc 파일은 현재 지원되지 않습니다.\n',
    'author': 'dbgsprw',
    'author_email': 'dbgsprw@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
