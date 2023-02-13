import boto3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--access-key', help='AWS access key ID')
parser.add_argument('-s', '--secret-key', help='AWS secret access key')
parser.add_argument('-r', '--region', help='AWS default region name')
parser.add_argument('-o', '--output', help='Output file to save the results')
args = parser.parse_args()

route53 = boto3.client('route53',
                      aws_access_key_id=args.access_key,
                      aws_secret_access_key=args.secret_key,
                      region_name=args.region)

response = route53.list_hosted_zones()

hosted_zone_ids = [hosted_zone['Id'] for hosted_zone in response['HostedZones']]

if args.output:
    output_file = open(args.output, 'w')

for hosted_zone_id in hosted_zone_ids:
    record_set_response = route53.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    for record_set in record_set_response['ResourceRecordSets']:
        name = record_set['Name']
        if name[-1] == '.':
            name = name[:-1]
        if args.output:
            output_file.write(name + '\n')
        print(name)

if args.output:
    output_file.close()
