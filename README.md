# Flask Resume Builder

## Overview

Flask Resume Builder is a web application built with Flask, HTML, CSS, JavaScript, and Jinja templating to help users create and customize professional resumes. The application provides an intuitive user interface for entering personal and professional information, with a single template available for customization.

## Features

- **User Authentication:** Secure user authentication using Flask sessions to protect user data.
- **Dynamic Form:** Interactive form using HTML and JavaScript to input personal details, education, work experience, skills, etc.
- **Template:** A professionally designed resume template using HTML, CSS, and Jinja templating.
- **Notifications:** Receive notifications for successful actions and errors.

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Template Engine:** Jinja
- **Database:** MySQL, Flask-SQLAlchemy
- **Authentication:** Flask Sessions

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/likhithkunder/Resume-Builder-.git
   ```

2. Install Dependencies:

   ```bash
   cd flask-resume-builder
   pip install flask Flask-SQLAlchemy
   ```

3. Set up environment variables:

   - Create a .env file in the root directory and add the necessary variables

4. Set up the database:

   - Execute the resume.sql and procedures&triggers.sql file in mysql command line client:

   ```bash
   source path/to/resume.sql
   source path/to/procedure&trigger.sql
   ```

5. Run the application:
   ```bash
   python resume.py
   ```
6. Open your browser and visit http://localhost:5000/.
