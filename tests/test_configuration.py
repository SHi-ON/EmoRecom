from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_local_server_defaults():
    for filename in ("server.py", "simpserver.py", "garbage/simpserver.py"):
        content = (ROOT / filename).read_text()
        assert "debug=False" in content
        assert "use_reloader=False" in content


def test_credentials_use_environment():
    source = (ROOT / "server.py").read_text()
    assert 'os.environ.get("GOOGLE_PLACES_API_KEY"' in source
    assert "GOOGLE_MAPS_BROWSER_KEY" in source


def test_browser_consent():
    js = (ROOT / "static" / "map.js").read_text()
    assert "navigator.geolocation.getCurrentPosition" in js
    assert "/recommendations" in js
