import subprocess
import json


def get_open_issues(repo):
    command = ['gh', 'issue', 'list',
               '--repo', repo,
               '--state', 'open',
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


def create_project(repo):
    owner_name, repo_name = repo.split('/')
    ids = _get_owner_and_repo_ids(owner_name, repo_name)

    command = _graphql_command(_gql_to_create_project(ids['owner_id'], ids['repo_id'], repo_name))
    response = json.loads(subprocess.check_output(command))

    return {
        'project_id': response['data']['createProjectV2']['projectV2']['id'],
        'project_name': response['data']['createProjectV2']['projectV2']['title']
    }


def _get_owner_and_repo_ids(owner_name, repo_name):
    command = _graphql_command(_gql_for_owner_and_repo_ids(owner_name, repo_name))
    response = json.loads(subprocess.check_output(command))

    return {
        'owner_id': response['data']['repository']['owner']['id'],
        'repo_id': response['data']['repository']['id']
    }


def _graphql_command(graphql):
    # Note: the last eleemnt of the command list is concatenated to avoid introducing a space
    return ['gh', 'api', 'graphql', '-f', 'query=' + graphql]


def _gql_for_owner_and_repo_ids(owner_name, repo_name):
    return f'''\
query get_owner_and_repo_ids {{
    repository(owner: "{owner_name}", name: "{repo_name}") {{
        id
        owner {{
            id
        }}
    }}
}}'''


def _gql_to_create_project(owner_id, repo_id, title):
    return f'''\
mutation create_project_v2 {{
    createProjectV2 (
        input: {{ ownerId: "{owner_id}", repositoryId: "{repo_id}", title: "{title}" }}
    ) {{
        projectV2 {{
            id
            title
        }}
    }}
}}'''
