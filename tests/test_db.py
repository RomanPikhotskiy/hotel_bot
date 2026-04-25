from database import CRUD, db


def test_add_new_user_does_not_create_duplicates(isolated_db):
    CRUD.create_table()

    CRUD.add_new_user("Test User", 42)
    CRUD.add_new_user("Test User", 42)

    users = list(db.Users.select().where(db.Users.id_tg == 42))
    assert len(users) == 1
    assert users[0].name == "Test User"


def test_add_new_hotel_saves_record(isolated_db):
    CRUD.create_table()

    CRUD.add_new_hotel(
        name="Hotel Name",
        address="Street 1",
        price=99.9,
        rating="5",
        preview="9.3",
        numb=0,
        id_user=1000,
        photos="https://img/1 https://img/2"
    )

    hotels = list(db.Hotels.select().where(db.Hotels.user_id == 1000))
    assert len(hotels) == 1
    assert hotels[0].name == "Hotel Name"
    assert hotels[0].address == "Street 1"
    assert float(hotels[0].price) == 99.9
    assert hotels[0].photos == "https://img/1 https://img/2"
