from faasactors.deploy import *
queueName = "fromPython3"
getNewQueue(queueName,"ProcessSQSRecord")
sendMessage(queueName, "firstTimeFromPython")