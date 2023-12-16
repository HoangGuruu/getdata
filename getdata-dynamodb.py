from flask import Flask, render_template, jsonify
import boto3
import plotly.graph_objects as go
from operator import itemgetter

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def data():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id='AKIA2WYEQAQ6LFOL3FO7', aws_secret_access_key='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')
    table = dynamodb.Table('Raspi-table')

    response = table.scan()
    data = response['Items']

    # Sắp xếp dữ liệu theo thời gian
    data.sort(key=lambda item: item['payload']['timestamp'])

    timestamps = [item['payload']['timestamp'] for item in data]
    ax_values = [float(item['payload']['ax']) for item in data]

    return jsonify(timestamps=timestamps, ax_values=ax_values)

if __name__ == '__main__':
    app.run(debug=True)
