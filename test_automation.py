import pytest
from app.automation import APP_ALLOWLIST

def test_allowlist_is_explicit():
    assert "notepad" in APP_ALLOWLIST
    assert "powershell" not in APP_ALLOWLIST
    assert "cmd" not in APP_ALLOWLIST
