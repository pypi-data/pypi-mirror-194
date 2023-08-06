#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
Test xtesting-db-populate - push on testApi.
'''

import xtesting_db_populate.api

testapi_uri = 'https://testapi'
pod_name = 'pod_test'
project_name = 'project_test'
case_name = 'case_test'

#
# Test pod
#

def test_pod_new_200(mocker, requests_mock):
    """Create a new pod."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_success = mocker.patch('xtesting_db_populate.api.print_success')
    requests_mock.get(f'{testapi_uri}/pods/{pod_name}',
                      status_code=404)
    json_data = {'name': pod_name}
    requests_mock.post(f'{testapi_uri}/pods',
                      json=json_data,
                      status_code=200)
    xtesting_db_populate.api.populate_pod(pod_name, testapi_uri)
    pr_job.assert_called()
    pr_success.assert_called()

def test_pod_new_201(mocker, requests_mock):
    """Create a new pod."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_success = mocker.patch('xtesting_db_populate.api.print_success')
    requests_mock.get(f'{testapi_uri}/pods/{pod_name}',
                      status_code=404)
    json_data = {'name': pod_name}
    requests_mock.post(f'{testapi_uri}/pods',
                      json=json_data,
                      status_code=201)
    xtesting_db_populate.api.populate_pod(pod_name, testapi_uri)
    pr_job.assert_called()
    pr_success.assert_called()

def test_pod_existing(mocker, requests_mock):
    """Skip creation as pod exists."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_skipped = mocker.patch('xtesting_db_populate.api.print_skipped')
    requests_mock.get(f'{testapi_uri}/pods/{pod_name}',
                      status_code=200)
    xtesting_db_populate.api.populate_pod(pod_name, testapi_uri)
    pr_job.assert_called()
    pr_skipped.assert_called()

def test_pod_error_get(mocker, requests_mock):
    """Raise error on getting pod status."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_failed = mocker.patch('xtesting_db_populate.api.print_failed_and_exit')
    requests_mock.get(f'{testapi_uri}/pods/{pod_name}',
                      status_code=500)
    xtesting_db_populate.api.populate_pod(pod_name, testapi_uri)
    pr_job.assert_called()
    pr_failed.assert_called()

def test_pod_error_post(mocker, requests_mock):
    """Raise error on pod creation."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_failed = mocker.patch('xtesting_db_populate.api.print_failed_and_exit')
    requests_mock.get(f'{testapi_uri}/pods/{pod_name}',
                      status_code=404)
    json_data = {'name': pod_name}
    requests_mock.post(f'{testapi_uri}/pods',
                      json=json_data,
                      status_code=500)
    xtesting_db_populate.api.populate_pod(pod_name, testapi_uri)
    pr_job.assert_called()
    pr_failed.assert_called()

#
# Test project
#

def test_project_new(mocker, requests_mock):
    """Create a new project."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_success = mocker.patch('xtesting_db_populate.api.print_success')
    requests_mock.get(f'{testapi_uri}/projects/{project_name}',
                      status_code=404)
    json_data = {'name': project_name}
    requests_mock.post(f'{testapi_uri}/projects',
                      json=json_data,
                      status_code=200)
    xtesting_db_populate.api.populate_project(project_name, testapi_uri)
    pr_job.assert_called()
    pr_success.assert_called()

def test_project_existing(mocker, requests_mock):
    """Skip creation as project exists."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_skipped = mocker.patch('xtesting_db_populate.api.print_skipped')
    requests_mock.get(f'{testapi_uri}/projects/{project_name}',
                      status_code=200)
    xtesting_db_populate.api.populate_project(project_name, testapi_uri)
    pr_job.assert_called()
    pr_skipped.assert_called()

def test_project_error_get(mocker, requests_mock):
    """Raise error on getting project status."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_failed = mocker.patch('xtesting_db_populate.api.print_failed_and_exit')
    requests_mock.get(f'{testapi_uri}/projects/{project_name}',
                      status_code=500)
    xtesting_db_populate.api.populate_project(project_name, testapi_uri)
    pr_job.assert_called()
    pr_failed.assert_called()

def test_project_error_post(mocker, requests_mock):
    """Raise error on project creation."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_failed = mocker.patch('xtesting_db_populate.api.print_failed_and_exit')
    requests_mock.get(f'{testapi_uri}/projects/{project_name}',
                      status_code=404)
    json_data = {'name': project_name}
    requests_mock.post(f'{testapi_uri}/projects',
                      json=json_data,
                      status_code=500)
    xtesting_db_populate.api.populate_project(project_name, testapi_uri)
    pr_job.assert_called()
    pr_failed.assert_called()

#
# Test case
#

def test_case_new(mocker, requests_mock):
    """Create a new case."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_success = mocker.patch('xtesting_db_populate.api.print_success')
    requests_mock.get(
        f'{testapi_uri}/projects/{project_name}/cases/{case_name}',
        status_code=404)
    json_data = {'name': case_name}
    requests_mock.post(
        f'{testapi_uri}/projects/{project_name}/cases',
        json=json_data,
        status_code=200)
    xtesting_db_populate.api.populate_case(project_name, case_name, testapi_uri)
    pr_job.assert_called()
    pr_success.assert_called()

def test_case_existing(mocker, requests_mock):
    """Skip creation as case exists."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_skipped = mocker.patch('xtesting_db_populate.api.print_skipped')
    requests_mock.get(
        f'{testapi_uri}/projects/{project_name}/cases/{case_name}',
        status_code=200)
    xtesting_db_populate.api.populate_case(project_name, case_name, testapi_uri)
    pr_job.assert_called()
    pr_skipped.assert_called()

def test_case_error_get(mocker, requests_mock):
    """Raise error on getting case status."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_failed = mocker.patch('xtesting_db_populate.api.print_failed_and_exit')
    requests_mock.get(
        f'{testapi_uri}/projects/{project_name}/cases/{case_name}',
        status_code=500)
    xtesting_db_populate.api.populate_case(project_name, case_name,
                                          testapi_uri)
    pr_job.assert_called()
    pr_failed.assert_called()

def test_case_error_post(mocker, requests_mock):
    """Raise error on case creation."""
    pr_job = mocker.patch('xtesting_db_populate.api.print_job')
    pr_failed = mocker.patch('xtesting_db_populate.api.print_failed_and_exit')
    requests_mock.get(
        f'{testapi_uri}/projects/{project_name}/cases/{case_name}',
        status_code=404)
    json_data = {'name': case_name}
    requests_mock.post(
        f'{testapi_uri}/projects/{project_name}/cases',
        json=json_data,
        status_code=500)
    xtesting_db_populate.api.populate_case(project_name, case_name,
                                          testapi_uri)
    pr_job.assert_called()
    pr_failed.assert_called()
