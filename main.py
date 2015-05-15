from wand.image import Image

with Image(filename='sample.eps') as img:
    scaler = 2
    img.resize(img.width * scaler, img.height * scaler)
    img.save(filename="sample@2x.png")

    scaler = 3
    img.resize(img.width * scaler, img.height * scaler)
    img.save(filename="sample@3x.png")


