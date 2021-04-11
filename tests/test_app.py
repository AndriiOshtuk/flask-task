import pytest
import datetime

from models import db, WishList, Gift


@pytest.fixture()
def create_wishlist(db):
    def _create_wishlist(name, due_date):
        item = WishList(name=name, due_date=due_date)
        db.session.add(item)
        return

    return _create_wishlist


@pytest.fixture()
def create_gift(db):
    def _create_gift(
        name,
        wishlist_id,
        description="description",
        price=20.0,
        url="http://127.0.0.1:5000/about",
    ):
        item = Gift(
            name=name,
            description=description,
            price=price,
            url=url,
            wishlist_id=wishlist_id,
        )
        db.session.add(item)
        return

    return _create_gift


@pytest.mark.usefixtures("app")
def test_get_wishlist_list(client, create_wishlist, create_gift):

    create_wishlist(name="WishList 1", due_date=datetime.date(2025, 11, 4))
    create_wishlist(name="WishList 2", due_date=datetime.date(2025, 11, 4))
    create_gift(name="Gift 1", wishlist_id=1)

    response = client.get("/wishlist/")

    content = response.get_json()

    assert response.status_code == 200

    assert content[0]["name"] == "WishList 1"
    assert content[0]["gifts"][0]["name"] == "Gift 1"
    assert len(content[0]["gifts"]) == 1

    assert content[1]["name"] == "WishList 2"
    assert len(content[1]["gifts"]) == 0


@pytest.mark.usefixtures("app")
def test_create_wishlist(client):

    test_data = {"name": "WishList 1", "due_date": "2025-11-04"}

    response = client.post("/wishlist/", json=test_data)

    # check response
    content = response.get_json()

    assert content["name"] == test_data["name"]
    assert content["due_date"] == test_data["due_date"]

    # check DB
    wishlist = WishList.query.get(1)
    due_date = wishlist.due_date.strftime("%Y-%m-%d")

    assert wishlist.name == test_data["name"]
    assert due_date == test_data["due_date"]


@pytest.mark.usefixtures("app")
def test_get_wishlist_detail(client, create_wishlist, create_gift):

    create_wishlist(name="WishList 1", due_date=datetime.date(2025, 11, 4))
    create_gift(name="Gift 1", wishlist_id=1)

    response = client.get("/wishlist/1")

    content = response.get_json()

    assert response.status_code == 200

    assert content["name"] == "WishList 1"
    assert content["gifts"][0]["name"] == "Gift 1"
    assert len(content["gifts"]) == 1


@pytest.mark.usefixtures("app")
def test_get_gift_detail(client, create_wishlist, create_gift):

    create_wishlist(name="WishList 1", due_date=datetime.date(2025, 11, 4))
    create_gift(
        name="Gift 1",
        wishlist_id=1,
        description="description",
        price=20.0,
        url="http://127.0.0.1:5000/about",
    )

    response = client.get("/gift/1")

    content = response.get_json()

    assert response.status_code == 200

    assert content["name"] == "Gift 1"
    assert content["wishlist_id"] == 1
    assert content["description"] == "description"
    assert content["price"] == 20.0
    assert content["url"] == "http://127.0.0.1:5000/about"


@pytest.mark.usefixtures("app")
def test_create_gift(client, create_wishlist):

    create_wishlist(name="WishList 1", due_date=datetime.date(2025, 11, 4))

    gift_test_data = {
        "name": "Gift 1",
        "description": "description",
        "price": 20.0,
        "url": "http://127.0.0.1:5000/about",
        "wishlist_id": 1,
    }
    response = client.post("/gift/", json=gift_test_data)

    # check response
    content = response.get_json()
    assert content["name"] == gift_test_data["name"]
    assert content["description"] == gift_test_data["description"]
    assert content["price"] == gift_test_data["price"]
    assert content["url"] == gift_test_data["url"]
    assert content["wishlist_id"] == gift_test_data["wishlist_id"]

    # check DB
    gift = Gift.query.get(1)
    assert gift.name == gift_test_data["name"]
    assert gift.description == gift_test_data["description"]
    assert gift.price == gift_test_data["price"]
    assert gift.url == gift_test_data["url"]
    assert gift.wishlist_id == gift_test_data["wishlist_id"]


@pytest.mark.usefixtures("app")
def test_integration(client):

    dummy_wishlist = {"name": "WishList 1", "due_date": "2025-11-04"}
    response = client.post("/wishlist/", json=dummy_wishlist)
    assert response.status_code == 200

    dummy_gift = {
        "name": "Gift 1",
        "description": "description",
        "price": 20.0,
        "url": "http://127.0.0.1:5000/about",
        "wishlist_id": 1,
    }
    response = client.post("/gift/", json=dummy_gift)
    assert response.status_code == 200

    response = client.get("/wishlist/")

    content = response.get_json()

    assert response.status_code == 200

    assert content[0]["name"] == "WishList 1"
    assert content[0]["gifts"][0]["name"] == "Gift 1"
    assert len(content[0]["gifts"]) == 1
