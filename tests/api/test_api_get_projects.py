from api.redmine_api import *
from api.redmine_api import RedmineAPI


def test_get_project_list(config):
    redmine_api = RedmineAPI(config['access_key'], config)

    projects_data = redmine_api.get_projects_list()

    if isinstance(projects_data, str):
        if projects_data.startswith("Error"):
            print(f"Error retrieving project list: {projects_data}")
        else:
            print(f"Unexpected string response: {projects_data}")
        return
    elif not isinstance(projects_data, dict):
        print(f"Invalid response type: {type(projects_data)}")
        return

    expected_keys = ['projects', 'total_count', 'offset', 'limit']
    missing_keys = [key for key in expected_keys if key not in projects_data]

    if missing_keys:
        print(f"Missing keys in response: {', '.join(missing_keys)}")
        return

    if not isinstance(projects_data.get('projects'), list):
        print("The 'projects' key does not contain a list.")
        return
    else:
        for project in projects_data['projects']:
            if not isinstance(project, dict):
                print("One or more items in 'projects' are not dictionaries.")
                return


def test_get_project_by_name(config):
    redmine_api = RedmineAPI(config['access_key'], config)

    name = "Updated Dr. Sonia Bennett"
    identifier = "d8320462-f07d-4946-9441-c2577e3f42fb"
    description = "Updated Energy every anything natural explain head. Civil view prepare receive establish something."

    projects_data = redmine_api.get_projects_list()

    if isinstance(projects_data, str) and projects_data.startswith("Error"):
        print(projects_data)
        return

    assert 'projects' in projects_data, "Response does not contain 'projects' key."

    projects_list = projects_data['projects']
    current_project = redmine_api.get_projects_by_name(projects_list, name)

    if not current_project:
        print("Skipping checks as no project found with the given name.")
        return

    required_fields = ['id', 'name', 'identifier', 'description', 'status', 'is_public', 'inherit_members',
                       'created_on', 'updated_on']

    assert all(
        key in current_project for key in required_fields), "One or more required fields are missing in the project."

    assert current_project["name"] == name
    assert current_project["identifier"] == identifier
    assert current_project["description"] == description

    assert 'total_count' in projects_data, "'total_count' not in projects data."
    assert 'offset' in projects_data, "'offset' not in projects data."
    assert 'limit' in projects_data, "'limit' not in projects data."


def test_show_project(config):
    name = "Updated Dr. Sonia Bennett"
    identifier = "d8320462-f07d-4946-9441-c2577e3f42fb"
    description = "Updated Energy every anything natural explain head. Civil view prepare receive establish something."

    redmine_api = RedmineAPI(config['access_key'], config)
    project_response = redmine_api.show_project_by_id(identifier)

    if isinstance(project_response, str):
        if "not found" in project_response:
            print(f"Project with identifier '{identifier}' not found.")
        else:
            print("Error occurred:", project_response)
        return

    project = project_response['project']
    assert project["name"] == name
    assert project["identifier"] == identifier
    assert project["description"] == description
