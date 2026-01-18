from utils.database import count_users

def test_user_count():
    total = count_users()
    assert total >= 0