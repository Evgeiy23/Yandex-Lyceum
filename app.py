from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index/<title>')
def index(title="Заголовок"):
    return render_template('base.html', title=title)


@app.route('/list_prof/<list_type>')
def list_prof(list_type):
    professions = [
        'инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач',
        'инженер по терраформированию', 'климатолог',
        'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
        'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода',
        'киберинженер', 'штурман', 'пилот дронов'
    ]
    return render_template(
        'list_prof.html',
        title='Список профессий',
        professions=professions,
        list_type=list_type
    )


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')