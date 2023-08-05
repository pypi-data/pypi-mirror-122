# python-comanage-api

Provide a limited Python 3 implementation of COmanage REST API v1: [https://spaces.at.internet2.edu/display/COmanage/REST+API+v1](https://spaces.at.internet2.edu/display/COmanage/REST+API+v1)

## Table of contents

- [TL;DR](#tldr)
- [API endpoints](#endpoints)
- [Usage](#usage)
- [SSH Key Authenticator Plugin in COmanage](#sshplugin)
- [References](#reference)

## <a name="tldr"></a>TL;DR

Install the latest version from PyPi

```console
pip install fabric-comanage-api
```

Create a COmanage API connection

```python
from comanage_api import ComanageApi

api = ComanageApi(
    co_api_url=COMANAGE_API_URL,
    co_api_user=COMANAGE_API_USER,
    co_api_pass=COMANAGE_API_PASS,
    co_api_org_id=COMANAGE_API_CO_ID,
    co_api_org_name=COMANAGE_API_CO_NAME,
    co_ssh_key_authenticator_id=COMANAGE_API_SSH_KEY_AUTHENTICATOR_ID
)
```

Get some data! (example using `cous_view_all()`)

```python
$ python
Python 3.9.6 (v3.9.6:db3ff76da1, Jun 28 2021, 11:49:53)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import json
>>> from comanage_api import ComanageApi
>>> api = ComanageApi(
...     co_api_url='https://FQDN_OF_REGISTRY',
...     co_api_user='co_123.api-user-name',
...     co_api_pass='xxxx-xxxx-xxxx-xxxx',
...     co_api_org_id='123',
...     co_api_org_name='RegistryName',
...     co_ssh_key_authenticator_id='123'
... )
>>> print(json.dumps(api.cous_view_all(), indent=4))
{
    "ResponseType": "Cous",
    "Version": "1.0",
    "Cous": [
        {
            "Version": "1.0",
            "Id": "38",
            "CoId": "3",
            "Name": "enrollment-approval",
            "Description": "Enrollment Approval Personnel - can approve or deny new registry members",
            "Lft": "66",
            "Rght": "67",
            "Created": "2021-09-10 14:33:11",
            "Modified": "2021-09-10 14:33:11",
            "Revision": "0",
            "Deleted": false,
            "ActorIdentifier": "http://cilogon.org/serverA/users/242181"
        },
        {
            "Version": "1.0",
            "Id": "39",
            "CoId": "3",
            "Name": "impact-users",
            "Description": "ImPACT Users - Registering with the ImPACT site will add new user's to this group",
            "Lft": "68",
            "Rght": "69",
            "Created": "2021-09-10 14:44:09",
            "Modified": "2021-09-10 14:44:09",
            "Revision": "0",
            "Deleted": false,
            "ActorIdentifier": "http://cilogon.org/serverA/users/242181"
        }
    ]
}
```

## <a name="endpoints"></a>API endpoints

Return types based on implementation status of wrapped API endpoints

- Implemented:
    - `--> dict`: Data is returned as a Python [Dictionary](https://docs.python.org/3/c-api/dict.html) object
    - `--> bool`: Success/Failure is returned as Python [Boolean](https://docs.python.org/3/c-api/bool.html) object
- Not Implemented: 
    - `--> dict`: raise exception (`HTTPError - 501 Server Error: Not Implemented for url: mock://not_implemented_501.local`)
    - `--> bool`: raise exception (`HTTPError - 501 Server Error: Not Implemented for url: mock://not_implemented_501.local`)

- ### [COU API](https://spaces.at.internet2.edu/display/COmanage/COU+API)
    - add: `cous_add(name: str, description: str, parent_id=None) -> dict`
    - delete: `cous_delete(cou_id: int) -> bool`
    - edit: `cous_edit(cou_id: int, name=None, description=None, parent_id=None) -> bool`
    - view all (per co): `cous_view_all() -> dict`
    - view one: `cous_view_one(cou_id: int) -> dict`

    **NOTE**: `cous_edit` has a special case where setting `parent_id=0` will reset the value of the `parent_id` of the COU to be None (have no parent)

- ### [CoPerson API](https://spaces.at.internet2.edu/display/COmanage/CoPerson+API)
    - add (not implemented): `copeople_add() -> dict`
    - delete (not implemented): `copeople_delete() -> bool`
    - edit (not implemented): `copeople_edit() -> bool`
    - find (not implemented): `copeople_find() -> dict`
    - match: `copeople_match(given=None, family=None, mail=None, distinct_by_id=True) -> dict`
    - view all (per co): `copeople_view_all() -> dict`
    - view all (per identifier): `copeople_view_per_identifier(identifier: str, distinct_by_id=True) -> dict`
    - view one: `copeople_view_one(coperson_id: int) -> dict`

- ### [CoPersonRole API](https://spaces.at.internet2.edu/display/COmanage/CoPersonRole+API)
    - add: `copersonroles_add(coperson_id: int, cou_id: int, status=None, affiliation=None) -> dict`
    - delete: `copersonroles_delete(copersonrole_id: int) -> bool`
    - edit: `copersonroles_edit(copersonrole_id: int, coperson_id=None, cou_id=None, status=None, affiliation=None) -> bool`
    - view all: `copersonroles_view_all() -> dict`
    - view all (per co_person): `copersonroles_view_per_coperson(coperson_id: int) -> dict`
    - view all (per cou): `copersonroles_view_per_cou(cou_id: int) -> dict`
    - view one: `copersonroles_view_one(copersonrole_id: int) -> dict`
    
    **NOTE**: when provided, valid values for `status` and `affiliation` as follows:

    ```python
    STATUS_OPTIONS = ['Active', 'Approved', 'Confirmed', 'Declined', 'Deleted', 'Denied', 'Duplicate', 
    'Expired', 'GracePeriod', 'Invited', 'Pending', 'PendingApproval', 'PendingConfirmation', 'Suspended']
    AFFILIATION_OPTIONS = ['affiliate', 'alum', 'employee', 'faculty', 'member', 'staff', 'student']
    ```

- ### [Identifier API](https://spaces.at.internet2.edu/display/COmanage/Identifier+API)
    - add (not implemented): `identifiers_add() -> dict`
    - assign (not implemented): `identifiers_assign() -> bool`
    - delete (not implemented): `identifiers_delete() -> bool`
    - edit (not implemented): `identifiers_edit() -> bool`
    - view all: `identifiers_view_all() -> dict`
    - view per entity: `identifiers_view_per_entity(entity_type: str, entity_id: int) -> dict`
    - view one: `identifiers_view_one(identifier_id: int) -> dict`

    **NOTE**: when provided, valid values for `entity_type` as follows:

    ```python
    ENTITY_OPTIONS = ['codeptid', 'cogroupid', 'copersonid', 'organizationid', 'orgidentityid']
    ```

- ### [Name API](https://spaces.at.internet2.edu/display/COmanage/Name+API)
    - add (not implemented): `names_add() -> dict`
    - delete (not implemented): `names_delete() -> bool`
    - edit (not implemented): `names_edit() -> bool`
    - view all: `names_view_all() -> dict`
    - view per person: `names_view_per_person(person_type: str, person_id: int) -> dict`
    - view one: `names_view_one(name_id: int) -> dict`

    **NOTE**: when provided, valid values for `person_type` as follows:

    ```python
    PERSON_OPTIONS = ['copersonid', 'orgidentityid']
    ```

- ### [SshKey API](https://spaces.at.internet2.edu/display/COmanage/SshKey+API) (**REQUIRES**: The [SSH Key Authenticator plugin](https://spaces.at.internet2.edu/display/COmanage/SSH+Key+Authenticator+Plugin) which manages SSH Public Keys for CO People.)
    - add (not working): `ssh_keys_add(coperson_id: int, ssh_key: str, key_type: str, comment=None, ssh_key_authenticator_id=None) -> dict`
    - delete: `ssh_keys_delete(ssh_key_id: int) -> bool`
    - edit: `ssh_keys_edit(ssh_key_id: int, coperson_id=None, ssh_key=None, key_type=None, comment=None, ssh_key_authenticator_id=None) -> bool`
    - view all: `ssh_keys_view_all() -> dict`
    - view all (per co_person): `ssh_keys_view_per_coperson(coperson_id: int) -> dict`
    - view one: `ssh_keys_view_one(ssh_key_id: int) -> dict`

    **NOTE**: when provided, valid values for `ssh_key_type` as follows:

    ```python
    SSH_KEY_OPTIONS = ['ssh-dss', 'ecdsa-sha2-nistp256', 'ecdsa-sha2-nistp384', 
    'ecdsa-sha2-nistp521', 'ssh-ed25519', 'ssh-rsa', 'ssh-rsa1']
    ```

    
**DISCLAIMER: The code herein may not be up to date nor compliant with the most recent package and/or security notices. The frequency at which this code is reviewed and updated is based solely on the lifecycle of the project for which it was written to support, and is not actively maintained outside of that scope. Use at your own risk.**



## <a name="usage"></a>Usage

Set up a virtual environment (`virtualenv` is used in these examples)

```console
virtualenv -p /usr/local/bin/python3 venv
source venv/bin/activate
```

### Install supporting packages

Install from PyPi

```console
pip install fabric-comanage-api
```

**OR** 

Install for Local Development

```console
pip install -r requirements.txt
```

### Configure your environment

Create a `.env` file from the included template if you don't want to put the API credentials in your code. Example code makes use of [python-dotenv](https://pypi.org/project/python-dotenv/)

```console
cp template.env .env
```

Configure `.env` based on your COmanage Registry settings

```env
# COmanage API user and pass
COMANAGE_API_USER=co_123.api-user-name
COMANAGE_API_PASS=xxxx-xxxx-xxxx-xxxx
# COmanage CO Information
COMANAGE_API_CO_NAME=RegistryName
COMANAGE_API_CO_ID=123
# COmanage registry URL
COMANAGE_API_URL=https://FQDN_OF_REGISTRY
# COmanage SshKeyAuthenticatorId
COMANAGE_API_SSH_KEY_AUTHENTICATOR_ID=123
```

### Example Code

See code in [examples](examples/) for a demonstration of how to use each endpoint

## <a name="sshplugin"></a>SSH Key Authenticator Plugin


The [SSH Key Authenticator plugin](https://spaces.at.internet2.edu/display/COmanage/SSH+Key+Authenticator+Plugin) manages SSH Public Keys for CO People.

- The SSH Key Authenticator plugin is available as of Registry v3.3.0. Prior to this version, SSH Key management is available via the CO Person canvas.

After registration you can find the value for `COMANAGE_API_SSH_KEY_AUTHENTICATOR_ID` in the URL for editing the Authenticator:

- It would be **3** in this example URL: [https://registry.cilogon.org/registry/authenticators/edit/3]()

### Adding a new SSH Key Authenticator in COmanage

To create a new SSH Key Authenticator first select the "Authenticators" option from the COmanage configuraiton page

![](./imgs/SshKeyAuthenticator_1.png)

Next select the "Add Authenticator" option

![](./imgs/SshKeyAuthenticator_2.png)

Populate the required fields and set Status to "Active" and "Add" the Authenticator

![](./imgs/SshKeyAuthenticator_3.png)

Upon success a green box will denote the new Authenticator has been added

![](./imgs/SshKeyAuthenticator_4.png)

Now when choosing the "Authenicators" option from the COmanage configuration page you should see your newly created Authenticator

![](./imgs/SshKeyAuthenticator_5.png)

Pressing the "Edit" option will display the fields for the Authenticator along with its `SshKeyAuthenticatorId` value in the URL (**3** in this example)

![](./imgs/SshKeyAuthenticator_6.png)

## <a name="reference"></a>References

- COmanage REST API v1: [https://spaces.at.internet2.edu/display/COmanage/REST+API+v1](https://spaces.at.internet2.edu/display/COmanage/REST+API+v1)
- COU API: [https://spaces.at.internet2.edu/display/COmanage/COU+API](https://spaces.at.internet2.edu/display/COmanage/COU+API)
- CoPerson API: [https://spaces.at.internet2.edu/display/COmanage/CoPerson+API](https://spaces.at.internet2.edu/display/COmanage/CoPerson+API)
- CoPersonRole API: [https://spaces.at.internet2.edu/display/COmanage/CoPersonRole+API](https://spaces.at.internet2.edu/display/COmanage/CoPersonRole+API)
- Identifier API: [https://spaces.at.internet2.edu/display/COmanage/Identifier+API](https://spaces.at.internet2.edu/display/COmanage/Identifier+API)
- Name API: [https://spaces.at.internet2.edu/display/COmanage/Name+API](https://spaces.at.internet2.edu/display/COmanage/Name+API)
- SsHKey API: [https://spaces.at.internet2.edu/display/COmanage/SshKey+API](https://spaces.at.internet2.edu/display/COmanage/SshKey+API)
- SSH Key Authenticator Plugin: [https://spaces.at.internet2.edu/display/COmanage/SSH+Key+Authenticator+Plugin](https://spaces.at.internet2.edu/display/COmanage/SSH+Key+Authenticator+Plugin)
- PyPi: [https://pypi.org](https://pypi.org)
