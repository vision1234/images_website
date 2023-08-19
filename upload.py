import os
from flask import Flask, render_template, request
import time
from PIL import Image
import utils
import arrow

app = Flask(__name__)

# 设置文件上传的目录
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['GENERATE_FOLDER'] = 'static/thumbnail'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取上传的文件和表单数据
        if "file" not in request.files:
            return "没有选择文件"
        cate = request.form['cate']
        tag = request.form['tag']
        tags = tag.replace("，", ",").split(",")
        thumbnail_path = os.path.join(app.config['GENERATE_FOLDER'], cate)
        images = request.files.getlist('file')
        # 创建目录（如果不存在）
        target_directory = os.path.join(app.config['UPLOAD_FOLDER'], cate)
        os.makedirs(target_directory, exist_ok=True)
        os.makedirs(thumbnail_path, exist_ok=True)
        conn = utils.get_conn()
        coll = utils.get_collect(conn, utils.coll)
        for file in images:
            # Check if a file with the same name exists in the target directory
            filename, file_extension = os.path.splitext(file.filename)
            timestamp = str(int(time.time()))
            target_file_path = os.path.join(target_directory, file.filename)
            if os.path.exists(target_file_path):
                file.filename = f"{filename}_{timestamp}{file_extension}"
            target_file_path = os.path.join(target_directory, file.filename)
            thumbnail_path_ = os.path.join(thumbnail_path, file.filename)
            file.save(target_file_path)
            generate_thumbnail(target_file_path, thumbnail_path_)
            update_mongo(coll, target_file_path, thumbnail_path_, cate, tags)
        return '文件上传成功！'
    else:
        # tags = utils.get_redis_tags()
        cates = utils.get_redis_cates()
        return render_template('upload.html', cate=cates)


def generate_thumbnail(input_image_path, output_image_path, target_size=(372, 557), fill_color=(255, 255, 255)):
    try:
        # 打开原始图片
        image = Image.open(input_image_path)
        print(image.size)

        # 确定缩略图的目标尺寸
        aspect_ratio = image.width / image.height
        if aspect_ratio > target_size[0] / target_size[1]:
            # 原图宽高比例大于目标宽高比例，取高380，按比例取缩略图的宽
            new_width = int(target_size[1] * aspect_ratio)
            final_size = (new_width, target_size[1])
        else:
            # 原图宽高比例小于目标宽高比例，取宽280，按比例取缩略图的高
            new_height = int(target_size[0] / aspect_ratio)
            final_size = (target_size[0], new_height)

        # 创建一张新的白色背景图
        new_image = Image.new("RGB", target_size, fill_color)

        # 将缩略图粘贴在新图上，居中显示，并拉伸到填满整个区域
        image = image.resize(final_size)
        x_offset = (target_size[0] - image.size[0]) // 2
        y_offset = (target_size[1] - image.size[1]) // 2
        new_image.paste(image, (x_offset, y_offset))

        # 保存缩略图
        print(output_image_path)
        new_image.save(output_image_path)
        print("缩略图已生成并保存至", output_image_path)

    except IOError as e:
        print("无法生成缩略图")
        print(e)
        # 使用示例


def update_mongo(coll, image_path, thumbnail_path, cate, tag):
    data = {
        "image_path": image_path.replace("\\", "/"),
        "thumbnail_path": thumbnail_path.replace("\\", "/"),
        "cate": cate,
        "tag": tag,
        "create_time": arrow.now().datetime
    }
    utils.add_one_data(coll, data)


# input_image_path = "C:\\Users\\70931\\Documents\\images_website\\static\\images\\游戏\\原神\\宵宫\\1e1a9ae6f99870f950a6dd1fb9e393e.jpg"
# output_image_path = "C:\\Users\\70931\\Desktop/test.jpg"
# generate_thumbnail(input_image_path, output_image_path)

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB（示例）
    app.run(debug=True, port=5001)
