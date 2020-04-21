# metrics

You can use [Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) to monitor, store, and access your metric data.  [AWS Lambda](https://aws.amazon.com/lambda/) and [Amazon API Gateway](https://aws.amazon.com/api-gateway/) have very tight integration with Amazon CloudWatch Metrics.

**Note** Your resource needs proper IAM permissions to create CloudWatch Logs Log Groups and Log Streams.


# Best practices

## Emit custom metrics using Embedded Metric Format (EMF)

[Embedded Metric Format (EMF)](https://aws.amazon.com/about-aws/whats-new/2019/11/amazon-cloudwatch-launches-embedded-metric-format/) was introduced in November 2019.  

It enables you to ingest complex high-cardinality application data in the form of logs and easily generate actionable metrics from them. It has traditionally been hard to generate actionable custom metrics from your ephemeral resources such as Lambda functions, and containers. With this launch, you do not have to rely on complex architecture or multiple third party tools to gain insights into these environments. By sending your logs in the new Embedded Metric Format, you can now easily create custom metrics without having to instrument or maintain separate code, while gaining powerful analytical capabilities on your log data.  

There are several benefits of this new feature. You can embed custom metrics alongside detailed log event data, and CloudWatch will automatically extract the custom metrics so you can visualize and alarm on them, for real-time incident detection. Additionally, the detailed log events associated with the extracted metrics can be queried using CloudWatch Logs Insights to provide deep insights into the root causes of operational events.

# Deploying sample application

A sample serverless application has been defined in (template.yml)[./template.yml].  This application is a Python function that returns a JSON payload of a lottery winner and the amount won.

The first step is to *build* the application including any dependencies.

```bash
sam build --use-container
```

Once the application has been bundled, it can be deployed by using the following command:

```bash
sam deploy --guided
```

# Examining custom metrics

Once the application has been deployed, it can be tested with an empty payload.  

```bash
export STACK_NAME=whatever_you_specified_during_guided_deploy
export FUNCTION=$(aws cloudformation describe-stack-resource --stack-name ${STACK_NAME} --logical-resource-id RandomWinnerFunction --query "StackResourceDetail.PhysicalResourceId" --output text)
aws lambda invoke \
    --function-name ${FUNCTION} \
    --payload '{ }' \
    response.json
```

The return value is stored in the file `response.json`.  This can be repeated any number of times to generate a function invocation.

The log group can be identified by running the following command.  Once identified, you can view the Log Streams in the AWS Console.  The Log Streams will contain the data emitted from the function handler `handler` in the file `index.py`.

```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/${STACK_NAME}" --query "logGroups[*].logGroupName" --output text
```

Sample data:

```bash
{
    "LogGroup": "random-winner-RandomWinnerFunction-UME6DVT4CLAW",
    "ServiceName": "random-winner-RandomWinnerFunction-UME6DVT4CLAW",
    "ServiceType": "AWS::Lambda::Function",
    "service": "payout_service",
    "Player": "Adam",
    "RequestId": "80308025-291a-437a-92d7-c073d132dac3",
    "executionEnvironment": "AWS_Lambda_python3.6",
    "memorySize": "128",
    "functionVersion": "$LATEST",
    "logStreamId": "2020/04/21/[$LATEST]2054349ab30a4bb6b196d94f8c74c82c",
    "_aws": {
        "Timestamp": 1587458198751,
        "CloudWatchMetrics": [
            {
                "Dimensions": [
                    [
                        "LogGroup",
                        "ServiceName",
                        "ServiceType",
                        "service"
                    ]
                ],
                "Metrics": [
                    {
                        "Name": "PayoutAmount",
                        "Unit": "Sum"
                    }
                ],
                "Namespace": "Lottery"
            }
        ]
    },
    "PayoutAmount": 97
}
```

You can view the custom data in the CloudWatch Metrics panel under the namespace **Lottery**.

![CloudWatch Metrics Custom Namespace](images/metrics-namespaces.png)

This is made possible through the use of EMF in [index.py](./src/index.py).  The metric and property values are emitted in the log and ingested as metrics.

```bash
...
...
    metrics.set_namespace('Lottery')
    metrics.put_dimensions({'service':'payout_service'})
    metrics.put_metric('PayoutAmount', random_number, 'Sum')
    metrics.set_property('Player', random_winner)
    metrics.set_property('RequestId', context.aws_request_id)
...
...
```