#   Copyright 2022 Illumio, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import os
import requests

# PCE API request call using requests module
def pce_request(pce, org_id, key, secret, verb, path, params=None,
                data=None, json=None, extra_headers=None):
    base_url = os.path.join(pce, 'orgs', org_id)
    headers = {
              'user-agent': 'aws-lambda-quarantine',
              'accept': 'application/json',
            }
    # Request Payload
    print(json)
    response = requests.request(verb,
                                os.path.join(base_url, path),
                                auth=(key, secret),
                                headers=headers,
                                params=params,
                                json=json,
                                data=data)
    return response


# Extracting the malicious IP from GuardDuty findings of type
# UnauthorizedAccess:EC2/SSHBruteForce and Recon:EC2/PortProbeUnprotectedPort
def get_malicious_ip(event):
    malicious_ips = []
    if event.get('source') == 'aws.guardduty':
        if event.get('detail').get('type') == 'UnauthorizedAccess:EC2/SSHBruteForce':
            if event.get('detail').get('service').get('action').get('networkConnectionAction').get('remoteIpDetails').get('ipAddressV4') is not None:
                malicious_ip = event.get('detail').get('service').get('action').get('networkConnectionAction').get('remoteIpDetails').get('ipAddressV4')
                print('Malicious IP is ' + str(malicious_ip))
                malicious_ips.append(malicious_ip)
        elif event.get('detail').get('type') == 'Recon:EC2/PortProbeUnprotectedPort':
            print(event.get('detail').get('service').get('additionalInfo').get('threatListName'))
            if event.get('detail').get('service').get('action').get('portProbeAction').get('portProbeDetails') is not None:
                for portProbes in event.get('detail').get('service').get('action').get('portProbeAction').get('portProbeDetails'):
                    malicious_ip = portProbes['remoteIpDetails']['ipAddressV4']
                    malicious_ips.append(malicious_ip)
    print(malicious_ips)
    return malicious_ips


# Updating the Illumio threat list based on the malicious IP
# intel received from GuardDuty findings
def update_illumio_policies(malicious_ips):
    # Getting the data from environment variables for the PCE API request
    pce_api = int(os.environ['ILO_API_VERSION'])
    pce = os.path.join('https://' + os.environ['ILLUMIO_SERVER'] + ':' + os.environ['ILO_PORT'], 'api', 'v%d' % pce_api)
    org_id = os.environ['ILO_ORG_ID']
    key = 'api_' + os.environ['ILO_API_KEY_ID']
    secret = os.environ['ILO_API_KEY_SECRET']
    ip_list = os.environ['THREAT_LIST_KEY']
    ip_list_href = 'sec_policy/draft/ip_lists/' + str(ip_list)
    response = pce_request(pce, org_id, key, secret, 'GET', ip_list_href).json()
    print('Received the following IP List from Illumio PCE')
    print(response)
    pce_ip_list = []
    for ip_obj in response['ip_ranges']:
        pce_ip_list.append(ip_obj.get('from_ip', None))
        pce_ip_list.append(ip_obj.get('to_ip', None))
    for ip in malicious_ips:
        exclude_ip = {
            'from_ip': ip,
            'exclusion': True
        }
        if exclude_ip not in response['ip_ranges'] and exclude_ip['from_ip'] not in pce_ip_list:
            response['ip_ranges'].append(exclude_ip)
        else:
            print('This IP is duplicate and will not be added - ' + exclude_ip['from_ip'])
    request_body = {
        'name': response['name'],
        'description': response['description'],
        'ip_ranges': response['ip_ranges']
    }
    resp = pce_request(pce, org_id, key, secret, 'PUT',
                       ip_list_href, json=request_body)
    # Printing the response
    print(resp.status_code)
    if resp.status_code == 204:
        policy_href = '/orgs/' + str(org_id) + ip_list_href
        body = {
            "update_description": "Adding IPs to threat list",
            "change_subset": {
                              "ip_lists": [{
                                            "href": policy_href
                                          }]
            }
        }
        res = pce_request(pce, org_id, key, secret, 'POST', 'sec_policy', json=body)
        print(res.status_code)
        return res.status_code
    else:
        return resp.status_code


# Lambda handler for getting findings and invoking Illumio PCE API calls
def lambda_handler(event, context):
    print('Shield AWS Environment using Illumio and AWS Guard Duty')
    malicious_ips = []
    malicious_ip_list = []
    malicious_ip_list = get_malicious_ip(event)
    for ip in malicious_ip_list:
        if ip not in malicious_ips:
            malicious_ips.append(ip)
    status = update_illumio_policies(malicious_ips)
    return {
        'statusCode': status,
        'body': malicious_ips
    }
