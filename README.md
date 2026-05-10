# hellbox-drawbot

A [hellbox](https://github.com/hellboxpy/hellbox) plugin that runs a [DrawBot](https://github.com/typemytype/drawbot) script against a font file to produce a specimen or other output.

## Usage

```python
from hellbox import Hellbox
from hellbox.jobs.drawbot import DrawBot

with Hellbox("specimen") as task:
    task.read("build/*.ttf") >> DrawBot("specimen.py") >> task.write("build/specimen")
```

All fonts from the previous chute are installed before the script runs, available as the `fontNames` list. The script is responsible for calling `saveImage` — any files saved during execution are passed to the next chute.

**specimen.py**

```python
W, H = 800, 600

newPage(W, H)
fill(1)
rect(0, 0, W, H)
fill(0)

for i, name in enumerate(fontNames):
    font(name, 48)
    text("Round", (40, H - 100 - i * 80))

saveImage("specimen.pdf")
```

## Installation

```sh
hell add hellbox-drawbot
```

## Development

```sh
uv sync
uv run pytest
```
