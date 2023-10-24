import os
import openai
import re
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from dotenv import load_dotenv
from tqdm import tqdm
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import requests

# Load environment variables from the .env file
load_dotenv()

# Initialize empty lists for categories and tags
post_categories = []
post_tags = []

# Define your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the WordPress client
site_url = os.getenv('WORDPRESS_SITE_URL')
username = os.getenv('WORDPRESS_USERNAME')
password = os.getenv('WORDPRESS_PASSWORD')
wp = Client(site_url, username, password)

# Define the file path
file_path = 'blog_post.txt'

# Initialize an empty list to store post titles
post_titles = []
    
# Function to get list of post titles
def get_post_titles():
    # Open the file for reading
    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading and trailing whitespace
            line = line.strip()
            # Check if the line is not empty and does not start with #
            if line and not line.startswith('#'):
                post_titles.append(line)
    # Return the post titles as a list
    return post_titles

# Function to check OpenAI status
def check_openai_status():
    status_url = "https://status.openai.com/api/v2/status.json"
    response = requests.get(status_url)
    if response.status_code == 200:
        status_data = response.json()
        return status_data
    return None

def extract_categories_tags(content):
    categories_match = re.search(r'^category:\s*([\w\s,]+)$', content, re.MULTILINE)
    tags_match = re.search(r'^tags:\s*([\w\s,]+)$', content, re.MULTILINE)

    if categories_match:
        categories_text = categories_match.group(1)
        individual_categories = [category.strip() for category in categories_text.split(',')]
        post_categories.extend(individual_categories)

    if tags_match:
        tags_text = tags_match.group(1)
        individual_tags = [tag.strip() for tag in tags_text.split(',')]
        post_tags.extend(individual_tags)

def format_code_snippets(content):
    # Define a regex pattern to identify code blocks
    code_pattern = re.compile(r'```(.*?)```', re.DOTALL)

    def format_code(match):
        code_block = match.group(1)
        language = get_code_language(code_block)
        formatted_code = format_code_block(code_block, language)
        return formatted_code
    
    # Use the code_pattern to format code blocks
    formatted_content = code_pattern.sub(format_code, content)
    return formatted_content

def format_code_block(code_block, language):
    # Use pygments to highlight the code with the specified language
    lexer = get_lexer_by_name(language, stripall=True)
    formatter = HtmlFormatter()
    formatted_code = highlight(code_block, lexer, formatter)
    return formatted_code

def get_code_language(code_block):
    language_mapping = {
        'python': 'python',
        'javascript': 'javascript',
        'json': 'json',
        'sql': 'sql',
        'bash': 'bash',
        'java': 'java',
        'c': 'c',
        'cpp': 'cpp',
        'php': 'php',
        'ruby': 'ruby',
        'perl': 'perl',
        'html': 'html',
        'css': 'css',
        'xml': 'xml',
        'go': 'go',
        'swift': 'swift',
        'typescript': 'typescript',
        'rust': 'rust',
        'scala': 'scala',
        'kotlin': 'kotlin',
        # Add more languages as needed
    }

    for keyword, language in language_mapping.items():
        if re.search(rf'\b{keyword}\b', code_block, re.IGNORECASE):
            return language

    return "text"  # Default to plain text

def generate_content(max_tokens, post_title):
    content = ""
    progress_bar = tqdm(total=max_tokens, unit=' tokens', dynamic_ncols=True, ascii=True)
    retry_count = 0  # Initialize the retry count

    try:
        # Continuously generate content until reaching the desired length or reaching max retries
        while len(content) < max_tokens and retry_count < 3:  # You can adjust the maximum number of retries
            system_intel = "As a senior DevOps Engineer, answer my question like you're writing a technical guide for junior engineers."
            prompt = f"""
            Create a blog post with the title: "{post_title}"
            
            Make the content should be undetectable by AI.
            
            Use the template format below:
            ---
            title: [Title]
            date: [Date]
            category: [Category]
            tags: [Tag1, Tag2, Tag3, Tag4, Tag5]
            meta_description: [Meta Description]
            focus_keyphrase: [Focus Keyphrase]
            ---

            # Introduction

            [Include a brief introduction to the topic and its significance.]

            ## Prerequisites

            Before you begin, ensure that you have:

            - [Prerequisite 1]
            - [Prerequisite 2]
            - [Prerequisite 3]

            ## Step 1: [Step Title]

            1. [Step 1 - Action 1]
            2. [Step 1 - Action 2]
            3. [Step 1 - Action 3]

            ## Step 2: [Step Title]

            1. [Step 2 - Action 1]
            2. [Step 2 - Action 2]
            3. [Step 2 - Action 3]

            [Continue with additional steps as needed.]

            # Conclusion

            [Summarize the key points of the guide and highlight the importance of the topic.]

            [Additional tips or notes if necessary.]
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_intel},
                    {"role": "user", "content": prompt}
                ],
                temperature=1,
                max_tokens=max_tokens - len(content),
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            if response.choices:
                new_content = response.choices[0].message['content']
                content += new_content
                progress_bar.set_description(f"Tokens Processed: {len(content)}/{max_tokens}")
                progress_bar.update(len(new_content))
            else:
                retry_count += 1  # Increase the retry count if there is no response

        # Close the progress bar
        progress_bar.close()

        return content

    except Exception as e:
        print(f"An error occurred during content generation: {e}")

        # Check the OpenAI status page
        status_data = check_openai_status()
        if status_data:
            incidents = status_data.get('incidents', [])
            if incidents:
                print("OpenAI Status Page - Incidents:")
                for incident in incidents:
                    print(f"- {incident.get('name', 'Unknown')} - {incident.get('status', 'No status available')}")

        return None

try:
    max_tokens = int(os.getenv('MAX_TOKENS'))  # Adjust based on the desired content length
    post_titles = get_post_titles()

    for post_title in post_titles:
        generated_content = generate_content(max_tokens, post_title)
        
        if generated_content:
            # Extract and update categories and tags
            extract_categories_tags(generated_content)

            # Format code snippets in the generated content
            formatted_content = format_code_snippets(generated_content)

            # Create a new blog post
            post = WordPressPost()
            post.title = post_title
            post.content = formatted_content

            # Set the post category, tags, and other properties
            post.terms_names = {
                'category': post_categories,  # Assign the extracted categories here
                'post_tag': post_tags,  # Assign the extracted tags here
            }

            # Save the post as a draft for review
            post.post_status = 'draft'

            # Create the draft post on your WordPress site
            post_id = wp.call(NewPost(post))

            print(f"Draft blog post created with ID {post_id}")

except Exception as e:
    print(f"An error occurred: {e}")
