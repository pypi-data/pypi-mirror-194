# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whisperer_ml',
 'whisperer_ml.config',
 'whisperer_ml.paths',
 'whisperer_ml.utils']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0,<0.3.0',
 'jupyter>=1.0.0,<2.0.0',
 'librosa==0.8.0',
 'numpy==1.22.3',
 'openai-whisper>=20230124,<20230125',
 'pyannote-audio>=2.1.1,<3.0.0',
 'pydub==0.25.1',
 'scipy==1.8.0',
 'torch==1.13.0',
 'torchaudio==0.13.0',
 'tqdm>=4.64.1,<5.0.0',
 'transformers>=4.25.1,<5.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['whisperer_ml = whisperer_ml.main:app']}

setup_kwargs = {
    'name': 'whisperer-ml',
    'version': '0.1.4',
    'description': "Go from raw audio to a text-audio dataset with OpenAI's Whisper",
    'long_description': "\n# whisperer\n\nGo from raw audio files to a speaker separated text-audio datasets automatically.\n\n![plot](https://github.com/miguelvalente/whisperer/blob/master/logo.png?raw=true)\n\n\n## Table of Contents\n\n- [Summary](#summary)\n- [Key Features](#key-features)\n- [Instalation](#instalation)\n- [How to use:](#how-to-use)\n   - [Using Multiple-GPUS](#using-multiple-gpus)\n   - [Configuration](#configuration)\n- [To Do](#to-do)\n- [Acknowledgements](#acknowledgements)\n\n## Summary\n\nThis repo takes a directory of audio files and converts them to a text-audio dataset with normalized distribution of audio lengths. *See ```AnalyzeDataset.ipynb``` for examples of the dataset distributions across audio and text length*\n\nThe output is a text-audio dataset that can be used for training a speech-to-text model or text-to-speech.\nThe dataset structure is as follows:\n```\n│── /dataset\n│   ├── metadata.txt\n│   └── wavs/\n│      ├── audio1.wav\n│      └── audio2.wav\n```\n\nmetadata.txt\n```\npeters_0.wav|Beautiful is better than ugly.\npeters_1.wav|Explicit is better than implicit.\n\n```\n\n## Key Features\n\n* Audio files are automatically split by speakers\n* Speakers are auto-labeled across the files\n* Audio splits on silences\n* Audio splitting is configurable\n* The dataset creation is done so that it follows Gaussian-like distributions on clip length. Which, in turn, can lead to Gaussian-like distributions on the rest of the dataset statistics. Of course, this is highly dependent on your audio sources.\n* Leverages the GPUs available on your machine. GPUs also be set explicitly if you only want to use some.\n\n\n## Instalation\n\nInstall from PyPi with pip\n```\npip install whisperer-ml\n```\n\n## How to use:\n\n\n1. Create data folder and move audio files to it\n```\nmkdir data data/raw_files\n```\n2. There are four commands\n   1. Convert\n      ```\n      whisperer_ml convert path/to/data/raw_files\n      ```\n   2. Diarize \n      ```\n      whisperer_ml diarize path/to/data/raw_files\n      ```\n   3. Auto-Label \n      ```\n      whisperer_ml auto-label path/to/data/raw_files number_speakers\n      ```\n   4. Transcribe \n      ```\n      whisperer_ml transcribe path/to/data/raw_files your_dataset_name\n      ```\n   5. Help lists all commands \n      ```\n      whisperer_ml --help \n      ```\n   6. You can run help on a specific command\n   ```\n      whisperer_ml convert --help\n   ```\n\n\n3. Use the ```AnalyseDataset.ipynb``` notebook to visualize the distribution of the dataset\n4. Use the ```AnalyseSilence.ipynb``` notebook to experiment with silence detection configuration\n\n### Using Multiple-GPUS\n\nThe code automatically detects how many GPU's are available and distributes the audio files in ```data/wav_files``` evenly across the GPUs.\nThe automatic detection is done through ```nvidia-smi```.\n\nYou can to make the available GPU's explicit by setting the environment variable ```CUDA_AVAILABLE_DEVICES```.\n\n### Configuration\n\nModify `config.py` file to change the parameters of the dataset creation. Including silence detection.\n## To Do\n\n- [x] Speech Diarization\n- [x] Replace click with typer\n\n\n## Acknowledgements\n\n\n - [AnalyseDataset.ipynb adapted from coqui-ai example](https://github.com/coqui-ai)\n - [OpenAI Whisper](https://github.com/openai/whisper)\n - [PyAnnote](https://github.com/pyannote/pyannote-audio)\n - [SpeechBrain](https://github.com/speechbrain/speechbrain)\n",
    'author': 'miguelvalente',
    'author_email': 'miguelvalente@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
