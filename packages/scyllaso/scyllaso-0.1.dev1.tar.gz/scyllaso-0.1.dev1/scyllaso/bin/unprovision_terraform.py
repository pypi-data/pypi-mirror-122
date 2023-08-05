import argparse
import yaml
from scyllaso import terraform


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("terraform_plan", help="The terraform_plan to execute (directory).", nargs='?')
    args = parser.parse_args()

    terraform_plan = args.terraform_plan
    if not terraform_plan:
        with open('properties.yml') as f:
            properties = yaml.load(f, Loader=yaml.FullLoader)
        terraform_plan = properties.get('terraform_plan')
        if not terraform_plan:
            raise Exception("Could not find 'terraform_plan' in properties.yml")

    terraform.destroy(terraform_plan)
