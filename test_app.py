import pytest
from three_topic_story import create_app, db
from three_topic_story.account.model import User
from three_topic_story.account.form import FormRegister
from flask import Response

TEST_USERNAME = 'test_user'
TEST_MAIL = 'three.topic.story.test@gmail.com'
TEST_PASSWORD = 'abcdefg'


@pytest.fixture
def client():
    app = create_app('test')

    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User('test_user', app.config.get('MAIL_USERNAME'),
                    app.config.get('MAIL_PASSWORD'))
        db.session.add_all([user])
        db.session.commit()
        print('Set DB successfully!')

        print(app.config)

        with app.test_client() as client:
            yield client


def register(client, username, email, password):
    return client.post('/account/register', data=dict(
        username=username, email=email, password=password, password2=password), follow_redirects=True)


def test_register_success(client):
    response = client.get('/account/register')
    assert response.status_code == 200
    assert b"Register Your Account" in response.data
    response = register(client, TEST_USERNAME, TEST_MAIL, TEST_PASSWORD)
    assert response.status_code == 200
    assert b"Register Your Account" not in response.data
    assert b"Welcome" in response.data
