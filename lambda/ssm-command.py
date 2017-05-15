########################
# Created by Chris Cooke
# Last Updated: 15/05/2017
#
# Required Env Vars:
# VPC_ID - ID of the network to find instances in
# COMMAND - command to run on the instance e.g. bash /path/to/script.sh
#
########################
from __future__ import print_function
import json
import random
import os
import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connections
ec2 = boto3.resource('ec2')
client = boto3.client('ssm')

def lambda_handler(event, context):
    print('boto3 version: %s' % boto3.__version__)

##################################################
## Get running Magento EC2 Instances to run crons
##################################################
    filters = [{
            'Name': 'tag:Software',
            'Values': ['Magento']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        },
           {
            'Name': 'vpc-id',
            'Values': [os.environ['VPC_ID']]
        }
    ]

    #filter the instances
    instances = ec2.instances.filter(Filters=filters)
    #locate all running instances
    RunningMagentoInstances = [instance.id for instance in instances]
    # pick ONE random instance from the running instances to run the cron task on
    CronInstance = random.choice(RunningMagentoInstances)

    #make sure there are actually instances to run the cron jobs on.
    if len(CronInstance) > 0:
    ##################################################
    ## Send the SSM command to the CronInstance
    ##################################################
      response = client.send_command(
          InstanceIds=[
              CronInstance
          ],
          DocumentName='AWS-RunShellScript',
          TimeoutSeconds=120,
          Comment='Runs Magento shell command',
          Parameters={
              "commands":
                    [os.environ['COMMAND']],
              "executionTimeout": [
                  "3600"
              ]
          }
      )

       # remove dates that are break json serialization
      response['Command'].pop("RequestedDateTime", None)
      response['Command'].pop("ExpiresAfter", None)
      print(response)
    else:
      print ("Error: No running Magento instances that match the filters can be found")
