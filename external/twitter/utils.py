import functools

from external.twitter import TWITTER_SETTINGS, CLIENT
from external.twitter.dao import User

my_user_id = TWITTER_SETTINGS.REAL_USER_ID
fake_user_id = TWITTER_SETTINGS.FAKE_USER_ID


def _wrap_response(response):
    users = []
    for usr in response.data:
        usr_data = {
            'user_label': usr.name,
            'user_name': usr.username,
            'user_id': usr.id
        }
        # usr_schema = User()
        # usr_schema.load(usr_data)
        users.append(usr_data)

    # usr_schema = User(many=True)
    # usr_schema.load(users)
    return users


def _wrap_user(func, **kwargs):
    def __wrapper(**kwargs):
        response = func(**kwargs)
        users = _wrap_response(response)
        return users

    return __wrapper


@_wrap_user
def get_followers(user_id=fake_user_id):
    response = CLIENT.get_users_followers(user_id)
    return response


@_wrap_user
def get_following(user_id=fake_user_id):
    response = CLIENT.get_users_following(user_id)
    return response


def follow_it(*users: User):
    for usr in users:
        CLIENT.follow(usr['user_id'])


def unfollow_it(*users: User):
    for usr in users:
        CLIENT.unfollow(usr.user_id)


if __name__ == '__main__':
    fake_following = get_following(user_id=fake_user_id)
    real_followers = get_following(user_id=my_user_id)

    dif_followers = [i for i in fake_following if i not in real_followers]
    follow_it(*dif_followers)

    # followers = get_followers()
    # followings = get_following()
    # print(followers)
    # print(followings)
