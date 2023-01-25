import time

import tweepy

import credentials


client = tweepy.Client (
    consumer_key = credentials.consumer_key,
    consumer_secret = credentials.consumer_secret,
    access_token = credentials.access_token,
    access_token_secret = credentials.access_token_secret
)

print("Go to the main page of any of your twitter lists."
" The link at the top of the page should look something like this:"
" https://twitter.com/i/lists/series-of-numbers."
" Copy that link and submit it below.\n")

twitter_list_url = input("Paste the twitter list link here: ")

# Removing unneeded information from the URL in order to obtain the twitter ID.
twitter_list_ID = int(twitter_list_url.split('/')[-1])
print(f"The name of your twitter list is \"{client.get_list(id=twitter_list_ID, user_auth=True).data['name'].capitalize()}\".\n")

twitter_list = client.get_list_members(id=twitter_list_ID, user_auth=True).data
name_of_twitter_list = client.get_list(id=twitter_list_ID, user_auth=True).data


def main():
    while True:
        try:
            remove_selected_users_question = int(input("\nWould you like to...\n"
                                                "1. Remove user(s) with a specific letter at the beginning of their username from this list?\n"
                                                "2. Remove ALL user(s) from this list?\n"
                                                "\nEnter number: "))
            if remove_selected_users_question not in {1, 2}:
                print("The input you entered is not valid. Please try again.")
                continue
        except ValueError:
            print("The input you entered is not valid. Please try again.")
            continue
        else:
            if remove_selected_users_question == 1:
                print('You selected the option to remove users with a specfic letter at the beginning of their username.')
                time.sleep(4)
                remove_users_with_specific_chars_at_beginning()
            elif remove_selected_users_question == 2:
                print('You selected option #2 (remove all users from twitter list).')
                time.sleep(4)
                remove_all_users()
            break


def remove_users_with_specific_chars_at_beginning():
    """Removing users with certain character(s) at the beginning of their username from a twitter list."""
    enter_beginning_of_username = input("Enter the first few character(s) or characters of the specified user(s)'s username: ")

    lst_of_usernames = [member.username for member in twitter_list if member.username.lower().startswith(enter_beginning_of_username.lower())]
    lst_of_ids = [member.id for member in twitter_list]

    if len(lst_of_usernames) == 0:
        print(f"\n ***This list contains 0 individuals whose username(s) start with the character(s) \"{enter_beginning_of_username}\". \n"
        "\nExiting program. ***")
        input()
    else:
        print(f"\n*** This list contains {len(lst_of_usernames)} individual(s) whose username(s) start with the character(s) \"{enter_beginning_of_username}\"."
        " You can find the user(s) listed below. ***\n")
        time.sleep(2)
        print("Press ENTER to continue.")
        input()

        for counter, member_info in enumerate(zip(lst_of_usernames, lst_of_ids)):
            print(f"{counter}. @{member_info[0]}")

        while True:
            answers = {'Y', 'N'}
            confirm_removal_process = input("\nWould you like to confirm the removal process. "
            "Remember, this will remove all the users from your selected list whose username(s) start with "
            "the character(s) you specified. Continue? (Y / N): ")
            if confirm_removal_process.upper() not in answers:
                print("\nPlease choose a valid option.\n")
                continue
            elif confirm_removal_process.upper() == "N":
                print("You selected (No). Exiting program.")
                break
            elif confirm_removal_process.upper() == "Y":
                for counter, member_info in enumerate(zip(lst_of_usernames, lst_of_ids)):
                    if member_info[0].lower().startswith(enter_beginning_of_username.lower()):
                        print(f"Removing @{member_info[0]} from the list titled \"{name_of_twitter_list.data['name'].capitalize()}.")
                        client.remove_list_member(id=twitter_list_ID, user_id=member_info[1], user_auth=True)
                        time.sleep(0.3)

            # Adding some hyphens as lines to separate usernames because I'm lowkey dyslexic .
                print('-' * 60)
                print(f"\n *** Removed a total of {len(lst_of_usernames)} users from this twitter list. ***"
                " Their usernames have been posted below.\n")

                for member_username in lst_of_usernames:
                    print(f"@{member_username}")

                print("Press ENTER to exit.")
                input()
                break


def remove_all_users():
    """Removing all members from a twitter list."""
    pagination_tokens = []
    IDs_of_users_to_remove = []
    total_amount_of_usernames = []

    next_token = None
    while True:
        # Meta info is basically a dictionary that contains the result count, and next token 
        # needed for pagination (aka moving to the "next" page) because the max results for the
        # client.get_list_members method only allows 100 users to be returned by default.
        response = client.get_list_members(id = twitter_list_ID, user_auth = True, pagination_token = next_token).meta

        if 'next_token' not in response:
            break
        else:
            # Update the list of pagination tokens with the next token 
            # needed to access the next page of the specified twitter list.
            pagination_tokens.append(response['next_token'])
            # Updating the value of the next token to the current value in meta_info_for_twitter_list
            # which is the dictionary that contains the result count, and next token needed for pagination.
            next_token = response['next_token']

    while True:
        answers = {'Y', 'N'}
        try:
            confirm_removal_process = input('\nConfirm the removal process (Enter \'Y\' or \'N\'): ')
            if confirm_removal_process.upper() not in answers:
                    raise ValueError
            if confirm_removal_process.upper() == 'N':
                print('You selected (No). Exiting program.')
                break
            elif confirm_removal_process.upper() == 'Y':
                # If there isn't a next token available or the length of the pagination_tokens list less than or equal to one,
                # this entire if-else block will allow all of the members of the specified twitter list to be added to the total_amount_of_usernames list.
                if len(pagination_tokens) <= 1:
                    # Adding the members associated with the pagination token list to the main list of users to be removed.
                    for token in pagination_tokens:
                        members = client.get_list_members(id = twitter_list_ID, user_auth = True, pagination_token = token).data
                        usernames = [[member.username.capitalize(), member.id] for member in members]
                        for member in usernames:
                            # Adding the IDs and usernames of each user to different lists.
                            IDs_of_users_to_remove.append(member[1])
                            total_amount_of_usernames.append(member[0])

                    # Adding the members not associated with the pagination token list to the main list of users to be removed.
                    for member in client.get_list_members(id = twitter_list_ID, user_auth = True).data:
                        total_amount_of_usernames.append(member.username.capitalize())
                        IDs_of_users_to_remove.append(member.id)
                else:
                    for token in pagination_tokens:
                        members = client.get_list_members(id = twitter_list_ID, user_auth = True, pagination_token = token).data
                        usernames = [[member.username.capitalize(), member.id] for member in members]
                        for member in usernames:
                            IDs_of_users_to_remove.append(member[1])
                            total_amount_of_usernames.append(member[0])
                
                # Displaying all of the users associated with the list.
                print('Below is a list of all the users that are members of your selected twitter list.')
                time.sleep(5)
                for counter, username in enumerate(sorted(total_amount_of_usernames), start = 1):
                    print(f"{counter}. @{username}")
                    time.sleep(0.02)
                
                print('Removing members.')
                time.sleep(4)
                for counter, member_info in enumerate(zip(sorted(total_amount_of_usernames), IDs_of_users_to_remove)):
                    print(f"Removing @{member_info[0]} from the list titled \"{name_of_twitter_list.data['name'].capitalize()}.")
                    client.remove_list_member(id=twitter_list_ID, user_id=member_info[1], user_auth=True)
                    time.sleep(0.020
                print("All users have been removed from the specified twitter list. Exiting program.")
                input()
                break
        except ValueError:
            print("\nPlease choose a valid option.\n")


if __name__ == '__main__':
    main()