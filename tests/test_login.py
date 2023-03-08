
def test_the_app_returns_the_homepage(client):

    response = client.get('/')
    assert response.status_code == 200

    # we can create a new user


def test_we_can_register_a_user(client):
    response = client.post('/register',
                           data=dict(
                               username="testuser",
                               name="test",
                               email="test@test.com",
                               password="testing",
                               grant_type="password"
                           ))
    assert response.status_code == 201


def test_we_can_register_and_login_a_user(client):
    data = dict(username="testuser",
                name="test",
                email="test@test.com",
                password="testing",
                grant_type="password"
                )
    response = client.post('/register',
                           data=data)
    assert response.status_code == 201
    
    response = client.post('/login', data=data, headers={"content-type": "application/x-www-form-urlencoded"})

    assert response.status_code == 200


def test_when_user_does_not_exist_we_get_an_error(client):
    response = client.post('/login', data={"username": "testuser", "password": "testing",
                           "grant_type": "password"}, headers={"content-type": "application/x-www-form-urlencoded"})

    assert response.status_code == 401


