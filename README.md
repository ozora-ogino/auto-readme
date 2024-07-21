# ozora-ogino/auto-readme

## Description
A tool to automate README generation in your repositories.

## Dependencies
- python
- github
- openai

## Recent Updates
Minor updates in the `update_readme.py` script:

- The imports of 'github' and 'openai' have been moved below basic script configurations.
- No changes in the installation, usage, or endpoints.

```python
import os
import sys
import logging
import time
import re

from github import Github
from openai import OpenAI

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
```

## Installation
Please refer to the installation guide found in the installation.md file.

## Usage
Please refer to the usage guide found in the usage.md file.

## Contributing
If you wish to contribute, please create a new issue and submit a pull request.

## License
Please refer to the LICENSE file for information about the license.

## Contact
Please submit a new issue for contact. 

**NOTE**: This README is auto-generated. If any discrepencies are found, please raise an issue.