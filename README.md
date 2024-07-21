# ozora-ogino/auto-readme

## Description
Auto-readme is a Python application designed to automatically generate README files for GitHub repositories. It detects updates or changes made in the repository, integrates important file information, and accordingly rebuilds the updated README.

## Dependencies
To operate this application, the following dependencies must be installed:
- Python 3.7+
- GitHub Python package

## Features
- Generates updated README files automatically based on code changes.
- Enhanced detection range for endpoint files in multiple languages including Go, Rust, Scala, Kotlin, and Swift.
- Extracts all file paths by recursively fetching the repository tree.
- Includes relevant information from the current README, code changes, and important files.

## Installation
Clone the repository and install the necessary packages using pip:
```bash
git clone https://github.com/ozora-ogino/auto-readme.git
cd auto-readme
pip install -r requirements.txt
```

## Usage
The following command initiates the application:
```bash
python update_readme.py
```
Upon execution, the script retrieves the repository tree, identifies any updates in the repository, and rebuilds the README as required.

## Recent Updates
The repository has undergone considerable changes to improve the overall performance of the automatic README generation. Key updates include:
- Implementation of logic to extract important files from the repository tree.
- Enhancement of the README generation instructions.
- Improved readability and comprehensibility of the README document generation process.
- Improved logging during the document generation process.
- Updated application logic for maintaining the current README state for the next iteration.

## Contributing
To contribute, fork the repository, make changes on your branch and submit a Pull Request. Modifications should not affect existing workflows but enrich the existing application features.

## License
This project is licensed under the MIT License.

## Important Files
The following are key files in this project:
- .github/README_TEMPLATE.md
- .github/workflows/auto-readme.yml
- LICENSE
- README.md
- update_readme.py

## Contact
For any inquiries or suggestions, kindly raise an issue on the project page of the repository.