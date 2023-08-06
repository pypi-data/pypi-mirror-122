import os
import sys
import json
import time
import signal
import logging
import argparse
from halo import Halo
from prettytable import PrettyTable
from colorlog import ColoredFormatter
from innocuousbook_api import InnoucousBookAPI

class InnocuousBookCLI:
    def __init__(self, token, host, **kwargs):
        self.version = "1.0.0"
        self.debug = True if 'debug' in kwargs and kwargs['debug'] else False
        self.init_logger()

        self.host = host
        self.token = token

        self.api = InnoucousBookAPI(self.token, host=self.host)

    def init_logger(self):
        if self.debug:
            LOG_LEVEL = logging.DEBUG
        else:
            LOG_LEVEL = logging.INFO
        datefmt = '%Y-%m-%d %H:%M:%S'
        LOGFORMAT = "%(log_color)s[%(asctime)s][%(levelname)-8s]%(reset)s %(log_color)s%(message)s%(reset)s"
        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT, datefmt)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)
        self.log = logging.getLogger('innocuousboolCLI')
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)

    def get_version(self):
        self.log.info(f"CLI version: {self.version}")
        self.log.info(f"Server version: {self.api.get_server_version()}")
    
    def generate_config_template(self):
        self.log.info(f"Generate recipe template: demo_recipe.json")
        with open("demo_recipe.json", "w") as f:
            json.dump(self.get_demo_recipe(), f, indent=4)
        
    def run_experiment(self, recipe):
        experiment = Halo(text="Creating experiment...", spinner="dots")
        experiment.start()
        recipe_dict = None
        with open(recipe, 'r') as f:
            recipe_dict = json.load(f)

        result = self.api.create_experiment(recipe_dict)
        if result["code"] == 0:
            self.api.wait_experiment_status(result["data"]["id"], "Running")
            experiment.text = "Running experiment..."
            while True:
                status = self.api.get_experiment(result["data"]["id"])["status"]
                if status == "End":
                    experiment.succeed("experiment success")
                    return True
                elif status == "Failed":
                    experiment.fail("experiment failed")
                    return False
                time.sleep(10)


    def updload_file(self, name, file_type, file_path):
        if file_type == "dataset":
            if not file_path:
                self.log.error("Please enter file path")
            return self.api.upload_dataset(file_path)
        else:
            if not name:
                self.log.error("Please enter name")
                return False
            if not file_path:
                self.log.error("Please enter file path")
                return False

            if os.path.isdir(file_path):
                if file_path[-1] != "/":
                    file_path = f"{file_path}/"
                if file_type == 'model':
                    return self.api.upload_model(name, file_path)
                elif file_type == 'function':
                    return self.api.upload_function(name, file_path)
            elif os.path.isfile(file_path):
                if file_type == 'requirements':
                    return self.api.upload_requirements(name, file_path)
    
    def list_file(self, file_type, output_format):
        if file_type == "model":
            files = self.api.list_model()
        elif file_type == "function":
            files = self.api.list_function()
        elif file_type == "dataset":
            files = self.api.list_dataset()
        elif file_type == "requirements":
            files = self.api.list_requirementst()

        if output_format == "table":
            my_table = PrettyTable()
            my_table.field_names = ["No.", "Name", "Path"]
            for index, item in enumerate(files):
                my_table.add_row([index, item['name'], item['path']])
            print(my_table)
        else:   # json
            json_data = json.dumps(files, indent=4)
            print(json_data)

    def get_demo_recipe(self):
        recipe = {
            "info": {
                "name": "demo-recipe",
                "description": "demo recipe",
                "instance": 4,
                "image": {
                    "id": 1
                }
            },
            "function": {
                "path": "data://function/pytorch_function/",
            },
            "model": {
                "path": None,
            },
            "dataset": {
                "path": "data://dataset/mnist.zip",
            },
            "requirements": {
                "id": None,
            },
            "config": {
                "trainer": [{"desc": "Learning rate", "name": "lr", "lower": 0.001, "upper": 0.01, "distribution": "uniform"}, {"desc": "Epochs", "name": "epochs", "lower": 2, "upper": 4, "distribution": "randint"}, {"desc": "Optimizer", "name": "optimizer", "value": "adam", "distribution": "const"}, {"desc": "Losses", "name": "losses", "value": "categorical_crossentropy", "distribution": "const"}, {"desc": "Batch size", "name": "batch_size", "value": 2, "distribution": "const"}, {"desc": "Shuffle", "name": "shuffle", "value": "True", "distribution": "const"}], 
                "trialer": [{"desc": "Number of experiment", "name": "samples", "value": 1, "distribution": "const"}, {"desc": "Metric", "name": "metric", "value": "accuracy", "distribution": "const"}, {"desc": "Mode", "name": "mode", "value": "max", "distribution": "const"}, {"desc": "Framework", "name": "framework", "value": "function", "distribution": "const"}, {"desc": "Search algorithm", "name": "search_algorithm", "value": "", "distribution": "const"}], 
                "function": [{"name": "lr", "value": 0.001, "distribution": "const"}, {"name": "epochs", "value": 2, "distribution": "const"}, {"name": "batch_size", "value": 256, "distribution": "const"}]
            }
        }
        return recipe

def signal_handler(sig, frame):
    print('')
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Innocuous book CLI', prog='innocuous')
    parser.add_argument('action', help='trial model/function,\nupload file,\ngenerate config,\nlist files', nargs='?', choices=('generate', 'trial', 'upload', 'list', 'version'))
    parser.add_argument('option', help='innocuous [list, upload] [function, model, dataset, requirements]', nargs='?', choices=('function', 'model', 'dataset', 'requirements'))
    parser.add_argument("-n", "--name", help="Name")
    parser.add_argument("-r", "--recipe", help="Recipe file")
    parser.add_argument("-p", "--path", help="Path")
    parser.add_argument("-o", "--output", default="table", help="Output format")

    args = parser.parse_args()

    token = os.getenv("INNOCUOUSBOOK_TOKEN")
    host = os.getenv("INNOCUOUSBOOK_HOST", "https://dashboard.innocuous.ai")

    cli = InnocuousBookCLI(token, host)

    if args.action == 'version':
        cli.get_version()
    elif args.action == 'trial':
        cli.run_experiment(args.recipe)
    elif args.action == 'upload':
        cli.updload_file(args.name, args.option, args.path)
    elif args.action == 'list':
        cli.list_file(args.option, args.output)
    elif args.action == 'generate':
        cli.generate_config_template()
        
    return 0
    
def call_cmd():
    signal.signal(signal.SIGINT, signal_handler)
    sys.exit(main())
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    sys.exit(main())
