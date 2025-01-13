# Company Review Platform

This platform allows users to leave reviews and feedback on various companies across multiple industries. The website promotes transparency by allowing customers to share their experiences with businesses, helping other users make informed decisions.

## Features

### Home Page
- View statistics of companies from various categories such as Electronics & Technology, Business Services, Vehicles & Transportation, Education & Training, and Shopping & Fashion.

### Company Categories
- Browse companies by category, including:
  - Electronics & Technology
  - Business Services
  - Education & Training
  - Vehicles & Transportation
  - Shopping & Fashion

### Company Details
- Explore detailed information about companies, including:
  - General company information
  - Customer reviews
  - Average ratings and detailed review breakdown (e.g., how many 1-star, 2-star, etc. reviews there are)

### Reviews
- Users can submit reviews for companies they’ve interacted with.
- Reviews include ratings (1-5 stars), comments, and suggestions.
- Reviews are displayed on company pages and contribute to the overall rating of each company.

### User Authentication
- Users can register, log in, and manage their own reviews.
- Users can also add, update, or delete their own companies (if they are the owner).

### Feedback
- Users can leave feedback on the platform itself, and a confirmation email is sent once feedback is submitted.

### API
- An API is available to fetch reviews for any company.
- The API allows sorting and filtering reviews.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/vladduucckk/scorexpert-company-review
    ```

2. Navigate to the project directory:
    ```bash
    cd scorexpert-company-review
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Add .env file
    ```bash
    touch .env
    ```
    **After create file**
    ```.env
    SECRET_KEY = yoursecretkey
    EMAIL_HOST_USER = youremail
    EMAIL_HOST_PASSWORD = youremailpassword
    ```

5. Apply migrations to set up the database:
    ```bash
    python manage.py migrate
    ```
6. Execute command in terminal for creation companies
      ```bash
    python manage.py create_categories
    ```

7. Start the development server:
    ```bash
    python manage.py runserver
    ```

8. Visit `http://127.0.0.1:8000/` in your browser.

## Technology Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS
- **Database**: SQLite
- **API**: Django Rest Framework


## Contact

For any questions or inquiries, please feel free to reach out at:  
- Email: vladislavmojseev@gmail.com
- GitHub: [https://github.com/vladduucckk](https://github.com/vladduucckk)

