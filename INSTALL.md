# Install instructions for Illumio Guard Duty Shield
Illumio has provided several deployment methods, the easiest of which is with the
included AWS Cloudformation yaml template. You can also choose to install this via
the AWS Management Console.

## CloudFormation
This template will create an IAM role with minimal permissions, a Lambda function
with the Illumio Guard Duty Shield container, and  CloudWatch Event rule.

You must first have the AWS CLI installed on your local system.
[Click here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
for install instructions.

You can deploy these configurations from the repository's root with this command:

```console
aws cloudformation deploy --template-file src/illumio-Guard-Duty-Shield.yaml --stack-name illumio-guard-duty-shield --capabilities CAPABILITY_NAMED_IAM
```

## AWS Management Console
If you wish to click through the install, instructions are included below.

1. Navigate to the AWS Lambda service and click the orange **Create function** button in the top right corner
1. Select **Container image** to deploy a container-based Lambda function
1. Provide a Function Name, such as `Illumio-Guard-Duty-Shield`
1. Enter the Illumio Guard Duty Shield Container image URI:
   `{URI_PLACEHOLDER}`
1. Click **Create Function** at the bottom right
1. You will be directed to the *Illumio-Guard-Duty-Shield*'s Function overview page
1. Select the **Configuration** tab towards the bottom of the page, and then **Environment variables**
1. Create the following Environmental variables by clicking **Edit** and **Add environment variable**
   * ILLUMIO_SERVER - Value should be the Illumio PCE URL without any https
   * ILO_API_KEY_ID - The API key id for the Lambda function to use
   * ILO_API_KEY_SECRET - The API key secret for the Lambda function to use
   * ILO_API_VERSION - Version of Illumio API
   * ILO_ORG_ID - Illumio PCE Org ID to be utilized for this deployment
   * ILO_PORT - Illumio PCE port for the Lambda to communicate for the API calls
   * THREAT_LIST_KEY - Numerical Id for the IP list to be updated on the PCE, which can be obtained from the PCE as shown in [this image](images/threat-list-key.jpg)
1. Once you have added values for each of these variables, click the orage **Save** button at he bottom right
1. We will need to create a CloudWatch Rule for this, so navigate to the AWS CloudWatch service
1. On the left side of the screen click **Rules** under Events
1. Click **Create rule** and under Event Source select GuardDuty as the Sevice Name
1. Click **Add target** to the right, and select **Illumio-Guard-Duty-Shield** as the Lambda Function
1. Click **Configure details** at the bottom right of the page and
1. Provide a Rule Name, such as `IllumioGuardDutyRule` and click **Create rule**
1. If you return to the Illumio-Guard-Duty-Shield Lambda function we created earlier, you will see an EventBridge (CloudWatch Events) has been added to the triggers.
