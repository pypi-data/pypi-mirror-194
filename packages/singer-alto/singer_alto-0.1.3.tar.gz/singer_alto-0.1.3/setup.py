# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alto']

package_data = \
{'': ['*']}

install_requires = \
['doit>=0.36.0',
 'dynaconf>=3.1.11,<4.0.0',
 'fsspec>=2023.1.0,<2024.0.0',
 'pex>=2']

entry_points = \
{'console_scripts': ['alto = alto.main:main']}

setup_kwargs = {
    'name': 'singer-alto',
    'version': '0.1.3',
    'description': 'A package for managing singer.io taps and targets',
    'long_description': '# Alto (WIP)\n\nA lightweight yet intelligent way to manage Singer based ELT.\n\n> How is this different than what exists today?\n\nUsing Meltano as the baseline of comparison, there are some noteworthy differences.\n\n- Significantly smaller dependency footprint by an order of magnitude. Alto only has 4 direct dependencies with no C or rust extensions in the dependency tree. The below comparison includes transitives:\n    - **Meltano**: 151\n    - **Alto**: 7\n- Because of its dependency footprint, it can be installed in very tiny containers and packaged formats such as `PEX` are cross platform compatible. It can also be used with `PyOxide` or `Nuitka`.\n- We use `PEX` (PythonEXecutable) for all plugins instead of loose venvs making plugins single files that are straightforward to cache.\n- We use a (simple) caching algorithm that makes the plugins re-usable across machines when combined with a remote filesystem.\n- We use `fsspec` to provide a filesystem abstraction layer that provides the exact same experience locally on a single machine as when plugged into a remote blob store such as `s3`, `gcs`, or any supported `fsspec` storage.\n- An order of magnitude (`>85%`) less code which makes iteration/maintenance or forking easier (in theory)\n- We use `Dynaconf` to manage configuration\n    - This gives us uniform support for json, toml, and yaml out of the box\n    - We get environment management \n    - We get configuration inheritance / deep merging\n    - We get `.env` support\n    - We get unique ways to render vars with `\'@format ` tokens\n\n**Meltano**\n```\n───────────────────────────────────────────────────────────────────────────────\nLanguage                 Files     Lines   Blanks  Comments     Code Complexity\n───────────────────────────────────────────────────────────────────────────────\nPython                     154     26842     2402      4262    20178       1106\n```\n\n**Alto**\n```\n───────────────────────────────────────────────────────────────────────────────\nLanguage                 Files     Lines   Blanks  Comments     Code Complexity\n───────────────────────────────────────────────────────────────────────────────\nPython                      12      2892      226       164     2502        190\n```\n\n\n\n## Example\n\nAn entire timed end-to-end example can be carried out via the below command.\n\nFrom start to finish, it will:\n\n1. Create a directory\n2. Initialize an alto project (create the `alto.toml` file)\n3. Run an extract -> load of an open API to target jsonl\n    1. Build PEX plugins for `tap-carbon-intensity` and `target-jsonl`\n    2. Dynamically generate config for the Singer plugin based on the toml file (supports toml/yaml/json)\n    3. Run discovery and cache catalog to ~/.alto/(project-name)/catalog\n    4. Apply user configuration to the catalog\n    5. Run the pipeline\n    6. Clean up the staging directory\n    7. Manage and persist the state\n\n```bash\n# Create a dir, init a project, run an end-2-end pipeline, show some output as proof\nmkdir example_project \\\n&& cd $_; yes | alto init; \\\ntime alto tap-carbon-intensity:target-jsonl; \\\ncat output/* | head -8; ls -l output; cd -; \\\ntree example_project\n```\n\nResulting in the below output:\n\n```\nexample_project\n├── .alto\n│   ├── logs\n│   │   └── dev\n│   └── plugins\n│       ├── 263b729b56cf48f4bc3d08b687045ad3f81713ce\n│       └── 60e33af4f316a41812ee404136d7a747011ba811\n├── .alto.json\n├── alto.secrets.toml\n├── alto.toml\n└── output\n    ├── entry-20230228T205342.jsonl\n    ├── generationmix-20230228T205342.jsonl\n    └── region-20230228T205342.jsonl\n\n5 directories, 8 files\n```\n\n`>>> cat alto.toml`\n\n```toml\n[default]\nproject_name = "4c167d53"\nextensions = []\nnamespace = "raw"\n\n[default.taps.tap-carbon-intensity]\npip_url = "git+https://gitlab.com/meltano/tap-carbon-intensity.git#egg=tap_carbon_intensity"\nnamespace = "carbon_intensity"\ncapabilities = ["state", "catalog"]\nselect = ["*.*"]\n\n[default.taps.tap-carbon-intensity.config]\n\n[default.targets.target-jsonl]\npip_url = "target-jsonl==0.1.4"\n\n[default.targets.target-jsonl.config]\ndestination_path = "output"\n```\n\n## The tale of a tiny binary\n\nOne can produce a sub 50mb binary with `nuitka` that can be built in a multistage docker image and copied into the final stage producing incredibly small containers.\n\n`nuitka3 --standalone --onefile --output-dir=build --output-filename=alto alto/main.py`\n\nResulting image based on bundled Dockerfile inspected with `dive`:\n\n```\n❯ CI=true dive tinysinger:test\n  Using default CI config\nImage Source: docker://tinysinger:test\nFetching image... (this can take a while for large images)\nAnalyzing image...\n  efficiency: 100.0000 %\n  wastedBytes: 0 bytes (0 B)\n  userWastedPercent: 0.0000 %\nInefficient Files:\nCount  Wasted Space  File Path\nNone\nResults:\n  PASS: highestUserWastedPercent\n  SKIP: highestWastedBytes: rule disabled\n  PASS: lowestEfficiency\nResult:PASS [Total:3] [Passed:2] [Failed:0] [Warn:0] [Skipped:1]\n```\n\nSo the example above could be ran like this:\n\n```bash\nmkdir example_project \\\n&& cd $_; yes | docker run -i -v$(pwd):/stage z3z1ma/alto:test-1 -- --root /stage init; \\\ntime docker run -v$(pwd):/stage z3z1ma/alto:test-1 -- --root /stage tap-carbon-intensity:target-jsonl; \\\ncat output/* | head -8; ls -l output; cd -; \\\ntree example_project\n```\n',
    'author': 'z3z1ma',
    'author_email': 'butler.alex2010@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
