#!/usr/bin/env python3

import json
import argparse
import time
import gh


def main(args):
    repos = []

    if args.target_repo is not None:
        repos = [args.target_repo]
    elif args.config_file is not None:
        with open(args.config_file) as file:
            repos = json.load(file)['targetRepos']

    for repo in repos:
        migrate_tickets(args.source_repo, repo, args.throttle_seconds)


def migrate_tickets(source_repo, target_repo, throttle_seconds):
    target_project = gh.create_project(target_repo)
    issues = gh.get_open_issues(source_repo)

    for issue in issues:
        gh.create_issue(target_project, issue)

        time.sleep(throttle_seconds)

    print(f'Tickets migrated for {target_repo}!')


def get_args():
    parser = argparse.ArgumentParser(
        'Migrate Issues from one GH repository to another')

    parser.add_argument('source_repo',
                        help="the <owner>/<name> name for the source repo",
                        type=str)

    parser.add_argument('--throttle_seconds',
                        help="number of second to wait between requests (default 5)",
                        default=5,
                        type=int)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--config_file',
                       help="path to a JSON config file",
                       default="config.json",
                       type=str)
    group.add_argument('--target_repo',
                       help="the <owner>/<name> name for the target repo",
                       type=str)

    return parser.parse_args()


if __name__ == '__main__':
    main(get_args())

