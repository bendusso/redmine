import pytest
import yaml
import faker


@pytest.fixture(scope='session')
def config():
    with open('../../config.yml', 'r') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope='session')
def faker_instance():
    return faker.Faker()
