import os

import numpy
from PIL import Image

from asciibee import constants


class AsciiImage:
    ascii_matrix: list = []

    def __init__(
        self,
        image_path: str,
        shader: list = constants.SHADERS[constants.DEFAULT_SHADER - 1],
        user_shader: str = None,
        chunk_size: int = None,
        invert_values: bool = False,
    ) -> None:
        self.image_path = image_path
        self.shader = shader if not user_shader else user_shader
        self.chunk_size = chunk_size
        self.invert_values = invert_values

    def _rotate_and_flip(self, matrix: list) -> list:
        rotated = numpy.rot90(matrix, 3)
        return numpy.flip(rotated, 1)

    def calculate_brightness(self, image):
        histogram = image.histogram()
        pixels = sum(histogram)
        brightness = scale = len(histogram)

        for index in range(0, scale):
            ratio = histogram[index] / pixels
            brightness += ratio * (-scale + index)

        return brightness

    def convert(self) -> None:
        with Image.open(self.image_path).convert("L") as image:
            if self.invert_values:
                self.shader = self.shader[::-1]

            if not self.chunk_size:
                self.chunk_size = int(image.width / 100)

            width_chunks = int(image.width / self.chunk_size)
            height_chunks = int(image.height / (self.chunk_size * 2))

            darkest_value = None
            lightest_value = None
            crops = []
            num_chunks = width_chunks * height_chunks
            current_chunk = 0
            for x in range(width_chunks):
                crops.append([])
                for y in range(height_chunks):
                    current_chunk += 1
                    percent_done = int((current_chunk / num_chunks) * 100)
                    print(f"Processing... {percent_done}%", end="\r")
                    crop = image.crop(
                        (
                            x * self.chunk_size,
                            y * self.chunk_size * 2,
                            (x + 1) * self.chunk_size,
                            (y + 1) * self.chunk_size * 2,
                        )
                    )
                    if not darkest_value:
                        darkest_value = self.calculate_brightness(crop)
                    if not lightest_value:
                        lightest_value = self.calculate_brightness(crop)
                    darkest_value = min(darkest_value, self.calculate_brightness(crop))
                    lightest_value = max(
                        lightest_value, self.calculate_brightness(crop)
                    )
                    crops[x].append((crop, self.calculate_brightness(crop)))
            for x in range(width_chunks):
                self.ascii_matrix.append([])
                for y in range(height_chunks):
                    crop, brightness = crops[x][y]
                    # What percentage of the full range is this pixel?
                    value = (brightness - darkest_value) / (
                        lightest_value - darkest_value
                    )
                    # What character should we use for this pixel?
                    char_index = int(value * (len(self.shader) - 1))
                    self.ascii_matrix[x].append(self.shader[char_index])

        self.ascii_matrix = self._rotate_and_flip(self.ascii_matrix)

    def show(self) -> None:
        for row in self.ascii_matrix:
            for char in row:
                print(char, end="")
            print()
        print(f"\nShader: {self.shader}")
        print(f"Chunk size: {self.chunk_size}")
        print(f"Inverted: {self.invert_values}")
        print("\nIncrease chunk size with -c to make image smaller.")
        print("Decrease chunk size with -c to make image larger.")
