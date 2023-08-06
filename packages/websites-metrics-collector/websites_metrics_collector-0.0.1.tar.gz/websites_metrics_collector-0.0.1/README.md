[![CircleCI](https://circleci.com/gh/antoniodimariano/websites_metrics_collector/tree/master.svg?style=svg&circle-token=809ef5a8af2efd28ede2d0385c31666146570ac5)](https://circleci.com/gh/antoniodimariano/websites_metrics_collector/tree/master)
# Websites Metrics Collector

#### Author: Antonio Di Mariano - antonio.dimariano@gmail.com

# Description

This service is part of the Websites Monitoring Application, a small distributed application that periodically produces and collects metrics about the availability of one or more websites.
This service is responsible for fetching and collecting the information from a list of URLs. The information collected is

* HTTP Status returned
* HTTP response time
* regexp pattern that is expected to be found on the HTML content

For each record, a message is produced to an Apache Kafka Topic. This service exposes a REST API Service with a `POST`
method to accept a list of URLs to fetch and process.


## Infra Requirements

This service requires an Apache Kafka Broker with the Schema Registry and AVRO support. 
In the `terraform` directory you will find the necessary scripts to create a token and a schema registry on Aiven ( https://aiven.com )

If you want to automate the creation of topics and schemas, you can use Terraform. Otherwise, you can do it yourself from the console.

### Steps to follow to use terraform:

1. Install terraform (https://www.terraform.io/downloads.html)
2. Edit the terraform.tfvars. You will need an API key from the Aiven console. Please follow instructions in https://help.aiven.io/en/articles/2059201-authentication-tokens to paste into the terraform.tfvars file. 

then run 
```shell
$ terraform init
$ terraform plan
$ terraform apply
```

("init" sets up the working directory and downloads the Aiven provider, "plan" shows you what changes will be made and "apply" actually makes the changes.)
For the full documentation of Aiven Terraform go https://github.com/aiven/terraform-provider-aiven/blob/master/docs/index.md. 
Go here for a lot of examples https://github.com/aiven/terraform-provider-aiven/tree/master/examples


###  Manually create your own Avro Schema


The default topic `websites_metrics` has the following schemas 

`websites_metrics-values`

```json
{
    "type": "record",
    "name": "example",
    "namespace": "example",
    "fields": [
        {
            "type": "string",
            "name": "url",
            "doc": "The checked URL"
        },
        {
            "type": "int",
            "name": "http_status",
            "doc": "The HTTP status "
        },
        {
            "type": "float",
            "name": "elapsed_time",
            "doc": "The elapsed_time of the request "
        },
        {
            "type": "boolean",
            "name": "pattern_verified",
            "doc": ""
        }
    ],
    "doc": "example"
}
```

`websites_metrics-key`

```json
{
    "doc": "example",
    "fields": [
        {
            "name": "service_name",
            "type": "string"
        }
    ],
    "name": "example",
    "namespace": "example",
    "type": "record"
}
```



# Requirements

* Python >=3.8

# Run

If you want to run from the source code, go to the directory websites_metrics_collector and run `python main`

If you want to use it as package (suggested method) install pip3 install websites_metrics_collector

Then

1. Set the ENV variables as show in this README.md
2. Then use it this way

```python
def start_service():
    from websites_metrics_collector.main import start
    start()
```


# Dependencies

* requests==2.26.0
* confluent-kafka-producers-wrapper==0.0.6  ( More information on https://github.com/antoniodimariano/confluent_kafka_producers_wrapper )
* aiohttp==3.7.4.post0

# Run test

**NOTE**: for simplicity, I am assuming you have a running Kafka broker for testing purposes


`python -m unittest tests/test_driver_class.py`

`python -m unittest test/test_fetching_info_from_websites.py`

`python -m unittest test/test_kafka_producer.py`

`python -m unittest test/test_patterns_in_text.py`

`python -m unittest test/test_rest_server.py`

**NOTE** In order to run the `test_rest_api` you have to start the service first



## Rest APIs

# Method to get metrics from a list of URLs a

* **POST http://SERVER\_URI:SERVER\_PORT/api/v1/websites_metrics**

### Header Fields

| HEADER FIELD  | VALUE                                                                                    |
|---------------|------------------------------------------------------------------------------------------|
| Content-Type  | Required. application/json                                                               |

### Payload Fields

A concatenated list with the following format
`[['http://urltofetch.com'],['optional 1st pattern to verify in the html','optional 2nd pattern to verify in the html',''optional Nth pattern to verify in the html']]`

Example

```json
[
  [
    "http://cloudbased.me",
    [
      "Microservices",
      "Antonio"
    ]
  ],
  [
    "http://ferrari.com",
    [
      "ferrari",
      "italia"
    ]
  ]
]
```

### Responses

* HTTP Status Code : 201

```json
{
  "urls": [
    [
      "http://cloudbased.me",
      [
        "Microservices",
        "Antonio"
      ]
    ],
    [
      "http://ferrari.com",
      [
        "ferrari",
        "italia"
      ]
    ]
  ],
  "submitted": true
}
```

* HTTP Status Code : 400 Bad or Wrong payload

Response:

```json
{
  "message": "Bad format! You need to send me a list of URLS [['http://urltofetch.com'],['optional 1st pattern to verify in the html','optional 2nd pattern to verify in the html',''optional Nth pattern to verify in the html']]. See the example.",
  "example": [
    [
      "http://cloudbased.me",
      [
        "Microservices",
        "Antonio"
      ]
    ],
    [
      "http://ferrari.com",
      [
        "ferrari",
        "italia"
      ]
    ],
    [
      "http://motoguzzi.com",
      [
        "italia"
      ]
    ]
  ]
}
```

* HTTP Status Code : 403 An error occurred.

Response

```json
{
  "message": "An Error occurred and the request or the payload cannot be processed. =..= No squealing, remember that it's all in your head =..="
}
```


# Service ENV configuration

If you are using a Broker that uses `SSL`, like Aiven.com, you need to download the following certificates files and
copy them to a folder

* Access Key
* Access Certificate
* CA Certificate

for more information about SSL and Kafka please read https://docs.confluent.io/3.0.0/kafka/ssl.html

| ENV Variable  | VALUE | DESCRIPTION                                                                       |
|---------------|------|------------------------------------------------------------------------------------|
| SERVICE_HOST    | string   | Optional. The hostname where to bind the REST server. The default value is `0.0.0.0`  |
| SERVICE_LISTEN_PORT    | string   | Optional. The port where to bind the REST server. The default value is `8080`  |
| brokers    | string   | Required. The FQDN of the Apache Kafka Brokers.|
| schema_registry    | string   | Required. The FQDN of the Service Registry.|
| ssl_ca_location    | string   | Required. he relative path to your ca.pem|
| ssl_certificate_location    | string   | Required. The relative path to your service.cert|
| ssl_key_location    | string   | Required. The relative path to your service.key |
| security_protocol    | string   | Required. SSL.|
| topic_for_producing_metrics    | string   | Optional. The Kafka Avro Topic where to produce messages to. The default value is `websites_metrics` |
| logging_level    | string   | Optional. The level of logging to use for the built-in `logging` package. The default is `logging.INFO`  |

**Example of mandatory ENV variables to use**

* brokers=kafka-xxx-yyy-abc.com:12026
* schema_registry=https://user:password@kafka-xxx-yyy-abc.com:12029
* ssl_ca_location=configuration/ca.pem
* ssl_certificate_location=configuration/service.cert
* ssl_key_location=configuration/service.key
* security_protocol=SSL
* persistence_conf=postgres://user:password@mydbhost.com:12024/metrics?sslmode=require

If your broker requires SASL authentication, like Confluent Cloud, these are the ENV variables to include

| ENV Variable  | VALUE | DESCRIPTION                                                                       |
|---------------|------|------------------------------------------------------------------------------------|
| SERVICE_HOST    | string   | Optional. The hostname where to bind the REST server. The default value is `0.0.0.0`  |
| SERVICE_LISTEN_PORT    | string   | Optional. The port where to bind the REST server. The default value is `8080`  |
| brokers    | string   | Required. The FQDN of the Apache Kafka Brokers.|
| schema_registry    | string   | Required. The FQDN of the Service Registry.|
| sasl_username    | string   | Required. YOUR USERNAME HERE|
| sasl_password    | string   | Required. YOUR PASSWORD HERE|
| schema_registry_basic_auth_user_info    | string   | Required. AUTH HERE |
| schema_registry_basic_auth_credentials_source    | string   | Required. USER_INFO.|
| sasl_mechanisms    | string   | Required. PLAIN.|
| security_protocol    | string   | Required. SASL_SSL.|
| persistence_conf    | string   | Required. The full string for connecting to your PostgreSQL database.|
| topic_for_producing_metrics    | string   | Optional. The Kafka Avro Topic where to produce messages to. The default value is `websites_metrics` |
| logging_level    | string   | Optional. The level of logging to use for the built-in `logging` package. The default is `logging.INFO`  |
