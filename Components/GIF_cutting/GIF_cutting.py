import os
from PIL import Image, ImageSequence

def parseGIF(gifname):
    # 将gif解析为图片
    # 读取GIF
    im = Image.open(gifname)
    # GIF图片流的迭代器
    iter = ImageSequence.Iterator(im)
    # 获取文件名
    file_name = gifname.split(".")[0]
    index = 1
    # 判断目录是否存在
    pic_dirct = "imgs/{0}".format(file_name)
    mkdirlambda = lambda x: os.makedirs(
        x) if not os.path.exists(x) else True  # 目录是否存在,不存在则创建
    mkdirlambda(pic_dirct)
    # 遍历图片流的每一帧,保存为
    for frame in iter:
        print("image %d: mode %s, size %s" % (index, frame.mode, frame.size))
        frame.save("imgs/%s/frame%d.png" % (file_name, index))  # 保存图片
        index += 1

    # frame0 = frames[0]
    # frame0.show()

    # 把GIF拆分为图片流
    imgs = [frame.copy() for frame in ImageSequence.Iterator(im)]


if __name__ == "__main__":
    parseGIF("Resources\Images\giphy.gif")
