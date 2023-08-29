# images_website

# 一个图片站

## 配置mongo和redis
在项目根目录创建config.py
并写入mongo和redis配置项
如：
```
username = '' # mongo用户名
password = '' # mongo密码
r_password = '' # redis密码
hostname = "" # mongo和redis的地址
port =     # mongo端口
r_port =   # redis端口
r_db =    # redis库序号
database = "" # mongo库
coll = ''  # mongo集合
r_cate_key = '' # redis分类集合，list
r_tag_key = '' # redis标签集合，set,暂时无用
```
## 上传
```
python upload.py
```
## 浏览下载
```
python app.py
```
本项目用目录名称对应图片分类，分类和标签用于搜索

```
static/images/<分类>
```
## 后续优化计划：
1. 去掉三级分类，太他妈繁琐了 √
2. 点击全屏预览 √
3. 前端展示缩略图，右键下载原图 √
4. 上传图片生成缩略图，放在同一目录，命名加sl前缀 √
5. mongo存图片信息，redis存图片分类和标签 √
6. 多文件上传（安卓微信除外）√
7. 全屏预览左右滑动翻页 √
8. 全屏状态下左右滑移动图片，上下滑切换图片
9. 加个关于页，介绍操作 √
