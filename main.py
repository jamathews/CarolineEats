import os
import glob
from random import shuffle
from PIL import Image

source_images = "/Users/jmathews/Pictures/2017-10-22 - Caroline Eats/Layers/*.png"
output = "/Users/jmathews/Pictures/2017-10-22 - Caroline Eats/generated_images"
rows = 6
columns = 6
image_width = 682
image_height = image_width * 2
thumb_width = 600
thumb_height = thumb_width * 2
image_count = 5
image_extension = ".jpg"


def generate_random_image():
    generated_image_basename, images = get_source_images()
    generated_image = assemble_image(images)
    save_image(generated_image, generated_image_basename)
    save_thumbnail(generated_image, generated_image_basename)


def get_source_images():
    images = glob.glob(source_images)
    shuffle(images)
    generated_image_basename = make_basename(images)
    while len(glob.glob(os.path.join(output, f"{generated_image_basename}*{image_extension}"))) > 0:
        shuffle(images)
        generated_image_basename = make_basename(images)
    return generated_image_basename, images


def save_image(generated_image, generated_image_basename):
    generated_image_filename = generated_image_basename + image_extension
    generated_image_full_path = os.path.join(output, generated_image_filename)
    generated_image.save(generated_image_full_path)


def save_thumbnail(generated_image, generated_image_basename):
    thumbnail_basename = "thumb_" + generated_image_basename
    thumbnail_filename = thumbnail_basename + image_extension
    thumbnail_full_path = os.path.join(output, thumbnail_filename)
    generated_image.thumbnail((thumb_width, thumb_height))
    generated_image.save(thumbnail_full_path)


def assemble_image(images):
    image_in_progress = Image.new("RGB", (image_width * columns, image_height * rows))
    for row in range(0, rows):
        for column in range(0, columns):
            image_index = (row * columns) + column
            image_name = images[image_index]
            image = Image.open(image_name)
            region = image.crop((0, 0, image_width, image_height))
            paste_destination = (column * image_width, row * image_height)
            image_in_progress.paste(region, paste_destination)
    return image_in_progress


def make_basename(images):
    filename = ""
    for image in images:
        filename += image.split(os.path.sep)[-1].split("_")[1]
        if images.index(image) < len(images) - 1:
            filename += "_"
    return filename


if __name__ == '__main__':
    for _ in range(0, image_count):
        generate_random_image()
