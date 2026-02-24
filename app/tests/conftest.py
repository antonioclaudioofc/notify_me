from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.modules.antonio_claudio_dev.service import AntonioClaudioDevService
from app.modules.arena_manager.service import ArenaManagerService


@pytest.fixture(scope="function")
def sent_emails():
    return {
        "contact": [],
        "verification": [],
        "owner_promotion": [],
        "new_court": [],
    }


@pytest.fixture(scope="function", autouse=True)
def mock_email_services(monkeypatch, sent_emails):
    def fake_send_message(contact):
        sent_emails["contact"].append(contact)

    def fake_send_verification_email(user_verification):
        sent_emails["verification"].append(user_verification)

    def fake_send_owner_promotion_email(user, arena):
        sent_emails["owner_promotion"].append((user, arena))

    def fake_send_new_court_email(user, arena, court):
        sent_emails["new_court"].append((user, arena, court))

    monkeypatch.setattr(
        AntonioClaudioDevService,
        "send_message",
        staticmethod(fake_send_message)
    )
    monkeypatch.setattr(
        ArenaManagerService,
        "send_verification_email",
        staticmethod(fake_send_verification_email)
    )
    monkeypatch.setattr(
        ArenaManagerService,
        "send_arena_owner_promotion_email",
        staticmethod(fake_send_owner_promotion_email)
    )
    monkeypatch.setattr(
        ArenaManagerService,
        "send_new_court_email",
        staticmethod(fake_send_new_court_email)
    )


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c
