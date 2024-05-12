from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from models.pub_sub import Subscriber
from main import app
from utils import get_mongo_client
from models.recommendation import PostRecommendation
from models.user import RegisterUser
import mock
from routers.user import auth_manager

test_user = {"id": "random"}
app.dependency_overrides[auth_manager] = lambda: test_user
client = TestClient(app)




def test_recommender(mocker):

    #Check for failure in getting the recommendation
    response = client.get("/recommender/get-recommendations?page=1")
    assert response.status_code == 400

    mocker.patch("routers.recommender.get_data_from_api", return_value={"list_recommendations": [], "message": "Retrieved posts by query"})
    mocker.patch("routers.recommender.get_posts_by_query", return_value=[])
    response = client.get("/recommender/get-recommendations?page=1&query=x")
    assert response.status_code == 200

# TODO change tests
# def test_post_sub():
#     sub = Subscriber(ip_address="123456789", port=1000)
#     response = client.post("/observer/subscribe", json=jsonable_encoder(sub))
#     assert response.status_code == 200
#     assert response.json() == {"message": "Observer subscribed"}

#     sub2 = Subscriber(ip_address="123456789", port=1000)
#     response = client.post("/observer/subscribe", json=jsonable_encoder(sub2))
#     assert response.status_code == 400


# def test_get_sub():
#     response = client.get("/observer/subscribers")
#     assert response.status_code == 200
#     assert "subscribers" in response.json() and type(response.json()["subscribers"]) is list


# def test_update_sub_fail(capsys):
#     update_subscribers(["random"])
#     captured = capsys.readouterr()
#     assert "Could not send update to" in captured.out
