import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('galery'))

    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template(
        'galery.html',
        title='Красная планета',
        images=images
    )


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(port=8080, host='127.0.0.1')