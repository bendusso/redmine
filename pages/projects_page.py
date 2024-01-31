from pages.base_page import BasePage


class ProjectsPage(BasePage):

    def navigate_to_projects_page(self, url):
        self.open_page(url)

    def create_project(self, project_info):
        self.page.click("a.icon.icon-add")
        project_data = {
            "input[id='project_name']": project_info['project_name'],
            "textarea[id='project_description']": project_info['project_description'],
            "input[id='project_identifier']": project_info['identifier'],
        }
        self.fill_form(project_data)
        self.page.click(('input[name="commit"]'))

    def get_project_by_name(self, name):
        projects = self.page.locator('a.project').element_handles()
        for project in projects:
            project_name = project.text_content()

            if project_name == name:
                return project

        print("There is no project in the list with the given name.")
        return False

    def get_project_description(self):
        return self.page.locator('.wiki > p')

    def click_sign_in(self):
        self.page.click(('a[class="login"]'))

    def click_projects(self):
        self.page.click(('a[class="projects"]'))
