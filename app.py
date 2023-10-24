import os
from flask import Flask, render_template, send_file, url_for, request, redirect
import random
import utils

app = Flask(__name__)

# 假设我们的图片文件存放在 static/images 目录下
image_folder = "static/images"
thumbnail_path = "static/thumbnail"
path_of_images = "images"
path_of_thumbnail = "thumbnail"
images_per_page = 12  # 每页显示12张图片
images_per_page_pc = 10
first_page_size = 6


# 预览页，显示分类的图片列表，两张一行，带分页
@app.route('/preview/<string:cate>')
def preview(cate):
    coll = utils.get_collect(utils.get_conn(), utils.coll)
    data = utils.select_by_cate(coll, cate)
    page = int(request.args.get("page", 1))
    mobile_keywords = ['iPhone', 'Android', 'Windows Phone']
    user_agent = request.headers.get('User-Agent')
    new_num = images_per_page_pc
    for kw in mobile_keywords:
        if kw in user_agent:
            new_num = images_per_page
            break
    start_idx = (page - 1) * new_num
    end_idx = start_idx + new_num
    paginated_images = data[start_idx:end_idx]
    total_pages = (len(data) + new_num - 1) // new_num
    print(paginated_images)
    return render_template("preview.html", images=paginated_images, page=page, total_pages=total_pages,
                           cate=cate, page_name='preview')


# 详情页，单张图片展示，加下载原图按钮
@app.route('/search/', defaults={'keyword': ''})
@app.route('/search/<string:keyword>')
def search(keyword, page=1):
    keyword = keyword.strip()
    collection = utils.get_collect(utils.get_conn(), utils.coll)
    query = {
        "$or": [
            {"cate": {"$regex": keyword, "$options": "i"}},
            {"tag": {"$regex": keyword, "$options": "i"}}
        ]
    }

    # 执行查询
    results = collection.find(query).sort('create_time', -1)
    mobile_keywords = ['iPhone', 'Android', 'Windows Phone']
    user_agent = request.headers.get('User-Agent')
    new_num = images_per_page_pc
    for kw in mobile_keywords:
        if kw in user_agent:
            new_num = images_per_page
            break
    if results.count() != 0:
        print(results.count())
        data = list(results)
        page = int(request.args.get("page", 1))
        start_idx = (page - 1) * new_num
        end_idx = start_idx + new_num
        paginated_images = data[start_idx:end_idx]
        total_pages = (len(data) + new_num - 1) // new_num
        return render_template("search.html", images=paginated_images, page=page, total_pages=total_pages,
                               keyword=keyword, message='以下是"' + keyword + '"的搜索结果')
    else:
        return render_template("search.html", images=[], page=page, total_pages=1,
                               keyword=keyword, message='未找到有关"' + keyword + '"的结果')
        # print(request.referrer)
        # previous_page = request.referrer
        # if previous_page is not None:
        #     return redirect(previous_page)
        # else:
        #     return redirect('/')


# 中间件函数，用于检查User Agent
@app.before_request
def check_user_agent():
    user_agent = request.headers.get('User-Agent')
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
        # 如果User Agent中包含手机相关的字符串，重定向到手机用户页面
        pass
    else:
        return "傻逼华为云"




@app.route('/')
def home():
    mobile_keywords = ['iPhone', 'Android', 'Windows Phone']
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    new_num = 10
    for keyword in mobile_keywords:
        if keyword in user_agent:
            new_num = first_page_size
            break

    conn = utils.get_conn()
    coll = utils.get_collect(conn, utils.coll)
    res = list(coll.find().sort('create_time', -1).limit(new_num))
    res_random = coll.aggregate([{'$sample': {'size': 12}}])
    print(res)
    return render_template("index.html", first_category_images=res, random_images=res_random)


@app.route('/more')
def more(page=1):
    mobile_keywords = ['iPhone', 'Android', 'Windows Phone']
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    page = int(request.args.get("page", 1))
    new_num = 10
    all_num = 100
    skip_size = 10
    for keyword in mobile_keywords:
        if keyword in user_agent:
            new_num = 12
            all_num = 96
            skip_size = first_page_size
            break

    conn = utils.get_conn()
    coll = utils.get_collect(conn, utils.coll)
    res = list(coll.find().sort('create_time', -1).limit(all_num).skip(skip_size))
    start_idx = (page - 1) * new_num
    end_idx = start_idx + new_num
    paginated_images = res[start_idx:end_idx]
    total_pages = (len(res) + new_num - 1) // new_num
    return render_template("preview.html", images=paginated_images, page=page, total_pages=total_pages,
                           cate='最新图片', page_name='more')


@app.route('/category')
def category():
    cates = utils.get_redis_cates()
    conn = utils.get_conn()
    coll = utils.get_collect(conn, utils.coll)
    data = []
    for cate in cates:
        conf_data = utils.select_by_cate(coll, cate, one=True)
        data.append(conf_data)
    print("a", sorted(cates))
    print(data)
    return render_template('category.html', cate=data)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=7009)
