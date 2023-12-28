import json
import boto3
import os

expected_files = ['omniture.tsv', 'regusers.tsv', 'urlmap.tsv']

def lambda_handler(event, context):
  message = event['Records'][0]['body']
  print(message)
  
  values = message.split(',')
  
  mybucket = values[-1]
  
  myfiles = values[:-1]
  
  print(mybucket)
  print(myfiles)
  
  glue_client = boto3.client('glue')
  
  count = 0
  
  for file in expected_files:
            
        if file in myfiles:
            count+=1
        
        else:
            count = 0
            break; 
        
    
  if count == len(expected_files):

    job_arguments = {
          '--SOURCE_BUCKET': mybucket,
          '--FILE_NAMES': ','.join(myfiles),
          '--DEST_BUCKET': os.environ["destBucket"]
      }
      
    response = glue_client.start_job_run(JobName=os.environ["jobname"], Arguments=job_arguments)
    print(response)
    print('GLUE JOB STARTED')
  
  else:
    print("Wrong files found")
  
 