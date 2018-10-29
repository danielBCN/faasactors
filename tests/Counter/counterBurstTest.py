import inspect

from faasactors.client import spawn, lookup
from tests.Counter.Counter import Counter
import boto3

from faasactors.utils.config import AWS_ROLE_ARN, AWS_REGION, LAMBDA_UPDATE
from tests.Counter import deferredInvoker
from utils.deploy import delete_lambda, set_lambda_concurrency
from utils.packaging import package_with_dependencies

lambdacli = boto3.client('lambda', region_name=AWS_REGION)

def deployDeferred(handler):
    # zip function-module and dependencies
    klass_path = inspect.getfile(deferredInvoker)
    zipfile, lamhand = package_with_dependencies(handler, klass_path)
    try:
        lambdacli.create_function(
            FunctionName='deferredTest',
            Runtime='python3.6',
            Role=AWS_ROLE_ARN,
            Code={'ZipFile': zipfile.getvalue()},
            Handler=lamhand,
            Publish=True,
            Description='Lambda which invokes more lambdas.',
            Timeout=30,
            MemorySize=3008,
        )
        print(f"New lambda deferredTest created successfully.")
    except lambdacli.exceptions.ResourceConflictException:
        print("Lambda already exists...")
        if LAMBDA_UPDATE:
            print("Updating Lambda...")
            delete_lambda('deferredTest')
            deployDeferred(handler)
        else:
            print("*NO* Lambda update. Proceeding...")




def main():
    actor = spawn("Counter", Counter, 900)
    actor.increment()


if __name__ == '__main__':
    main()
