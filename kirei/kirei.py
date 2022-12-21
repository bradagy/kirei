import time

import tweepy

import credentials


def main():

    client = tweepy.Client (
        consumer_key=credentials.consumer_key,
        consumer_secret=credentials.consumer_secret,
        access_token=credentials.access_token,
        access_token_secret=credentials.access_token_secret
    )

    twitter_lst = client.get_list_members(id="1602825510702268416", user_auth=True).data
    name_of_lst = client.get_list(id="1602825510702268416", user_auth=True).data

    lst_of_usernames = [member.username for member in twitter_lst]
    lst_of_ids = [member.id for member in twitter_lst]

    beginning_of_username = 'Bowtied'

    print(f'\n*** There are {len(twitter_lst)} users in this list. Below are all the users who usernames start with {beginning_of_username.title()}. ***\n')
    time.sleep(2)
    print('Press enter to continue')
    input()

    for member_username, member_id in zip(lst_of_usernames, lst_of_ids):
            print(f"Username -> {member_username} | ID -> {member_id}")

            if member_username.lower().startswith(beginning_of_username.lower()):
                print(f"Removing {member_username} | ID: {member_id} from the list titled \"{name_of_lst.data['name'].capitalize()}\"\n")
                client.remove_list_member(id="1602825510702268416", user_id=member_id, user_auth=True)
                time.sleep(0.3)

        
            # Adding some hyphens as lines to separate usernames because I'm lowkey dyslexic .
            # print('-' * 60 + "\n")

    print(f"\n *** Removed a total of {len(lst_of_ids)} users from this twitter list. ***"
    " Below are there associated usernames alongside their twitter IDs.")

    for member_username, member_id in zip(lst_of_usernames, lst_of_ids):
        print(f"Username -> {member_username} | ID -> {member_id}")


if __name__ == '__main__':
    main()

    # Preventing the console from closing immediately.
    input()