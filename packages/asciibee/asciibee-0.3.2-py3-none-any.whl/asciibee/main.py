import argparse

from asciibee import constants, image

shader_help_text = ""
for shader in constants.SHADERS:
    shader_help_text += f'{constants.SHADERS.index(shader) + 1}: "{shader}"\n    '

parser = argparse.ArgumentParser(
    prog="asciibee",
    description=f"""Convert an image to ASCII art

    The default settings are tuned to work best with fine art. Play with
    different shaders, chunk sizes, and value inversion for different results.
    Remember to decrease your font size if you can't see the whole image.

    Scaling is accomplished by dividing the image into chunks and converting
    each chunk to a single character. The chunk size can be adjusted with the -c
    flag. The chunk size defaults to the pixel width of the image divided by
    100. The output will tell you what chunk size was used.

    Shaders (note that each begins with one empty space):

    {shader_help_text}""",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument("image_path", help="Path to the image to convert")
parser.add_argument(
    "-s",
    "--shader",
    help=f"The shader to use (they increase in complexity); default {constants.DEFAULT_SHADER}",
    type=int,
    choices=range(1, len(constants.SHADERS) + 1),
    default=constants.DEFAULT_SHADER,
    required=False,
)
parser.add_argument(
    "-S",
    "--user-shader",
    help="Define your own shader as a sequence of characters; surround with quotes",
    required=False,
)
parser.add_argument(
    "-c",
    "--chunk-size",
    help=f"Size of the chunks to covert to ASCII (larger chunks emit smaller images)",
    type=int,
    required=False,
)
parser.add_argument(
    "-i",
    "--invert-values",
    help="Invert the value scale (i.e. darker values will use heavier characters)",
    action="store_true",
)

args = parser.parse_args()


def main():
    ascii_image = image.AsciiImage(
        args.image_path,
        shader=constants.SHADERS[args.shader - 1],
        user_shader=args.user_shader,
        chunk_size=args.chunk_size,
        invert_values=args.invert_values,
    )
    ascii_image.convert()
    ascii_image.show()


if __name__ == "__main__":
    main()
