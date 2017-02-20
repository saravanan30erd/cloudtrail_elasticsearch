# cloudtrail_elasticsearch
Index live streaming cloudtrail data from s3 to elasticsearch

# steps
 - Configure cloudtrail s3 bucket to invoke a lambda function whenever objects are uploaded to that bucket.
 - Create a AWS lambda function to manipulate the cloudtrail data and store it to elasticsearch.

