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
" https://twitter.com/i/lists/series-of-numbers"
" Copy that link and submit it below.\n")

twitter_list_url = input("Paste the twitter list link here: ")

# Removing unneeded information from the URL in order to obtain the twitter ID.
stripped_twitter_list_url = int(twitter_list_url.split('/')[-1])
print(f"The name of your twitter list is \"{client.get_list(id=stripped_twitter_list_url, user_auth=True).data['name'].capitalize()}\".\n")

twitter_list = client.get_list_members(id=stripped_twitter_list_url, user_auth=True).data
name_of_twitter_list = client.get_list(id=stripped_twitter_list_url, user_auth=True).data


def main():
    while True:
            try: 
                remove_selected_users_question = int(input("\nWould you like to...\n"
                                                    "1. Remove users with a specific letter at the beginning of their username from this list?\n"
                                                    "2. Remove ALL users from this list?\n"
                                                    "3. Remove multiple selected users from this list?\n"
                                                    "\nEnter number: "))
            except ValueError:
                print("The input you entered is not valid. Please try again.")
                continue
            else:
                if remove_selected_users_question == 1:
                    users_with_a_specific_letter()
                elif remove_selected_users_question == 2:
                    remove_all_users()
                elif remove_selected_users_question == 3:
                    remove_selected_users()
                break


def users_with_a_specific_letter():
    """Removing users with certain letters at the beginning of their username from a twitter list."""

def remove_all_users():
    """Removing all members from a twitter list."""

def remove_selected_users():
    """Removing selected members from a twitter list."""

    # enter_beginning_of_username = input("Enter the first few letters of the specified user(s)'s username: ")

    # lst_of_usernames = [member.username for member in twitter_list if member.username.startswith(enter_beginning_of_username)]
    # lst_of_ids = [member.id for member in twitter_list]

    # print(f"\n*** This list contains {len(lst_of_usernames)} individual(s) whose username(s) start with the letter \"K\"."
    # " You can find the user(s) listed below.\n")
    # time.sleep(2)

    # print("Press enter to continue.")
    # input()

    # for counter, member_info in enumerate(zip(lst_of_usernames, lst_of_ids)):
    #     print(f"{counter}. {member_info[0]}")
    
    # remove_selected_users_question = int(input("\nWould you like to:\n"
    #                                     "1. Remove one member from this list?\n"
    #                                     "2. Remove ALL members from this list?\n"
    #                                     "3. Remove multiple selected members from this list?\n")) 

    # select_user_by_number = int(input("Enter a number for the user you would like to remove: "))
    # for counter, member_info in enumerate(zip(lst_of_usernames, lst_of_ids)):
    #     if question == counter:
    #         print(f"{counter}. {member_info[0]} is the user you would like to remove, correct?")

    # for counter, member_info in enumerate(zip(lst_of_usernames, lst_of_ids)):
    #     print(member_info[0].lower())
        # print(f"{counter}. {member_info[0]}")
        # print(f"Username -> {member_username} | ID -> {member_id}")

        # if member_username.lower().startswith(enter_beginning_of_username.lower()):
        #     print(f"Removing {member_username} | ID: {member_id} from the list titled \"{name_of_twitter_list.data['name'].capitalize()}\"\n")
        #     client.remove_list_member(id=stripped_twitter_list_url, user_id=member_id, user_auth=True)
        #     time.sleep(0.3)


        # Adding some hyphens as lines to separate usernames because I'm lowkey dyslexic .
        # print('-' * 60 + "\n")

    # print(f"\n *** Removed a total of {len(lst_of_ids)} users from this twitter list. ***"
    # " Below are there associated usernames alongside their twitter IDs.")

    # for member_username, member_id in zip(lst_of_usernames, lst_of_ids):
    #     print(f"Username -> {member_username} | ID -> {member_id}")


# if __name__ == '__main__':
    # main()

main()