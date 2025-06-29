import subprocess

def ask_mistral(question):
    """
    Calls your local Mistral model via command line or Python API
    Replace the example below with your actual call.
    """

    # Example: call a CLI tool that takes question as argument and returns answer
    try:
        result = subprocess.run(
            ['mistral-cli', '--query', question],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "Sorry, I couldn't get an answer right now."
    except Exception as e:
        return f"Error: {str(e)}"
