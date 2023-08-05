# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tail_jsonl', 'tail_jsonl._private']

package_data = \
{'': ['*']}

install_requires = \
['corallium>=0.1.0', 'dotted-notation>=0.9.2']

entry_points = \
{'console_scripts': ['tail-jsonl = tail_jsonl.scripts:start']}

setup_kwargs = {
    'name': 'tail-jsonl',
    'version': '1.2.2',
    'description': 'Pretty Print Tailed JSONL Logs',
    'long_description': '# tail-jsonl\n\nTail JSONL Logs\n\n## Background\n\nI wanted to find a tool that could:\n\n1. Convert a stream of JSONL logs into a readable `logfmt`-like output with minimal configuration\n1. Show exceptions on their own line\n\nI investigated a lot of alternatives such as: [humanlog](https://github.com/humanlogio/humanlog), [lnav](https://docs.lnav.org/en/latest/formats.html#), [goaccess](https://goaccess.io/get-started), [angle-grinder](https://github.com/rcoh/angle-grinder#rendering), [jq](https://github.com/stedolan/jq), [textualog](https://github.com/rhuygen/textualog), etc. but nothing would both cleanly format the JSONL data and show the exception.\n\n![.github/assets/demo.gif](https://raw.githubusercontent.com/KyleKing/tail-jsonl/main/.github/assets/demo.gif)\n\n## Installation\n\n[Install with `pipx`](https://pypi.org/project/pipx/)\n\n```sh\npipx install tail-jsonl\n```\n\n## Usage\n\nPipe JSONL output from any file, kubernetes (such as [stern](https://github.com/stern/stern)), Docker, etc.\n\n```sh\n# Example piping input in shell\necho \'{"message": "message", "timestamp": "2023-01-01T01:01:01.0123456Z", "level": "debug", "data": true, "more-data": [null, true, -123.123]}\' | tail-jsonl\ncat tests/data/logs.jsonl | tail-jsonl\n\n# Optionally, pre-filter or format with jq, grep, awk, or other tools\ncat tests/data/logs.jsonl | jq \'.record\' --compact-output | tail-jsonl\n\n# An example stern command (also consider -o=extjson)\nstern envvars --context staging --container gateway --since="60m" --output raw | tail-jsonl\n\n# Or with Docker Compose (note that awk, cut, and grep all buffer. For awk, add \'; system("")\')\ndocker compose logs --follow | awk \'match($0, / \\| \\{.+/) { print substr($0, RSTART+3, RLENGTH); system("") }\' | tail-jsonl\n```\n\n## Configuration\n\nOptionally, specify a path to a custom configuration file. See an example configuration file at: [tests/config_default.toml](https://github.com/KyleKing/tail-jsonl/blob/main/tests/config_default.toml)\n\n```sh\necho \'...\' | tail-jsonl --config-path=~/.tail-jsonl.toml\n```\n\n## Project Status\n\nSee the `Open Issues` and/or the [CODE_TAG_SUMMARY]. For release history, see the [CHANGELOG].\n\n## Contributing\n\nWe welcome pull requests! For your pull request to be accepted smoothly, we suggest that you first open a GitHub issue to discuss your idea. For resources on getting started with the code base, see the below documentation:\n\n- [DEVELOPER_GUIDE]\n- [STYLE_GUIDE]\n\n## Code of Conduct\n\nWe follow the [Contributor Covenant Code of Conduct][contributor-covenant].\n\n### Open Source Status\n\nWe try to reasonably meet most aspects of the "OpenSSF scorecard" from [Open Source Insights](https://deps.dev/pypi/tail_jsonl)\n\n## Responsible Disclosure\n\nIf you have any security issue to report, please contact the project maintainers privately. You can reach us at [dev.act.kyle@gmail.com](mailto:dev.act.kyle@gmail.com).\n\n## License\n\n[LICENSE]\n\n[changelog]: ./docs/CHANGELOG.md\n[code_tag_summary]: ./docs/CODE_TAG_SUMMARY.md\n[contributor-covenant]: https://www.contributor-covenant.org\n[developer_guide]: ./docs/DEVELOPER_GUIDE.md\n[license]: https://github.com/kyleking/tail-jsonl/LICENSE\n[style_guide]: ./docs/STYLE_GUIDE.md\n',
    'author': 'Kyle King',
    'author_email': 'dev.act.kyle@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyleking/tail-jsonl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.12,<4.0.0',
}


setup(**setup_kwargs)
