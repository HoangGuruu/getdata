from flask import Flask, render_template, jsonify
import boto3
import plotly.graph_objects as go
from operator import itemgetter

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/data')
def data():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id='AKIA2WYEQAQ6KE2HU6M5', aws_secret_access_key='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')
    table = dynamodb.Table('DataRaspi2')

    response = table.scan() 
    data = response['Items'] 
 
    # Sắp xếp dữ liệu theo thời gian
    data.sort(key=lambda item: item['payload']['timestamp'])
    lat_values = [float(item['payload']['lat']) for item in data]
    lon_values = [float(item['payload']['lon']) for item in data] 

 
    timestamps = [item['payload']['timestamp'] for item in data]
    ax_values = [float(item['payload']['ax']) for item in data]

    return jsonify(timestamps=timestamps, ax_values=ax_values, lat_values=lat_values, lon_values=lon_values)

if __name__ == '__main__':
    app.run(debug=True)
