from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from models.pub_sub import Subscriber
from main import app
from utils import get_mongo_client
from models.recommendation import PostRecommendation
import mock
from models.post import Post, Comment
from routers.user import auth_manager


test_user = {"id": "f8a21c66-fdd2-4f3a-8eff-229a18d747e4"}
app.dependency_overrides[auth_manager] = lambda: test_user
client = TestClient(app)





post_recommendation = PostRecommendation(
    post_id="random",
    topics=["random"],
    date="random",
)

post = Post(
    source_ids=["random"],
    topics=["random"],
    summary="random",
    title="random",
    media="random",
    date="random",
    upvotes=0,
    downvotes=0
)

comment = Comment(
    content="random",
    post_id="random",
    upvotes=0,
    downvotes=0
)

annotator_client = get_mongo_client()["annotator"]

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_annotator():


    response = client.post("/annotator/add-post", json=jsonable_encoder(post))
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_get_post():
    response = client.get(f"/annotator/get-post?post_id={post.id}")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_get_all_posts():
    response = client.get("/annotator/get-all-posts")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_upvote_post():
    response = client.put(f"/annotator/upvote-post?post_id={post.id}")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_downvote_post():
    response = client.put(f"/annotator/upvote-comment?comment_id={comment.id}")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_downvote_post():
    response = client.put(f"/annotator/downvote-post?post_id={post.id}")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_downvote_comment():
    response = client.put(f"/annotator/downvote-comment?comment_id={comment.id}")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_remove_upvote_comment():
    response = client.put(f"/annotator/remove-upvote-comment?comment_id={comment.id}")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_remove_downvote_comment():
    response = client.put(f"/annotator/remove-downvote-comment?comment_id={comment.id}")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_remove_upvote_post():
    response = client.put(f"/annotator/remove-upvote-post?post_id={post.id}")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_remove_downvote_post():
    response = client.put(f"/annotator/remove-downvote-post?post_id={post.id}")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_comment_post():
    response = client.post("/annotator/comment", json=jsonable_encoder(comment))
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_get_comments():
    response = client.get(f"/annotator/get-comments?post_id={post.id}")
    assert response.status_code == 200

@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_get_comment():
    response = client.get(f"/annotator/get-comment?comment_id={comment.id}")
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
