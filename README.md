# e-Diary
#### Video Demo:  https://youtu.be/ukIp15cIm5E
## Digital Diary Web Application

**Introduction**

This web application is a simple diary management system built with Python using the Flask web framework and an SQLite database. The frontend of the web application is made using HTML and CSS. Users can register, log in, and manage their diary entries through an intuitive web interface. The application provides features for adding, reading, editing, and deleting diary entries, offering a convenient way for users to maintain a digital diary.

**Features**

**1. User Registration and Login:**
- Users can register for an account, providing a unique username and a secure password.
- Existing users can log in with their credentials.
- Passwords are securely hashed for storage.

**2. Dashboard:**
- After logging in, users are directed to a dashboard where they can access various diary-related functionalities.

**3. Adding Diary Entries:**
- Users can add new diary entries through a user-friendly form.
- The application checks for existing entries on the current date to avoid duplicate entries.

**4. Reading Diary Entries:**
- Users can view diary entries by selecting a specific date through a dedicated form.
- If an entry exists for the selected date, the application displays the text.

**5. Editing Diary Entries:**
- Users can edit existing diary entries, providing a seamless way to update their thoughts.
- The application allows users to modify the text of a diary entry.

**6. Deleting Diary Entries:**
- Users can delete unwanted diary entries, offering flexibility in managing their diary content.

**7. Logout:**
- Users can log out of their accounts, terminating their active sessions.

**Setup and Usage**

**1. Environment Setup:**
- Ensure you have Python installed on your system.
- Install the required dependencies using the following command: pip install Flask Flask-Session cs50

**2. Database Initialization:**
- The application uses SQLite as the database. The database is named database.db and is initialized automatically when the application runs.

**3. Running the Application:**
- Execute the following command in the terminal to start the Flask development server: flask run
- Access the application by visiting link given in terminal in your web browser.

**4. User Interaction:**
- Register for a new account or log in with existing credentials.
- Explore the dashboard for adding, reading, editing, and deleting diary entries.
- Log out when finished to secure your session.

**Important Notes**
- This application emphasizes secure password management through hashing.
- Flash messages are utilized for providing user feedback.

**Credits**
    This web application is developed using Flask and utilizes the CS50 library for database interactions. Special thanks to the Flask community and CS50 for providing valuable resources and tools.