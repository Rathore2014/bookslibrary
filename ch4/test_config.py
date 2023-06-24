from typer.testing import CliRunner
import books


def run_books(*params):
    runner = CliRunner()
    result = runner.invoke(books.app, params)
    return result.output.rstrip()


def test_run_books():
    assert run_books("version") == books.__version__


def test_patch_get_path(monkeypatch, tmp_path):
    def fake_get_path():
        return tmp_path

    monkeypatch.setattr(books.cli, "get_path", fake_get_path)
    assert run_books("config") == str(tmp_path)


def test_patch_home(monkeypatch, tmp_path):
    full_books_dir = tmp_path / "bookslib_db"

    def fake_home():
        return tmp_path

    monkeypatch.setattr(books.cli.pathlib.Path, "home", fake_home)
    assert run_books("config") == str(full_books_dir)


def test_patch_env_var(monkeypatch,     tmp_path):
    monkeypatch.setenv("CARDS_DB_DIR", str(tmp_path))
    assert run_books("config") == str(tmp_path)
