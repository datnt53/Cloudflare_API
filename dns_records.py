import CloudFlare
import json


def get_dns_record(email, api_token, zone_id):
    cf = CloudFlare.CloudFlare(email=email, token=api_token)
    dns_records = cf.zones.dns_records(zone_id)
    jsonfile = open("dns_records.json", "w")
    jsonfile.write(json.dumps(dns_records, indent=4))
    jsonfile.close()
    return dns_records


def create_dns_record(email, api_token, zone_id, **kwargs):
    cf = CloudFlare.CloudFlare(email=email, token=api_token)
    dns_datas = [
        {
            'name': kwargs['domain'].split('.')[0] + '1',
            'type': kwargs['type'],
            'content': kwargs['target'],
            'proxied': True
        }
    ]

    for dns in dns_datas:
        try:
            dns_records = cf.zones.dns_records.post(zone_id, data=dns)
            print('Creating DNS Records - {name}: DONE'.format(name=dns_records['name']))
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            print('API Error: {error}'.format(error=e))
