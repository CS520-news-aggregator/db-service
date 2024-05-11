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


# def test_get_sub():
#     response = client.get("/observer/subscribers")
#     assert response.status_code == 200
#     assert "subscribers" in response.json() and type(response.json()["subscribers"]) is list


# def test_update_sub_fail(capsys):
#     update_subscribers(["random"])
#     captured = capsys.readouterr()
#     assert "Could not send update to" in captured.out
