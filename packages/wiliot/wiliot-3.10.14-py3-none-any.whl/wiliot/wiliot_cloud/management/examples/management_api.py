# """
# Copyright (c) 2016- 2022, Wiliot Ltd. All rights reserved.
#
# Redistribution and use of the Software in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form, except as used in conjunction with
#   Wiliot's Pixel in a product or a Software update for such product, must reproduce
#   the above copyright notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the distribution.
#
#   3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#   may be used to endorse or promote products or services derived from this Software,
#   without specific prior written permission.
#
#   4. This Software, with or without modification, must only be used in conjunction
#   with Wiliot's Pixel or with Wiliot's cloud service.
#
#   5. If any Software is provided in binary form under this license, you must not
#   do any of the following:
#   (a) modify, adapt, translate, or create a derivative work of the Software; or
#   (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#   discover the source code or non-literal aspects (such as the underlying structure,
#   sequence, organization, ideas, or algorithms) of the Software.
#
#   6. If you create a derivative work and/or improvement of any Software, you hereby
#   irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#   royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#   right and license to reproduce, use, make, have made, import, distribute, sell,
#   offer for sale, create derivative works of, modify, translate, publicly perform
#   and display, and otherwise commercially exploit such derivative works and improvements
#   (as applicable) in conjunction with Wiliot's products and services.
#
#   7. You represent and warrant that you are not a resident of (and will not use the
#   Software in) a country that the U.S. government has embargoed for use of the Software,
#   nor are you named on the U.S. Treasury Department’s list of Specially Designated
#   Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#   You must not transfer, export, re-export, import, re-import or divert the Software
#   in violation of any export or re-export control laws and regulations (such as the
#   United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#   and use restrictions, all as then in effect
#
# THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
# OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
# WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
# QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
# IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
# ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
# FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
# (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
# (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
# (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
# (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
# """
"""
 The following code snippet shows how to use pyWiliot for Wiliot's cloud services:
 Please change the owner IDs and tag IDs to match your credentials before running the following code
"""

# Import the library
from wiliot.wiliot_cloud.management.management import *
import os

# Initialise an Wiliot client object
wiliot = ManagementClient(os.environ.get('WILIOT_OAUTH_USERNAME'),
                          os.environ.get('WILIOT_OAUTH_PASSWORD'),
                          'test_owner1')

# Define an owner ID
owner_id = "test_owner1"  # ToDo: add here your owner ID

# Get a list of tags owned by the owner
print(wiliot.get_tags())

# Get a list of applications owned by the owner
print(wiliot.get_applications())

# Get tag_1's  details
print(wiliot.get_tag_details("tag_1"))  # ToDo: add here your tag ID and same as for the rest of the code

# Get a list of applications tag_1 is associated with
print(wiliot.get_associated_apps_to_tag("tag_1"))

# Associate tags: tag_1 and tag_2 with the applications: app_1 and app_2
wiliot.associate_tags(["tag_1", "tag_2"], ["app_1", "app_2"])

# Batch associate tags with applications using a CSV file
# The file should have the following format
# tags_file.csv:
#
# tagId,applicationId
# tag_1,app_1
# tag_1,app_2
# tag_2,app_2
# .....
wiliot.batch_associate_tags("/path/to/tags.csv")

# Disassociate tags: tag_1 and tag_2 from applications app_1 and app_2
wiliot.disassociate_tags(["tag_1", "tag_2"], ["app_1", "app_2"])

# Batch disassociate tags using a CSV file. The file format is the
# same as the format CSV file for batch association
wiliot.batch_disassociate_tags("/path/to/tags.csv")

# Create a label
wiliot.create_label("label_1")

# Add tags to the label
wiliot.add_tags_to_label("label_1", ["tag_1", "tag_2"])

# Remove tags from label
wiliot.remove_tags_from_label("label_1", ["tag_1"])

# Associate a label to an application
wiliot.associate_labels(["label_1"], ["app_1", "app_2"])

# Get a list of applications a label is associated to
wiliot.get_associated_apps_to_label("label_1")

# Disassociate a label from an application
wiliot.disassociate_labels(["label_1"], ["app_1", "app_2"])

# Create an application
# First - create an event policy
event_policy = EventPolicy(policy_name="my-policy", filters=[EventFilter(Event.HERE, confidence=0.5),
                                                             EventFilter(Event.GONE, confidence=0.5),
                                                             EventFilter(Event.BACK, confidence=0.5)])
# Then create the application
wiliot.create_application(app_id='test-application-id',
                          app_name='test_application',
                          event_fields=['eventValue', 'eventName', 'tagId'],
                          event_document="{\"eventName\":\"{{eventName}}\", "
                                         "\"eventValue\":\"{{eventValue}}\", "
                                         "\"tagId\":\"{{tagId}}\"}",
                          http_endpoint=HttpEndpoint(url='https://example.com', headers={'Authorization': 'Basic'},
                                                     method='POST'),
                          event_policy=event_policy)
