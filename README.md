Py-Goodbye 👋
A Python tool to help you fetch your Instagram following list and automatically unfollow selected accounts, using Python + Excel.

Py-Goodbye is perfect for account cleanup and for saying goodbye to those random accounts you followed and now have zero idea why 😅.



📦 Features
    1. Fetch your following list in chunks

    2. Saves data in a simple Excel file (Following_list.xlsx)

    3. Mark accounts to unfollow by just editing the Excel sheet

    4. Automatically unfollows selected accounts and updates the file

    5. Keeps track of progress using max_id.txt (so you can pick up where you left off)



⚙️ Configuration
You can tweak these values directly in the Py-Goodbye-Ins.py file:
    LIMIT_USERS = 500         # Max number of accounts to fetch  
    PER_PAGE_LIMIT = 50       # Users per request (chunk size)  
    RUN_MODE = "fs"           # "fs" = fetch & save, "u" = unfollow marked ones  
    FILENAME = "Following_list.xlsx"

Set RUN_MODE to:

    "fs" → Fetch and save your following list

    "u" → Unfollow accounts marked with 1 in the Excel file

    Note: Make sure the Excel file is closed while running the script. Open = chaos :D


📓 How to Use
    Step 1. Set Instagram Credentials
        In the same folder, create a .env file like this:
            IG_USERNAME=your_username
            IG_PASSWORD=your_password

    Step 2. Fetch Mode (fs)
        1. Set RUN_MODE = "fs" in Py-Goodbye-Ins.py
        2. Run: python Py-Goodbye-Ins.py
        3. It will:
                Log in to your account and Fetch the users/accounts you are following 
                Save them to "Following_list.xlsx" with details: id, username, profile_link, unfollow?

    Step 3. Mark & Unfollow
        1. Open Following_list.xlsx
        2. In the column unfollow?, put 1 for the accounts you want to unfollow
        3. Save and close the file
        4. Set RUN_MODE = "u"
        5. Run again: Py-Goodbye-Ins.py
        6. This will:
                Unfollow users marked with 1
                Update their status to "Done" in the Excel file


💡 SomeTips
    ● max_id.txt helps resume fetching users in chunks. Set it to 0 if you want to start over from scratch.

    ● Keep the Excel file closed while the script runs.

    ● Don’t go too fast, Instagram has limits.


🛠 Quick Setup
    1. Clone the repo
        git clone https://github.com/musayyab1/py-goodbye.git
        cd py-goodbye
    
    2. Install dependencies
        pip install -r requirements.txt


📁 File Structure
        Py-Goodbye/
        ├── Py-Goodbye-Ins.py        # Main script
        ├── .env                     # Instagram login credentials
        ├── max_id.txt               # Tracks pagination state
        ├── Following_list.xlsx      # Excel file with user data
        └── requirements.txt         # Dependencies list



