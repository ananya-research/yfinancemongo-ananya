import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
table = dynamodb.Table("StockData")

response = table.scan()
print(response["Items"])
