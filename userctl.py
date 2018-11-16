#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


DESCRIPTION = "Utility to manage and list users."
PROGNAME = "userctl"


def execute_remote_cmd(cmd, host):
    """Execute the given command 'cmd' on the given remote host 'host'."""
    proc = subprocess.Popen(["ssh", host, cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    comm = proc.communicate()[0]
    return comm.decode('utf-8').strip().split('\n')


def add_ssh_key(keyfile, host, username):
    """
    Read the contents of the given 'keyfile' and write it to the specified
    remote user's authorized_keys file.
    """
    f = open(keyfile, "r")
    key = f.readlines()[0]
    f.close()
    return execute_remote_cmd("echo '" + key + "' >> /home/" + username + "/.ssh/authorized_keys", host)


def list_users(host):
    """Parse the contents of /etc/passwd on the given remote 'host'."""
    return execute_remote_cmd("awk -F: '{ print \"username: \" $1 \" \"\"userid: \" $3 \" \" \"comment: \" $5 }' /etc/passwd", host)


def modify_user(action, host, username):
    """Perform the specified action on a given 'username' and 'host'."""
    if action == "create":
        return execute_remote_cmd("useradd -m " + username, host)
    elif action == "remove":
        return execute_remote_cmd("userdel -fr " + username, host)


def parse_args(args: list) -> None:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=DESCRIPTION, prog=PROGNAME)
    actions = parser.add_argument_group("Actions")
    actions.add_argument("-L", "--list-users", action="store_true",
                         help="List users.")
    actions.add_argument("-C", "--create", metavar="USERNAME",
                         help="Create the specified user account.")
    actions.add_argument("-R", "--remove", metavar="USERNAME",
                         help="Remove the specified user account.")
    options = parser.add_argument_group("Options")
    options.add_argument("-H", "--hostname",
                         help="Hostname of the server to run commands on.", required=True)
    options.add_argument("-s", "--ssh-pub-key", dest='ssh_key', metavar="PATH_TO_SSH_PUBKEY",
                         help="Specify an optional SSH public key to have added to the user's authorized_keys.")
    return parser.parse_args(args)


def main():
    """Action!"""
    parsed_args = parse_args(sys.argv[1:])
    ssh_key = None

    if parsed_args.ssh_key:
        ssh_key = parsed_args.ssh_key
        if not os.path.isfile(ssh_key):
            print("The provided SSH public key does not appear to be a file!")
            ssh_key = None

    if parsed_args.create:
        user = parsed_args.create
        host = parsed_args.hostname
        modify_user("create", host, user)
        if ssh_key:
            add_ssh_key(ssh_key, host, user)
        print("The user '" + user + "' has been created!")
    elif parsed_args.remove:
        user = parsed_args.remove
        modify_user("remove", parsed_args.hostname, user)
        print("The user '" + user + "' has been removed!")
    elif parsed_args.list_users:
        for line in list_users(parsed_args.hostname):
            print(line)


if __name__ == '__main__':
    main()
