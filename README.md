# ozora-ogino/auto-readme

## Description
Auto-readme is a Python application designed to automatically generate README files for GitHub repositories. The application fetches updates or changes made in the repository, retrieves content from important files, and seamlessly rebuilds the updated README. An update has been made to the `update_readme.py` file, heightening the standards for generating the best possible README content.

## Features
- Automatic generation of updated README files triggered by changes in the repository code.
- Enhanced detection range for endpoint changes in multiple languages, including Python, Java, JavaScript and Go.
- Recursive fetching of the repository tree to extract all file paths.
- Integration of relevant details from the current README, important file contents, and the detected code changes.
- Truncation of extensive file contents and diff information to optimize the README update process and enhance performance.
- Various error handling mechanisms, protecting the process from unexpected issues.
- Improved guidelines for creating the presentable and all-embracing README content.

## Usage
1. Copy following into `.github/workflows/auto-readme.yml` in your repo.

```.github/workflows/auto-readme.yml

name: Update README

on:
  pull_request:
    types: [closed]
    paths-ignore:
      - 'README.md'

env:
  OPENAI_MODEL: gpt-4
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
      ...

IMPORTANT: As part of the new guidelines for generating impressive README content, please perform a forced addition whenever a template has been changed. Follow the exact template format, incorporate relevant information from the current README, code changes, and important file contents for completeness. Attempt to improve readability by use of tables, toggles, code blocks, etc., where necessary. Replace placeholder tags with actual content and format it in Markdown without any redundant explanation or starting from a code block. If no significant changes are necessary, append 'NO_CHANGES_NEEDED' to your update. Avoid referring to external documents, instead, include all the necessary information within the README document.