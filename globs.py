import pathlib

current_directory = pathlib.Path(__file__).parent.resolve()
images_directory = current_directory / "images"
USAGE_PATH = "example_usage.json" # Replace with actual path in Prod obviously.