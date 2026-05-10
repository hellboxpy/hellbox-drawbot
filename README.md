# hellbox-drawbot

A [hellbox](https://github.com/hellboxpy/hellbox) plugin that runs a [DrawBot](https://github.com/typemytype/drawbot) script against a font file to produce a specimen or other output.

## Usage

```python
from hellbox import Hellbox
from hellbox.jobs.drawbot import DrawBot

with Hellbox("specimen") as task:
    task.read("build/*.ttf") >> DrawBot("specimen.py") >> task.write("build/specimen")
```

The DrawBot script is executed with `fontName` bound to the installed font and can call any DrawBot drawing functions. By default the output is saved as a PDF; pass `format="png"` (or any format DrawBot supports) to change it.

```python
DrawBot("specimen.py", format="png")
```

## Installation

```sh
pip install hellbox-drawbot
```
