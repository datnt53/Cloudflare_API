import CloudFlare
import json
import maskpass
import dns_records
import globals
import spectrums
import firewall_rules


def get_zones(email, api_token):
    cf = CloudFlare.CloudFlare(email=email, token=api_token)
    zone_id = ""
    zone_name = ""
    zones = cf.zones.get()
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
    return zone_id, zone_name


def get_rate_limiting_rules(email, api_token, zone_id):
    cf = CloudFlare.CloudFlare(email=email, token=api_token)
    ratelimit_rules = cf.zones.rate_limits(zone_id)
    jsonfile = open("rate_limiting_rules.json", "w")
    jsonfile.write(json.dumps(ratelimit_rules, indent=4))
    jsonfile.close()
    return ratelimit_rules


def get_page_rules(email, api_token, zone_id):
    cf = CloudFlare.CloudFlare(email=email, token=api_token)
    page_rules = cf.zones.pagerules(zone_id)
    jsonfile = open("page_rules.json", "w")
    jsonfile.write(json.dumps(page_rules, indent=4))
    jsonfile.close()
    return page_rules


def main():
    email = input("Enter Email: ")
    api_token = maskpass.askpass("Enter Token: ")
    zone_info = get_zones(email, api_token)
    globals.init()

    # Backing up all configurations
    dns_records.get_dns_record(email, api_token, zone_info[0])
    spectrums.get_spectrums(email, api_token, zone_info[0])
    firewall_rules.get_firewall_rules(email, api_token, zone_info[0])
    get_rate_limiting_rules(email, api_token, zone_info[0])
    get_page_rules(email, api_token, zone_info[0])

    # Creating DNS Record
    dns_records.create_dns_record(email, api_token, zone_info[0], **globals.DNS_DATA)

    # Creating Spectrum
    spectrums.create_spectrums(email, api_token, zone_info[0], **globals.DNS_DATA)

    # Creating firewall rules
    firewall_rules.create_firewall_rules(email, api_token, zone_info[0], **globals.DNS_DATA)


if __name__ == '__main__':
    main()
