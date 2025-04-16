1. Incorrect script path: src="styles/profile.js" should be src="scripts/profile.js" in profile.html
2. userCounts ID doesn't match JavaScript which uses userCount in profile.html
3. in profile.js adding baseURL variable
4. added function to show all current users in profile.js
5. changed post to get in @get_users in users.py
6. changed delete all to delete one with a filter to find the required data from databse
7. added try except block for security and catching if the user_id is not found