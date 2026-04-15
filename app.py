from flask import Flask, url_for, render_template_string

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Пейзажи Марса</title>
    <style>
      h1 { text-align: center; margin: 30px 0; }
      .carousel { max-width: 800px; margin: 0 auto; }
    </style>
  </head>
  <body>
    <h1>Пейзажи Марса</h1>
    
    <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img src="{{ url_for('static', filename='img/mars1.jpg') }}" class="d-block w-100" alt="Mars 1">
        </div>
        <div class="carousel-item">
          <img src="{{ url_for('static', filename='img/mars2.jpg') }}" class="d-block w-100" alt="Mars 2">
        </div>
        <div class="carousel-item">
          <img src="{{ url_for('static', filename='img/mars3.jpg') }}" class="d-block w-100" alt="Mars 3">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
"""


@app.route('/carousel')
def carousel():
    return render_template_string(HTML)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')