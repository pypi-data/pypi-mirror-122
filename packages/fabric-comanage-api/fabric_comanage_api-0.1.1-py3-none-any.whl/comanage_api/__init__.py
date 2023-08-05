import requests_mock
from requests import Session

# fabric-comanage-api version
__VERSION__ = "0.1.1"


class ComanageApi(object):
    """
    fabric-comanage-api:

    Provide a limited Python 3 client implementation (wrapper) for
    COmanage REST API v1: https://spaces.at.internet2.edu/display/COmanage/REST+API+v1


    Attributes
    ----------
    co_api_url: str
        COmanage registry URL (required)
    co_api_user: str
        COmanage API username (required)
    co_api_pass: str
        COmanage API password (required)
    co_api_org_id: int
        COmanage Org ID (required)
    co_api_org_name: str
        COmanage Org Name (required)
    co_ssh_key_authenticator_id: int = None
        SSH Authenticator Plugin ID (optional)

    """

    def __init__(self, co_api_url: str, co_api_user: str, co_api_pass: str, co_api_org_id: int,
                 co_api_org_name: str, co_ssh_key_authenticator_id: int = None):
        # COmanage API user and pass
        self._CO_API_USER = str(co_api_user)
        self._CO_API_PASS = str(co_api_pass)
        # COmanage CO information
        self._CO_API_ORG_NAME = str(co_api_org_name)
        self._CO_API_ORG_ID = int(co_api_org_id)
        # COmanage Registry URL
        if str(co_api_url).endswith('/'):
            self._CO_API_URL = str(co_api_url)[:-1]
        else:
            self._CO_API_URL = str(co_api_url)
        # COmanage SshKeyAuthenticatorId
        if co_ssh_key_authenticator_id:
            self._CO_SSH_KEY_AUTHENTICATOR_ID = int(co_ssh_key_authenticator_id)
        else:
            self._CO_SSH_KEY_AUTHENTICATOR_ID = 0
        # Status Type options
        self.STATUS_OPTIONS = ['Active', 'Approved', 'Confirmed', 'Declined', 'Deleted', 'Denied', 'Duplicate',
                               'Expired',
                               'GracePeriod', 'Invited', 'Pending', 'PendingApproval', 'PendingConfirmation',
                               'Suspended']
        # Affiliation Type options
        self.AFFILIATION_OPTIONS = ['affiliate', 'alum', 'employee', 'faculty', 'member', 'staff', 'student']
        # Entity Type options
        self.ENTITY_OPTIONS = ['codeptid', 'cogroupid', 'copersonid', 'organizationid', 'orgidentityid']
        # Person Type options
        self.PERSON_OPTIONS = ['copersonid', 'orgidentityid']
        # SSH Key Type options
        self.SSH_KEY_OPTIONS = ['ssh-dss', 'ecdsa-sha2-nistp256', 'ecdsa-sha2-nistp384', 'ecdsa-sha2-nistp521',
                                'ssh-ed25519', 'ssh-rsa', 'ssh-rsa1']
        # create mock response session
        self._mock_session = Session()
        self._adapter = requests_mock.Adapter()
        self._mock_session.mount('mock://', self._adapter)
        # add mock adapters
        self._MOCK_501_URL = 'mock://not_implemented_501.local'
        self._adapter.register_uri('GET', self._MOCK_501_URL, reason='Not Implemented', status_code=501)
        # create comanage_api session
        self._s = Session()
        self._s.auth = (self._CO_API_USER, self._CO_API_PASS)

    # Import COmanage API endpoint methods
    from ._copeople import copeople_add, copeople_delete, copeople_edit, copeople_find, copeople_match, \
        copeople_view_all, copeople_view_per_identifier, copeople_view_one
    from ._copersonroles import copersonroles_add, copersonroles_delete, copersonroles_edit, copersonroles_view_all, \
        copersonroles_view_per_coperson, copersonroles_view_per_cou, copersonroles_view_one
    from ._cous import cous_add, cous_delete, cous_edit, cous_view_all, cous_view_one
    from ._identifiers import identifiers_add, identifiers_assign, identifiers_delete, identifiers_edit, \
        identifiers_view_all, identifiers_view_per_entity, identifiers_view_one
    from ._names import names_add, names_delete, names_edit, names_view_all, names_view_per_person, names_view_one
    from ._sshkeys import ssh_keys_add, ssh_keys_delete, ssh_keys_edit, ssh_keys_view_all, ssh_keys_view_per_coperson, \
        ssh_keys_view_one
