from wand.image import Image

with Image(filename="assets/starchy/S0.png") as image:
    image.shear("transparent", 20, 30)
    image.format = "png"
    image.display()