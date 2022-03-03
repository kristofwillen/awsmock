# awsmock
This repo contains a playground of scripts how to mock AWS boto3 API calls.
Also, some pydantic class implementations of boto3 resources.

In the cfn_schemas directory, the schemas of all AWS services are defined.  A Python pydantic implementation class can be defined for each file as such :

```bash
$ pip install datamodel-code-generator[http]

$ wget https://schema.cloudformation.us-east-1.amazonaws.com/CloudformationSchema.zip
$ mkdir cfn_schemas
$ mv CloudformationSchema.zip cfn_schemas/
$ cd cfn_schemas/
$ unzip CloudformationSchema.zip
$ cd ..
$ datamodel-codegen  --input cfn_schemas/aws-s3-bucket.json --input-file-type jsonschema --output aws_s3_bucket.py
$ cat aws_s3_bucket.py
```

