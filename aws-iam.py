import boto3
import argparse
import json
import datetime


client = boto3.client('iam')


def converter(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"{type(obj)} not datetime")

def get_role(role_name, policy_name):
    try:
        response = client.get_role(RoleName=role_name)
        json_object = json.dumps(response, default=converter)
        loads = json.loads(json_object)
        RoleName = loads['Role']['RoleName']
        if(RoleName == role_name):
            print('Provided Role '+RoleName+' Exists')
            list_attached_policies(RoleName,policy_name)
        else:
            print(RoleName+" Doesn't Exists")
    except Exception as e:
        print(e)


def list_attached_policies(RoleName, policy_name):
    try:
        existingPolicy=[]
        response = client.list_attached_role_policies(RoleName=RoleName)
        json_object = json.dumps(response, default=converter)
        loads = json.loads(json_object)
        PolicyArn = loads['AttachedPolicies']
        for chunks in PolicyArn:
            policyName = chunks['PolicyName']
            if(policyName == policy_name):
                print('Provided Policy '+policyName+' exists')
            else:
                print(policyName+' Policy exists')
    except Exception as e:
        print(e) 

def main():
    parser = argparse.ArgumentParser(
        prog='CHECK IAM', description='Preflight-Checks', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-r', '--role-name', type=str,
                        help='RoleName', required=True)
    parser.add_argument('-a', '--account-id', type=str,
                        help='ACCOUNTID', required=True)
    parser.add_argument('-p', '--policy-name', type=str,
                        help='PolicyName', required=True)
    args = parser.parse_args()

    get_role(args.role_name, args.policy_name)


if __name__ == "__main__":
    main()
