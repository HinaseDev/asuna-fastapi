from main import app
from fastapi.testclient import TestClient
import pathlib as p
import json
import globs

client = TestClient(app)

def test_get_usage():
    response = client.get("/usage")
    assert response.status_code == 200
    assert response.json() == json.load(open(globs.USAGE_PATH))

def test_get_random_images():
    images_path = globs.images_directory
    for image_type in images_path.iterdir():
        if image_type.is_dir():
            images = [img for img in image_type.iterdir() if img.is_file()]
            if images:
                response = client.get(f"/api/random/{image_type.name}")
                assert response.status_code == 200
                data = response.json()
                assert "fileName" in data and "url" in data

def test_get_random_image_invalid():
    response = client.get("/api/random/nonexistent_category")
    assert response.status_code == 200
    assert response.json() == {"error": "Picture category not found or there are no images in this category"}

