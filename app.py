import os
from flask import Flask, render_template, send_file, url_for, request
import random

app = Flask(__name__)

# 假设我们的图片文件存放在 static/images 目录下
image_folder = "static/images"
path_of_images = "images"
images_per_page = 12  # 每页显示12张图片


# 预览页，显示分类的图片列表，两张一行，带分页
@app.route('/preview/<string:first_level_category>/<string:second_level_category>/<string:third_level_category>')
def preview(first_level_category, second_level_category, third_level_category):
    images = []
    category_level1 = first_level_category
    category_level2 = second_level_category
    category_level3 = third_level_category
    if os.path.isdir(os.path.join(image_folder, category_level1, category_level2, category_level3)):
        category_level4_images = os.listdir(
            os.path.join(image_folder, category_level1, category_level2, category_level3))
        for image_file in category_level4_images:
            image = {
                "category_level1": category_level1,
                "category_level2": category_level2,
                "category_level3": category_level3,
                "filename": (
                    os.path.join(path_of_images, category_level1, category_level2, category_level3,
                                 image_file)).replace("\\", "/"),  # 图片文件相对路径，包含分类信息
            }
            images.append(image)
    page = int(request.args.get("page", 1))
    start_idx = (page - 1) * images_per_page
    end_idx = start_idx + images_per_page

    paginated_images = images[start_idx:end_idx]

    total_pages = (len(images) + images_per_page - 1) // images_per_page
    return render_template("preview.html", images=paginated_images, page=page, total_pages=total_pages,
                           first_level_category=category_level1, second_level_category=category_level2,
                           third_level_category=category_level3)


# 详情页，单张图片展示，加下载原图按钮
@app.route('/image/<path:image_path>')
def image_detail(image_path):
    images = []
    for category_level1 in os.listdir(image_folder):
        if os.path.isdir(os.path.join(image_folder, category_level1)):
            # 遍历一级分类目录下的子目录，作为二级分类
            for category_level2 in os.listdir(os.path.join(image_folder, category_level1)):
                if os.path.isdir(os.path.join(image_folder, category_level1, category_level2)):
                    # 遍历二级分类目录下子目录，作为三级分类
                    for category_level3 in os.listdir(os.path.join(image_folder, category_level1, category_level2)):
                        if os.path.isdir(os.path.join(image_folder, category_level1, category_level2, category_level3)):
                            category_level4_images = os.listdir(
                                os.path.join(image_folder, category_level1, category_level2, category_level3))
                            for image_file in category_level4_images:
                                image = {
                                    "category_level1": category_level1,
                                    "category_level2": category_level2,
                                    "category_level3": category_level3,
                                    "filename": (
                                        os.path.join(path_of_images, category_level1, category_level2, category_level3,
                                                     image_file)).replace("\\", "/"),  # 图片文件相对路径，包含分类信息
                                }
                                images.append(image)
    image = next((img for img in images if img["filename"] == image_path), None)
    if image:
        return render_template("detail.html", image=image)
    else:
        return "Image not found", 404


# 下载原图
@app.route('/download/<path:image_path>')
def download_image(image_path):
    return send_file((os.path.join("static", image_path)).replace("\\", "/"), as_attachment=True)


@app.route('/')
def home():
    images = []
    first_category_images = {}  # Dictionary to store first-level category names and their images
    for category_level1 in os.listdir(image_folder):
        if os.path.isdir(os.path.join(image_folder, category_level1)):
            # 遍历一级分类目录下的子目录，作为二级分类
            for category_level2 in os.listdir(os.path.join(image_folder, category_level1)):
                if os.path.isdir(os.path.join(image_folder, category_level1, category_level2)):
                    # 遍历二级分类目录下子目录，作为三级分类
                    for category_level3 in os.listdir(os.path.join(image_folder, category_level1, category_level2)):
                        if os.path.isdir(os.path.join(image_folder, category_level1, category_level2, category_level3)):
                            category_level4_images = os.listdir(
                                os.path.join(image_folder, category_level1, category_level2, category_level3))
                            for image_file in category_level4_images:
                                image = {
                                    "category_level1": category_level1,
                                    "category_level2": category_level2,
                                    "category_level3": category_level3,
                                    "filename": (
                                        os.path.join(path_of_images, category_level1, category_level2, category_level3,
                                                     image_file)).replace("\\", "/"),  # 图片文件相对路径，包含分类信息
                                }
                                images.append(image)
    for category_level1 in os.listdir(image_folder):
        if os.path.isdir(os.path.join(image_folder, category_level1)):
            for category_level2 in os.listdir(os.path.join(image_folder, category_level1)):
                if os.path.isdir(os.path.join(image_folder, category_level1, category_level2)):
                    for category_level3 in os.listdir(os.path.join(image_folder, category_level1, category_level2)):
                        if os.path.isdir(os.path.join(image_folder, category_level1, category_level2, category_level3)):
                            image_files = os.listdir(
                                os.path.join(image_folder, category_level1, category_level2, category_level3))
                            if image_files:
                                image_filename = image_files[0]  # Get the first image in the third-level category
                                image_path = (
                                    os.path.join(path_of_images, category_level1, category_level2, category_level3,
                                                 image_filename)).replace("\\", "/")
                                image = {
                                    "category_level1": category_level1,
                                    "filename": image_path
                                }
                                first_category_images[category_level1] = image
                                break  # Only select the first image for each first-level category
                    if category_level1 in first_category_images:  # If we found an image for the first-level category, stop the loop
                        break
    print(first_category_images)
    # Randomly select some images for the random section
    num_random_images = 12  # You can adjust the number of random images to display
    random_images = random.sample(images, num_random_images)
    print(first_category_images)
    return render_template("index.html", first_category_images=first_category_images, random_images=random_images)


@app.route('/second/<string:first_level_category>')
def second_and_third_level_category(first_level_category):
    print(first_level_category)
    third_category_images = {}  # Dictionary to store first-level category names and their images
    print(os.path.join(image_folder, first_level_category))
    if os.path.isdir(os.path.join(image_folder, first_level_category)):
        for category_level2 in os.listdir(os.path.join(image_folder, first_level_category)):
            level3_list = []
            print("aaa", os.path.join(image_folder, first_level_category, category_level2))
            if os.path.isdir(os.path.join(image_folder, first_level_category, category_level2)):
                for category_level3 in os.listdir(os.path.join(image_folder, first_level_category, category_level2)):

                    if os.path.isdir(
                            os.path.join(image_folder, first_level_category, category_level2, category_level3)):
                        image_files = os.listdir(
                            os.path.join(image_folder, first_level_category, category_level2, category_level3))
                        if image_files:
                            print(666)
                            image_filename = image_files[0]  # Get the first image in the third-level category
                            image_path = (
                                os.path.join(path_of_images, first_level_category, category_level2, category_level3,
                                             image_filename)).replace("\\", "/")
                            image = {
                                "category_level1": first_level_category,
                                "category_level2": category_level2,
                                "category_level3": category_level3,
                                "filename": image_path
                            }
                            level3_list.append(image)
                third_category_images[category_level2] = level3_list
    print(third_category_images)
    return render_template("second.html",
                           first_level_category=first_level_category, third_category_images=third_category_images
                           )


if __name__ == '__main__':
    app.run(debug=True)
