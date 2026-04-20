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
app.config['SECRET_KEY'] = 'mars_explorer_secret_key'

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('form_page.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('form_page.html', title='Регистрация', form=form, message="Пользователь уже есть")
        user = User(
            surname=form.surname.data, name=form.name.data, age=form.age.data,
            position=form.position.data, speciality=form.speciality.data,
            address=form.address.data, email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('form_page.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('form_page.html', title='Авторизация', form=form, message="Неправильный логин или пароль")
    return render_template('form_page.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            job=form.job.data, team_leader=form.team_leader.data,
            work_size=form.work_size.data, collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('form_page.html', title='Adding a Job', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = AddJobForm()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if not job:
        abort(404)
    if job.team_leader != current_user.id and current_user.id != 1:
        abort(403)
    if request.method == "GET":
        form.job.data = job.job
        form.team_leader.data = job.team_leader
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished
    if form.validate_on_submit():
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/')
    return render_template('form_page.html', title='Editing a Job', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if not job:
        abort(404)
    if job.team_leader == current_user.id or current_user.id == 1:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(403)
    return redirect('/')


@app.route("/departments")
def list_departments():
    db_sess = db_session.create_session()
    depts = db_sess.query(Department).all()
    return render_template("departments.html", departments=depts, title="List of Departments")


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dept = Department(
            title=form.title.data, chief=form.chief.data,
            members=form.members.data, email=form.email.data
        )
        db_sess.add(dept)
        db_sess.commit()
        return redirect('/departments')
    return render_template('form_page.html', title='Adding a Department', form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    db_sess = db_session.create_session()
    dept = db_sess.query(Department).filter(Department.id == id).first()
    if not dept:
        abort(404)
    if dept.chief != current_user.id and current_user.id != 1:
        abort(403)
    if request.method == "GET":
        form.title.data = dept.title
        form.chief.data = dept.chief
        form.members.data = dept.members
        form.email.data = dept.email
    if form.validate_on_submit():
        dept.title = form.title.data
        dept.chief = form.chief.data
        dept.members = form.members.data
        dept.email = form.email.data
        db_sess.commit()
        return redirect('/departments')
    return render_template('form_page.html', title='Editing a Department', form=form)


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    dept = db_sess.query(Department).filter(Department.id == id).first()
    if not dept:
        abort(404)
    if dept.chief == current_user.id or current_user.id == 1:
        db_sess.delete(dept)
        db_sess.commit()
    else:
        abort(403)
    return redirect('/departments')


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()