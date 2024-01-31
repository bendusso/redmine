from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage


def test_create_project(browser, config, faker_instance):
    projects_page = ProjectsPage(browser)
    login_page = LoginPage(browser)

    projects_page.navigate_to_projects_page(config['projects_url'])

    credentials = {
        "login": config['credentials']['login'],
        "password": config['credentials']['password'],
    }

    projects_page.click_sign_in()
    login_page.set_page(projects_page.page)
    login_page.login(credentials)

    expected_message = "Successful creation."

    try:
        project_name = faker_instance.name()
        project_description = faker_instance.text().replace('\n', ' ')
        identifier = faker_instance.uuid4()

        project_details = {
            "project_name": project_name,
            "project_description": project_description,
            "identifier": identifier,
        }

        projects_page.create_project(project_details)
        flash_notice = projects_page.get_flash_notice()
        notice_text = flash_notice.inner_text() if flash_notice else None
        assert notice_text == expected_message, f"Unexpected flash notice: {notice_text}"
        projects_page.click_projects()
        created_project = projects_page.get_project_by_name(project_name)
    finally:
        assert created_project.text_content() == project_name
        created_project.click()
        created_project_description = projects_page.get_project_description()
        assert created_project_description.text_content() == project_description
        assert projects_page.page.url.endswith(identifier)
