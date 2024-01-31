import requests


class RedmineAPI:

    def __init__(self, access_key, config):
        self.access_key = access_key
        self.config = config

    def generate_headers(self):
        return {
            'X-Redmine-API-Key': self.access_key,
            'Content-Type': 'application/json'
        }

    def create_project(self, data):
        url = self.config['redmine_projects_json_url']

        headers = self.generate_headers()

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            projects_data = response.json()
            return projects_data, None
        else:
            return None, f"Error: {response.status_code} - {response.text}"

    def update_project(self, identifier, **kwargs):
        url = self.config['redmine_projects_url'] + '/' + identifier + '.json'

        headers = self.generate_headers()
        project_data = {key: value for key, value in kwargs.items() if value is not None}

        if not project_data:
            return "No data provided for update"

        data = {"project": project_data}
        response = requests.put(url, json=data, headers=headers)

        if response.status_code == 204:
            return "Project updated successfully"
        else:
            return f"Error: {response.status_code} - {response.text}"

    def delete_project(self, identifier):
        url = self.config["redmine_projects_url"] + '/' + identifier + '.json'

        headers = self.generate_headers()
        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            return "Project deleted successfully"
        else:
            return f"Error: {response.status_code} - {response.text}"

    def get_projects_list(self):
        url = self.config['redmine_projects_json_url']

        response = requests.get(url)

        if response.status_code == 200:
            projects_data = response.json()
            return projects_data
        elif response.status_code == 400:
            return "Error: The projects resource was not found."
        elif response.status_code == 500:
            return "Error: Internal server error."
        else:
            return f"Error: {response.status_code} - {response.text}"

    def show_project_by_id(self, identifier):
        url = self.config['redmine_projects_url'] + '/' + identifier + '.json'

        response = requests.get(url)

        if response.status_code == 404:
            return f"Project with identifier '{identifier}' not found."
        elif response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        projects_data = response.json()
        return projects_data

    def get_projects_by_name(self, projects, name):
        if not isinstance(projects, list):
            print("Error: The provided 'projects' variable is not a list.")
            return None

        for project in projects:
            if 'name' in project and project['name'] == name:
                return project

            print(f"There is no project in the list with the name '{name}'.")
            return False
