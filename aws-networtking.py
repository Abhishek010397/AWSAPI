from re import T
import boto3
import argparse
import json
import datetime

client = boto3.client('ec2', region_name='us-east-1')


def converter(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"{type(obj)} not datetime")

def describe_vpc(vpc_id):
    try:
        response = client.describe_vpcs(
            VpcIds=[vpc_id]
            )
        json_object = json.dumps(response, default=converter)
        loads = json.loads(json_object)
        VpcId=loads['Vpcs'][0]['VpcId']
        if(VpcId == vpc_id):
            print(VpcId+' exists')
    except Exception as e:
        print(e)

def describe_subnets(subnet_id1,subnet_id2,subnet_id3,vpc_id):
    try:
        response=client.describe_subnets(
            SubnetIds=[
                subnet_id1,
                subnet_id2,
                subnet_id3
            ]
        )
        json_object = json.dumps(response, default=converter)
        loads = json.loads(json_object)
        Subnets=loads['Subnets']
        for subnet in Subnets:
            VpcId=subnet['VpcId']
            if (VpcId == vpc_id):
                subnet_id=subnet['SubnetId']
                print(subnet_id+' Matched for existing '+VpcId)
                print('\n')
    except Exception as e:
        print(e)


def main():
    parser = argparse.ArgumentParser(
        prog='CHECK NETWORKING', description='Preflight-Checks-For-Networking', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-id', '--vpc-id', type=str,
                        help='RoleName', required=True)
    parser.add_argument('-sid1','--subnet-id1',type=str,help='Subnet-ID1',required=True)
    parser.add_argument('-sid2', '--subnet-id2', type=str,help='Subnet-ID2', required=True)
    parser.add_argument('-sid3', '--subnet-id3', type=str,help='Subnet-ID3', required=True)
    args = parser.parse_args()

    describe_vpc(args.vpc_id)
    describe_subnets(args.subnet_id1,args.subnet_id2,args.subnet_id3,args.vpc_id)


if __name__ == "__main__":
    main()
