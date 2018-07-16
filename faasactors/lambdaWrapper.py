import boto3

from faasactors.userCode import userCode



def lambdaWrapper(event, context):
    #readFromDB()

    u = userCode()
    u.userFunction()

    #writeToDB()

def readFromDB():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def writeToDB():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table("table0")



