from pathlib import Path
from tuxpkg.get_makefile import run


class TestGetMakefile:
    def test_file_exists(self, capsys):
        run()
        out, _ = capsys.readouterr()
        path = Path(out.strip())
        assert path.exists()
        assert "\ndeb: " in path.read_text()
