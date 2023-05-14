from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    user_name = request.form['user_name']
    computer_name = request.form['computer_name']
    static_ip = request.form['static_ip']

    # 读取已存在的数据
    try:
        existing_data = pd.read_excel('ip_log.xlsx')
        if 'User Name' not in existing_data.columns:
            existing_data['User Name'] = ''
        if 'Computer Name' not in existing_data.columns:
            existing_data['Computer Name'] = ''
        if 'Static IP' not in existing_data.columns:
            existing_data['Static IP'] = ''
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    # 检查重复的IP或计算机名称
    if (existing_data['Static IP'] == static_ip).any() and (existing_data['Computer Name'] == computer_name).any():
        return render_template('index.html', error_msg_ip='已有相同的IP，请重新输入', error_msg_cn='已有相同的计算机名称，请重新输入', user_name=user_name, static_ip=static_ip, computer_name=computer_name)
    elif (existing_data['Static IP'] == static_ip).any():
        return render_template('index.html', error_msg_ip='已有相同的IP，请重新输入', user_name=user_name, static_ip=static_ip, computer_name=computer_name)
    elif (existing_data['Computer Name'] == computer_name).any():
        return render_template('index.html', error_msg_cn='已有相同的计算机名称，请重新输入', user_name=user_name, static_ip=static_ip, computer_name=computer_name)

    # 创建新的数据行
    df = pd.DataFrame({'User Name': [user_name], 'Computer Name': [computer_name], 'Static IP': [static_ip]})

    # 合并新数据并保存到Excel文件
    updated_data = pd.concat([existing_data, df], ignore_index=True)
    updated_data.to_excel('ip_log.xlsx', index=False)

    return render_template('index.html', success='Registration successful!')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
