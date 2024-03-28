import os
import sys
import git
import yaml
from openai import OpenAI
import pyperclip

def load_commits(repo_path, size):
    repo = git.Repo(repo_path)
    if repo.head.is_valid() is False:
        return []

    iter_commits = repo.iter_commits()

    commit_messages = []
    for i, commit in enumerate(iter_commits):
        if i == size:
            break
        commit_messages.append(commit.message)
    return commit_messages


def load_context_parameters_from_yaml(file_path):
    """
    Carrega uma lista de parâmetros strings de um arquivo YAML e retorna como uma lista Python.
    Se o arquivo não existir ou não contiver a chave 'context', retorna uma lista vazia.
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
        parameters = yaml_data.get('context', [])
    return parameters

def load_log_parameters_from_yaml(file_path):
    """
    Carrega uma lista de parâmetros strings de um arquivo YAML e retorna como uma lista Python.
    Se o arquivo não existir ou não contiver a chave 'log_size', retorna zero.
    """
    if not os.path.exists(file_path):
        return 0

    with open(file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
        history_size = yaml_data.get('log_size', 0)
    return history_size


def get_git_diff(repo_path):
    """
    Obtém o diff dos arquivos alterados no repositório Git.
    """
    repo = git.Repo(repo_path) 
    return repo.git.diff(None)


def generate_commit_message(diff, context_settings, logs):
    """
    Gera uma mensagem de commit em inglês usando a API do ChatGPT.
    """
    prompt = f"Generate a commit message based on the following diff:\n{diff}\n\nGenerated commit message:"
    client = OpenAI()

    system_values = [{"role": "system",
                      "content": "You are a developer writing messages to a commit with a very declaritive with a "
                                 "format to opensource project"},
                     {"role": "system",
                      "content": "The best format is a list with breakline and start the list with a * with"
                                 "the changes separates"},
                     ]
    for param in context_settings:
        system_values.append({"role": "system", "content": param})

    for log in logs:
        system_values.append({"role": "system", "content": f"That is a sample from message in this project: {log}"})

    system_values.append({"role": "user", "content": prompt}, )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=system_values,
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/your/git/repo")
        sys.exit(1)

    project_path = sys.argv[1]
    if not os.path.exists(project_path):
        print("Error: Provided directory does not exist.")
        sys.exit(1)
    
    settings_path = project_path+"/.pycommit.yml"
    settings_context_values = load_context_parameters_from_yaml(settings_path)
    settings_logsize_value = load_log_parameters_from_yaml(settings_path)
    diff_value = get_git_diff(project_path)
    log_values = load_commits(project_path, settings_logsize_value)

    commit_message = generate_commit_message(diff_value, settings_context_values, log_values)
    print(commit_message)
    pyperclip.copy(commit_message)
