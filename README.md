# AI-Generated WordPress Blog Post Automation

![GitHub](https://img.shields.io/github/license/imgeraldalinio/AI-Generated-WordPress-Blog-Post-Automation)
![GitHub last commit](https://img.shields.io/github/last-commit/imgeraldalinio/AI-Generated-WordPress-Blog-Post-Automation)
![GitHub contributors](https://img.shields.io/github/contributors/imgeraldalinio/AI-Generated-WordPress-Blog-Post-Automation)

Automate the process of generating WordPress blog posts using AI. This project simplifies the creation of technical blog posts, complete with code formatting, and publishes them on your WordPress site.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project is designed to streamline the process of generating technical blog posts using AI-powered content generation. It includes a Python script that interacts with OpenAI's GPT-4 model to create high-quality, informative, and undetectable blog posts. The script can be configured with various options and deployed in your CI/CD pipeline for automatic content generation.

## Prerequisites

Before you get started, ensure you have the following in place:

- **OpenAI API Key**: You need an API key to interact with the GPT-4 model. Get your API key from [OpenAI](https://beta.openai.com/signup/).
- **WordPress Site**: You should have a WordPress site with XML-RPC enabled. Ensure you have the site URL, username, and password.

## Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/imgeraldalinio/AI-Generated-WordPress-Blog-Post-Automation.git
    cd AI-Generated-WordPress-Blog-Post-Automation
    ```
2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```
    This command will install all the required libraries listed in the `requirements.txt` file.

3. Create a `.env` file in the project root directory and set your environment variables:
    ```ini
    OPENAI_API_KEY=your_openai_api_key
    WORDPRESS_SITE_URL=https://example.com/xmlrpc.php
    WORDPRESS_USERNAME=your_wordpress_username
    WORDPRESS_PASSWORD=your_wordpress_password
    MAX_TOKENS=400
    ```

4. Run the script to generate and publish your blog posts.

## Usage

- Customize your post title by editing the `post_title` variable value.
- The content automatically generate a `post_categories`, and `post_tags` in your content.
- Adjust the `max_tokens` value to control the length of generated content.
- Modify the template format in the `generate_content` function to match your desired blog post structure.
- Ensure your WordPress post settings align with the template format.

Run the script to create draft posts on your WordPress site. You can then review and publish them manually:
```bash
python generate-blog-post.py
```

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/imgeraldalinio/AI-Generated-WordPress-Blog-Post-Automation/blob/main/LICENSE) file for details.

**Note:** It's important to use this project responsibly and ensure that generated content complies with ethical and legal standards. Be cautious with the information and content generated by AI models.

For any questions or issues, please open a GitHub [issue](https://github.com/imgeraldalinio/AI-Generated-WordPress-Blog-Post-Automation/issues).
