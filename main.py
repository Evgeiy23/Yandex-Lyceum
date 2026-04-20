from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.jobs import AddJobForm
from forms.department import DepartmentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs, title="Works log")


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        if form.category.data:
            from data.category import Category
            for cat_id in form.category.data.split(','):
                category = db_sess.query(Category).get(cat_id.strip())
                if category:
                    job.categories.append(category)
        
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('form_page.html', title='Adding a Job', form=form)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()