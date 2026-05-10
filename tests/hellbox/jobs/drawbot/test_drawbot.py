from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from hellbox.jobs.drawbot import DrawBot
from hellbox.source_file import SourceFile


class TestDrawBot:
    def test_init(self):
        assert DrawBot("specimen.py")

    def test_flush_empty(self):
        assert DrawBot("specimen.py").flush([]) == []

    def test_flush(self, tmp_path):
        file = MagicMock()

        def fake_exec(self, script, font_paths, output_dir):
            (output_dir / "specimen.pdf").write_bytes(b"")

        with patch("builtins.open", mock_open(read_data="# script")):
            with patch.object(DrawBot, "_exec_script", fake_exec):
                result = DrawBot("specimen.py").flush([file])

        assert len(result) == 1
        assert isinstance(result[0], SourceFile)
        assert result[0].content_path.name == "specimen.pdf"
        assert result[0].original_path.name == "specimen.pdf"

    def test_flush_returns_all_saved_files(self, tmp_path):
        file = MagicMock()

        def fake_exec(self, script, font_paths, output_dir):
            (output_dir / "specimen-light.pdf").write_bytes(b"")
            (output_dir / "specimen-bold.pdf").write_bytes(b"")

        with patch("builtins.open", mock_open(read_data="# script")):
            with patch.object(DrawBot, "_exec_script", fake_exec):
                result = DrawBot("specimen.py").flush(files=[file])

        assert [r.content_path.name for r in result] == [
            "specimen-bold.pdf",
            "specimen-light.pdf",
        ]

    def test_flush_passes_all_font_paths(self):
        files = [MagicMock(), MagicMock()]
        files[0].content_path = Path("/fonts/Regular.ttf")
        files[1].content_path = Path("/fonts/Bold.ttf")

        with patch("builtins.open", mock_open(read_data="# script")):
            with patch.object(DrawBot, "_exec_script") as mock_exec:
                DrawBot("specimen.py").flush(files)

        _, font_paths, _ = mock_exec.call_args[0]
        assert font_paths == [Path("/fonts/Regular.ttf"), Path("/fonts/Bold.ttf")]
