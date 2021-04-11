## Quick Start

### Requirements:
1. Implement `WishList` and `Gift` models and create migrations for them (without `photo`, `is_booked`, `user`, `photo` fields)
2. Implement LIST (/wishlist/) and GET (/wishlist/:id/) to return information about each checklist and gifts.

Approximate response:
```
{
  "id": 0,
  "name": "",
  "due_date": "",
  "gifts": [
    {
      "id": 0,
      "name": "",
      "description": "",
      ...
    }
  ]
}
```

3. Implement basic POST to /wishlist/ and POST /gift/
4. (Most complex one) Write integration tests for step 2 and 3 (note: some fixtures should be fixed)

Tip: `Flask-Marshmallow` might be good for data serialization, but you can implement that even without marshmallow library.

```shell
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# Apply migrations
python3 manage.py db upgrade

# Run project
python3 app.py

# Check that project is working
curl http://127.0.0.1:5000/about/
```

### Tests

```shell
pytest tests
```
