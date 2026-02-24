def test_verification_route_returns_201_and_schedules_email(
    client,
    sent_emails
):
    payload = {
        "email": "user@email.com",
        "token": "token-de-teste",
    }

    response = client.post(
        "/notifications/arena-manager/verification",
        json=payload
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Email de verificação enviado. Verifique sua caixa de entrada!"
    }
    assert len(sent_emails["verification"]) == 1


def test_verification_route_returns_422_without_token(client):
    payload = {
        "email": "user@email.com",
    }

    response = client.post(
        "/notifications/arena-manager/verification",
        json=payload
    )

    assert response.status_code == 422


def test_owner_promotion_route_returns_201_and_schedules_email(
    client,
    sent_emails
):
    payload = {
        "user": {
            "id": 1,
            "name": "João",
            "email": "joao@email.com",
        },
        "arena": {
            "id": 10,
            "name": "Arena Centro",
        },
    }

    response = client.post(
        "/notifications/arena-manager/owner-promotion",
        json=payload
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Email de promoção de dono da arena enviado com sucesso!"
    }
    assert len(sent_emails["owner_promotion"]) == 1


def test_new_court_route_returns_201_and_schedules_email(
    client,
    sent_emails
):
    payload = {
        "user": {
            "id": 1,
            "name": "João",
            "email": "joao@email.com",
        },
        "arena": {
            "id": 10,
            "name": "Arena Centro",
        },
        "court": {
            "id": 25,
            "name": "Quadra 01",
        },
    }

    response = client.post(
        "/notifications/arena-manager/new-court",
        json=payload
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Email de nova quadra enviado com sucesso!"
    }
    assert len(sent_emails["new_court"]) == 1
