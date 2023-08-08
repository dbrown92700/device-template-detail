# device-template-detail
Includes 2 Scripts
- main.py: Generates a list of all Device Templates with their corresponding Feature Templates from vManage
- template_copy.py: Copies an existing device template to a different device model

## Install and Run

> git clone https://github.com/dbrown92700/device-template-detail

> cd device-template-detail

> pip install -r requirements.txt
## List templates
> python3 main.py

Script will prompt the user for the vManage address and a username and password (hidden).

There is an option to include or exclude Default Device Templates.  If you exclude them, default templates that are attached will still be included.

Enter the vManage address as a domain name or IP address.  The script will use port 443 by default to specify a different port, use the format:
> address:port

## Copy template to new device model
> python3 template_copy.py

- Enter vManage details at the prompts.
- Select source template
- Select target device model
- Choose a unique name for the new device template

The script will add the target device model to all the necessary feature templates and create the new device template.
