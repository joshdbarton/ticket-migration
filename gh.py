import subprocess
import json


def get_open_issues(repo):
    command = ['gh', 'issue', 'list',
               '--repo', repo,
               '--state', 'open',
               '--json', 'title,body',
               '--limit', '100']

    return json.loads(subprocess.check_output(command))


def create_issue(repo_id, issue):
    title = issue['title']
    body = issue['body']
    label_ids = []

    command = _graphql_command(_gql_to_create_issue(repo_id, title, body, label_ids))
    response = json.loads(subprocess.check_output(command))

    return {
        'id': response['data']['createIssue']['issue']['id'],
        'repo_id': repo_id,
        'title': title,
        'body': body
    }


def add_issue_to_project(project, issue):
    project_id = project['id']
    issue_id = issue['id']

    command = _graphql_command(_gql_to_add_issue_to_project(project_id, issue_id))
    response = json.loads(subprocess.check_output(command))

    return {
        'project_item_id': response['data']['addProjectV2ItemById']['item']['id'],
        'project_id': project_id,
        'issue_id': issue_id
    }


def create_project(repo):
    owner_name, repo_name = repo.split('/')
    ids = _get_owner_and_repo_ids(owner_name, repo_name)
    repo_id = ids['repo_id']
    owner_id = ids['owner_id']

    command = _graphql_command(_gql_to_create_project(owner_id, repo_id, repo_name))
    response = json.loads(subprocess.check_output(command))

    return {
        'id': response['data']['createProjectV2']['projectV2']['id'],
        'title': response['data']['createProjectV2']['projectV2']['title'],
        'repo_id': repo_id,
        'owner_id': owner_id
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


def _gql_to_create_issue(repo_id, title, body, label_ids):
    return f'''\
mutation create_issue_in_project {{
    createIssue (input: {{
        repositoryId: {json.dumps(repo_id)},
        title: {json.dumps(title)},
        body: {json.dumps(body)},
        labelIds: {json.dumps(label_ids)}
    }}) {{
        issue {{
            id
        }}
    }}
}}'''


def _gql_to_add_issue_to_project(project_id, issue_id):
    return f'''\
mutation add_project_v2_item_by_id {{
    addProjectV2ItemById (
        input: {{ projectId: "{project_id}", contentId: "{issue_id}" }}
    ) {{
        item {{
            id
        }}
    }}
}}'''


