
import gzip
import json
import base64
import boto3

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        #.encode('utf8'),
        'headers': {
            'Content-Type': 'application/json',
            #'Content-Type': 'text',
        },
    }


def lambda_handler(event, context):
    

    cw_data = event['awslogs']['data']
    #cw_data = str(event['awslogs']['data'])
    #cw_logs = gzip.GzipFile(fileobj=BytesIO(base64.b64decode(cw_data, validate=True))).read()
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)
    log_events = payload['logEvents']
    #log_events = json.loads(cw_logs)
    for log_event in log_events:
        a = log_event['message']
    print(a)
    log_events_data = json.loads(a)
    
      
    
    source = log_events_data['eventSource']
    nameevent = log_events_data['eventName']
    user = log_events_data['userIdentity']['principalId']
    secret = log_events_data['requestParameters']['secretId']
    msg = "Hi Team,     We have detected the %s event from AWS Secret Manager Service with below details:    Event Source- %s    Event Name- %s    User- %s  Secret-Id- %s " % (nameevent,source,nameevent,user,secret)
    subj = "Attention! Describe Secret Event Detected by user- %s" % (user)    
   
    if 'DescribeSecret' in nameevent:
        MY_SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:695292474035:sachin-secret'
        sns_client = boto3.client('sns')
        sns_client.publish(
        TopicArn = MY_SNS_TOPIC_ARN,
        Subject = subj,
        Message = msg
        )
        
        return respond(None, "Thanks for using this command. Sending Mail.....")
    else:

        return respond(None, "Thanks for using this fucntion but event detected is diff:%s" % (nameevent))

    
    
 {
  "awslogs": {
    "data": "H4sIAAAAAAAAAJVU227bOBD9lULPYUJdKFN6qjZ2ArfbJrWMtJt1YVDSyBGqW0mqbhr43zukbCfNdhebJwIzZ84Mz1wenAaUEhtY3vfgxM40WSbrd7M0TS5nzonTbVuQaA4j5kVeMAmoz9Bcd5tL2Q09epTI76qWKMglaCK2iuR1NxRaiqomiFPkaSxhge+6YVCOJKmWIJpn/OtzQ7A0BOtBERBKExfxashULqteV117UdUapHLiv538DvIvzmfLN/sGrTbWB6cqkNYPOQ8jl3qBS6kfcT+YhDRkURRMJpOAhy6NXJ+jmbqMYwnciyYMLZhNVyiMFg3+0Q1ZQMPQCxHknhwEQ/qHlQMm4w2WgkWtnHjluKeUr5yTlTMokPMCvZW+Rw9iNUpsMYlSQwPFoqvBQntZtXnVi3pejP7FVeJN/7p5c/n2dvHmQ3B1++fFdTwq/bq1+qrTvGtssJBjYnxjlD9WWsXxUz1jMaYjEvOdJR/TBWBp36BI06v1no2ooe87qdcs4wXjfkZZEZZZWJ79W9Y874ZW7wt+mu7gRpXewv3hR+n8+KMbz/vj0+z9JwtUCEPpzrtWw3c96rS3zbFskM+ke5lmvxWoEs0zgawwZnTlXpkzpbpT0YgfXYtm8+mX6vZ/RDIT8l40+5l4Kf8OGbaQzYsLKEAKsxVToYXRy7iE1rLKBg1qVBDX84AZE3rU8wgNCXWXNIgZi73w1pbVlCIZ9J2Z3BzBY/GlqBXG7XaG2w79smr+SRTGjMY+HYksLO0GmY/A8UaoRrS4PvJXfR8DjopMwax7BqkNGwXdqgVsDqt2PA7jJNlE8+ukKLCN6iDqqzlOlmxFfZQ82WCW37slfB1w66+FxCLMgTkMpKlg38ZNpe+GjOjuC7RjFzBd37UKZjU05v4grB3q+pFvPrWRWY5npMh94vquIAFnGRHZJCfYVo+WWQk8ZI867IOoLzhwryRZzjkJAjYhnLsFKVkERZF7pe+yfe2iuGprc2u0HODYpuPR2aqkr85FPX517IKp1x7NxygJuFYVmpL/nl7Lfo4DsunkvYW8O1L+stoS7BUU9YXsGlx0ZVcY8SYhKujsPu9+Ai60ULCHBgAA"
  }
}
