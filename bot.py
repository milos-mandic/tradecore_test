import yaml
import string
import os
import random

from operator import itemgetter

from bot.requests import user_signup, post_creation, post_like, get_others_posts

cwd = os.getcwd()
print(cwd)
stream = open('bot/config.yaml', 'r')
config = yaml.load(stream)


def eligible_users(posts):
    list_of_eligible_users = list()
    users_with_posts = dict()
    for post in posts:
        if post.get("creator").get("email") not in users_with_posts.keys():
            users_with_posts[post.get("creator").get("email")] = list()
        if len(post.get("users_liked")) == 0:
            users_with_posts[post.get("creator").get("email")].append(post.get('id'))
    for user in users_with_posts.keys():
        if len(users_with_posts[user]) > 0:
            list_of_eligible_users.append(user)
    return list_of_eligible_users


def eligible_posts(posts, list_of_eligible_users):
    list_of_eligible_posts = list()
    for post in posts:
        if post.get("creator").get("email") in list_of_eligible_users:
            list_of_eligible_posts.append(post.get("id"))
    return list_of_eligible_posts


def signup_users():
    number_of_users = config.get('number_of_users')
    default_username = config.get('default_username')
    default_password = config.get('default_password')
    users = list()
    for user in range(number_of_users):
        token = user_signup(username=default_username + str(user),
                            email=default_username + str(user) + '@gmail.com',
                            password=default_password)
        if token is not None:
            users.append({'token': token,
                          'no_of_posts': 0})
            print('I have created a user: {}'.format(default_username + str(user) + '@gmail.com'))
    return users


def create_random_posts(users):
    max_posts_per_user = config.get('max_posts_per_user')
    for user in users:
        no_of_posts = random.randint(1, max_posts_per_user)
        for post in range(no_of_posts):
            random_text = ''.join(random.choice(string.ascii_uppercase) for _ in range(50))
            post_id = post_creation(user.get('token'), random_text)
            if post_id is not None:
                print('I have created a post: {}'.format(post_id))
        user["no_of_posts"] = no_of_posts
    return sorted(users, key=itemgetter('no_of_posts'), reverse=True)


def start_to_like_posts(sorted_users):
    for user in sorted_users:
        max_likes_per_user = config.get('max_likes_per_user')
        for like in range(max_likes_per_user):
            posts = get_others_posts(user.get('token'))
            list_of_eligible_posts = eligible_posts(posts, eligible_users(posts))
            if not list_of_eligible_posts:
                print('No more posts with 0 likes!')
                return
            else:
                post_id = post_like(user.get('token'), random.choice(list_of_eligible_posts))
                if post_id is not None:
                    print('I have liked a post: {}'.format(post_id))


if __name__ == '__main__':
    created_users = signup_users()
    users_sorted_by_number_of_posts = create_random_posts(created_users)
    start_to_like_posts(users_sorted_by_number_of_posts)
