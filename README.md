# userctl

Manage users on a remote system.

This is a small program that executes commands on remote systems in order to create or remove users, as well as list existing users.

An optional SSH public key file may be provided when creating a user, if it is the contents are written to the new user's `~/.ssh/authorized_keys` file.

## Usage

To see all options:
    
    ./userctl.py --help

To create a user:

    ./userctl.py --create mario --hostname mushroom.kingdom.com --ssh-pub-key ~/.ssh/id_ed25519.pub

To remove a user:

    ./userctl.py --remove mario --hostname mushroom.kingdom.com

To see all users, their UIDs, and comments:

    ./userctl.py --list-users --hostname mushroom.kingdom.com

