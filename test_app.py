from app import app

def test_home():
    client = app.test_client()
    response = client.get("/health")
    
    assert response.status_code == 200
    