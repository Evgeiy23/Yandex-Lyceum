from data import db_session
from data.users import User


def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()

    captain = User(
        surname="Scott",
        name="Ridley",
        age=21,
        position="captain",
        speciality="research engineer",
        address="module_1",
        email="scott_chief@mars.org"
    )

    colonist1 = User(
        surname="Watney",
        name="Mark",
        age=35,
        position="specialist",
        speciality="botanist",
        address="module_2",
        email="mark_watney@mars.org"
    )

    colonist2 = User(
        surname="Vogel",
        name="Alex",
        age=40,
        position="specialist",
        speciality="chemist",
        address="module_1",
        email="alex_vogel@mars.org"
    )

    colonist3 = User(
        surname="Johanssen",
        name="Beth",
        age=28,
        position="specialist",
        speciality="system engineer",
        address="module_1",
        email="beth_j@mars.org"
    )

    db_sess.add(captain)
    db_sess.add(colonist1)
    db_sess.add(colonist2)
    db_sess.add(colonist3)

    db_sess.commit()


if __name__ == '__main__':
    main()