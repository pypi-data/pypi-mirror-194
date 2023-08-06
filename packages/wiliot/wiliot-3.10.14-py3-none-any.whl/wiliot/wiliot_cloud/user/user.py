"""
Copyright (c) 2016- 2022, Wiliot Ltd. All rights reserved.

Redistribution and use of the Software in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

  2. Redistributions in binary form, except as used in conjunction with
  Wiliot's Pixel in a product or a Software update for such product, must reproduce
  the above copyright notice, this list of conditions and the following disclaimer in
  the documentation and/or other materials provided with the distribution.

  3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
  may be used to endorse or promote products or services derived from this Software,
  without specific prior written permission.

  4. This Software, with or without modification, must only be used in conjunction
  with Wiliot's Pixel or with Wiliot's cloud service.

  5. If any Software is provided in binary form under this license, you must not
  do any of the following:
  (a) modify, adapt, translate, or create a derivative work of the Software; or
  (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
  discover the source code or non-literal aspects (such as the underlying structure,
  sequence, organization, ideas, or algorithms) of the Software.

  6. If you create a derivative work and/or improvement of any Software, you hereby
  irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
  royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
  right and license to reproduce, use, make, have made, import, distribute, sell,
  offer for sale, create derivative works of, modify, translate, publicly perform
  and display, and otherwise commercially exploit such derivative works and improvements
  (as applicable) in conjunction with Wiliot's products and services.

  7. You represent and warrant that you are not a resident of (and will not use the
  Software in) a country that the U.S. government has embargoed for use of the Software,
  nor are you named on the U.S. Treasury Department’s list of Specially Designated
  Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
  You must not transfer, export, re-export, import, re-import or divert the Software
  in violation of any export or re-export control laws and regulations (such as the
  United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
  and use restrictions, all as then in effect

THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
(SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
(A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
(B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
(C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
"""
from wiliot.wiliot_cloud.api_client import Client, WiliotCloudError


class UserClient(Client):
    
    def __init__(self, oauth_username, oauth_password, owner_id, env='', log_file=None):
        self.client_path = ""
        self.owner_id = owner_id
        super().__init__(oauth_username, oauth_password, env=env, log_file=log_file)
    
    def get_users(self):
        """
        Get all users
        :return: A list of users defined for this owner
        """
        path = "owner/{owner_id}/user".format(owner_id=self.owner_id)
        res = self._get(path)
        return res.get('data', [])
    
    def get_owners(self):
        """
        Get all owners the current user has access to
        :return: a list of dictionaries each with two keys: 'id' and 'name'
        """
        path = "user/owners"
        res = self._get(path)
        return res.get('data', [])
    
    def add_user(self, email=None, user_id=None):
        """
        Add a user to the owner, using either the user's email or an existing user ID.
        If a user with that email doesn't already have an account on Wiliot's system,
        they will get an email inviting them to set their password. Caller should provide
        either an email address or a user_id, not both
        :param email: String - The email used to identify the user
        :param user_id: String - The ID of the user to add -
        :return: True if successful
        """
        assert email is not None or user_id is not None, "Either email or user_id must be provided"
        if email is not None:
            path = "owner/{owner_id}/user".format(owner_id=self.owner_id)
            if email is not None:
                payload = {
                    "user": {
                        "email": email
                    }
                }
        else:
            path = "owner/{owner_id}/user/{user_id}".format(owner_id=self.owner_id, user_id=user_id)
            payload = None
        
        res = self._post(path, payload)
        return res["data"]
    
    def remove_user(self, user_id):
        """
        Remove a user from this owner's account. Calling this function will disable the user's access
        to owner's data via the API but will not delete the user's account
        :param user_id: UUID - identifier for the user to remove. Can be retrieved by calling get_users
        :return: True if successful
        """
        path = "owner/{owner_id}/user/{user_id}".format(owner_id=self.owner_id, user_id=user_id)
        res = self._delete(path)
        return res["data"]
    
    def update_user_roles(self, user_id, roles):
        """
        Update the list of roles applied to the user
        :param user_id: String - The used ID to be modified
        :param roles: List - of roles to apply to the user. Currently, only "editor" and "admin" are supported
        :return: True if successful
        """
        assert isinstance(roles, list), "Expecting a list for parameter roles"
        for role in roles:
            assert role in ["admin", "editor"], "Allowed roles are: 'editor' and 'admin'"
        path = "owner/{owner_id}/user/{user_id}".format(owner_id=self.owner_id, user_id=user_id)
        payload = {
            "roles": roles
        }
        res = self._put(path, payload)
        return res["data"]
    
    def get_account_info(self):
        """
        Get account info
        :return: A dictionary with account info
        """
        path = "owner/{owner_id}/account".format(owner_id=self.owner_id)
        res = self._get(path)
        returned_value = res.get('data', [])
        if isinstance(returned_value, list):
            return returned_value[0]
        else:
            return returned_value
    
    def update_account_info(self, name):
        """
        Update account information. Currently only account name can be changed
        :param name: String - The account's human-readable name
        :return: True if successful
        """
        path = "owner/{owner_id}/account".format(owner_id=self.owner_id)
        payload = {
            'name': name
        }
        res = self._put(path, payload)
        return res["data"]
