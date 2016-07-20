#!/bin/bash -ex

# Deployed to jpalbeza @ 6152-5215-1637

SOURCE_DIR=`pwd`
LAMBDA_ARN=IcicleSearch
ZIP_FILE=${LAMBDA_ARN}.zip
S3_BUCKET=lambda.us-west-2.icicle.doobi.com

# Operate in a temporary directory
TMP_DIR=`mktemp -d`
trap "rm -rf $TMP_DIR" EXIT
pushd $TMP_DIR
trap "popd" EXIT

cp -Rpf $SOURCE_DIR/* .

# Install dependencies onto pwd
pip install -r requirements.txt -t .

# Create the delivery zip file. This package contains the handler and all dependencies.
rm -f $ZIP_FILE
zip -r $ZIP_FILE *

# Upload to S3
aws s3 cp $ZIP_FILE s3://$S3_BUCKET

# Update the lambda with this new code
aws lambda update-function-code --function-name $LAMBDA_ARN --s3-bucket $S3_BUCKET --s3-key $ZIP_FILE
