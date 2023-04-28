from project import generate_password

# Tests for projects
def test_generate_password():
    assert len(generate_password()) == 16
    assert len(generate_password(32)) == 32