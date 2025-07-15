import os
import google.generativeai as genai
import praw
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Reddit setup
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def extract_username(url):
    return url.rstrip('/').split('/')[-1]

def get_user_data(username, limit=50):
    user = reddit.redditor(username)
    posts, comments = [], []
    try:
        for post in user.submissions.new(limit=limit):
            posts.append({
                "title": post.title,
                "body": post.selftext,
                "url": f"https://reddit.com{post.permalink}"
            })
        for comment in user.comments.new(limit=limit):
            comments.append({
                "body": comment.body,
                "url": f"https://reddit.com{comment.permalink}"
            })
    except Exception as e:
        print(f"Error fetching data: {e}")
    return posts, comments

def build_prompt(posts, comments):
    content = ""
    for post in posts:
        content += f"Post Title: {post['title']}\nContent: {post['body']}\nLink: {post['url']}\n\n"
    for comment in comments:
        content += f"Comment: {comment['body']}\nLink: {comment['url']}\n\n"

    prompt = f"""
You are to analyze Reddit user activity and build a **qualitative user persona** in this format:

Name:
Photo: (N/A)
Quote:

Bio / Background:

Personality:

Goals:

Frustrations:

Motivations:

Preferred Channels:

Favorite Brands:

Technological Proficiency:

Demographics:
- Age:
- Gender:
- Occupation:
- Location:

Cite Reddit post/comment links or direct quotes to justify inferences.

Reddit Activity:
{content}

User Persona:
"""
    return prompt

def generate_persona(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return None

def save_to_file(username, content):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    url = input("Enter Reddit profile URL: ").strip()
    username = extract_username(url)
    posts, comments = get_user_data(username)
    if not posts and not comments:
        print("No data found.")
        return
    prompt = build_prompt(posts, comments)
    persona = generate_persona(prompt)
    if persona:
        save_to_file(username, persona)
        print(f"Saved to output/{username}_persona.txt")
    else:
        print("Persona generation failed.")

if __name__ == "__main__":
    main()
