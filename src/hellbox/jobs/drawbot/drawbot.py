import os
import tempfile
from pathlib import Path

from hellbox import Chute, Hellbox
from hellbox.source_file import SourceFile


class DrawBot(Chute):
    """DrawBot runs a DrawBot script with all provided fonts installed."""

    def __init__(self, filepath):
        self.filepath = filepath

    def flush(self, files):
        if not files:
            return []
        Hellbox.info(f"Running DrawBot ({self.filepath})")
        script = open(self.filepath).read()
        output_dir = Path(tempfile.mkdtemp())
        self._exec_script(script, [f.content_path for f in files], output_dir)
        return [
            SourceFile(p, p)
            for p in sorted(output_dir.iterdir())
            if p.is_file()
        ]

    def _exec_script(self, script, font_paths, output_dir):
        installs = "\n".join(f'fontNames.append(installFont("{p}"))' for p in font_paths)
        prev_dir = os.getcwd()
        try:
            os.chdir(output_dir)
            exec(
                "from drawBot import newDrawing, installFont, saveImage, endDrawing\n"
                "newDrawing()\n"
                "fontNames = []\n"
                + installs + "\n"
                + script + "\n"
                "endDrawing()\n"
            )
        finally:
            os.chdir(prev_dir)
