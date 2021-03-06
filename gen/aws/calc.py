def get_spot(name, spot_price):
    if spot_price:
        return '"SpotPrice": "{}",'.format(spot_price)
    else:
        return ''

entry = {
    'default': {
        'resolvers': '["169.254.169.253"]',
        'num_private_slaves': '5',
        'num_public_slaves': '1',
        'master_instance_type': 'm3.xlarge',
        'slave_instance_type': 'm3.xlarge',
        'public_slave_instance_type': 'm3.xlarge',
        'nat_instance_type': 'm3.medium',
        'ip_detect_filename': 'gen/ip-detect/aws.sh',

        # If set to empty strings / unset then no spot instances will be used.
        'master_spot_price': '',
        'slave_spot_price': '',
        'slave_public_spot_price': ''
    },
    'must': {
        'aws_master_spot_price': lambda master_spot_price: get_spot('master', master_spot_price),
        'aws_private_agent_spot_price': lambda slave_spot_price: get_spot('slave', slave_spot_price),
        'aws_public_agent_spot_price':
            lambda slave_public_spot_price: get_spot('slave_public', slave_public_spot_price),
        'aws_region': '{ "Ref" : "AWS::Region" }',
        'exhibitor_explicit_keys': 'false',
        'cluster_name': '{ "Ref" : "AWS::StackName" }',
        'master_discovery': 'master_http_loadbalancer',
        # The cloud_config template variables pertaining to "cloudformation.json"
        'master_cloud_config': '{{ master_cloud_config }}',
        'agent_private_cloud_config': '{{ slave_cloud_config }}',
        'agent_public_cloud_config': '{{ slave_public_cloud_config }}',
        # template variable for the generating advanced template cloud configs
        'cloud_config': '{{ cloud_config }}',
        'oauth_available': 'true',
        'oauth_enabled': '{ "Ref" : "OAuthEnabled" }'
    }
}
