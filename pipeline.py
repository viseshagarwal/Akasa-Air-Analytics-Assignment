import os
import subprocess
import platform
import shutil
import webbrowser


def run_command(command):
    """Helper function to run a command in the shell."""
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        exit(1)


def create_virtual_environment():
    """Creates a virtual environment."""
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        run_command("python -m venv venv")
        print("Virtual environment created.")
    else:
        print("Virtual environment already exists. Skipping creation step.")


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
    if os.path.exists('.env'):
        print(".env file already exists. Skipping creation step.")
    else:
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


def start_jupyter_or_vscode():
    """Starts Jupyter Notebook server if available, otherwise opens VS Code."""
    print("Checking for Jupyter Notebook...")

    # Check if Jupyter is installed by checking if it's in the system path
    if shutil.which("jupyter"):
        try:
            print("Jupyter Notebook found. Starting Jupyter Notebook server...")
            run_command("jupyter notebook")
        except Exception as e:
            print(f"Failed to start Jupyter Notebook: {e}")
    else:
        print("Jupyter Notebook not found. Opening VS Code...")
        try:
            run_command("code .")  # Opens VS Code in the current folder
        except Exception as e:
            print(f"Failed to open VS Code: {e}")


def generate_html_report():
    """Runs the script to generate the HTML report."""
    if not os.path.exists("reports/aviation_report.html"):
        print("Generating HTML report...")
        run_command("python generate_report.py")
        print("HTML report generated: reports/aviation_report.html")
    else:
        print("HTML report already exists. Skipping report generation step.")

    # Open the HTML report in the default browser
    report_path = os.path.abspath("reports/aviation_report.html")
    print(f"Opening the report in the browser: {report_path}")
    webbrowser.open(f"file://{report_path}")


def main():
    # Step 1: Set up and activate virtual environment
    create_virtual_environment()
    activate_virtual_environment()

    # Step 2: Install dependencies
    install_dependencies()

    # Step 3: Set up .env file interactively
    setup_env_file()

    # Step 4: Ensure MySQL server is running
    check_mysql_server()

    # Step 5: Start Jupyter Notebook if available, otherwise VS Code
    start_jupyter_or_vscode()

    # Step 6: Generate HTML report after analysis and open it in the browser
    generate_html_report()


if __name__ == "__main__":
    main()
