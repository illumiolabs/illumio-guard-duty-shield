# Install instructions for Illumio Guard Duty Shield
Illumio has provided two deployment methods, either as a container using
the included Dockerfile, or as a .zip file. These instructions are intended for
a Unix-type system, such as Linux or macOS.

## Docker Container
These instructions require that [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git),
[Docker](https://docs.docker.com/engine/install/),
and the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
be installed locally.
1. Clone the illumio-guard-duty-shield repository and navigate to the directory
```bash
git clone https://github.com/illumiolabs/illumio-guard-duty-shield.git
cd ./illumio-guard-duty-shield
```
2. Build the docker image
```bash
docker build -t illumio-guard-duty-shield:latest -f src/Docker/Dockerfile .
```
3. Create a new ECR repo and push the image. Substitute your accountID and region where required
```bash
aws ecr create-repository --region <region> --repository-name illumio-guard-duty-shield --image-scanning-configuration scanOnPush=true
docker tag illumio-guard-duty-shield:latest <accountID>.dkr.ecr.<region>.amazonaws.com/illumio-guard-duty-shield:latest
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <accountID>.dkr.ecr.<region>.amazonaws.com
docker push <accountID>.dkr.ecr.<region>.amazonaws.com/illumio-guard-duty-shield:latest
```
4. You can automate the final steps by using the included CloudFormation template
to complete the following steps:
    1. Edit the src/Docker/illumio-Guard-Duty-Shield-Docker.yaml file with your relevant variables and then use CloudFormation to create the Illumio Guard Duty Shield Lambda function
    ```bash
    aws cloudformation deploy --template-file src/Docker/illumio-Guard-Duty-Shield-Docker.yaml --stack-name illumio-guard-duty-shield --capabilities CAPABILITY_NAMED_IAM
    ```
5. Otherwise, you may log in to AWS and continue with the AWS Web UI
6. Navigate to the AWS Lambda service and click the orange **Create function** button in the top right corner
7. Select **Container image** to deploy a container-based Lambda function
8. Provide a Function Name, such as `Illumio-Guard-Duty-Shield`
9. Enter the Container image URI you pushed earlier
```bash
<accountID>.dkr.ecr.<region>.amazonaws.com/illumio-guard-duty-shield:latest
```
10. Click **Create Function** at the bottom right
11. You will be directed to the *Illumio-Guard-Duty-Shield*'s Function overview page
12. Select the **Configuration** tab towards the bottom of the page, and then **Environment variables**
13. Create the following Environmental variables by clicking **Edit** and **Add environment variable**
  * ILLUMIO_SERVER - The Illumio PCE hostname (ex. illumiopce.company.com)
  * ILO_API_KEY_ID - The API key id
  * ILO_API_KEY_SECRET - The API key secret
  * ILO_API_VERSION - Version of Illumio API
  * ILO_ORG_ID - Illumio PCE Org ID to be utilized for this deployment
  * ILO_PORT - Illumio PCE port
  * THREAT_LIST_KEY - Numerical href id of the IP list to be updated. It is found in the URL as seen in [this image](images/threat-list-key.jpg)
14. Once you have added values for each of these variables, click the orange **Save** button at the bottom right
15. We will need to create a CloudWatch Rule for this, so navigate to the AWS CloudWatch service
16. On the left side of the screen click **Rules** under Events
17. Click **Create rule** and under Event Source select GuardDuty as the Sevice Name
18. Click **Add target** to the right, and select **Illumio-Guard-Duty-Shield** as the Lambda Function
19. Click **Configure details** at the bottom right of the page and
20. Provide a Rule Name, such as `IllumioGuardDutyRule` and click **Create rule**
21. If you return to the Illumio-Guard-Duty-Shield Lambda function we created earlier, you will see an EventBridge (CloudWatch Events) has been added to the triggers.


## .zip File
These instructions require that [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
and [pip3](https://pip.pypa.io/en/stable/installation/) are installed locally.

1. Clone the illumio-guard-duty-shield repository and navigate to the app subdirectory
```bash
git clone https://github.com/illumiolabs/illumio-guard-duty-shield.git
cd ./illumio-guard-duty-shield/src/app
```
2. Install the requests package to a subdirectory with pip
```bash
pip3 install requests --target ./package
```
3. Navigate to the package subdirectory, create a .zip file in the zip folder
containing the package folder contents, then add the lambda_function.py to the
.zip file, and return to the root directory.
```bash
cd ./package
zip -r ../src/zip/illumio-guard-duty-shield.zip .
cd ../src/app/
zip -g ../zip/illumio-guard-duty-shield.zip lambda_function.py
```
4. You can automate the final steps by using the included CloudFormation template
and an S3 bucket to complete the following steps:
    1. If necessary, create an S3 bucket
    ```bash
    aws s3api create-bucket --bucket <globally unique bucket name> --region <region> --create-bucket-configuration LocationConstraint=<region>
    ```
    2. Upload the zip file to your S3 bucket
    ```bash
    aws s3 cp src/zip/illumio-guard-duty-shield.zip s3://<globally unique bucket name>/
    ```
    3. Edit the src/zip/illumio-Guard-Duty-Shield.yaml file with your relevant variables
    and then use CloudFormation to create the Illumio Guard Duty Shield Lambda function
    ```bash
    aws cloudformation deploy --template-file src/zip/illumio-Guard-Duty-Shield.yaml --stack-name illumio-guard-duty-shield --capabilities CAPABILITY_NAMED_IAM
    ```
5. Otherwise, you may log in to AWS and continue with the AWS Web UI
6. Navigate to the AWS Lambda service and click the orange **Create function** button in the top right corner
7. Select **Author from scratch** to deploy from a .zip file
8. Provide a Function Name, such as `Illumio-Guard-Duty-Shield`
9. Click **Create Function** at the bottom right
10. Within "Code source" panel click **Upload from** and select **Upload a .zip file**
11. Click **Upload** and choose the illumio-guard-duty-shield.zip file created in the src/zip folder
12. Next, click the **Configuration** tab, and then **Environment variables**
13. Create the following Environmental variables by clicking **Edit** and **Add environment variable**
* ILLUMIO_SERVER - The Illumio PCE hostname (ex. illumiopce.company.com)
* ILO_API_KEY_ID - The API key id
* ILO_API_KEY_SECRET - The API key secret
* ILO_API_VERSION - Version of Illumio API
* ILO_ORG_ID - Illumio PCE Org ID to be utilized for this deployment
* ILO_PORT - Illumio PCE port
* THREAT_LIST_KEY - Numerical href id of the IP list to be updated. It is found in the URL as seen in [this image](images/threat-list-key.jpg)
14. Once you have added values for each of these variables, click the orange **Save** button at the bottom right
