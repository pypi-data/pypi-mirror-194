Cloudhealth REST Client
=======================

This is a Python REST Client for the Cloudhealth service.

## Installation

```shell
pip install cloudhealth-client

# Clone repo
git clone https://github.com/albertonarro/cloudhealth-client.git
```


## Python Usage

```python
>>> from cloudhealth import client
>>> ch = client.CloudHealth(api_key='Ali23melAS$E#@$Im3lsim1!')

# List all queryable assets
>>> ch.assets.list()
['AwsInstanceType', 'AwsAvailabilityZone', 'AwsAccount', ... ]

# List Reports of Specific Type
>>> ch.reports.list_by_type('cost')
{
  'links': {
    'cost/billing_rules': {'href': 'https://chapi.cloudhealthtech.com/olap_reports/cost/billing_rules'}, 
    'cost/current': {'href': 'https://chapi.cloudhealthtech.com/olap_reports/cost/current'}, 
    ...
    ...
  }
}
```


## Testing

[!WIP]

## Contributions..

[!WIP]
