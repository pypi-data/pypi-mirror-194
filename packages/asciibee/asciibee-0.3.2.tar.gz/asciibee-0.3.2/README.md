# `<(||')` asciibee `<(||')`

An image-to-ascii-art converter

## Description

The default settings are tuned to work best with fine art. Play with different
shaders, chunk sizes, and value inversion for different results. Remember to
decrease your font size if you can't see the whole image.

Scaling is accomplished by dividing the image into chunks and converting each
chunk to a single character. The chunk size can be adjusted with the -c flag.
The chunk size defaults to the pixel width of the image divided by 100. The
output will tell you what chunk size was used.

## Installation

`$ pip install asciibee`

## Usage

The best way to learn how to use the app is via the help text:

`$ asciibee --help`

The most simple command is passing in a path to an image file:

`$ asciibee ~/Downloads/starrynight.png`

You can use it as an importable module as well.

```python
from asciibee.image import AsciiImage
image = AsciiImage('/Users/jnakama/Downloads/port.jpeg')
image.convert()  # Converts the image to a matrix of ASCII characters
image.ascii_matrix # It's stored here
image.show()  # Prints the characters
```

## Development

The build system and package manager is [poetry](https://python-poetry.org/).

The easiest way to run the app locally:

`$ poetry run python -m asciibee.main <path_to_image>`

You can also install the deps and run it without the `poetry run` prefix.

```text
                    ...         .....             ......
                   ..,,-,.         ..,.        ..,,....
                      ..,-..         .,,.     .,..
                         .-..         .,-,,..-..             ......
                          ..,,.      .####+###+..         ..,,,,,,..
                            ..+-..   -+@@@##@@#+  .....,,,,,.
                              ..,---.-++++++#+#-.,--,,,....
                                 ..-#++#######++#+,.
                        .  ..      ,#++@@@@#@@@#+..            ...
                    ..,,-,-,-,,,..,-++##@@##@###+++-,,,..,,,,,,,..
                      ......,,,-++++#+###########+++----,,,... .
             .....,,,,,,----------+++-###+#++#+++++----------,,,,,,......
       ...,,,-,,,,,,,,,-,,,,--------+-..#####-..,+-+----,,,-----,-,,,---,,,,....
    ...,,,,,,,,,,-,,,,,,,,,-,--,,--,.-+########+-,--+-----,,,,,,,---,,--,---,,,,,..
  ..,,,,,,.,,.,,,,,,,.,,--,,,,-,--..-+####@@@@@##-.,-+-,,,--,,,,,,,,--,,,,,,--,,,,.
  .,,,,,,.,.,,.,,,..,,-,,,,,,,--+..,++++++++#####+-.,----,,-,,-,,,,,,,,,-,,.,,,-,,.
  .,,,,,,.,,,.,,,,,,,,,,,,,,-,-+. .+###++#####@###+...---,,,,-,,------,,,,,,,,,..
    ...,,,,,,,.,,,,,,,,,,,,,,-,.  ,#@@@#-+###@@@@@#,   ,-,,,,,,,,,,,,,,,.,,....
                ..........,-,...  ,+##++++###@@@##+-.    .,,,.....   .
                     ..,-,...     ,+##++#++++######-.      ..,..
                    .,,,...       ,#@@##+##@@#@@@@#-.        .,,.
                   .,,.           .+####++#@@@@@@#+..         .,.
                   ...            ..+++++++######+,.          ...
                                    .+###++####@#-.
                                     ,+##+######-.
                                     ...-##@#+-...
                                        ..--...
```
