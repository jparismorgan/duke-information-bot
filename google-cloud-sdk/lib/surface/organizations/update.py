# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command to update an organization."""

import textwrap

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.organizations import flags
from googlecloudsdk.command_lib.organizations import orgs_base
from googlecloudsdk.core import log


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA)
class Update(orgs_base.OrganizationCommand):
  """Update the name of an organization.

  Updates the given organization with new name.

  This command can fail for the following reasons:
      * There is no organization with the given ID.
      * The active account does not have permission to update the given
        organization.

  DEPRECATED: This command is deprecated and will be removed in a future
  release.
  """

  detailed_help = {
      'EXAMPLES': textwrap.dedent("""\
          The following command updates an organization with the ID
          `123456789` to have the name "Foo Bar and Grill":

            $ {command} 123456789 --display_name="Foo Bar and Grill"
    """),
  }

  @staticmethod
  def Args(parser):
    flags.IdArg('you want to update.').AddToParser(parser)
    parser.add_argument('--display-name', required=True,
                        help='New display name for the organization.')

  def Format(self, args):
    return self.ListFormat(args)

  def Run(self, args):
    log.warn(
        'This command is deprecated and will be removed in a future release.')
    service = self.OrganizationsClient()
    org_ref = self.GetOrganizationRef(args.id)
    request = (service.client.MESSAGES_MODULE
               .CloudresourcemanagerOrganizationsGetRequest(
                   organizationsId=org_ref.organizationsId))
    org = service.Get(request)
    org.displayName = args.display_name
    result = service.Update(org)
    log.UpdatedResource(org_ref)
    return result
