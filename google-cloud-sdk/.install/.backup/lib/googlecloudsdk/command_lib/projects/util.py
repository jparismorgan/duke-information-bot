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

"""Common utility functions for all projects commands."""

from googlecloudsdk.core import resources


PROJECTS_COLLECTION = 'cloudresourcemanager.projects'
PROJECTS_API_VERSION = 'v1'


def ParseProject(project_id):
  # Override the default API map version so we can increment API versions on a
  # API interface basis.
  registry = resources.REGISTRY.Clone()
  registry.RegisterApiByName('cloudresourcemanager', PROJECTS_API_VERSION)
  return registry.Parse(project_id, collection=PROJECTS_COLLECTION)


def ProjectsUriFunc(resource):
  ref = ParseProject(resource.projectId)
  return ref.SelfLink()
