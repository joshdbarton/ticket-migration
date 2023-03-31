# The Great Ticket Migrator

_Bow before it_

## Dependencies

This script depends on the [gh cli](https://cli.github.com/). If you don't have it, install it before you continue.

There are no other dependencies...so that's nice.

## Usage

There are two modes.

1. Migrate to multiple target repos using a config file.
1. Migrate to a single target repo via command line arguments.

### Targeting Multiple Repos (this is probably what you want)

1. Copy the `config.json.example` file to `config.json`.
1. Add the repos you wish to target to the `targetRepos` array in the `config.json` file. The repos should be listed in the form `org_name/repo_name`.
1. Make sure the `migrate_tickets.py` file has execute permissions.
1. Run this command specifying the source repo as a command line argument.

    ```shell
    ./migrate_tickets.py source_org/source_repo
    ```

### Targeting a Single Repo

1. Make sure the `migrate_tickets.py` file has execute permissions.
1. Run this command specifying the source repo as a command line argument.

    ```shell
    ./migrate_tickets.py source_org/source_repo --target_repo target_org/target_repo
    ```

