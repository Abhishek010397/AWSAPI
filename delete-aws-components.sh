#!/bin/bash

delete_loadbalancers() {
    declare -a loadbalancerArn=($(aws elbv2 describe-load-balancers --query "LoadBalancers[?VpcId == '$1'].LoadBalancerArn" --region $2 | sed 's/[][]//g' | sed 's/ *$//g' | sed 's/,/ /g'))
    if [[ ${#loadbalancerArn[@]} > 0 ]]
    then
        echo "Deleting LoadBalancers"
        for ele in ${loadbalancerArn[@]}
        do
        loadbalancer_arn=$(echo $ele | sed -e 's/^"//' -e 's/"$//')
        delete_loadbalancers=$(aws elbv2 delete-load-balancer --load-balancer-arn $loadbalancer_arn --region $2)
        done
    else
        echo "No LoadBalancers Exists"
    fi
}

delete_targetGroups(){
    declare -a targetGroupArn=($(aws elbv2 describe-target-groups --query "TargetGroups[?VpcId == '$1'].TargetGroupArn" --region $2 | sed 's/[][]//g' | sed 's/ *$//g' | sed 's/,/ /g'))
    if [[ ${#targetGroupArn[@]} > 0 ]]
    then
        echo "Deleting TargetGroups"
        for ele in ${targetGroupArn[@]}
        do
        targetgroup_arn=$(echo $ele | sed -e 's/^"//' -e 's/"$//')
        delete_targetGroups=$(aws elbv2 delete-target-group --target-group-arn $targetgroup_arn --region $2)
        done    
    else
        echo "No TargetGroups Exists"
    fi 
}

delete_ec2Instances() {
    declare -a ec2Instances=($(aws ec2 describe-instances --query "Reservations[].Instances[?VpcId == '$1'].InstanceId" --region $2 |  sed 's/[][]//g' | sed 's/,/ /g' | xargs))
    if [[ ${#ec2Instances[@]} > 0 ]]
    then
        echo "Terminating EC2 Instances"
        for instance in ${ec2Instances[@]}
        do
        terminate_instance=$(aws ec2 terminate-instances --instance-ids $instance --region $2)
        done
    else
        echo "No EC2 Instance Exists"
    fi
}


echo "VpcID: $1"
echo "Region: $2"


delete_loadbalancers $1 $2
delete_targetGroups $1  $2
delete_ec2Instances $1  $2
      
