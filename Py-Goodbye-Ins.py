# --- IMPORTS ---
from instagrapi import Client
import time
import random
import os
from dotenv import load_dotenv # For loading environment variables from .env file

import pandas as pd  
from datetime import datetime 



# --- CONFIG ---
'''
Set your Instagram username and password in a `.env` file like this:
IG_USERNAME=your_username
IG_PASSWORD=your_password

USAGE GUIDE:
1. Set RUN_MODE to "fs" to fetch accounts you are following.
   → The list will be saved in an Excel file called "Following_list.xlsx".

2. Open the Excel file, go to the last column "unfollow?".
   → Mark 1 for any accounts you want to unfollow.
   → Save and close the file.

3. Set RUN_MODE to "u" to unfollow all marked accounts.
   → The program will unfollow them and mark them as "Done" in the same Excel sheet.

'''
load_dotenv() # Activates the environment variables so we can use them via os.getenv()
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")


''' --- SETTINGS YOU CAN CHANGE --- '''
LIMIT_USERS = 500          # Total number of users to fetch, total follows instagram allows is 7500
PER_PAGE_LIMIT = 50        # Number of users per request (each chunk)
RUN_MODE = "fs"           # Options: Set RUN_MODE to "fs" to fetch&save accounts you are following to an excel file or "u" to unfollow accounts marked for unfollowing

FILENAME = "Following_list.xlsx" # Name of the Excel file to save the followed users/accounts list
# --- END OF CONFIG ---


#=======================Getting the list of users you are following & saving in an excel sheet=======================

def fetch_followed_accounts(cl, username, user_id, limit_users,per_page_limit):
    #To get following count
    user_info = cl.user_info_by_username(username)
    #print(user_info.following_count)
    
    

    # Keep track of how many users you've fetched so far
    users_fetched = 0

    # Dictionary to store all fetched following users
    following = {}


    # max_id represents the offset (i.e., starting index) for paginated fetching (used to get next chunk) Exm: max_id = 50 means get 51st user it seems
    # max_id = None
    # Try & resume from previous max_id
    MAX_ID_FILE = "max_id.txt"
    if os.path.exists(MAX_ID_FILE):
        with open(MAX_ID_FILE, "r") as f:
            max_id = f.read().strip()
            max_id = max_id if max_id else None  # If file is empty, set max_id to None

    else:
        max_id = None


    # Fetch in chunks until limit hit or there are no more users
    while users_fetched < limit_users:

        # Get a chunk of users you're following, along with next max_id for pagination
        chunk, max_id = cl.user_following_v1_chunk(user_id, max_id=max_id, max_amount=per_page_limit)

        # Save max_id to resume later
        with open(MAX_ID_FILE, "w") as f:
            f.write(max_id if max_id else "")



        print(f"Fetched {len(chunk)} users in this page")

        # Convert the list into a dict: {user_id: user_obj}
        chunk_dict = {user.pk: user for user in chunk}
        # Add the new users to your main dictionary
        following.update(chunk_dict)

        # Update running count
        users_fetched += len(chunk)

        print(f"Total fetched so far: {users_fetched}")

        # If max_id is None, Instagram has no more data to return
        if not max_id:
            break

        # Wait for a few seconds between requests to stay under radar lol
        time.sleep(random.uniform(2.5, 4.0)) #keeps it non-uniform to avoid detection 

    print(f"Total followed accounts fetched: {len(following)}")

    # Print usernames and profile URLs
    for i, user in enumerate(following.values(), 1):
        print(f"{i}. {user.username} - https://instagram.com/{user.username}")

    return following


def save_following_to_excel(following, filename):

    # Prepare the rows for Excel
    rows = []

    fetched_date = datetime.now().strftime("%Y-%m-%d ")  # %H:%M:%S | Format: 2025-04-15 14:30:00


    for user_id, user in following.items():
        rows.append({
            "id": user_id,
            "username": user.username,
            "profile_link": f"https://instagram.com/{user.username}",
            "fetched_date": fetched_date,
            "unfollow?": ""  # leave blank for now
        })

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=["id", "username", "profile_link", "fetched_date", "unfollow?"])



    # Check if file exists
    if os.path.exists(filename):
        with pd.ExcelWriter(filename, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            # Get current number of rows to calculate where to start writing
            existing_df = pd.read_excel(filename)
            startrow = len(existing_df) + 1
            df.to_excel(writer, index=False, header=False, startrow=startrow)
    else:
        # File doesn't exist: create it with headers
        df.to_excel(filename, index=False)

    print("✅ Following list saved to 'Following_list.xlsx'")


#=======================Getting the list of users to unfollow from the excel sheet & unfollowing them=======================

def unfollow_users_marked(cl, filename):

     # Load the Excel file
    df = pd.read_excel(filename)

    # Filter rows marked for unfollowing
    to_unfollow = df[df["unfollow?"] == 1]

    if to_unfollow.empty:
        print("No users marked for unfollowing.")
        return
    
    print(f"Found {len(to_unfollow)} users marked for unfollowing...")


    # Check each user and unfollow
    for idx, row in to_unfollow.iterrows():
        user_id = int(row["id"])
        try:
            cl.user_unfollow(user_id)
            print(f"Unfollowed {row['username']}")

            # Mark as done, changes 1 to 'Done'
            df.at[idx, "unfollow?"] = "Done"

            time.sleep(random.uniform(2.5, 4.0)) #non-uniform sleep

        except Exception as e:
            print(f"Failed to unfollow {row['username']} (ID: {user_id}) — {e}")

    # Save the updated Excel file
    df.to_excel(filename, index=False)
    print("Excel file updated. Unfollowed accounts/users are marked as 'Done' in 'Unfollow?' column.")


def main():
    # --- LOGIN ---
    cl = Client()

    if not USERNAME or not PASSWORD:
        raise ValueError("Instagram credentials are missing. Please check your .env file and set your instagram username and password there.")
    else:
        cl.login(USERNAME, PASSWORD)
        print("Logged in successfully!")

        print(f"Username: @{USERNAME}")
        # Get your user ID
        user_id = cl.user_id

        if RUN_MODE == "fs":
            # Fetch and save following list
            following = fetch_followed_accounts(cl, USERNAME, user_id, LIMIT_USERS, PER_PAGE_LIMIT)
            save_following_to_excel(following, FILENAME)
        elif RUN_MODE == "u":
            unfollow_users_marked(cl, FILENAME)
        else:
            print(f"RUN_MODE not set: {RUN_MODE}. Please use 'fs' or 'u'.")


if __name__ == "__main__":
    main()

    