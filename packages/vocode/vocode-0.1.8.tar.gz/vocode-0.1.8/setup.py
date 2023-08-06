# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vocode', 'vocode.input_device', 'vocode.models', 'vocode.output_device']

package_data = \
{'': ['*']}

install_requires = \
['pyaudio==0.2.13',
 'pydantic==1.10.5',
 'python-dotenv==0.21.1',
 'typing-extensions==4.5.0',
 'websockets==10.4']

setup_kwargs = {
    'name': 'vocode',
    'version': '0.1.8',
    'description': 'The all-in-one voice SDK',
    'long_description': '# vocode Python SDK\n\n```python\nimport asyncio\nimport signal\n\nfrom vocode.conversation import Conversation\nfrom vocode.helpers import create_microphone_input_and_speaker_output\nfrom vocode.models.transcriber import DeepgramTranscriberConfig\nfrom vocode.models.agent import LLMAgentConfig\nfrom vocode.models.synthesizer import AzureSynthesizerConfig\n\nif __name__ == "__main__":\n    microphone_input, speaker_output = create_microphone_input_and_speaker_output(use_first_available_device=True)\n\n    conversation = Conversation(\n        input_device=microphone_input,\n        output_device=speaker_output,\n        transcriber_config=DeepgramTranscriberConfig.from_input_device(microphone_input),\n        agent_config=LLMAgentConfig(prompt_preamble="The AI is having a pleasant conversation about life."),\n        synthesizer_config=AzureSynthesizerConfig.from_output_device(speaker_output)\n    )\n    signal.signal(signal.SIGINT, lambda _0, _1: conversation.deactivate())\n    asyncio.run(conversation.start())\n```\n',
    'author': 'Ajay Raj',
    'author_email': 'ajay@vocode.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
