import os
from flask import Flask, render_template, request
import time

app = Flask(__name__)

# 设置文件上传的目录
app.config['UPLOAD_FOLDER'] = 'static/images'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取上传的文件和表单数据
        file = request.files['file']
        directory1 = request.form['directory1']
        directory2 = request.form['directory2']
        directory3 = request.form['directory3']

        print(os.path.join(app.config['UPLOAD_FOLDER'], directory1, directory2, directory3))
        # 检查是否选择了三级目录
        # if not directory1 or not directory2 or not directory3:
        #     return '请填写完整的目录信息！'

        # 创建目录（如果不存在）
        target_directory = os.path.join(app.config['UPLOAD_FOLDER'], directory1, directory2, directory3)
        os.makedirs(target_directory, exist_ok=True)

        # Check if a file with the same name exists in the target directory
        filename, file_extension = os.path.splitext(file.filename)
        timestamp = str(int(time.time()))
        target_file_path = os.path.join(target_directory, file.filename)
        while os.path.exists(target_file_path):
            file.filename = f"{filename}_{timestamp}{file_extension}"
            target_file_path = os.path.join(target_directory, file.filename)

        file.save(target_file_path)

        return '文件上传成功！'

    return render_template('upload.html')


if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB（示例）
    app.run(debug=True, port=5001)
