import os
from flask import Flask, render_template, send_file, url_for, request, redirect, jsonify, json, Response
import random
import utils
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# app.config['JSON_AS_ASCII'] = False
# app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
# 假设我们的图片文件存放在 static/images 目录下
image_folder = "static/images"
thumbnail_path = "static/thumbnail"
path_of_images = "images"
path_of_thumbnail = "thumbnail"
images_per_page = 12  # 每页显示12张图片
images_per_page_pc = 10
first_page_size = 6


# 搜索接口，带分类参数，参数为‘’时搜索全部
@app.route('/search')
def search():
    keyword = request.args.get('keyword', '').strip()
    cate = request.args.get('cate', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', images_per_page))
    collection = utils.get_collect(utils.get_conn(), utils.coll)
    query = {
        "$and": [
            {
                "$or": [
                    {"cate": {"$regex": keyword, "$options": "i"}},
                    {"tag": {"$regex": keyword, "$options": "i"}}
                ]
            },
            {"cate": {"$regex": cate, "$options": "i"}}
        ]
    }

    # 执行查询
    results = collection.find(query, {'_id': 0}).sort('create_time', -1)
    mobile_keywords = ['iPhone', 'Android', 'Windows Phone']
    user_agent = request.headers.get('User-Agent')
    new_num = images_per_page_pc
    for kw in mobile_keywords:
        if kw in user_agent:
            new_num = images_per_page
            break
    page_size = new_num
    data_num = results.count()
    # data = list(results)
    start_idx = (page - 1) * new_num
    # end_idx = start_idx + new_num
    results.limit(new_num).skip(start_idx)
    paginated_images = list(results)  # data[start_idx:end_idx]
    total_pages = (data_num + new_num - 1) // new_num
    data = {"data": paginated_images, 'total_pages': total_pages, 'page': page, 'page_size': new_num}
    # return jsonify(data)
    resp = Response(json.dumps(data, ensure_ascii=False), content_type='application/json')
    # resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# 修改api
@app.route('/edit', methods=['POST'])
def edit():
    data = request.json
    data["tag"] = list(data["tag"].replace("，", ",").split(","))
    print(data["tag"])
    collection = utils.get_collect(utils.get_conn(), utils.coll)
    results = utils.update_by_img_path(collection, data)
    if results.modified_count:
        success = True
    else:
        success = False
    # return jsonify(data)
    resp = Response(json.dumps({"success": success, "modified_count": results.modified_count}, ensure_ascii=False),
                    content_type='application/json')
    # resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# 删除api
@app.route('/del', methods=['POST'])
def dele():
    data = request.json
    collection = utils.get_collect(utils.get_conn(), utils.coll)
    results = utils.delete_by_img_path(collection, data)
    image_path = data["image_path"]
    thumbnail_path = data["thumbnail_path"]
    os.remove(image_path)
    os.remove(thumbnail_path)
    data = {
        "deleted_count": results.deleted_count
    }
    resp = Response(json.dumps(data, ensure_ascii=False), content_type='application/json')
    # resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# return Response(json.dumps(data, ensure_ascii=False), content_type='application/json')


@app.route('/getCate')
def get_cate():
    data = utils.get_redis_cates()
    resp = Response(json.dumps(data, ensure_ascii=False), content_type='application/json')
    return resp


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username', '') == 'admin':
        if data.get('password', '') == utils.get_manage_pass().decode('utf-8'):
            return {"success": True}
        else:
            print(utils.get_manage_pass().decode('utf-8'))
    return {"success": False}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7010)
