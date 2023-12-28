import json
  
def lambda_handler(event, context):     
    # Get the input parameters    
    bucket = event['bucket']     
    files = event['files']          
    # Print the received file names    
    print(f"Received files in bucket '{bucket}': {files}")
   