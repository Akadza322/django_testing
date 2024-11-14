import pytest
from model_bakery import baker
from students.models import Course, Student
from rest_framework.test import APIClient
import random


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture()
def curs_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture()
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.mark.django_db
def test_courses(client, curs_factory):
    curs = curs_factory(_quantity=1)
    id_curs = curs[0].id
    response = client.get(f'/courses/?id={id_curs}')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == curs[0].name

@pytest.mark.django_db
def test_curses_list(client, curs_factory):
    curs_list = curs_factory(_quantity=10)
    response = client.get('/courses/')
    data_list = response.json()

    assert response.status_code == 200
    for i, c in enumerate(data_list):
        assert c['name'] == curs_list[i].name


@pytest.mark.django_db
def test_filter_id_courses(client, curs_factory):
    list_curses = (
        curs_factory(_quantity=10)
    )
    r = (
        random.randint(0,9)
    )
    id_curse = list_curses[r].id

    response = client.get(f'/courses/?id={id_curse}')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == list_curses[r].name


@pytest.mark.django_db
def test_filter_name_courses(client, curs_factory):
    list_curses = curs_factory(_quantity=10)
    r = random.randint(0,9)
    name_curse = list_curses[r].name

    response = client.get(f'/courses/?name={name_curse}')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == list_curses[r].name


@pytest.mark.django_db
def test_create_course(client):
    count_before = Course.objects.count()
    data = {
        'name': 'python',
        'students': []
        }
    response = client.post('/courses/', data)

    assert response.status_code == 201
    assert Course.objects.count() == count_before + 1


@pytest.mark.django_db
def test_patch_course(client, curs_factory):
    list_curses = curs_factory(_quantity=10)
    r = random.randint(0,9)
    id_course = list_curses[r].id
    data = {
        'name': 'python',
        'students': []
    }

    response = client.patch(f'/courses/{id_course}/', data)
    result = Course.objects.filter(id=id_course).first()

    assert response.status_code == 200
    assert result.name == 'python'


@pytest.mark.django_db
def test_delete_course(client, curs_factory):
    list_courses = curs_factory(_quantity=10)
    r = random.randint(0, 9)
    id_course = list_courses[r].id
    count_before = Course.objects.count()

    response = client.delete(f'/courses/{id_course}/')

    assert response.status_code == 204
    assert Course.objects.count() == count_before - 1