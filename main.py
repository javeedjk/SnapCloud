import os
from flask import Flask, redirect, request, Response, session
from google.cloud import storage
import io


storage = storage.Client()
bucket_name = "cloud-computing-fil"

app = Flask(__name__)


@app.route('/')
def index():
    
    indexhtml = """
    <body>
    <br/>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <table align = 'center'>
            <tr>
                <td>Select a image</td>
                <td><input type="file" name="image" accept="image/**" required></td>
            </tr>
            <tr>
                <td colspan = 2 align = 'center'> <input type='submit' value='upload'</td>
            </tr>
        </table>
        <h2 align='center'>Avaiable Items </h2>
    </form>
    <ul align='center'>
    """
    image_files = all_image_files()
    for image in image_files:
        indexhtml += f'<li><a href="/files/{image}">{image}</a></li>'
    indexhtml += '''</ul>
    </body>'''
    return indexhtml

@app.route('/upload', methods=["POST"])
def upload_image():
    image = request.files['image']


    bucket = storage.bucket(bucket_name)
    blob_image = bucket.blob(image.filename)
    blob_image.upload_from_file(file_obj=image, rewind=True)
    
    
    return redirect("/")

@app.get('/images')
def all_image_files():
    images = []
    all_bucket_files = storage.list_blobs(bucket_name)
    for file in all_bucket_files:
        if file.name.lower().endswith(".jpeg") or file.name.lower().endswith(".jpg") or  file.name.lower().endswith(".png"):
            images.append(file.name)
    return images

@app.get('/files/<filename>')
def source_image_files(filename):

    html_file = f'''
    <br/>
    <body>
    <div style="background: radial-gradient(black, transparent); padding: 50px; 
                                border-radius: 120px; margin-left: 100px; margin-right: 100px;">
        <a href="/" style="padding: 50px;">Back to Home Page</a>
    <br/>
        <center >
            <h2>{filename}</h2>
            <img src="/images/{filename}" width='55%'>
        
        <br/><br/>
        </center>
    </div>
    </body>
    '''

    return html_file


@app.get('/images/<imagename>')
def getfile(imagename):
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(imagename)
    file_data = blob.download_as_bytes()
    return Response(io.BytesIO(file_data), mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host="localhost",port=5060, debug=True)
