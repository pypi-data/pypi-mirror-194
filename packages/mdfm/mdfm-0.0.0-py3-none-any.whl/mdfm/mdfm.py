import os
import subprocess
import multiprocessing
import pathlib
import argparse
from termcolor import colored

DEMOS = """
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
"""


def rsync(source_dir, target_dir):
    subprocess.call([
        "rsync",
        "-auP",
        "--delete",
        source_dir,
        target_dir,
    ])


def restore(instance):
    app_name = instance['app_name']
    tgt_path = pathlib.Path(instance['source_dir']).expanduser().resolve()
    src_path = pathlib.Path(
        instance['target_dir'], app_name).expanduser().resolve()

    if not src_path.exists():
        print("restore path: " + str(src_path) + " is not exists.")
        return
    if not tgt_path.exists():
        os.makedirs(tgt_path)
    if not tgt_path.is_dir():
        return

    print(colored("app_name: %s restore start." % app_name, "green"))

    for relative_dir in instance['relative_dirs']:
        abs_src_path = str(pathlib.Path.joinpath(
            src_path, relative_dir).resolve()) + '/'
        abs_tgt_path = str(pathlib.Path.joinpath(
            tgt_path, relative_dir).resolve()) + '/'
        if not os.path.exists(abs_tgt_path):
            os.makedirs(abs_tgt_path)
        print(colored("app_name: %s start resync relative_dir: %s ." %
              (app_name, relative_dir), "yellow"))
        print(abs_src_path)
        print(abs_tgt_path)
        rsync(abs_src_path, abs_tgt_path)
        print(colored("app_name: %s end resync relative_dir: %s ." %
              (app_name, relative_dir), "yellow"))

    for relative_file in instance['relative_files']:
        abs_src_path = str(pathlib.Path.joinpath(
            src_path, relative_file).resolve())
        abs_tgt_path = str(pathlib.Path.joinpath(
            tgt_path, relative_file).resolve())
        print(colored("app_name: %s start resync relative_file: %s ." %
              (app_name, relative_file), "yellow"))
        rsync(abs_src_path, abs_tgt_path)
        print(colored("app_name: %s end resync relative_file: %s ." %
              (app_name, relative_file), "yellow"))

    print(colored("app_name: %s restore end." % app_name, "green"))


def backup(instance):
    app_name = instance['app_name']
    src_path = pathlib.Path(instance['source_dir']).expanduser().resolve()
    tgt_path = pathlib.Path(
        instance['target_dir'], app_name).expanduser().resolve()

    if not src_path.exists():
        print("backup path: " + str(src_path) + " is not exists.")
        return
    if not tgt_path.exists():
        os.makedirs(tgt_path)
    if not tgt_path.is_dir():
        return

    print(colored("app_name: %s backup start." % app_name, "green"))

    for relative_dir in instance['relative_dirs']:
        abs_src_path = str(pathlib.Path.joinpath(
            src_path, relative_dir).resolve()) + '/'
        abs_tgt_path = str(pathlib.Path.joinpath(
            tgt_path, relative_dir).resolve()) + '/'
        if not os.path.exists(abs_tgt_path):
            os.makedirs(abs_tgt_path)
        print(colored("app_name: %s start resync relative_dir: %s ." %
              (app_name, relative_dir), "yellow"))
        rsync(abs_src_path, abs_tgt_path)
        print(colored("app_name: %s end resync relative_dir: %s ." %
              (app_name, relative_dir), "yellow"))

    for relative_file in instance['relative_files']:
        abs_src_path = str(pathlib.Path.joinpath(
            src_path, relative_file).resolve())
        abs_tgt_path = str(pathlib.Path.joinpath(
            tgt_path, relative_file).resolve())
        print(colored("app_name: %s start resync relative_file: %s ." %
              (app_name, relative_file), "yellow"))
        rsync(abs_src_path, abs_tgt_path)
        print(colored("app_name: %s end resync relative_file: %s ." %
              (app_name, relative_file), "yellow"))

    print(colored("app_name: %s backup end." % app_name, "green"))


def init_instances(args):
    import json
    instances = []

    if args.demo:
        print("DEMOS: " + DEMOS)
        print("Start run demos:")
        instances.extend(json.loads(DEMOS))
    else:
        config_file = str(pathlib.Path(
            args.config_file).expanduser().resolve())

        if args.init_config:
            with open(config_file, "w") as f:
                f.write(DEMOS)
                f.close()
            print(colored("Notes: Config's file init-created. path: " +
                  args.config_file, "green"))
            print(colored("Warning: You'd better modify this file. ", "yellow"))
        elif not os.path.exists(config_file):
            print(colored("ConfigOpenError: Config's file is not exists.", "red"))
            print(colored(
                "Notes: You try '-I or --init-config' create a config's file. (.mdfm.json)", "green"))
        else:
            with open(config_file, "r") as f:
                import json
                try:
                    obj = json.loads(f.read())
                    instances.extend(obj)
                except Exception as e:
                    print(
                        colored("ConfigFormatError: You must modify this file.", "red"))
                    print(colored("    OR", "red"))
                    print(colored("Notes: Try '-D or --run-demo' run a demo.", "red"))
                    raise
                else:
                    pass
                finally:
                    pass

    return instances


def init_args():
    parser = argparse.ArgumentParser(prog="mdfm",
                                     description=colored("mdfm is a linux tools for My Dot Files Manager. (backup or restore)", "green"))

    parser.add_argument('-D', '--run-demo', dest="demo",
                        action='store_true')
    parser.add_argument('-I', '--init-config', dest="init_config",
                        action='store_true')

    parser.add_argument('-C', '--config-file', dest="config_file",
                        type=str, default='~/.mdfm.json', help='(Default: ~/.mdfm.json)')

    parser.add_argument('-P', '--multi-process-number', dest="process_number",
                        type=int, default='1', help="multiprocessing support. Default is 1.")

    action_mt = parser.add_mutually_exclusive_group()
    action_mt.add_argument("-B", "--backup-action", dest="action_mt",
                           default=True, action='store_true', help="action is backup. backup value eq True. By Default.")
    action_mt.add_argument("-R", "--restore-action", dest="action_mt",
                           default=False, action='store_false',
                           help="action is restore. backup value eq False.")

    return parser.parse_args()


def main():
    args = init_args()
    instances = init_instances(args)

    if len(instances) == 0:
        return

    processes_pool = multiprocessing.Pool(processes=args.process_number)

    if args.action_mt:
        output = processes_pool.map(backup, instances)
    else:
        output = processes_pool.map(restore, instances)


if __name__ == "__main__":
    main()
