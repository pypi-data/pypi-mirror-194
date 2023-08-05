# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['espeak_phonemizer']

package_data = \
{'': ['*'],
 'espeak_phonemizer': ['espeakng/espeak-ng-data/*',
                       'espeakng/espeak-ng-data/lang/*',
                       'espeakng/espeak-ng-data/lang/aav/*',
                       'espeakng/espeak-ng-data/lang/art/*',
                       'espeakng/espeak-ng-data/lang/azc/*',
                       'espeakng/espeak-ng-data/lang/bat/*',
                       'espeakng/espeak-ng-data/lang/bnt/*',
                       'espeakng/espeak-ng-data/lang/ccs/*',
                       'espeakng/espeak-ng-data/lang/cel/*',
                       'espeakng/espeak-ng-data/lang/cus/*',
                       'espeakng/espeak-ng-data/lang/dra/*',
                       'espeakng/espeak-ng-data/lang/esx/*',
                       'espeakng/espeak-ng-data/lang/gmq/*',
                       'espeakng/espeak-ng-data/lang/gmw/*',
                       'espeakng/espeak-ng-data/lang/grk/*',
                       'espeakng/espeak-ng-data/lang/inc/*',
                       'espeakng/espeak-ng-data/lang/ine/*',
                       'espeakng/espeak-ng-data/lang/ira/*',
                       'espeakng/espeak-ng-data/lang/iro/*',
                       'espeakng/espeak-ng-data/lang/itc/*',
                       'espeakng/espeak-ng-data/lang/jpx/*',
                       'espeakng/espeak-ng-data/lang/map/*',
                       'espeakng/espeak-ng-data/lang/myn/*',
                       'espeakng/espeak-ng-data/lang/poz/*',
                       'espeakng/espeak-ng-data/lang/roa/*',
                       'espeakng/espeak-ng-data/lang/sai/*',
                       'espeakng/espeak-ng-data/lang/sem/*',
                       'espeakng/espeak-ng-data/lang/sit/*',
                       'espeakng/espeak-ng-data/lang/tai/*',
                       'espeakng/espeak-ng-data/lang/trk/*',
                       'espeakng/espeak-ng-data/lang/urj/*',
                       'espeakng/espeak-ng-data/lang/zle/*',
                       'espeakng/espeak-ng-data/lang/zls/*',
                       'espeakng/espeak-ng-data/lang/zlw/*',
                       'espeakng/espeak-ng-data/voices/!v/*',
                       'espeakng/espeak-ng-data/voices/mb/*',
                       'espeakng/x64/*',
                       'espeakng/x86/*']}

setup_kwargs = {
    'name': 'espeak-phonemizer-windows',
    'version': '1.0.1',
    'description': 'Uses espeak-ng to transform text into IPA phonemes.',
    'long_description': "# eSpeak Phonemizer Windows\n\n\nUses [espeak-ng](https://github.com/espeak-ng/espeak-ng) to transform text into [IPA](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) phonemes.\n\nThis is a fork of [espeak-phonemizer](https://github.com/rhasspy/espeak-phonemizer) that adds support for Windows.\n\n## Installation\n\nNext, install espeak_phonemizer_windows:\n\n```sh\npip install espeak_phonemizer_windows\n```\n\nIf installation was successful, you should be able to run:\n\n```sh\nespeak-phonemizer --version\n```\n\n## Basic Phonemization\n\nSimply pass your text into the standard input of `espeak-phonemizer`:\n\n```sh\necho 'This is a test.' | espeak-phonemizer -v en-us\nðɪs ɪz ɐ tˈɛst\n```\n\n### Separators\n\nPhoneme and word separators can be changed:\n\n```sh\necho 'This is a test.' | espeak-phonemizer -v en-us -p '_' -w '#'\nð_ɪ_s#ɪ_z#ɐ#t_ˈɛ_s_t\n```\n\n### Punctuation and Stress\n\nSome punctuation can be kept (.,;:!?) in the output:\n\n```sh\necho 'This: is, a, test.' | espeak-phonemizer -v en-us --keep-punctuation\nðˈɪs: ˈɪz, ˈeɪ, tˈɛst.\n```\n\nStress markers can also be dropped:\n\n```sh\necho 'This is a test.' | espeak-phonemizer -v en-us --no-stress\nðɪs ɪz ɐ tɛst\n```\n\n### Delimited Input\n\nThe `--csv` flag enables delimited input with fields separated by a '|' (change with `--csv-delimiter`):\n\n```sh\necho 's1|This is a test.' | espeak-phonemizer -v en-us --csv\ns1|This is a test.|ðɪs ɪz ɐ tˈɛst\n```\n\nPhonemes are added as a final column, allowing you to pass arbitrary metadata through to the output.\n\n",
    'author': 'mush42',
    'author_email': 'ibnomer2011@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mush42/espeak-phonemizer-windows',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
