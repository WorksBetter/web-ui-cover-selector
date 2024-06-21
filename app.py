import csv
import os
from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_api_key = os.getenv('SUPABASE_API_KEY')


csv_file_path = 'gutenberg_books_top100.csv'
table_name = 'ebooks'


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Replace with a strong secret key to sign the user session
app.config['SESSION_TYPE'] = 'filesystem'
from flask_session import Session
Session(app)

# Initialize the Supabase client
supabase: Client = create_client(supabase_url, supabase_api_key)

# Load the scraped data
def load_data():
    books = []
    with open('gutenberg_books_top100.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Split the Cover URLs string into a list
            if 'Cover URLs' in row and row['Cover URLs'] != 'No cover URLs available':
                row['Cover URLs'] = row['Cover URLs'].split(', ')
                books.append(row)
    return books

# Save selected cover URL to a separate CSV file
def save_selected_cover(book_id, cover_url):
    with open('selected_covers.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([book_id, cover_url])

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    books = load_data()
    selected_books = session.get('selected_books', [])

    # Exclude books that have already been selected
    books_to_render = [book for book in books if book['Book ID'] not in selected_books]

    # Implement pagination
    books_per_page = 10
    start = (page - 1) * books_per_page
    end = start + books_per_page
    paginated_books = books_to_render[start:end]

    return render_template('index.html', books=paginated_books, page=page)

@app.route('/select_cover', methods=['POST'])
def select_cover():
    book_id = request.form['book_id']
    cover_url = request.form['cover_url']
    book_id = int(book_id)
    print(book_id, cover_url)
    # save_selected_cover(book_id, cover_url)

    # Save selected cover URL to Supabase
    try:
        response = supabase.table('ebooks').update({'manually_picked_cover': cover_url}).eq('id', book_id).execute()
        print(f"Update response: {response}")
    except Exception as e:
        print(f"Error updating Supabase: {e}")
    
    selected_books = session.get('selected_books', [])
    selected_books.append(book_id)
    session['selected_books'] = selected_books
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
