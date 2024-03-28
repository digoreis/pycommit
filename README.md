# PyCommit

This project automates the process of generating commit messages based on the changes made in your Git repository. It utilizes the OpenAI API to generate meaningful commit messages in English.

## Installation

1. Clone this repository to your local machine:
`git clone <repository-url>`
2. Install the required dependencies:
`pip install -r requirements.txt`
3. Set up your OpenAI API key:
   - Sign up for an account on the [OpenAI website](https://openai.com/).
   - Generate an API key.
   - Set the API key as an environment variable or directly in the script.

## Usage

To use this tool, follow these steps:

1. Navigate to the root directory of your Git repository.
2. Run the script `commit.py` with the path to your repository as an argument:

`python commit.py /path/to/your/git/repo`

3. If you have a `.pycommit.yml` file in your repository with custom parameters, the script will utilize those parameters. Otherwise, it will use default parameters.
4. The script will generate a commit message based on the changes in your repository and copy it to your clipboard.

## Configuration

You can customize the behavior of the commit message generation by modifying the `.pycommit.yml` file in your repository. Here is an example of how to structure the file:

```yaml
context:
  - "Custom parameter 1"
  - "Custom parameter 2"
  - "Custom parameter 3"
```

Each parameter specified in the context section will be included in the context for generating the commit message.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.