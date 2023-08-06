from subprocess import check_output
import subprocess
import re 

def add_subcommand_push(subparsers):
    parser = subparsers.add_parser('push')
    parser.set_defaults(func=push)
    parser.add_argument("-n", "--name", help="Input your modelreg name", required=True)
    parser.add_argument("-p", "--path", help="Input your modelreg folder relative path", required=True)
    parser.add_argument("-c", "--cmt", help="Input your comments of modelreg changes", required=True)

def push(args):
    if not re.match("^[a-zA-Z0-9/.-]+$", args.name):
        print("Format modelreg name is not valid, please refer link: https://mlem.ai/doc/gto/user-guide/#git-tags-format")
        return
    subprocess.check_output(["dvc", "add", args.path])
    subprocess.check_output(["dvc", "push"])
    subprocess.check_output(["gto", "annotate", args.name, "--path", args.path])
    subprocess.check_output(["git", "add", ".", "-A"])
    subprocess.check_output(["git", "commit", "-m", args.cmt])
    model_name = args.name
    command = "gto register {}".format(model_name)
    subprocess.check_output(command, shell=True)
    modelreg_latest = "{}@latest".format(model_name)
    version = subprocess.check_output(["gto", "show", modelreg_latest, "--version"]).decode("utf-8").strip()
    branch = args.name + "@" + version
    subprocess.check_output(["git", "push", "origin", branch])
