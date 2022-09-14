import subprocess
import argparse
import json
import time

parser = argparse.ArgumentParser('Migrate Issues from one GH repository to another')
parser.add_argument(help="the <owner>/<name> repository name for the existing repo", type=str, dest='old_repo')
parser.add_argument(help="the <owner>/<name> repository name for the new repo", type=str, dest='new_repo')

args = parser.parse_args()

issues = json.loads(subprocess.check_output(f'gh issue list --repo {args.old_repo} --json "title,body" --limit 100'))
for issue in issues:
    subprocess.run('gh issue create --repo {} --title "{}" --body "{}"'.format(args.new_repo, issue['title'], issue['body']))
    time.sleep(5)

print('Tickets migrated!')
