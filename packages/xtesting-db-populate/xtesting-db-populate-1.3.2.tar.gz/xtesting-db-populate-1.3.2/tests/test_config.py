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

import xtesting_db_populate.config
import pytest
from yaml import dump

@pytest.mark.parametrize("env_url", [
    'https://testapi.test/api/v1/test',
    'http://testapi.test/api/v1/test',
    'https://testapi.test/api/v2/test',
    'https://testapi.test/api/v1',
    'https://www.testapi.test/api/v1',
    ])
def test_geturl(env_url, mocker):
    """Test testapi getter."""
    pr_job = mocker.patch('xtesting_db_populate.config.print_job')
    pr_success = mocker.patch('xtesting_db_populate.config.print_success')
    os_get = mocker.patch('os.environ.get', lambda x: env_url)
    url = xtesting_db_populate.config.get_testapi_url()
    assert 'testapi.test/api/v' in url
    assert url.startswith('http')
    pr_job.assert_called()
    pr_success.assert_called()

def test_geturl_no_var(mocker):
    """Test testapi getter with no var."""
    pr_job = mocker.patch('xtesting_db_populate.config.print_job')
    pr_failed = mocker.patch(
        'xtesting_db_populate.config.print_failed_and_exit')
    os_get = mocker.patch('os.environ.get', lambda x: '')
    xtesting_db_populate.config.get_testapi_url()
    pr_job.assert_called()
    pr_failed.assert_called()

@pytest.mark.parametrize("env_url", [
    'htts://testapi.test/api/v1/test',
    'https:/testapi.test/api/v1/test',
    'https://testapi.test/api/',
    'https://testapi.test/v1/',
    ])
def test_geturl_bad_url(env_url, mocker):
    """Test testapi getter with a bad url."""
    pr_job = mocker.patch('xtesting_db_populate.config.print_job')
    pr_failed = mocker.patch(
        'xtesting_db_populate.config.print_failed_and_exit')
    os_get = mocker.patch('os.environ.get', lambda x: env_url)
    xtesting_db_populate.config.get_testapi_url()
    pr_job.assert_called()
    pr_failed.assert_called()

def test_get_pods_from_file(mocker):
    """Test pods getter from file."""
    fakefile = "---\npods:\n    - pod1\n    - pod2\n"
    mockopen = mocker.mock_open(read_data=fakefile)
    pr_job = mocker.patch('xtesting_db_populate.config.print_job')
    pr_success = mocker.patch('xtesting_db_populate.config.print_success')
    mocker.patch('xtesting_db_populate.config.open', mockopen)
    pods = xtesting_db_populate.config.get_pods_list()
    assert pods == ['pod1', 'pod2']
    pr_job.assert_called()
    pr_success.assert_called()

def test_get_pods_from_var(mocker):
    """Test pods getter from var ."""
    mockopen = mocker.mock_open()
    mockopen.side_effect = IOError
    pr_job = mocker.patch('xtesting_db_populate.config.print_job')
    pr_success = mocker.patch('xtesting_db_populate.config.print_success')
    pr_skipped = mocker.patch('xtesting_db_populate.config.print_skipped')
    mocker.patch('xtesting_db_populate.config.open', mockopen)
    mocker.patch('os.environ.get', lambda x: "pod1")
    pods = xtesting_db_populate.config.get_pods_list()
    assert pods == ['pod1']
    pr_job.assert_called()
    pr_skipped.assert_called()
    pr_success.assert_called()

def test_get_pods_skipped(mocker):
    """Test pods getter with no informations."""
    mockopen = mocker.mock_open()
    mockopen.side_effect = IOError
    pr_job = mocker.patch('xtesting_db_populate.config.print_job')
    pr_skipped = mocker.patch('xtesting_db_populate.config.print_skipped')
    pods = xtesting_db_populate.config.get_pods_list()
    assert pods == []
    pr_job.assert_called()
    pr_skipped.assert_called()

def test_get_cases(mocker):
    """Test test cases."""
    fake_testscases = {
    'tiers': [
        {   'name': 'bashtest',
            'testcases':[
                {'case_name': 'test1',
                 'project_name': 'prj1'
                },
                {'case_name': 'test2',
                 'project_name': 'prj1',
                }
                ]
            }
        ]
    }
    ret_tests_by_project = {
        'prj1': ['test1', 'test2']
    }
    mockopen = mocker.mock_open(read_data=dump(fake_testscases))
    pr_job = mocker.patch('xtesting_db_populate.config.print_job')
    pr_success = mocker.patch('xtesting_db_populate.config.print_success')
    mocker.patch('xtesting_db_populate.config.open', mockopen)
    testcases = xtesting_db_populate.config.get_testcases()
    assert testcases == ret_tests_by_project
    pr_job.assert_called()
    pr_success.assert_called()

def test_get_cases_unknown_file(mocker):
    """Test test cases with file error."""
    mockopen = mocker.mock_open()
    mockopen.side_effect = IOError
    pr_job = mocker.patch('xtesting_db_populate.config.print_job')
    pr_failed = mocker.patch(
        'xtesting_db_populate.config.print_failed_and_exit')
    mocker.patch('xtesting_db_populate.config.open', mockopen)
    xtesting_db_populate.config.get_testcases()
    pr_job.assert_called()
    pr_failed.assert_called()

def test_get_cases_bad_file(mocker):
    """Test test cases with file error."""
    fake_testscases = {
    'tiers': [
        {   'name': 'bashtest',
            'BADKEY':[
                {'case_name': 'test1',
                 'project_name': 'prj1'
                },
                {'case_name': 'test2',
                 'project_name': 'prj1',
                }
                ]
            }
        ]
    }
    ret_tests_by_project = {
        'prj1': ['test1', 'test2']
    }
    mockopen = mocker.mock_open(read_data=dump(fake_testscases))
    pr_job = mocker.patch('xtesting_db_populate.config.print_job')
    pr_failed = mocker.patch(
        'xtesting_db_populate.config.print_failed_and_exit')
    mocker.patch('xtesting_db_populate.config.open', mockopen)
    xtesting_db_populate.config.get_testcases()
    pr_job.assert_called()
    pr_failed.assert_called()
