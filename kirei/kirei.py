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
            if remove_selected_users_question not in [1, 2]:
                print("The input you entered is not valid. Please try again.")
                continue
        except ValueError:
            print("The input you entered is not valid. Please try again.")
            continue
        else:
            if remove_selected_users_question == 1:
                remove_users_with_specific_chars_at_beginning()
            elif remove_selected_users_question == 2:
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
            answers = ['Y', 'N']
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


# def remove_all_users():
#     """Removing all members from a twitter list."""



if __name__ == '__main__':
    main()
