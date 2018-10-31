import clearbit

from pyhunter import PyHunter
from django.conf import settings
from requests.exceptions import HTTPError

hunter = PyHunter(settings.EMAILHUNTER_KEY)


def check_email_existence(email):
    """
    Checks if the email exists by using hunter.io service.
    :param email: email to be checked
    :type email: string
    :return: True if the email is verified, otherwise False. If there's no more calls left return None
    :type: boolean or None
    """
    calls_left = hunter.account_information().get('calls').get('left')
    if calls_left > 0:
        request_body = hunter.email_verifier(email)
        return request_body.get('webmail')
    else:
        print("No more calls left for hunter.io API service!")
        return


def enrich_user(user):
    """

    :param user:
    :type user: User
    :return:
    """
    clearbit.key = settings.CLEARBIT_KEY
    try:
        response = clearbit.Enrichment.find(email=user.email, stream=True)
        if 'person' in response:
            person = response['person']
            if person.get('name').get('familyName') is not None:
                user.profile.last_name = person.get('name').get('familyName')
            if person.get('name').get('givenName') is not None:
                user.profile.first_name = person.get('name').get('givenName')
            if person.get('avatar') is not None:
                user.profile.avatar = person.get('avatar')
            if person.get('facebook').get('handle') is not None:
                user.profile.facebook_handle = person.get('facebook').get('handle')
            if person.get('github').get('handle') is not None:
                user.profile.github_handle = person.get('github').get('handle')
            if person.get('googleplus').get('handle') is not None:
                user.profile.google_plus_handle = person.get('googleplus').get('handle')
            if person.get('linkedin').get('handle') is not None:
                user.profile.linkedin_handle = person.get('linkedin').get('handle')
            if person.get('twitter').get('handle') is not None:
                user.profile.twitter_handle = person.get('twitter').get('handle')
            user.profile.save()
    except HTTPError:
        print("No more calls left for Clearbit API service!")
    except TypeError:
        print("No more calls left for Clearbit API service!")
