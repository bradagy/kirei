import time

import tweepy

import credentials


# Authentication
client = tweepy.Client (
    consumer_key = credentials.consumer_key,
    consumer_secret = credentials.consumer_secret,
    access_token = credentials.access_token,
    access_token_secret = credentials.access_token_secret
)


def main():
    """Removing users with certain letters at the beginning of their username from a twitter list."""
    print("Go to the main page of any of your specified twitter lists."
    " The link at the top of the page should look something like this:"
    " https://twitter.com/i/lists/series-of-numbers"
    " Copy that link and submit it below.")

    twitter_list_url = input("Paste the twitter list link here: ")

    # Removing unneeded information from the URL in order to obtain the twitter ID.
    stripped_twitter_list_url = int(twitter_list_url.split('/')[-1])
    print(f"The name of your twitter list is \"{client.get_list(id=stripped_twitter_list_url, user_auth=True).data['name'].capitalize()}\".")

    twitter_list = client.get_list_members(id=stripped_twitter_list_url, user_auth=True).data
    name_of_lst = client.get_list(id=stripped_twitter_list_url, user_auth=True).data

    enter_beginning_of_username = input("Enter the first few letters of the specified person's username: ")

    lst_of_usernames = [member.username for member in twitter_list]
    lst_of_ids = [member.id for member in twitter_list]

    print(f'\n*** There are {len(twitter_list)} users in this list. Below are all the users who usernames start with {enter_beginning_of_username.title()}. ***\n')
    time.sleep(2)
    print('Press enter to continue')
    input()

    for member_username, member_id in zip(lst_of_usernames, lst_of_ids):
        print(f"Username -> {member_username} | ID -> {member_id}")

        if member_username.lower().startswith(enter_beginning_of_username.lower()):
            print(f"Removing {member_username} | ID: {member_id} from the list titled \"{name_of_lst.data['name'].capitalize()}\"\n")
            client.remove_list_member(id=stripped_twitter_list_url, user_id=member_id, user_auth=True)
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