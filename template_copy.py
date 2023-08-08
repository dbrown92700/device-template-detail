#!python
# Copies a device template to another device model

from vmanage_api import VmanageRestApi
from getpass import getpass
import json

"""
- List Current templates
- List device models
- Prompt for new template name
- Pull current definition
- Add model to all current feature templates
- Push new definition
"""


def vmanage_login():
    # Prompt for vManage login details and log in to vManage
    vmanage_ip = input('Input vManage address in the format {name or ip}:{port}  : ')
    vmanage_user = input('Input vManage user name: ')
    vmanage_password = getpass('Input vManage password: ')
    vmanage = VmanageRestApi(vmanage_ip, vmanage_user, vmanage_password)
    if vmanage.token:
        print('\nvManage Login Success\n')
        return vmanage
    else:
        print('\nLogin issue')
        exit()


# Print all templates in a json policy structure. Calls recursively for sub-policies and indents accordingly
def features_update(vmanage, json_data, templates, model):

    for feature in json_data:
        for feature_def in templates:
            if feature_def['templateId'] == feature['templateId']:
                if model not in feature_def['deviceType']:
                    feature_def['deviceType'].append(model)
                    updated_temp = {
                        "templateName": feature_def["templateName"],
                        "templateDescription": feature_def["templateDescription"],
                        "templateType": feature_def["templateType"],
                        "deviceType": feature_def["deviceType"],
                        "templateMinVersion": "15.0.0",
                        "templateDefinition": json.loads(feature_def["templateDefinition"]),
                        "factoryDefault": False
                    }
                    url = f'/template/feature/{feature["templateId"]}'
                    update_status = vmanage.put_request(url, updated_temp)
                    print(f'  {feature_def["templateName"]}...{update_status}')
                    continue
                else:
                    print(f'  {feature_def["templateName"]}...no update needed')
                if 'subTemplates' in list(feature.keys()):
                    features_update(vmanage, feature['subTemplates'], templates, model)


if __name__ == '__main__':

    vmanage = vmanage_login()

    # Get a list of device templates
    print('\nTemplates Available:\n-------------------\n')
    device_templates = vmanage.get_request('/template/device')['data']
    for num, device in enumerate(device_templates):
        if device['configType'] == 'template':
            print(f'{num:003}: {device["templateName"]}')
    source_template = input(f'Which template do you want to duplicate: ')

    # Get a list of device templates
    print('\nModels Available:\n----------------\n')
    device_models = vmanage.get_request('/device/models')['data']
    for num, model in enumerate(device_models):
        print(f'{num:003}: {model["displayName"]}')
    target_model_choice = input(f'Which template do you want to duplicate: ')

    target_name = input(f'What do you want to name the new template: ')

    source_template_definition = vmanage.get_request(f'/template/device/object/'
                                                     f'{device_templates[int(source_template)]["templateId"]}')
    target_model = device_models[int(target_model_choice)]['name']

    # Get a list of feature templates and update all feature_templates with target model
    feature_templates = vmanage.get_request(f'/template/feature/')['data']
    print('\nUpdating feature templates with target model.')
    features_update(vmanage, source_template_definition['generalTemplates'], feature_templates, target_model)
    new_template = {
        "templateName": target_name,
        "templateDescription": source_template_definition["templateDescription"],
        "deviceType": target_model,
        "configType": "template",
        "factoryDefault": False,
        "policyId": source_template_definition["policyId"],
        "featureTemplateUidRange": source_template_definition["featureTemplateUidRange"],
        "connectionPreferenceRequired": source_template_definition["connectionPreferenceRequired"],
        "connectionPreference": source_template_definition["connectionPreference"],
        "generalTemplates": source_template_definition["generalTemplates"]
    }
    print('\nPushing new device template.')
    new_template_id = vmanage.post_request('/template/device/feature', new_template)
    print(f'Template {new_template_id} created.')

    vmanage.logout()
    exit()
