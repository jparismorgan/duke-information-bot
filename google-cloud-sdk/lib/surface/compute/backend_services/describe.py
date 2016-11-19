# Copyright 2014 Google Inc. All Rights Reserved.
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

"""Command for describing backend services."""

from googlecloudsdk.api_lib.compute import backend_services_utils
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.calliope import base


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Describe(base_classes.GlobalDescriber):
  """Describe a backend service."""

  @staticmethod
  def Args(parser):
    base_classes.GlobalDescriber.Args(parser, 'compute.backendServices')

  @property
  def service(self):
    return self.compute.backendServices

  @property
  def resource_type(self):
    return 'backendServices'


Describe.detailed_help = {
    'brief': 'Describe a backend service',
    'DESCRIPTION': """\
        *{command}* displays all data associated with a backend service in a
        project.
        """,
}


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA)
class DescribeBeta(base_classes.MultiScopeDescriber):
  """Describe a backend service."""

  SCOPES = [base_classes.ScopeType.regional_scope,
            base_classes.ScopeType.global_scope]

  @staticmethod
  def Args(parser):
    base_classes.MultiScopeDescriber.AddScopeArgs(
        parser, 'backendServices', DescribeBeta.SCOPES,
        command='alpha compute backend-services list')

  def CreateReference(self, args):
    default_scope = base_classes.ScopeType.global_scope
    if backend_services_utils.IsRegionDefaultModeWarnOtherwise(
        print_warning=(
            getattr(args, 'global', None) is None and
            getattr(args, 'region', None) is None)):
      default_scope = base_classes.ScopeType.regional_scope
    return super(DescribeBeta, self).CreateReference(
        args, default=default_scope)

  @property
  def global_service(self):
    return self.compute.backendServices

  @property
  def regional_service(self):
    return self.compute.regionBackendServices

  @property
  def zonal_service(self):
    return None

  @property
  def global_resource_type(self):
    return 'backendServices'

  @property
  def regional_resource_type(self):
    return 'regionBackendServices'

  @property
  def zonal_resource_type(self):
    return None


DescribeBeta.detailed_help = base_classes.GetMultiScopeDescriberHelp(
    'backend service', DescribeBeta.SCOPES)
