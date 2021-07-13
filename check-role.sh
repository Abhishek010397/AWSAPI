#!/bin/bash 

echo "RoleName: $1";
echo "ACCOUNTID: $2";
echo "PolicyName: $3";


get_role_arn=$(aws iam get-role --role-name $1 | grep Arn | awk '{print $2}' | sed 's/\(.*\),/\1 /' | sed 's/"//g') 
if [ $get_role_arn == "arn:aws:iam::$2:role/$1" ] 
then 
  policies=$(aws iam list-attached-role-policies --role-name $1 | grep PolicyName | awk '{print$2}' | sed 's/\(.*\),/\1 /' | sed 's/"//g')
  for policy in $policies
  do 
    if [ $policy == $3 ] 
    then 
      echo " $policy Matched "
      get_policy_arn=$(aws iam list-attached-role-policies --role-name $1 --query "AttachedPolicies[?PolicyName=='$policy'].PolicyArn" | sed 's/[][]//g' | sed 's/^[[:space:]]*//g' | sed 's/"//g' | tr -d "\n" ) 
      policy_version_id=$(aws iam get-policy --policy-arn $get_policy_arn | grep DefaultVersionId | awk '{print $2}' | sed 's/\(.*\),/\1 /' | sed 's/"//g') 
      get_policy_document=$(aws iam get-policy-version --policy-arn $get_policy_arn --version-id $policy_version_id )
      echo "Policy Document"
      echo  $get_policy_document
    fi 
  done 
else
  echo "$1 doesn't exists" 
fi 