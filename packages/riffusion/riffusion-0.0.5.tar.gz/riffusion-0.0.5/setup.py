# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['riffusion',
 'riffusion.external',
 'riffusion.streamlit',
 'riffusion.streamlit.pages',
 'riffusion.util']

package_data = \
{'': ['*']}

install_requires = \
['accelerate>=0.16.0,<0.17.0',
 'argh>=0.27.2,<0.28.0',
 'dacite>=1.8.0,<2.0.0',
 'demucs>=4.0.0,<5.0.0',
 'diffusers>=0.9.0',
 'flask-cors>=3.0.10,<4.0.0',
 'flask>=2.2.2,<3.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pillow>=9.4.0,<10.0.0',
 'plotly>=5.13.0,<6.0.0',
 'pydub>=0.25.1,<0.26.0',
 'pysoundfile>=0.9.0.post1,<0.10.0',
 'scipy>=1.10.0,<2.0.0',
 'soundfile>=0.11.0,<0.12.0',
 'sox>=1.4.1,<2.0.0',
 'streamlit>=1.17.0,<1.18.0',
 'torch>=1.13.1,<2.0.0',
 'torchaudio>=0.13.1,<0.14.0',
 'torchvision>=0.14.1,<0.15.0',
 'transformers>=4.26.1,<5.0.0',
 'watchdog>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['riffusion = riffusion.cli:main',
                     'riffusion-playground = riffusion.playground:main',
                     'riffusion-server = riffusion.server:main']}

