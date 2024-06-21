# web-ui-cover-selector

This Flask application allows users to view and select cover images for books. The selected covers are managed and stored using Supabase.

## Prerequisites
Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- pip for installing dependencies


## Installation
Clone the repository to your local machine:

```
git clone https://github.com/WorksBetter/web-ui-cover-selector.git
cd web-ui-cover-selector
```


Install the required Python packages:

`pip install -r requirements.txt`


## Configuration
Create a `.env` file in the root directory and add your Supabase URL, API key, and a secret key for Flask:

```
SUPABASE_URL='Your_Supabase_URL'
SUPABASE_API_KEY='Your_Supabase_API_Key'
SECRET_KEY='Your_Flask_Secret_Key' //this can be any random string that flask will use to sign the sessions
```


## Running the Application
To start the server, run:

`flask run`


This will start the Flask server on `http://127.0.0.1:5000/`. Navigate to this URL in your web browser to start using the application.

##Features
Browse the books.
View available cover images.
Select and save preferred book covers to Supabase.
