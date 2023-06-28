#!python
# Generates a list of device templates with their feature templates

from vmanage_api import VmanageRestApi
from getpass import getpass
from datetime import datetime


# Print all templates in a json policy structure. Calls recursively for sub-policies and indents accordingly
def feature_list(json_data, indent):

    for feature in json_data:
        file.write(f'{"   " * indent}{feature["templateType"]}: {feature_template_names[feature["templateId"]]}\n')
        if 'subTemplates' in list(feature.keys()):
            file.write(f'{"   "*(indent+1)}Subtemplates:\n')
            feature_list(feature['subTemplates'], indent+1)


# Prompt for vManage login details and log in to vManage
vmanage_ip = input('Input vManage address in the format {name or ip}:{port}  : ')
vmanage_user = input('Input vManage user name: ')
vmanage_password = getpass('Input vManage password: ')
include_defaults = False
if input('Type "yes" to include default templates with no devices attached: ') == 'yes':
    include_defaults = True

vmanage = VmanageRestApi(vmanage_ip, vmanage_user, vmanage_password)
if vmanage.token:
    print('\nvManage Login Success\n')
else:
    print('\nLogin issue')
    exit()

# Open file to write to
tm = datetime.now()
file = open(f'TemplateList.{vmanage_ip}.{tm.year}{tm.month:02}{tm.day:02}.{tm.hour:02}{tm.minute:02}.txt', 'w')

# Get feature templates from vManage and create a dictionary of ID's to Names
feature_templates = vmanage.get_request('/template/feature')['data']
feature_template_names = {}
for template in feature_templates:
    feature_template_names[template['templateId']] = template['templateName']

# Get local policy templates from vManage and create a dictionary of ID's to Names
policy_templates = vmanage.get_request('/template/policy/vedge/')['data']
policy_template_names = {}
for policy in policy_templates:
    policy_template_names[policy['policyId']] = policy['policyName']

# Get a list of device templates
device_templates = vmanage.get_request('/template/device')['data']

# Iterate through device templates and create feature list for each
for template in device_templates:
    if template['factoryDefault'] and not include_defaults and (template['devicesAttached'] == 0):
        continue
    print(f'{template["templateName"]} : {template["devicesAttached"]} Devices Attached')
    file.write(f'{template["templateName"]} : {template["devicesAttached"]} Devices Attached\n')
    if template['configType'] == 'template':
        template_definition = vmanage.get_request(f'/template/device/object/{template["templateId"]}')
        try:
            file.write(f'   Local Policy: {policy_template_names[template_definition["policyId"]]}\n')
        except KeyError:
            file.write('   Local Policy: none\n')
        feature_list(template_definition['generalTemplates'], 1)
    else:
        file.write('   CLI Template\n')

# Clean up
vmanage.logout()
file.close()
