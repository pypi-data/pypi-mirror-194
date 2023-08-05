# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sunvox', 'sunvox.buffered', 'sunvox.tools']

package_data = \
{'': ['*'],
 'sunvox': ['lib/copy-libs.sh',
            'lib/linux/lib_arm64/sunvox.so',
            'lib/linux/lib_x86/*',
            'lib/linux/lib_x86_64/*',
            'lib/macos/lib_arm64/*',
            'lib/macos/lib_x86_64/*',
            'lib/windows/lib_x86/*',
            'lib/windows/lib_x86_64/*']}

extras_require = \
{'buffered': ['numpy'], 'tools': ['numpy', 'scipy', 'tqdm']}

setup_kwargs = {
    'name': 'sunvox-dll-python',
    'version': '0.3.4.2.1.0.2',
    'description': 'Python ctypes-based wrapper for the SunVox library',
    'long_description': 'Overview of sunvox-dll-python\n=============================\n\n..  start-badges\n\n|buildstatus| |docs|\n\n.. |buildstatus| image:: https://img.shields.io/travis/metrasynth/sunvox-dll-python.svg?style=flat\n    :alt: build status\n    :scale: 100%\n    :target: https://travis-ci.org/metrasynth/sunvox-dll-python\n\n.. |docs| image:: https://readthedocs.org/projects/sunvox-dll-python/badge/?version=latest\n    :alt: Documentation Status\n    :scale: 100%\n    :target: https://sunvox-dll-python.readthedocs.io/en/latest/?badge=latest\n\n..  end-badges\n\nPart of the Metrasynth_ project.\n\n.. _Metrasynth: https://metrasynth.github.io/\n\n\nPurpose\n-------\n\nProvides access to all of the SunVox DLL functions described\nin the ``sunvox.h`` header file.\n\n\nRequirements\n------------\n\n- Python 3.7+\n\n- One of these supported operating systems:\n\n    - macOS (64-bit)\n\n    - Linux (32-bit, 64-bit)\n\n    - Windows (32-bit, 64-bit)\n\n\nAbout SunVox\n------------\n\nFrom the `SunVox home page`_:\n\n    SunVox is a small, fast and powerful modular synthesizer with pattern-based sequencer (tracker).\n    It is a tool for those people who like to compose music wherever they are, whenever they wish.\n    On any device. SunVox is available for Windows, OS X, Linux, Maemo, Meego, Raspberry Pi,\n    Windows Mobile (WindowsCE), PalmOS, iOS and Android.\n\n.. _SunVox home page: http://www.warmplace.ru/soft/sunvox/\n',
    'author': 'Matthew Scott',
    'author_email': 'matt@11craft.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/metrasynth/sunvox-dll-python',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
