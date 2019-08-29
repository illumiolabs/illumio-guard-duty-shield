# Illumio Guard Duty Shield

[![Slack](images/slack.svg)](http://slack.illumiolabs.com)
[![License](images/license.svg)](LICENSE)

**Project Description**

This repo contains the lambda function code that can leverage AWS GuardDuty findings to prevent
malicious IPs and domains from accessing your AWS hosted applications by using threat intel
from the GuardDuty findings and using it to complement Illumio policy rules

**Project Technology stack**

The AWS lambda function is written in python3.6 and uses the same runtime in AWS Lambda
For more details on python3.6 runtime - please visit https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html


**Project workflow**

![](images/guard-duty-workflow.jpg)


## Installation

Detailed instructions on how to install, configure, and get the project running are mentioned
in [INSTALL](INSTALL.md) document.

## Support

The AWS Lambda Function is released and distributed as open source software subject to the
[LICENSE](LICENSE). Illumio has no obligation or responsibility related to the AWS Lambda
Function with respect to support, maintenance, availability, security or otherwise. Please
read the entire [LICENSE](LICENSE) for additional information regarding the permissions and
limitations. You can engage with the author & contributors team and community on SLACK.

## Help or Docs

If you have questions, please use slack for asking them.
If you have issues, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Contributing

Instructions on how to contribute:  [CONTRIBUTING](CONTRIBUTING.md).

## Links

 * Screencast showing the Lambda working https://labs.illumio.com
 * Illumio documentation page for configuring Illumio ASP https://support.illumio.com/public/documentation/index.html
