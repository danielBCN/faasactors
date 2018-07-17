import importlib
import json

from faasactors.actor import Actor


def lambda_wrapper(event, context):
    for record in event['Records']:
        message = json.loads(record["body"])

        actor_name = message["TO"]
        assert actor_name == context.function_name
        method = message["METHOD"]
        args = message["PARAMS"][0]
        kwargs = message["PARAMS"][1]

        actor_clazz_name = "Node"  # FIXME: hardcoded
        actor_module_name = "ring"  # FIXME: hardcoded
        actor_module = importlib.__import__(actor_module_name)

        clazz = getattr(actor_module, actor_clazz_name)
        a = Actor(actor_name, clazz)
        a.load()
        a.invoke(method, args, kwargs)
        a.dump()
