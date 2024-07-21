# ozora-ogino/auto-readme

## Description
Auto-readme is a Python application designed to automatically generate README files for GitHub repositories. The application fetches updates or changes made in the repository, retrieves content from important files, and seamlessly rebuilds the updated README.

Updates have been made to the `update_readme.py` file, altering the guidelines for generating the best possible README content.

## Features
- Automatic generation of updated README files triggered by changes in the repository code.
- Enhanced detection range for endpoint changes in multiple languages, including Python, Java, JavaScript and Go.
- Recursive fetching of the repository tree to extract all file paths.
- Integration of relevant details from the current README, important file contents, and the detected code changes.
- Truncation of extensive file contents and diff information to optimize the README update process and enhance performance.
- Various error handling mechanisms, including content generation errors and exceeding maximum content length.

## Usage
To use Auto-readme, follow these steps:

1. Copy following into `.github/workflows/auto-readme.yml` in your repo.
Please refer to this example for how to set up the `.github/workflows/auto-readme.yml` in your repo.

```yaml
# README Updater Action
#
# This GitHub Action automatically updates the README.md file based on changes in Pull Requests.
# It uses OpenAI's language models to generate concise and informative updates,
# focusing on critical changes such as workflows, package.json, and application endpoints.
#
# Usage Instructions:
# 1. Copy this entire file to .github/workflows/update-readme.yml in your repository.
# 2. Create a .github/README_TEMPLATE.md file in your repository with the structured template.
# 3. Set up the required secrets and variables in your repository:
#    - Go to your repository's Settings > Secrets and variables > Actions
#    - Add a new repository secret named OPENAI_API_KEY with your OpenAI API key
#    - Add a new repository secret named GH_TOKEN with a GitHub Personal Access Token
#      (The token should have 'repo' scope for private repositories, or 'public_repo' for public repositories)
# 4. Configure your repository settings:
#    - Go to your repository's Settings >...
```

2. Add `.github/README_TEMPLATE.md`. (Refer to the provided example)

## License
MIT License

Copyright (c) 2024 Ozora Ogino

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell...