REDDIT SENTIMENT TRACKER


# Initialize Reddit client (read credentials from env)
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("SECRET_KEY"),
    user_agent=os.getenv("USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),     # Needed for scripts using password grant
    password=os.getenv("REDDIT_PW")
)



--------------------
-1. Setup PRAW client                                                           - CURRENT
    Replace your manual authentication in main.py with a PRAW instance that uses your existing environment variables.
-2. Fetch posts (and later comments) from your target subreddit(s)
    Write a function in reddit_client.py that fetches posts from a given subreddit, including necessary fields like title, body/selftext, author, timestamp, score, and subreddit.
    Make sure to handle pagination or limiting the number of posts (using limit parameter).
-3. Save the fetched data
    Design a simple PostgreSQL schema (or SQLite if you prefer to start lightweight).
    Use SQLAlchemy or psycopg2 to write posts into the database.
    Ensure your schema supports storing fields like post ID, author, timestamp, title/body, score, and subreddit.
    Add indexes on fields like subreddit and created_at for performance.
-4. Store raw JSON
    Optionally, save the raw API response JSON in your /data folder for debugging and backup.
-5. Add logging
    Add basic logging to track your data fetching progress and errors.
----------------------


1	PRAW data collection (posts only) + PostgreSQL storage
2	VADER integration + basic CLI output ("rich" or "click")
3	Error handling + logging + config file
4	Dockerize + write README.md
5	Add 2-3 pytest tests + GitHub Actions

--------------------------------------------------------------------------------------------
1. Project Structure
reddit_sentiment_tracker/
│
├── src/
│   ├── reddit_client.py        # Reddit API logic (PRAW)
│   ├── sentiment.py            # Sentiment analysis logic
│   ├── database.py             # SQLite/PostgreSQL logic
│   ├── main.py                 # CLI entry point
|   |-- config.ini              # config file for api keys, subreddits to monitor
│
├── data/                       # Store raw data or logs
├── tests/                      # Unit tests
├── requirements.txt
├── README.md

2. Fetch reddit data
- Use PRAW to collect comments/posts for a subreddit or keyword.
- Save as raw JSON and into DB (SQLite or Postgres).
- Ensure timestamp, author, score, subreddit, and body/title are saved.
- add indexes for frequently used queries for performance

Example job-relevant features:
    Support both comments and posts.
    Handle API rate limiting gracefully.
    Write logs (useful in job interviews to explain errors handled)

3. Sentiment Analysis
Use VADER (fast, standard for social media) or TextBlob for early version.
Key:
    Normalize and clean text.
    Score each item and store compound, pos, neg, neu values.
    Add a sentiment_label (positive/neutral/negative).

Job-worthy detail:
    Store both raw and cleaned text in the database.

4. Database Storage
Use SQLite or PostgreSQL with SQLAlchemy for clean code.

Schema suggestion:
posts (
    id SERIAL PRIMARY KEY,
    source TEXT,  -- 'post' or 'comment'
    subreddit TEXT,
    title TEXT,
    body TEXT,
    created_at TIMESTAMP,
    sentiment_score FLOAT,
    sentiment_label TEXT,
    keyword TEXT
)

5. CLI Tool or Backend Script (rich library for user friendly output)
Make it easy to use like:
python main.py --keyword "bitcoin" --subreddit "cryptocurrency" --limit 50

Even better:
    Add argparse for flags
    Log summary: average sentiment, most extreme comments, top upvoted, etc.

6. Useful Output
Even without frontend:
Export .csv or .json of top comments.

Print CLI summaries like:
Sentiment Summary for 'bitcoin':
Positive: 23%
Neutral: 60%
Negative: 17%

Most Positive Post: "This project is revolutionizing..."

----------------------------------------------------------------------------------------------------------
OPTIONAL: 
    Create a REST API using FastAPI if you want to show off Python web skills (no UI needed).
    Build simple Dashboaord "streamlit"
