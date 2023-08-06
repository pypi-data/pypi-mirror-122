import fire
from ml_models.driver import main
class CliCommand:
    def __init__(self):
        self.main = main

if __name__ == '__main__':
    fire.Fire(CliCommand)