setup_kwargs = {
    'name': 'riffusion',
    'version': '0.0.5',
    'description': 'Stable diffusion for real-time music generation.',
    'long_description': '# :guitar: Riffusion\n\n<!-- markdownlint-disable MD033 MD034 -->\n\n<a href="https://github.com/riffusion/riffusion/actions/workflows/ci.yml?query=branch%3Amain"><img alt="CI status" src="https://github.com/riffusion/riffusion/actions/workflows/ci.yml/badge.svg" /></a>\n<img alt="Python 3.9 | 3.10" src="https://img.shields.io/badge/Python-3.9%20%7C%203.10-blue" />\n<a href="https://github.com/riffusion/riffusion/tree/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-yellowgreen" /></a>\n\nRiffusion is a library for real-time music and audio generation with stable diffusion.\n\nRead about it at https://www.riffusion.com/about and try it at https://www.riffusion.com/.\n\nThis is the core repository for riffusion image and audio processing code.\n\n* Diffusion pipeline that performs prompt interpolation combined with image conditioning\n* Conversions between spectrogram images and audio clips\n* Command-line interface for common tasks\n* Interactive app using streamlit\n* Flask server to provide model inference via API\n* Various third party integrations\n\nRelated repositories:\n\n* Web app: https://github.com/riffusion/riffusion-app\n* Model checkpoint: https://huggingface.co/riffusion/riffusion-model-v1\n\n## Citation\n\nIf you build on this work, please cite it as follows:\n\n```txt\n@article{Forsgren_Martiros_2022,\n  author = {Forsgren, Seth* and Martiros, Hayk*},\n  title = {{Riffusion - Stable diffusion for real-time music generation}},\n  url = {https://riffusion.com/about},\n  year = {2022}\n}\n```\n\n## Install\n\nTested in CI with Python 3.9 and 3.10.\n\nIt\'s highly recommended to set up a virtual Python environment with `conda` or `virtualenv`:\n\n```shell\nconda create --name riffusion python=3.9\nconda activate riffusion\n```\n\nInstall Python package:\n\n```shell\npip install -U riffusion\n```\n\nor clone the repository and install from source:\n\n```shell\ngit clone https://github.com/riffusion/riffusion.git\ncd riffusion\npython -m pip install --editable .\n```\n\nIn order to use audio formats other than WAV, [ffmpeg](https://ffmpeg.org/download.html) is required.\n\n```shell\nsudo apt-get install ffmpeg          # linux\nbrew install ffmpeg                  # mac\nconda install -c conda-forge ffmpeg  # conda\n```\n\nIf torchaudio has no backend, you may need to install `libsndfile`. See [this issue](https://github.com/riffusion/riffusion/issues/12).\n\nIf you have an issue, try upgrading [diffusers](https://github.com/huggingface/diffusers). Tested with 0.9 - 0.11.\n\nGuides:\n\n* [Simple Install Guide for Windows](https://www.reddit.com/r/riffusion/comments/zrubc9/installation_guide_for_riffusion_app_inference/)\n\n## Backends\n\n### CPU\n\n`cpu` is supported but is quite slow.\n\n### CUDA\n\n`cuda` is the recommended and most performant backend.\n\nTo use with CUDA, make sure you have torch and torchaudio installed with CUDA support. See the\n[install guide](https://pytorch.org/get-started/locally/) or\n[stable wheels](https://download.pytorch.org/whl/torch_stable.html).\n\nTo generate audio in real-time, you need a GPU that can run stable diffusion with approximately 50\nsteps in under five seconds, such as a 3090 or A10G.\n\nTest availability with:\n\n```python\nimport torch\ntorch.cuda.is_available()\n```\n\n### MPS\n\nThe `mps` backend on Apple Silicon is supported for inference but some operations fall back to CPU,\nparticularly for audio processing. You may need to set\n`PYTORCH_ENABLE_MPS_FALLBACK=1`.\n\nIn addition, this backend is not deterministic.\n\nTest availability with:\n\n```python\nimport torch\ntorch.backends.mps.is_available()\n```\n\n## Command-line interface\n\nRiffusion comes with a command line interface for performing common tasks.\n\nSee available commands:\n\n```shell\nriffusion -h\n```\n\nGet help for a specific command:\n\n```shell\nriffusion image-to-audio -h\n```\n\nExecute:\n\n```shell\nriffusion image-to-audio --image spectrogram_image.png --audio clip.wav\n```\n\n## Riffusion Playground\n\nRiffusion contains a [streamlit](https://streamlit.io/) app for interactive use and exploration.\n\nRun with:\n\n```shell\nriffusion-playground\n```\n\nAnd access at http://127.0.0.1:8501/\n\n<img alt="Riffusion Playground" style="width: 600px" src="https://i.imgur.com/OOMKBbT.png" />\n\n## Run the model server\n\nRiffusion can be run as a flask server that provides inference via API. This server enables the [web app](https://github.com/riffusion/riffusion-app) to run locally.\n\nRun with:\n\n```shell\nriffusion-server --host 127.0.0.1 --port 3013\n```\n\nYou can specify `--checkpoint` with your own directory or huggingface ID in diffusers format.\n\nUse the `--device` argument to specify the torch device to use.\n\nThe model endpoint is now available at `http://127.0.0.1:3013/run_inference` via POST request.\n\nExample input (see [InferenceInput](https://github.com/hmartiro/riffusion-inference/blob/main/riffusion/datatypes.py#L28) for the API):\n\n```json\n{\n  "alpha": 0.75,\n  "num_inference_steps": 50,\n  "seed_image_id": "og_beat",\n\n  "start": {\n    "prompt": "church bells on sunday",\n    "seed": 42,\n    "denoising": 0.75,\n    "guidance": 7.0\n  },\n\n  "end": {\n    "prompt": "jazz with piano",\n    "seed": 123,\n    "denoising": 0.75,\n    "guidance": 7.0\n  }\n}\n```\n\nExample output (see [InferenceOutput](https://github.com/hmartiro/riffusion-inference/blob/main/riffusion/datatypes.py#L54) for the API):\n\n```json\n{\n  "image": "< base64 encoded JPEG image >",\n  "audio": "< base64 encoded MP3 clip >"\n}\n```\n\n## Tests\n\nTests live in the `test/` directory and are implemented with `unittest`.\n\nTo run all tests:\n\n```shell\npython -m unittest test/*_test.py\n```\n\nTo run a single test:\n\n```shell\npython -m unittest test.audio_to_image_test\n```\n\nTo preserve temporary outputs for debugging, set `RIFFUSION_TEST_DEBUG`:\n\n```shell\nRIFFUSION_TEST_DEBUG=1 python -m unittest test.audio_to_image_test\n```\n\nTo run a single test case within a test:\n\n```shell\npython -m unittest test.audio_to_image_test -k AudioToImageTest.test_stereo\n```\n\nTo run tests using a specific torch device, set `RIFFUSION_TEST_DEVICE`. Tests should pass with\n`cpu`, `cuda`, and `mps` backends.\n\n## Development Guide\n\nInstall additional packages for dev with `python -m pip install -r requirements-dev.txt`.\n\n* Linters: `ruff`, `flake8`, `pylint`\n* Formatter: `black`\n* Type checker: `mypy`\n* Docstring checker: `pydocstyle`\n\nThese are configured in `pyproject.toml`.\n\nThe results of `mypy .`, `black .`, and `ruff .` *must* be clean to accept a PR.\n\nCI is run through GitHub Actions from `.github/workflows/ci.yml`.\n\nContributions are welcome through pull requests.\n',
    'author': 'Hayk Martiros',
    'author_email': 'hayk.mart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
