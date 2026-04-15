import os
from flask import Flask, request, url_for, render_template_string

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'

HTML = """
<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" 
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <title>Отбор астронавтов</title>
  </head>
  <body>
    <div class="container">
      <h2>Загрузка фотографии</h2>
      <h1>Для участия в миссии</h1>
      <form method="post" enctype="multipart/form-data" class="mt-4">
        <div class="mb-3">
          <label for="formFile" class="form-label">Приложите фотографию</label>
          <input class="form-control" type="file" id="formFile" name="file" required>
        </div>
        {% if img_path %}
          <img src="{{ img_path }}" alt="Ваше фото" class="img-preview">
        {% endif %}
        <button type="submit" class="btn btn-danger w-100">Отправить</button>
      </form>
    </div>
  </body>
</html>
"""


@app.route('/load_photo', methods=['GET', 'POST'])
def load_photo():
    img_path = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = file.filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            img_path = url_for('static', filename=f'img/{filename}')

    return render_template_string(HTML, img_path=img_path)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(port=8080, host='127.0.0.1')