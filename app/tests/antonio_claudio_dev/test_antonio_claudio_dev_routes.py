def test_home_returns_welcome_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Notify Me API"}


def test_contact_route_returns_201_and_schedules_background_task(
    client,
    sent_emails
):
    payload = {
        "name": "Antonio Claudio",
        "email": "antonio@email.com",
        "message": "Olá! Gostei muito do seu portfólio.",
    }

    response = client.post(
        "/notifications/antonio-claudio-dev/contact/",
        json=payload
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Mensagem recebida. Entrarei em contato em breve!"
    }
    assert len(sent_emails["contact"]) == 1


def test_contact_route_returns_422_for_invalid_payload(client):
    payload = {
        "name": "Ana",
        "email": "email-invalido",
        "message": "curta",
    }

    response = client.post(
        "/notifications/antonio-claudio-dev/contact/",
        json=payload
    )

    assert response.status_code == 422
