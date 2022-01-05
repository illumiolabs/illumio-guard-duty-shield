# Illumio Guard Duty Shield

[![Slack](images/slack.svg)](http://slack.illumiolabs.com)
[![License](images/license.svg)](LICENSE)

**Project Description**

This repo provides an AWS Lambda function designed to monitor
AWS GuardDuty for malicious IPs, and import them into an Illumio PCE IP list.
This allows Illumio customers to prevent malicious IPs and domains from accessing
AWS-hosted applications by using threat intel from GuardDuty findings to
complement Illumio policy rules.

**Project Technology stack**

The application is written for Python 3.6+ and is designed to be run as an AWS Lambda function.
For more details on packging Lambda functions please visit https://docs.aws.amazon.com/lambda/latest/dg/lambda-functions.html

**Project workflow**

![](images/guard-duty-workflow.jpg)


## Installation

Detailed instructions on how to quickly deploy the Lambda container are located
in the [INSTALL](INSTALL.md) document.

## Support

The AWS Lambda container is released and distributed as open source software subject to the
[LICENSE](LICENSE). Illumio has no obligation or responsibility related to the AWS Lambda
container with respect to support, maintenance, availability, security or otherwise. Please
read the entire [LICENSE](LICENSE) for additional information regarding the permissions and
limitations. You can engage with the author & contributors team and community on SLACK.

## Help or Docs

If you have questions, please use slack for asking them.
If you have issues, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Contributing

Instructions on how to contribute:  [CONTRIBUTING](CONTRIBUTING.md).

## Links

 * Illumio documentation page for configuring Illumio ASP https://support.illumio.com/public/documentation/index.html
