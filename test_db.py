from app import db

def test_memory_roundtrip(tmp_path, monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "database_path", str(tmp_path / "test.db"))
    db.init_db()
    item_id = db.add_memory("Build Kitsune")
    assert item_id > 0
    assert db.get_memories()[0]["content"] == "Build Kitsune"
