import os
import subprocess
import platform
import shutil


def run_command(command):
    """Helper function to run a command in the shell."""
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        exit(1)


def clone_repository(repo_url):
    """Clones the repository."""
    print("Cloning the repository...")
    run_command(f"git clone {repo_url}")
    print("Repository cloned.")


def navigate_to_project_directory():
    """Navigate to the project directory."""
    os.chdir("Akasa-Air-Analytics-Assignment")
    print("Navigated to project directory.")


def create_virtual_environment():
    """Creates a virtual environment."""
    print("Creating virtual environment...")
    run_command("python -m venv venv")
    print("Virtual environment created.")


def activate_virtual_environment():
    """Activates the virtual environment."""
    print("Activating virtual environment...")
    os_name = platform.system()
    if os_name == "Windows":
        run_command("venv\\Scripts\\activate")
    else:
        run_command("source venv/bin/activate")
    print("Virtual environment activated.")


def install_dependencies():
    """Installs required dependencies."""
    print("Installing dependencies from requirements.txt...")
    run_command("pip install -r requirements.txt")
    print("Dependencies installed.")


def get_env_values():
    """Prompts the user for .env values."""
    db_user = input("Enter DB_USERNAME: ")
    db_password = input("Enter DB_PASSWORD: ")
    db_host = input("Enter DB_HOST: ")
    db_port = input("Enter DB_PORT: ")
    db_name = input("Enter DB_NAME: ")

    return {
        "DB_USER": db_user,
        "DB_PASSWORD": db_password,
        "DB_HOST": db_host,
        "DB_PORT": db_port,
        "DB_NAME": db_name
    }


def write_env_file(env_values):
    """Writes the collected values to the .env file."""
    with open('.env', 'w') as env_file:
        for key, value in env_values.items():
            env_file.write(f"{key}={value}\n")
    print(".env file updated with database credentials.")


def setup_env_file():
    """Sets up the .env file interactively."""
    print("Setting up .env file...")
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print(".env file created from .env.example.")
    else:
        print(".env.example file not found. Creating a new .env file.")

    # Get values from the user and write them to the .env file
    env_values = get_env_values()
    write_env_file(env_values)


def check_mysql_server():
    """Check if MySQL server is running (optional)."""
    print("Ensure your MySQL server is running and the necessary database is created.")


def start_jupyter_notebook():
    """Starts Jupyter Notebook server."""
    print("Starting Jupyter Notebook server...")
    run_command("jupyter notebook")


def generate_html_report():
    """Runs the script to generate the HTML report."""
    print("Generating HTML report...")
    run_command("python generate_report.py")
    print("HTML report generated: reports/aviation_report.html")


def main():
    repo_url = "https://github.com/viseshagarwal/Akasa-Air-Analytics-Assignment.git"

    # Step 1: Clone the repository
    clone_repository(repo_url)

    # Navigate to the project directory
    navigate_to_project_directory()

    # Step 2: Set up and activate virtual environment
    create_virtual_environment()
    activate_virtual_environment()

    # Step 3: Install dependencies
    install_dependencies()

    # Step 4: Set up .env file interactively
    setup_env_file()

    # Step 5: Ensure MySQL server is running
    check_mysql_server()

    # Step 6: Start Jupyter Notebook and guide user to execute notebook cells manually
    start_jupyter_notebook()

    # Step 7: Generate HTML report after analysis
    generate_html_report()


if __name__ == "__main__":
    main()
