import flask
from flask import Flask, request, render_template
import boto3, requests, json
import os

app = Flask(__name__)

ENDPOINT = 'https://xmv69ith93.execute-api.us-east-1.amazonaws.com/fast-stage'



def s3_bucket(image_name):
    s3_client = boto3.client('s3', aws_access_key_id='',
                             aws_secret_access_key='')
    print('client name is.....', s3_client)
    s3_resource = boto3.resource('s3', aws_access_key_id='',
                                 aws_secret_access_key='')
    print('client name is.....', s3_resource)
    # my_bucket = s3_resource.Bucket('ml-flow01')
    # print('bucket name is....', bucket)
    # try:
    # response = s3_client.upload_file('README.md', my_bucket, 'README.md')
    # response = s3_resource.Bucket('ml-flow01').put_object(Key=uploaded_file.filename, Body=uploaded_file)
    s3 = boto3.resource('s3')
    s3_resource.Bucket('ml-flow01').upload_file(f'static/images/{image_name}', image_name)
    response= api_endpoint(image_name)
    return response


def api_endpoint(image_name):
    # s3_bucket()
    data = {'key1': image_name}
    response = requests.post(
        ENDPOINT, data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    return response


@app.route('/')
def index():
    # response = api_endpoint('jay')
    # print(response)
    # print(response.status_code, response.content, response.reason, response.text)
    return render_template('index.html')


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    uploaded_file = request.files['myfile']
    uploaded_file.save(os.path.join('static/images', uploaded_file.filename))
    response= s3_bucket(uploaded_file.filename)

    return render_template('index.html', text= response.text, filename_= uploaded_file.filename)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
