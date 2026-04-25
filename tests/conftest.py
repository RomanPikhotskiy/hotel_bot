from pathlib import Path
from types import SimpleNamespace
import sys

import pytest
from peewee import SqliteDatabase


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

ENV_FILE = ROOT_DIR / ".env"
CREATED_ENV = False

if not ENV_FILE.exists():
    ENV_FILE.write_text("BOT_TOKEN=test_token\nRAPID_API_KEY=test_key\n", encoding="utf-8")
    CREATED_ENV = True


@pytest.fixture(scope="session", autouse=True)
def clear_temp_env_file():
    yield
    if CREATED_ENV and ENV_FILE.exists():
        ENV_FILE.unlink()


class _DataContext:
    def __init__(self, storage: dict, chat_id: int):
        self.storage = storage
        self.chat_id = chat_id

    def __enter__(self):
        return self.storage.setdefault(self.chat_id, {})

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeBot:
    def __init__(self):
        self.storage = {}
        self.messages = []
        self.replies = []
        self.states = []
        self.edited_messages = []
        self.media_groups = []

    def send_message(self, chat_id, text, reply_markup=None):
        self.messages.append({"chat_id": chat_id, "text": text, "reply_markup": reply_markup})

    def reply_to(self, message, text):
        self.replies.append({"chat_id": message.chat.id, "text": text})

    def set_state(self, *args):
        self.states.append(args)

    def retrieve_data(self, chat_id):
        return _DataContext(self.storage, chat_id)

    def edit_message_text(self, text, chat_id, message_id, reply_markup=None):
        self.edited_messages.append(
            {"chat_id": chat_id, "message_id": message_id, "text": text, "reply_markup": reply_markup}
        )

    def send_media_group(self, chat_id, media):
        self.media_groups.append({"chat_id": chat_id, "media": media})


@pytest.fixture
def fake_bot():
    return FakeBot()


@pytest.fixture
def message_factory():
    def _factory(text: str, user_id: int = 100, chat_id: int = 100):
        user = SimpleNamespace(
            id=user_id,
            first_name="Test",
            last_name="User",
            full_name="Test User"
        )
        chat = SimpleNamespace(id=chat_id)
        return SimpleNamespace(text=text, from_user=user, chat=chat)

    return _factory


@pytest.fixture
def callback_factory():
    def _factory(chat_id: int = 100, data: str = "0", message_id: int = 1):
        chat = SimpleNamespace(id=chat_id)
        message = SimpleNamespace(chat=chat, message_id=message_id)
        return SimpleNamespace(data=data, message=message)

    return _factory


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    from database import db

    test_db = SqliteDatabase(tmp_path / "test_history.db")
    test_db.bind([db.Users, db.Cities, db.Hotels], bind_refs=False, bind_backrefs=False)
    monkeypatch.setattr(db, "dbs", test_db)
    test_db.connect()
    yield test_db
    if not test_db.is_closed():
        test_db.close()
