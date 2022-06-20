import CloudFlare
import json


def get_firewall_rules(email, api_token, zone_id):
    cf = CloudFlare.CloudFlare(email=email, token=api_token)
    fw_rules = cf.zones.firewall.rules.get(zone_id)
    jsonfile = open("firewall_rules.json", "w")
    jsonfile.write(json.dumps(fw_rules, indent=4))
    jsonfile.close()
    return fw_rules


def create_firewall_rules(email, api_token, zone_id, **kwargs):
    cf = CloudFlare.CloudFlare(email=email, token=api_token)

    # Get Priority of last rule
    fw_rules = cf.zones.firewall.rules.get(zone_id)
    id_last = fw_rules[len(fw_rules)-1]['id']
    priority_last = fw_rules[len(fw_rules)-1]['priority']

    # Update Priority of Last Rule
    pri_data = [
        {
            "id": id_last,
            "priority": priority_last + 1000
        }
    ]
    update_fw_rules = cf.zones.firewall.rules.patch(zone_id, data=pri_data)

    # Create new Rules
    firewall_data = [
        {
            "action": "block",
            "paused": False,
            "priority": priority_last,
            "description": "Block Bot Subdomain " + kwargs['domain'].split('.')[0].upper(),
            "filter": {
                'expression': "(http.host eq \"" + kwargs['domain'] + "\" "
                              "and cf.bot_management.score le 10 "
                              "and not cf.bot_management.verified_bot)",
                "paused": False
            }
        },
        {
            "action": "managed_challenge",
            "paused": False,
            "priority": priority_last + 500,
            "description": "Challenge BOT Subdomain " + kwargs['domain'].split('.')[0].upper(),
            "filter": {
                "expression": "(http.host eq \"" + kwargs['domain'] + "\" "
                              "and cf.bot_management.score gt 10 "
                              "and cf.bot_management.score le 29)",
                "paused": False
            }
        }
    ]

    for firewall in firewall_data:
        # Convert to list format
        firewall_lst = [firewall]

        # POST Request to create Rule
        try:
            firewall_rules = cf.zones.firewall.rules.post(zone_id, data=firewall_lst)
            print('Creating Firewall Rules - {name}: DONE'.format(name=firewall_rules[0]['description']))
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            print('API Error: {error}'.format(error=e))
