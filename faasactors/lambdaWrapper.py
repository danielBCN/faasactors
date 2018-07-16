import boto3
import importlib
from faasactors.userCode import userCode



def lambdaWrapper(event, context):
    # readFromDB()
    actor = "ActorX"
    method = "sayHello"
    userModule = importlib.__import__(actor)

    clazz = getattr(userModule, actor)
    inst = clazz()
    invoke = getattr(inst, method)
    invoke()


    # writeToDB()

def readFromDB():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def writeToDB():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table("table0")



