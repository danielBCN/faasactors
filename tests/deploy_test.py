from faasactors.utils.deploy import *
from tests.handler_example import my_handler


def main():
    new_lambda("deployed_lambda", my_handler)
    #  set_lambda_concurrency("deployed_lambda", 1)
    #  delete_lambda("deployed_lambda")


if __name__ == "__main__":
    main()
