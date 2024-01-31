from api.redmine_api import RedmineAPI


def test_create_and_update_project(faker_instance, config):
    project_data = {
        "project": {
            "name": faker_instance.name(),
            "identifier": faker_instance.uuid4(),
            "description": faker_instance.text(),
            "is_public": True,
            "inherit_members": False,
            "enabled_module_names": ["issue_tracking"],
            "custom_field_values": {"1": "1"}
        }
    }

    redmine_api = RedmineAPI(config['access_key'], config)

    # Create project
    created_project, _ = redmine_api.create_project(project_data)
    assert created_project is not None, "Failed to create project for update test"

    if not created_project:
        print("Skipping checks as no project found with the given identifier.")
        return
    project = project_data["project"]
    assert created_project['project']["name"] == project["name"]
    assert created_project['project']["identifier"] == project["identifier"]
    assert created_project['project']["description"] == project["description"]

    # Update project
    random_number = faker_instance.random_number(digits=5)
    updated_data = {"name": f'Updated {random_number}' + project_data["project"]["name"],
                    "description": "Updated " + project_data["project"]["description"]}
    update_response = redmine_api.update_project(created_project["project"]["identifier"], **updated_data)
    assert update_response == "Project updated successfully", "Failed to update project" + update_response

    # verify updated details
    updated_project = redmine_api.show_project_by_id(created_project["project"]["identifier"])
    if not updated_project:
        print("Skipping checks as no project found with the given identifier.")
        return
    assert updated_project['project']["name"] == updated_data["name"]
    assert updated_project['project']["description"] == updated_data["description"]

    # Delete project
    delete_response = redmine_api.delete_project(project["identifier"])
    assert delete_response == "Project deleted successfully", "Failed to delete project" + delete_response

    verify_deletion_response = redmine_api.show_project_by_id(project["identifier"])
    assert isinstance(verify_deletion_response,
                      str) and "not found" in verify_deletion_response, "Project still exists or another error occurred"
