from app.utils.validators import valid_email, valid_phone, valid_tg

# валидаторы


def test_valid_email():

    assert valid_email('test@example.com') is True
    assert valid_email('bad') is False
    assert valid_email('no-at-sign.com') is False


def test_valid_phone():

    assert valid_phone('+71234567890') is True
    assert valid_phone('71234567890') is False
    assert valid_phone('+abc') is False


def test_valid_tg():

    assert valid_tg('@username') is True
    assert valid_tg('username') is False
# POST / notifications


def test_create_notification(client, mock_publish):

    response = client.post('/api/v1/notifications', json={
        'type': 'email',
        'recipient': 'test@example.com',
        'message': 'Привет',
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'queued'
    assert 'id' in data
    mock_publish.assert_called_once()


def test_create_invalid_email(client, mock_publish):

    response = client.post('/api/v1/notifications', json={
        'type': 'email',
        'recipient': 'bad-email',
        'message': 'Привет',
    })
    assert response.status_code == 400
# GET / notifications/<id >


def test_get_notification(client, mock_publish):

    # сначала создаём
    created = client.post('/api/v1/notifications', json={
        'type': 'email',
        'recipient': 'test@example.com',
        'message': 'Привет',
    })
    notif_id = created.get_json()['id']
    # потом читаем
    response = client.get(f'/api/v1/notifications/{notif_id}')
    assert response.status_code == 200
    assert response.get_json()['id'] == notif_id


def test_get_notification_not_found(client):

    response = client.get('/api/v1/notifications/no-such-id')
    assert response.status_code == 404
# GET / notifications(список)


def test_list_notifications(client, mock_publish):

    client.post('/api/v1/notifications', json={
        'type': 'email', 'recipient': 'a@example.com', 'message': 'A',
    })
    client.post('/api/v1/notifications', json={
        'type': 'email', 'recipient': 'b@example.com', 'message': 'B',
    })
    response = client.get('/api/v1/notifications')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 2
    assert len(data['items']) == 2
