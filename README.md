# ozora-ogino/auto-readme

## Description
Auto-readme is a Python application designed to automatically generate README files for GitHub repositories. The application fetches updates or changes made in the repository, retrieves content from important files, and seamlessly rebuilds the updated README.

Updates have been made to the `update_readme.py` file, altering the guidelines for generating the best possible README content.

## Features
- Automatic generation of updated README files triggered by changes in the repository code.
- Enhanced detection range for endpoint changes in multiple languages, including Python, Java, JavaScript, and Go.
- Recursive fetching of the repository tree to extract all file paths.
- Integration of relevant details from the current README, important file contents, and the detected code changes.
- Truncation of extensive file contents and diff information to optimize the README update process and enhance performance.
- Various error handling mechanisms, including retries and validation steps, to ensure robust and reliable README updates.

## Usage
1. Copy the following into `.github/workflows/auto-readme.yml` in your repo.

```yaml
name: Update README

on:
  pull_request:
    types: [closed]
    paths-ignore:
      - 'README.md'

env:
  OPENAI_MODEL: gpt-4o
  TARGET_BRANCH: main

jobs:
  update-readme:
    runs-on: ubuntu-latest
    if: |
      github.event.pull_request.merged == true &&
      !startsWith(github.event.pull_request.title, 'AutoReadme:')
    permissions:
      contents: write
      pull-requests: write
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
        token: ${{ secrets.GH_TOKEN }}

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
      
    - name: Install Dependencies
      run: pip install -r requirements.txt

    - name: Update README
      run: python update_readme.py
      env:
        GH_TOKEN: ${{ secrets.GH_TOKEN }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        GITHUB_REPOSITORY: ${{ github.repository }}
        PR_NUMBER: ${{ github.event.pull_request.number }}
        OPENAI_MODEL: ${{ env.OPENAI_MODEL }}
```

## License
MIT License

```
MIT License

[Full license text here]
```

## Contributing
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push to the branch.
5. Create a new Pull Request.

---

By following these instructions, you ensure your repository has the most up-to-date changes reflected in the README automatically, keeping it accurate and useful for all users and contributors.