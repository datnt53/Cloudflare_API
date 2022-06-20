import CloudFlare
import json


def get_spectrums(email, api_token, zone_id):
    cf = CloudFlare.CloudFlare(email=email, token=api_token)
    spectrums = cf.zones.spectrum.apps.get(zone_id)
    jsonfile = open("spectrums.json", "w")
    jsonfile.write(json.dumps(spectrums, indent=4))
    jsonfile.close()
    return spectrums


def create_spectrums(email, api_token, zone_id, dns_name, **kwargs):
    cf = CloudFlare.CloudFlare(email=email, token=api_token)
    spectrum_datas = [
        {
            'dns': {
                'type': kwargs['type'],
                'name': kwargs['domain']
            },
            'origin_dns': {
                'name': dns_name
            },
            'protocol': 'tcp/443',
            'origin_port': 443,
            'ip_firewall': False,
            'proxy_protocol': 'off',
            'tls': 'off',
            'traffic_type': 'https',
            'edge_ips': {
                'type': 'dynamic',
                'connectivity': 'all'
            }
        }
    ]

    for spectrum in spectrum_datas:
        try:
            spectrums = cf.zones.spectrum.apps.post(zone_id, data=spectrum)
            print('Creating Spectrum - {name}: DONE'.format(name=spectrums['dns']['name']))
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            print('API Error: {error}'.format(error=e))
