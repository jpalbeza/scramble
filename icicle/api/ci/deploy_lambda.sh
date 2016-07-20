#!/bin/bash -e

LAMBDA_ARN=$1
SOURCE_DIR=`pwd`
LAMBDA_NAME=IcicleSearch
ZIP_FILE=${LAMBDA_NAME}.zip
S3_BUCKET=s3://lambda.us-west-2.icicle.doobi.com

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
aws s3 cp $ZIP_FILE $S3_BUCKET

# Update the lambda with this new code
aws lambda update-function-code --function-name $LAMBDA_ARN --s3-bucket $S3_BUCKET --s3-key $S3_BUCKET/$ZIP_FILE
