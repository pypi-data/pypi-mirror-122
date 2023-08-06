# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['vid2pdf']
install_requires = \
['Pillow>=8.3,<9.0', 'click>=8.0,<9.0', 'ffmpy>=0.3,<0.4', 'tqdm>=4.62,<5.0']

entry_points = \
{'console_scripts': ['vid2pdf = vid2pdf:main_cli']}

setup_kwargs = {
    'name': 'vid2pdf',
    'version': '1.1.0',
    'description': 'Simple helper utility to convert a video file to PDF image series',
    'long_description': "# vid2pdf\nSimple helper utility to convert a video file to PDF image series\n\n## External Requirements\n\n`vid2pdf` requires ffmpeg to be extracted to the `/utils/ffmpeg` folder. The latest version of ffmpeg can be downloaded from [ffmpeg.org](https://www.ffmpeg.org/download.html). Existing local ffmpeg installations are not currently supported.\n\nIf not using a precompiled build, Python must be installed on your local machine. You can download the latest version of Python for your OS from [python.org](https://www.python.org/downloads/)\n\n## Installation\n\nThis project utilizes [`poetry`](https://python-poetry.org/) for dependency & environment management. Clone or download this repository to your local machine and create a new environment:\n\n```bash\n$ cd <project_dir>\n$ poetry install\n```\n\nThough it's recommended to utilize `poetry`, the project may also be installed via `pip`:\n\n```bash\n$ cd <project_dir>\n$ pip install .\n```\n\nAlternatively, prebuilt binaries are provided at https://github.com/sco1/vid2pdf/releases\n\n## Usage\n\n`vid2pdf` can be invoked using Python:\n```bash\n$ python vid2pdf.py\n```\n\nOr, if a prebuilt binary is present, this may be called directly\n```bash\n$ vid2pdf.exe\n```\n\n### Input Parameters\nUnless otherwise noted, all input parameters are prompted in the CLI\n#### `input_video`\nThe default behavior is to open a GUI dialog for the user to specify a the input video file. An optional `-cli` flag may be passed to bypass this GUI and instead prompt for the video file path in the CLI.\n\n#### `output_dir`\nPDF output directory. If this value is not specified, this defaults to the parent directory of the input video.\n\n#### `start_time`\nVideo start time for capture, as `hh:mm:ss.sss`. If this value is not specified, the beginning of the video is used.\n\n#### `end_time`\nVideo end time for capture, as `hh:mm:ss.sss`. If this value is not specified, the end of the video is used.\n\n### Examples\n\n```bash\n$ python vid2pdf.py\nEnter the output directory path [X:\\vid2pdf\\test]:\nEnter start time (hh:mm:ss.sss). Leave blank to use the video start:\nEnter end time (hh:mm:ss.sss). Leave blank to use the video end: 00:00:01.000\n<ffmpeg output snipped>\nLoading 30 frames...\n100%|███████████████████████████████████████| 29/29 [00:00<00:00, 852.82it/s]\nGenerating PDF ... done\n```\n\n```bash\n$ python vid2pdf.py -cli\nEnter the video file path: X:\\vid2pdf\\test\\test_video.mp4\nEnter the output directory path [X:\\vid2pdf\\test]:\nEnter start time (hh:mm:ss.sss). Leave blank to use the video start:\nEnter end time (hh:mm:ss.sss). Leave blank to use the video end: 00:00:01.000\n<ffmpeg output snipped>\nLoading 30 frames...\n100%|███████████████████████████████████████| 29/29 [00:00<00:00, 852.82it/s]\nGenerating PDF ... done\n```\n",
    'author': 'sco1',
    'author_email': 'sco1.git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sco1/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
