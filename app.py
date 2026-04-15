import json
import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/member')
def member():
    json_path = os.path.join(app.root_path, 'templates', 'crew.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        crew_list = json.load(f)
        
    return render_template('member.html', title='Член экипажа', members=crew_list)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')