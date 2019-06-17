from __future__ import absolute_import, print_function, unicode_literals
import boto3


def clean_old_lambda_versions(marker = ''):
    client = boto3.client('lambda')
    if marker == '':
    	functions = client.list_functions()
    else:
	functions = client.list_functions(Marker=marker)			
    for function in functions['Functions']:
	#if function['FunctionName'] != "lamda-at-edge-name": #uncomment and replace lamda-at-edge-name with your lambda at edge to ignore lambda at edge 
	  while True:
          	versions = client.list_versions_by_function(FunctionName=function['FunctionArn'])['Versions']
          	if len(versions) == 1:
                	print('{}: done'.format(function['FunctionName']))
              		break
          	for version in versions:
              		if version['Version'] != function['Version']:
                  		arn = version['FunctionArn']
                  		print('delete_function(FunctionName={})'.format(arn))
                  		#client.delete_function(FunctionName=arn)  # uncomment me once you've checked
	#else : #uncomment in-accordance with above if
	#  print('Not lambda')
    if 'NextMarker' in functions:
		clean_old_lambda_versions(functions['NextMarker'])  
        

if __name__ == '__main__':
    clean_old_lambda_versions()
