import boto3
from .automl import AWS_ACC_KEY_ID, AWS_SEC_ACC_KEY, AWS_REGION_NAME
import time
from botocore.exceptions import ClientError

client_ecs = boto3.client('ecs',
						aws_access_key_id=AWS_ACC_KEY_ID,
						aws_secret_access_key=AWS_SEC_ACC_KEY,
						region_name=AWS_REGION_NAME)

def get_servicesArns_of_cluster(cluster_name):
	while True:
		try:
			return client_ecs.list_services(cluster=cluster_name)['serviceArns']
		except ClientError:
			time.sleep(1)
			pass

def get_service(cluster_name, service_name):
	while True:
		try:
			return client_ecs.describe_services(cluster=cluster_name, services=[service_name])['services'][0]
		except ClientError:
			time.sleep(1)
			pass

def get_max_instances(cluster_name, service_name):
	# TODO: IMPLEMENT
	return 5

def update_service_desiredCount(cluster_name, service_name, desiredCount):
	while True:
		try:
			client_ecs.update_service(cluster=cluster_name, service=service_name, desiredCount=desiredCount)
			break
		except ClientError:
			time.sleep(1)
			pass

def drain_instance(cluster_name, instance_id):
	instances_arns = client_ecs.list_container_instances(cluster=cluster_name)['containerInstanceArns']
	container_instances = client_ecs.describe_container_instances(cluster=cluster_name, containerInstances=instances_arns)['containerInstances']
	for container_instance in container_instances:
		if container_instance['ec2InstanceId'] == instance_id:
			container_instance_arn = container_instance['containerInstanceArn']
			client_ecs.update_container_instances_state(cluster=cluster_name, containerInstances=[container_instance_arn], status='DRAINING')
			break

def activate_instance(cluster_name, instance_id):
	instances_arns = client_ecs.list_container_instances(cluster=cluster_name)['containerInstanceArns']
	container_instances = client_ecs.describe_container_instances(cluster=cluster_name, containerInstances=instances_arns)['containerInstances']
	for container_instance in container_instances:
		if container_instance['ec2InstanceId'] == instance_id:
			container_instance_arn = container_instance['containerInstanceArn']
			client_ecs.update_container_instances_state(cluster=cluster_name, containerInstances=[container_instance_arn], status='ACTIVE')
			break

def run_model_deployment(version_id, model_uri):
	response = client_ecs.run_task(
	    launchType='FARGATE',
	    cluster='arn:aws:ecs:eu-west-3:749868801319:cluster/FargateCluster',
		    networkConfiguration={
		        'awsvpcConfiguration': {
		            'subnets': [
		                'subnet-60c56d09',
		            ],
		            'securityGroups': [
		                'sg-ffec8896',
		            ],
		            'assignPublicIp': 'ENABLED'
		        }
		    },
		    overrides={
		        'containerOverrides': [
		            {
		                'name': 'main',
		                'environment': [
		                    {
		                        'name': 'MODEL_URI',
		                        'value': str(model_uri)
		                    },
		                    {
		                        'name': 'VERSION_ID',
		                        'value': str(version_id)
		                    },
		                ],
		            },
		        ],
		    },
		    referenceId='testing-fargate-task-1',
		    taskDefinition='sagemaker_deploy'
		)
	return response['ResponseMetadata']['HTTPStatusCode']

### DEPRECATED ######
def update_flask_service_instances(service, num_instances, cluster_name):
	num_instances = min(num_instances, 20)
	num_instances = max(num_instances, 0)
	print(f"update_flask_service_instances : INFO : Requesting {num_instances} for service {service}...")
	try:
		response = client_ecs.update_service(
			cluster=cluster_name,
			service=service,
			desiredCount=int(num_instances),
			forceNewDeployment=True
		)
	except Exception:
		return False
	return True

def get_service_instaces_status(cluster, service_name):
	print(f"get_service_instaces_status : INFO : Getting info of service {service_name} (cluster {cluster})...")
	try:
		response = client_ecs.describe_services(cluster=cluster, services=[service_name])
		service = response['services'][0]
		desired = service['desiredCount']
		running = service['runningCount']
		return desired, running
	except:
		return 0, 0

def services_ready(cluster, service_list):
	response = client_ecs.describe_services(cluster=cluster, services=service_list)
	services = response['services']
	for service in services:
		name    = service['serviceName']
		desired = service['desiredCount']
		running = service['runningCount']
		print(f"services_ready : INFO : Service {name}: Desired = {desired}, Running = {running}")
		if desired != running:
			return False
	return True

def create_cluster(cluster_name):
	response = client_ecs.create_cluster(clusterName=cluster_name)

def create_task_definition(task_definition_name, ecr_image):
	response = client_ecs.register_task_definition(
	    family=task_definition_name,
	    taskRoleArn='arn:aws:iam::749868801319:role/ecsTaskExecutionRole',
	    executionRoleArn='arn:aws:iam::749868801319:role/ecsTaskExecutionRole',
	    networkMode='bridge',
	    containerDefinitions=[
	        {
	            'name': 'CONTAINER',
	            'image': ecr_image,
	            'cpu': 0,
	            'memory': 6144,
	            'portMappings': [
	                {
	                    'containerPort': 5000,
	                    'hostPort': 5000,
	                    'protocol': 'tcp'
	                },
					{
	                    'containerPort': 5555,
	                    'hostPort': 5555,
	                    'protocol': 'tcp'
	                }
	            ],
	            'essential': True,
	            'workingDirectory': '/'
	        },
	    ],
	    requiresCompatibilities=[
	        'EC2',
	    ],
	    cpu='2000',
	    memory='6144'
	)
	if int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
		print(f'create_task_definition : INFO : Created TaskDefinition {task_definition_name}!')
		return str(response['taskDefinition']['taskDefinitionArn'])
	else:
		print(f'create_task_definition : ERROR : Could not create TaskDefinition {task_definition_name}!')
		return False

def create_service(cluster, serviceName, taskDefinition, targetGroupArn):
	response = client_ecs.create_service(
	    cluster=cluster,
	    serviceName=serviceName,
	    taskDefinition=taskDefinition,
	    loadBalancers=[
	        {
	            'targetGroupArn': targetGroupArn,
	            'containerName': 'CONTAINER',
	            'containerPort': 5000
	        },
	    ],
	    desiredCount=0,
	    launchType='EC2',
	    role='arn:aws:iam::749868801319:role/ecsServiceRole',
	    deploymentConfiguration={
	        'maximumPercent': 200,
	        'minimumHealthyPercent': 0
	    },
	    placementStrategy=[
	        {
	            'type': 'binpack',
	            'field': 'memory'
	        },
	    ],
	    healthCheckGracePeriodSeconds=2147483646,
	    schedulingStrategy='REPLICA',
	    enableECSManagedTags=True
	)
	return int(response['ResponseMetadata']['HTTPStatusCode']) == 200
