# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from django.conf import settings
from PIL import Image, ImageDraw
import os
from django.http import JsonResponse
from django.http import HttpResponse
import base64
import io
import json
from wxcloudrun import UpAndDownloadFile as fileLoad
def imgs_read():
    # # 打开图片
    # im1 = Image.open("12.jpg")
    # # 打开图片
    # im2 = Image.open("17.jpg")
    # imgs = [im1, im2]
    # 定义文件夹路径
    folder_path = os.path.join(settings.BASE_DIR, 'static', '1')


    # 获取文件夹中的所有文件名
    filenames = os.listdir(folder_path)

    # 保存所有图像的列表
    images = []

    # 遍历文件名列表
    for filename in filenames:
        # 构建文件路径
        file_path = os.path.join(folder_path, filename)
        # 读取图像
        image = Image.open(file_path)
        # 将图像添加到列表中
        images.append(image)

    print(len(images))
    # 在这里，您可以使用图像列表进行所需的操作

    return images

def imgs_centre(img):
    im1 = Image.open("./static/中心图/1.png")
    width, height = img.size
    width1, height1 = im1.size
    #图片中心坐标
    x, y = (width-width1)//2, (height-height1)//2
    img.paste(im1,(x,y))
    # img.show()
    print("处理完成")
    return img

def imgs_combine_16_9(imgs):
    result = Image.new("RGBA", (1920, 1080), "black")
    # 将图片依次粘贴到空白图片上
    x_offset = 10
    y_offset = 10
    row = 0
    y_add = imgs[0].height + 15
    for im in imgs:
        # im.convert("RGB")
        # result = Image.alpha_composite(result, im)
        if (x_offset + 40 < 1920):
            result.paste(im, (x_offset, y_offset))
            x_offset += im.width + 10
            row += 1
            # print(row)
        else:
            x_offset = 10
            y_offset += y_add
            result.paste(im, (x_offset, y_offset))
            x_offset += im.width + 10
            row = 1
            # print(row)

    #
    # result.show()
    # 保存合并后的图片
    # result.save("merged_image.jpg")
    return result

def imgs_combine_3_4(imgs):

    # 打开图片
    # im1 = Image.open("image1.jpg")
    # im2 = Image.open("image2.jpg")
    # im3 = Image.open("image3.jpg")
    #
    # # 将图片组成一个列表
    # images = [im1, im2, im3]
    # for im in imgs:
    #     im.show()
    # 创建一个空白图片，用于保存合并后的图片
    # result = Image.new("RGBA", (imgs[0].width*2, imgs[1].height * len(imgs)), "black")
    result = Image.new("RGBA", (840, 1440), "black")
    # 将图片依次粘贴到空白图片上
    x_offset = 10
    y_offset = 10
    row =0
    y_add = imgs[0].height+15
    for im in imgs:
        # im.convert("RGB")
        # result = Image.alpha_composite(result, im)
        if(x_offset+40 < 840):
            result.paste(im, (x_offset, y_offset))
            x_offset += im.width+10
            row += 1
            # print(row)
        else:
            x_offset = 10
            y_offset += y_add
            result.paste(im, (x_offset, y_offset))
            x_offset += im.width + 10
            row = 1
            # print(row)

    #
    # result.show()
    result2 = Image.new("RGBA", (1080, 1440), "black")
    result2.paste(result, (100, 0))
    result2.show()
    # 保存合并后的图片
    # result.save("merged_image.jpg")


def fillet_Process(imgs,radius,mode):
    r_imgs = []
    #在竖图里放横图
    if(mode== 1):
        H_SIZE =110
    # 在横图图里放横图-少图
    elif(mode==2):
        H_SIZE = 200
    else:
        H_SIZE =165


    for im in imgs:
        # 图片缩放
        # im.thumbnail(small_size)

        # 获取图片的尺寸
        width, height = im.size
        new_width = int(width * H_SIZE / height)
        im = im.resize((new_width, H_SIZE))
        # 设置圆角的半径
        # radius = 50

        # 创建圆角遮罩
        width, height = im.size
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 2 * radius, 2 * radius), fill=255)
        draw.ellipse((width - 2 * radius, 0, width, 2 * radius), fill=255)
        draw.ellipse((0, height - 2 * radius, 2 * radius, height), fill=255)
        draw.ellipse((width - 2 * radius, height - 2 * radius, width, height), fill=255)
        draw.rectangle((radius, 0, width - radius, height), fill=255)
        draw.rectangle((0, radius, width, height - radius), fill=255)

        # 使用遮罩将图片处理为圆角
        im = im.convert("RGBA")
        im.putalpha(mask)

        # ##第二种方法
        # draw = ImageDraw.Draw(im)
        #
        # # 创建圆角矩形
        # rounded_rectangle = (0, 0, width, height)
        # # 填充圆角矩形
        # draw.rounded_rectangle(rounded_rectangle,radius, fill=(255, 255, 255))

        r_imgs.append(im)

    return r_imgs
    # im.show()
    # 保存处理后的图片
    # im.save("rounded_image.png")
def image2byte(image):
    '''
    图片转byte
    image: 必须是PIL格式
    image_bytes: 二进制
    '''
    # 创建一个字节流管道
    img_bytes = io.BytesIO()
    #把PNG格式转换成的四通道转成RGB的三通道，然后再保存成jpg格式
    # image = image.convert("RGB")
    # 将图片数据存入字节流管道， format可以按照具体文件的格式填写
    image.save(img_bytes, format="PNG")
    
    # 从字节流管道中获取二进制-返回
    # image_bytes = img_bytes.getvalue()
    return img_bytes

def base642img(imgInfo):
    # 解码 base64 编码的图像数据
    decoded_image_data = base64.b64decode(imgInfo)

    # 将解码后的二进制数据封装为字节流
    image_data = io.BytesIO(decoded_image_data)

    # 使用 PIL 库打开图像
    image = Image.open(image_data)

    return image
# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#图片合成
def test_pro(imgs):
    # imgs_read()
    imgs = fillet_Process(imgs, 15, 2)
    # imgs_combine_3_4(imgs)
    img = imgs_combine_16_9(imgs)
    #中心图添加
    # img = imgs_centre(img)
    #保存图片
    # path = "./static/temp/"+'userid.png'
    # print(path)
    # img.save(path)
    fileObject = image2byte(img)
    fileLoad.UpLoad(fileObject,'userid')

    # img.show()
    # 获取图片二进制
    # img_bytes = image2byte(img)
    # print(img_bytes)
    # img_base64 = base64.b64encode(img_bytes)
    # print(img_base64)
    return 'is ok'

def test_upload(request,_):
    # data = json.loads(request.body)
    # imgInfo = data['imgInfo']
    imgs = []
    # for im in imgInfo:
    #     img = base642img(im)
    #     imgs.append(img)
    # img_base64 = test_pro(imgs)
    img_Byte = fileLoad.DownLoad(request)
    for img in img_Byte:
    # 将解码后的二进制数据封装为字节流
        image_data = io.BytesIO(img)
    # 使用 PIL 库打开图像
        image = Image.open(image_data)
        imgs.append(image)
    img_base64 = test_pro(imgs)
    response = HttpResponse(img_base64)
    return response

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# https://pypi.tuna.tsinghua.edu.cn/simple  镜像