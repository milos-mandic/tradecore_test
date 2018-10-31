import requests
import json

BASE_URL = "http://localhost:8000/api"


def user_signup(username, email, password):
    """

    :param username:
    :param email:
    :param password:
    :return:
    """
    url = BASE_URL + '/users/'
    payload = {
        "user": {
            "username": username,
            "email": email,
            "password": password
        }
    }
    headers = {
        'Content-Type': "application/json",
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        return json.loads(response.text).get("user").get("token")
    else:
        print(response.text)


def user_login(email, password):
    """

    :param email:
    :param password:
    :return:
    """
    url = BASE_URL + '/users/login/'
    payload = {
        "user": {
            "email": email,
            "password": password
        }
    }
    headers = {
        'Content-Type': "application/json",
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return json.loads(response.text).get("user").get("token")
    else:
        print(response.text)


def post_creation(token, text):
    """

    :param token:
    :param text:
    :return:
    """
    url = BASE_URL + '/posts/'
    payload = {
        "text": text
    }
    headers = {
        'Authorization': "Token " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        return json.loads(response.text).get("post").get("id")
    else:
        print(response.text)


def post_like(token, post_id):
    """

    :param token:
    :param post_id:
    :return:
    """
    url = BASE_URL + '/post_like/' + str(post_id) + '/'
    payload = {}
    headers = {
        'Authorization': "Token " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("PUT", url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return json.loads(response.text).get("post").get("id")


def post_unlike(token, post_id):
    """

    :param token:
    :param post_id:
    :return:
    """
    url = BASE_URL + '/post_unlike/' + str(post_id) + '/'
    payload = {}
    headers = {
        'Authorization': "Token " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("PUT", url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return json.loads(response.text).get("post").get("id")
    else:
        print(response.text)


def get_others_posts(token):
    """

    :param token:
    :return:
    """
    url = BASE_URL + '/others_posts/'
    headers = {
        'Authorization': "Token " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(response.text)
