from faasactors.deploy import new_lambda, getNewQueue, sendMessage
from faasactors.lambdaWrapper import lambdaWrapper

lambdaName = "glueLambda2"
queueName = "glueQueue2"
new_lambda(lambdaName,lambdaWrapper, actorPath="./ActorX.py")
getNewQueue(queueName, lambdaName)
sendMessage(queueName, "param0")
# Check out the logs to see if Lambda printed "Hello!!" (from ActorX)