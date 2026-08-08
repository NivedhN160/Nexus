# Contributing to NEOS

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.

## Adding New Tools

To add a new capability to NEOS:
1. Navigate to the `tools/` directory.
2. Create a new python file for your tool or add to an existing category.
3. Ensure your tool function has a clear, descriptive docstring. NEOS's LLM engine parses these docstrings directly to understand how to use the tool.
4. Register the tool in `tools/__init__.py`.

## Code of Conduct

By participating, you are expected to uphold this Code of Conduct. Please report unacceptable behavior to the repository administrators.
