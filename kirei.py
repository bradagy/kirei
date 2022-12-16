import time

import tweepy

import credentials


client = tweepy.Client(
    consumer_key=credentials.consumer_key,
    consumer_secret=credentials.consumer_secret,
    access_token=credentials.access_token,
    access_token_secret=credentials.access_token_secret
)

twitter_lst = client.get_list_members(id="1602825510702268416", user_auth=True).data
name_of_lst = client.get_list(id="1602825510702268416", user_auth=True).data

lst_of_usernames = [member.username for member in twitter_lst]
lst_of_ids = [member.id for member in twitter_lst]

beginning_of_username = 'bowtied'

print(f'\n*** There are {len(twitter_lst)} users in this list.'
    ' Below are all the users who usernames start with bowtied. ***\n')
time.sleep(2)

for member_username, member_id in zip(lst_of_usernames, lst_of_ids):
    print(f"Username:{member_username} | ID:{member_id}")

    if member_username.lower().startswith(beginning_of_username):
        print(f"Removing {member_username} from the list titled \"{name_of_lst.data['name']}\"")
    # Adding some hyphens as lines to separate usernames because I'm lowkey dyslexic .
    print('-' * 60 + "\n")
