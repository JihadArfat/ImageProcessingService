from pathlib import Path
from matplotlib.image import imread, imsave
import math
import random


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self, angle=-90):
        radians = math.radians(angle)
        cos_val = math.cos(radians)
        sin_val = math.sin(radians)

        new_data = []
        height, width = len(self.data), len(self.data[0])

        for y in range(height):
            new_row = []
            for x in range(width):
                new_x = int((x - width / 2) * cos_val - (y - height / 2) * sin_val + width / 2)
                new_y = int((x - width / 2) * sin_val + (y - height / 2) * cos_val + height / 2)

                if 0 <= new_x < width and 0 <= new_y < height:
                    new_row.append(self.data[new_y][new_x])
                else:
                    new_row.append(0)  # Fill with black for out-of-bounds

            new_data.append(new_row)

        self.data = new_data

    def salt_n_pepper(self, amount=0.02):
        height, width = len(self.data), len(self.data[0])
        num_pixels = int(height * width * amount)

        for _ in range(num_pixels):
            y = random.randint(0, height - 1)
            x = random.randint(0, width - 1)
            self.data[y][x] = 0 if random.random() < 0.5 else 255

    def concat(self, other_img, direction='horizontal'):
        if direction not in ('horizontal', 'vertical'):
            raise ValueError("Invalid 'direction'. Use 'horizontal' or 'vertical'.")

        if direction == 'horizontal':
            new_width = len(self.data[0]) + len(other_img.data[0])
            new_height = max(len(self.data), len(other_img.data))
        else:
            new_width = max(len(self.data[0]), len(other_img.data[0]))
            new_height = len(self.data) + len(other_img.data)

        new_data = []

        for y in range(new_height):
            new_row = []

            for x in range(new_width):
                if direction == 'horizontal':
                    if x < len(self.data[0]):
                        new_row.append(self.data[y][x])
                    else:
                        new_row.append(other_img.data[y][x - len(self.data[0])])
                else:
                    if y < len(self.data):
                        new_row.append(self.data[y][x])
                    else:
                        new_row.append(other_img.data[y - len(self.data)][x])

            new_data.append(new_row)

        self.data = new_data

    def segment(self, threshold=128):
        new_data = []

        for row in self.data:
            new_row = []

            for pixel_value in row:
                new_pixel_value = 255 if pixel_value >= threshold else 0
                new_row.append(new_pixel_value)

            new_data.append(new_row)

        self.data = new_data
