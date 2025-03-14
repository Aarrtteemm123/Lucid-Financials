from fastapi import APIRouter
from views import LoginView, PostView

view_router = APIRouter()
api_router = APIRouter()

login_view = LoginView()
posts_view = PostView()

view_router.add_api_route('/login', login_view.login, methods=['POST'])
view_router.add_api_route('/signup', login_view.signup, methods=['POST'])

view_router.add_api_route('/add-post', posts_view.add_post, methods=['POST'])
view_router.add_api_route('/get-posts', posts_view.get_posts, methods=['GET'])
view_router.add_api_route('/delete-post', posts_view.delete_post, methods=['DELETE'])
