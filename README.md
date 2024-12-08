# TrueDetector API

## 📖 Description

A RESTful API built with Django, leveraging Django's built-in database, with advanced search functionalities and spam detection capabilities, allowing users to efficiently search for contacts and identify potential spammers:
• Register and manage their profiles.
• Search for phone numbers and names in a global database.
• Mark phone numbers as spam.
• View spam likelihood for phone numbers.
• Maintain a contact list with personalized names for phone numbers.

This is an ideal project for:
📱 Developers building call-management or contact book applications.
🤝 Teams tackling spam identification with collaborative reporting systems.
🌐 Organizations needing a central directory with personalized user experiences.

---

## ✨ Features
1. **User Authentication**:
   - Register with name, phone number, and password (email is optional).
   - Unique phone numbers for each user.
   - Login required to access any endpoint.

2. **Contact Management**:
   - Users can maintain a personal contact list.

3. **Search**:
   - Search by **phone number**:
      1. If the phone number belongs to a registered user:
        - Only the profile of that registered user is shown in the search results.
        - If the searching user exists in the contact list of the registered user, the registered user's email is also displayed.
      2. Else if the phone number is found in contact lists:
        - The search results will display all users who have saved the number in their contact list.
        - Each result shows the name as saved by different users, the phone number, and the spam likelihood.

   - Search by **name**:
     - Returns matches for names starting with or containing the given name query.

4. **Spam Reporting**:
   - Users can mark any phone number as spam.
   - Spam likelihood is calculated based on user actions.

5. **Security**:
   - Token-based authentication.
   - Secure password storage with Django’s `AbstractBaseUser`.

Note:
It is assumed that the user’s phone contacts will be automatically imported into the app’s global database. This functionality is not implemented as part of this project.

---

## Prerequisites

- Python 3.8+
- Django 4.x
- PostgreSQL (or any preferred relational database)

---

## Setup

Follow these steps to set up the project locally:

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/phone-directory-api.git
   cd phone-directory-api

2. **Create a virtual environment**:
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

