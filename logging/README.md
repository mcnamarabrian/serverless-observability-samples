# logging

You can use [Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) to monitor, store, and access your log files from Amazon Elastic Compute Cloud (Amazon EC2) instances, AWS CloudTrail, Route 53, and other sources. [AWS Lambda](https://aws.amazon.com/lambda/) and [Amazon API Gateway](https://aws.amazon.com/api-gateway/) have very tight integration with Amazon CloudWatch Logs.

**Note** Your resource needs proper IAM permissions to create CloudWatch Logs Log Groups and Log Streams.


# Best practices

## Use structured logging

There are logging libraries that allow logs to be stored in a structured fashion. Tools like CloudWatch Logs Insights can automatically index the keys in a log message to make them query-able.

## Set a log retention period

CloudWatch Logs are retained indefinitely.  Please configure your rention period to match your business needs. Consider exporting data from CloudWatch Logs to more cost-effective solutions like [Amazon S3](https://aws.amazon.com/s3/) if your business requires long-term retention.

# Analyzing logs

You can use CloudWatch Logs Insights to interactively search and analyze your log data. You can perform queries to help you more efficiently and effectively respond to operational issues. CloudWatch Logs Insights includes a purpose-built query language with a few simple but powerful commands. Sample queries are included for several types of AWS service logs, including AWS Lambda.

## Sample queries

### p90 duration of a function

It can be helpful to understand the overall duration of a Lambda function by percentile.  A percentile indicates the relative standing of a value in a dataset.  For example, pct(@duration, 90) returns the @duration value at which 90 percent of the values of @duration are lower than this value, and 10 percent are higher than this value.

```bash
filter @type = "REPORT" | stats avg(@duration), max(@duration), percentile(@duration, 90) by bin(1m)
```
### Average max memory + p90 memory used

It can be useful to understand the amount of memory used during a function's execution.  The query below illustrates how to determine this information in 1min buckets.

```bash
filter @type = "REPORT" | stats avg(@maxMemoryUsed), percentile(@maxMemoryUsed, 90) by bin(1m)
```

### Function timeouts

It can be helpful to know when a function times out.  The query below illustrates the timeouts that occur in bins of 1 minute.

```bash
filter @message like "Task timed out after" | stats count() by bin(1min)
```

### Function cold starts

It can be helpful to know how often cold starts are occurring.  The query below illustrates how to capture function cold starts , warm starts, and associate data in bins of 1 minute.

```bash
filter @type = "REPORT" | parse @message /Init Duration: (?<init>\S+)/ | stats count() - count(init) as warmStarts, count(init) as coldStarts, median(init) as avgInitDuration, max(init) as maxInitDuration, avg(@maxMemoryUsed)/1024/1024 as avgMemoryUsed by bin(5min)
```

# Deploying sample application

The first step is to *build* the application including any dependencies.

```bash
sam build --use-container
```

Once the application has been bundled, it can be deployed by using the following command:

```bash
sam deploy --guided
```
