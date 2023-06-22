#!python
# Generates a list of device templates with their feature templates

from vmanage_api import VmanageRestApi
from getpass import getpass


def feature_list(json_data, indent):

    for feature in json_data:
        file.write(f'{"   " * indent}{feature["templateType"]}: {feature_template_names[feature["templateId"]]}\n')
        if 'subTemplates' in list(feature.keys()):
            file.write(f'{"   "*(indent+1)}Subtemplates:\n')
            feature_list(feature['subTemplates'], indent+1)


file = open('TemplateList.txt', 'w')

vmanage_ip = input('Input vManage address in the format {name or ip}:{port}  : ')
vmanage_user = input('Input vManage user name: ')
vmanage_password = getpass('Input vManage password: ')
include_defaults = False
if input('Type "yes" to include default templates with no devices attached: ') == 'yes':
    include_defaults = True

vmanage = VmanageRestApi(vmanage_ip, vmanage_user, vmanage_password)
if vmanage.token:
    print('\nvManage Login Success\n')

feature_templates = vmanage.get_request('/template/feature')['data']
feature_template_names = {}
for template in feature_templates:
    feature_template_names[template['templateId']] = template['templateName']

device_templates = vmanage.get_request('/template/device')['data']

for template in device_templates:
    if template['factoryDefault'] and not include_defaults and (template['devicesAttached'] == 0):
        continue
    print(f'{template["templateName"]} : {template["devicesAttached"]} Devices Attached')
    file.write(f'{template["templateName"]} : {template["devicesAttached"]} Devices Attached\n')
    if template['configType'] == 'template':
        template_definition = vmanage.get_request(f'/template/device/object/{template["templateId"]}')
        feature_list(template_definition['generalTemplates'], 1)
    else:
        file.write('   CLI Template\n')

vmanage.logout()
file.close()
