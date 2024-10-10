import subprocess


def install_requirements():
    try:
        # Define the command to install requirements
        command = ["pip", "install", "-r", "requirements.txt"]

        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Print the output
        print("Requirements installation output:\n", result.stdout)
        print("Requirements installation error (if any):\n", result.stderr)

    except subprocess.CalledProcessError as e:
        print("An error occurred while installing requirements:", e)
        raise


def run_pyinstaller():
    try:
        # Define the command to run pyinstaller with additional data
        command = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "api.py",
        ]

        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Print the output
        print("PyInstaller output:\n", result.stdout)
        print("PyInstaller error (if any):\n", result.stderr)

    except subprocess.CalledProcessError as e:
        print("An error occurred while running PyInstaller:", e)


if __name__ == "__main__":
    install_requirements()
    run_pyinstaller()
