import subprocess
import json


def get_issues(repo):
    command = ['gh', 'issue', 'list',
               '--repo', repo,
               '--json', 'title,body',
               '--limit', '100']

    return json.loads(subprocess.check_output(command))


def create_issue(repo, issue):
    title = issue['title']
    body = issue['body']

    command = ['gh', 'issue', 'create',
               '--repo', repo,
               '--title', title,
               '--body', body]

    subprocess.check_call(command)

