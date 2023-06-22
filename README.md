# device-template-detail
Generates a list of all Device Templates with their corresponding Feature Templates from vManage

## Install and Run

> git clone https://github.com/dbrown92700/device-template-detail

> cd device-template-detail

> pip install -r requirements.txt

> python3 main.py

Script will prompt the user for the vManage address and a username and password (hidden).

There is an option to include or exclude Default Device Templates.  If you exclude them, default templates that are attached will still be included.

Enter the vManage address as a domain name or IP address.  The script will use port 443 by default to specify a different port, use the format:
> address:port
