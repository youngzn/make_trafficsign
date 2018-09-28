from PIL import Image, ImageFilter, ImageEnhance
import random
import os


def resize_base(base_im):
    base_im = base_im.resize((1280, 1024))
    base_im = ImageEnhance.Color(base_im).enhance(0.5 + 0.5 * random.random())  # Adjust the color
    base_im = ImageEnhance.Contrast(base_im).enhance(0.8 + 0.5 * random.random())  # Adjust the contrast
    base_im = ImageEnhance.Sharpness(base_im).enhance(0.8 + 0.5 * random.random())  # Adjust the sharpness
    return base_im


def resize_light(logo_im):
    logo_im = ImageEnhance.Color(logo_im).enhance(0.5 + 0.5 * random.random())  # Adjust the saturation
    logo_im = ImageEnhance.Contrast(logo_im).enhance(0.5 + 0.5 * random.random())  # Adjust the color
    # logo_im = ImageEnhance.Sharpness(logo_im).enhance(0.7 + 0.3 * random.random())  # Adjust the sharpness
    logo_im = logo_im.filter(ImageFilter.GaussianBlur(radius=0.8 + 0.5 * random.random()))  # 需要对logo进行模糊化处理
    logo_min = 20 + random.randint(0, 30)

    if logo_im.size[0] > logo_im.size[1]:
        logo_im = logo_im.resize((int(logo_min * logo_im.size[0] / logo_im.size[1]), logo_min))
    else:
        logo_im = logo_im.resize((logo_min, int(logo_min * logo_im.size[1] / logo_im.size[0])))

    logo_im = logo_im.resize((int(random.uniform(0.9, 1) * logo_im.size[0]),
                              int(random.uniform(0.9, 1) * logo_im.size[1])))
    coor = [random.randint(1, int(1280 - 1.1 * logo_im.size[0])), random.randint(1, 350)]
    return coor, logo_im


def resize_sign(logo_im, style):
    logo_im = ImageEnhance.Color(logo_im).enhance(0.5 + 0.5 * random.random())  # Adjust the saturation
    logo_im = ImageEnhance.Contrast(logo_im).enhance(0.5 + 0.5 * random.random())  # Adjust the color
    # logo_im = ImageEnhance.Sharpness(logo_im).enhance(0.7 + 0.3 * random.random())  # Adjust the sharpness
    logo_im = logo_im.filter(ImageFilter.GaussianBlur(radius=1.0 + 0.4 * random.random()))  # 需要对logo进行模糊化处理
    if style == "ETC":
        logo_w = random.randint(100, 400)
    elif style == "long":
        logo_w = random.randint(200, 600)
    elif style == "PorCar":
        logo_w = random.randint(100, 300)
    else:  # square
        logo_w = random.randint(40, 100)
    logo_im = logo_im.resize((logo_w,  int(logo_w * (logo_im.size[1] / logo_im.size[0]))))
    logo_im = logo_im.resize((int(random.uniform(0.9, 1) * logo_im.size[0]),
                              int(random.uniform(0.9, 1) * logo_im.size[1])))
    coor = [random.randint(1, int(1280 - 1.1 * logo_im.size[0])), random.randint(30, 400)]
    return coor, logo_im


def add_logo(work_dir, num, base_path, logo_path, base_name, logo_name):
    base_im = Image.open(base_path)
    logo_im = Image.open(logo_path)
    base_im = resize_base(base_im)
    if os.path.splitext(logo_name)[0][:1] == str(2):  # light
        coor, logo_im = resize_light(logo_im)
    elif os.path.splitext(logo_name)[0][:4] == str(1011) or os.path.splitext(logo_name)[0][:4] == str(
            1012):  # <<<<< and >>>>
        coor, logo_im = resize_sign(logo_im, "long")
    elif os.path.splitext(logo_name)[0][:4] == str(1014):  # ETC
        coor, logo_im = resize_sign(logo_im, "ETC")
    elif os.path.splitext(logo_name)[0][:4] == str(1009) or os.path.splitext(logo_name)[0][:4] == str(
            1013):  # car and P
        coor, logo_im = resize_sign(logo_im, "PorCar")
    else:
        coor, logo_im = resize_sign(logo_im, "square")
    base_im.paste(logo_im, (coor[0], coor[1]), logo_im)
    if (coor[0] + logo_im.size[0]) > 1280 or (coor[1] + logo_im.size[1]) > 1024:
        print("error---error---error---error---error---error---error---error---error---error---error")
    base_im.save(os.path.join(os.path.join(work_dir, "JPEGImages"), "%06d.jpg" % num))
    return coor, logo_im


if __name__ == "__main__":
    work_dir = 'C:\\Users\\young\\Desktop\\test'
    base_path = "C:\\Users\\young\\Desktop\\test\\before\\base\\0001.jpg"
    logo_path = "C:\\Users\\young\\Desktop\\test\\before\\logo\\1001\\10010001.png"
    base_name = "0001.jpg"
    logo_name = "10010001.png"
    add_logo(work_dir, 1, base_path, logo_path, base_name, logo_name)
