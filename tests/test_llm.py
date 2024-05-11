from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from models.llm import PostAnalysis
from main import app
import mock
from utils import get_mongo_client

client = TestClient(app)


@mock.patch("routers.llm.llm_client", get_mongo_client()["llm_test"])
def test_add_analysis_no_post():
    post_analysis = PostAnalysis(
        post_id="random",
        completion={
            "title": "random",
            "summary": "random",
        },
    )
    response = client.post("/llm/add-analysis", json=jsonable_encoder(post_analysis))
    assert response.status_code == 400

