import json
import os
import boto3

expected_files = ['omniture.tsv', 'regusers.tsv', 'urlmap.tsv']
files = []
sqs = boto3.client('sqs')
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')
bucket_name = ""

def lambda_handler(event, context): 
    try:
        s3_event = json.loads(event['Records'][0]['body'])
        if 'Event' in s3_event and s3_event['Event'] == 's3:TestEvent':
            print("Test Event")
        else:
            mybucket = s3_event['Records'][0]['s3']['bucket']['name']
            bucket_name = mybucket
            filename = s3_event['Records'][0]['s3']['object']['key']
            
            print(mybucket)
            print(filename)
            
            response = s3_client.head_object(Bucket=mybucket, Key=filename)

            file_size = response['ContentLength']
            
            if file_size < 1024:  # Check if the file size is less than 10KB

                # lambda_function_name = "aws-poc-lambda-4"

                payload = {
     
                     "bucket": mybucket,
    
                     "files": filename
    
                }
          
    
                lambda_client.invoke(
        
                  FunctionName=os.environ["Lambda3Name"],
        
                  InvocationType='Event',  # Asynchronous invocation
        
                  Payload=json.dumps(payload)
        
                )
          
                print("lambda3 Invoked")
            
            if filename in expected_files:
                files.append(filename)
                
            print(files) 
                   
    except Exception as exception:
        print(exception)
        
       
    count = 0
    message = []
    for file in expected_files:
        if file in files:
            count+=1
            message.append(file)
        else:
            count = 0
            break; 
    
    
    if count == len(expected_files):
        message.append(bucket_name)
        message_body = ','.join(message) 
    
        response = sqs.send_message(
                        QueueUrl=os.environ["Queue2url"],
                        MessageBody=message_body
                    )
        print((f"Message sent to SQS with ID: {response['MessageId']}"))
        
        
        files.clear()
        message.clear()

	    
    