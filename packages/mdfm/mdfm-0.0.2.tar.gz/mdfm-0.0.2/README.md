# mdfm

mdfm is a linux tools for My Dot Files Manager. (backup or restore)

### Usage

```
python -m mdfm -h
usage: mdfm [-h] [-D] [-I] [-C CONFIG_FILE] [-P PROCESS_NUMBER] [-B | -R]

mdfm is a linux tools for My Dot Files Manager. (backup or restore)

options:
  -h, --help            show this help message and exit
  -D, --run-demo
  -I, --init-config
  -C CONFIG_FILE, --config-file CONFIG_FILE
                        (Default: ~/.mdfm.json)
  -P PROCESS_NUMBER, --multi-process-number PROCESS_NUMBER
                        multiprocessing support. Default is 1.
  -B, --backup-action   action is backup. backup value eq True. By Default.
  -R, --restore-action  action is restore. backup value eq False.
```

### Config file Format

```
[
    {
        "app_name":     "mdfm-demo",
        "description":  "test demo.",
        "source_dir":   "demo_dir/src",
        "target_dir":   "demo_dir/tgt",
        "relative_dirs": [
            "test_dir",
            ".test_empty_dir"
        ],
        "relative_files": [
            ".test_file"
        ]
    }
]
```

### Environment setup

Python version: 3

### How to install dependences?

```bash
python -m pip install -r requirements.txt
pip install mdfm
```

### How to build dist file(\*.whl)?

```bash
python -m pip install setuptools wheel twine
python setup.py sdist bdist_wheel
```

or

```bash
python -m venv .venv
chmod +x .venv/bin/activate
.venv/bin/activate
pip install -U pip setuptools wheel
pip wheel .
```
