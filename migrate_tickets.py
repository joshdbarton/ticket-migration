import subprocess
import argparse
import json
import time


def migrate_tickets(source_repo, target_repo, throttle_seconds):
    issues = json.loads(subprocess.check_output(f'gh issue list --repo {source_repo} --json "title,body" --limit 100'))
    for issue in issues:
        subprocess.run('gh issue create --repo {} --title "{}" --body "{}"'.format(target_repo, issue['title'], issue['body']))
        time.sleep(throttle_seconds)
    print(f'Tickets migrated for {target_repo}!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Migrate Issues from one GH repository to another')
    parser.add_argument('source_repo', help="the <owner>/<name> repository name for the source repo", type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--target_repo', help="the <owner>/<name> repository name for the target repo", type=str)
    group.add_argument('--config_file', help="path to a JSON config file", type=str)
    parser.add_argument('--throttle_seconds', help="number of second to wait between requests (default 5)", default=5, type=int)

    args = parser.parse_args()
    if args.target_repo is not None:
        migrate_tickets(args.source_repo, args.target_repo, args.throttle_seconds)
    elif args.config_file is not None:
        with open(args.config_file) as file:
            repos = json.load(file)
            for repo in repos['targetRepos']:
                migrate_tickets(args.source_repo, repo, args.throttle_seconds)

