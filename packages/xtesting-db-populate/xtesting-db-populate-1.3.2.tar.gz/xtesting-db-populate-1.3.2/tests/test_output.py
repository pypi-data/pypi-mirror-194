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
Test xtesting-db-populate - test output.
'''

import xtesting_db_populate.output
import pytest

def test_skipped(capfd):
    """Test print_skipped message."""
    xtesting_db_populate.output.print_skipped()
    out, err = capfd.readouterr()
    assert 'skipped' in out

def test_skipped_with_msg(capfd):
    """Test print_skipped message."""
    xtesting_db_populate.output.print_skipped('test')
    out, err = capfd.readouterr()
    assert 'test' in out
    assert 'skipped' in out

def test_success(capfd):
    """Test print_skipped message."""
    xtesting_db_populate.output.print_success()
    out, err = capfd.readouterr()
    assert 'success' in out

def test_success(capfd):
    """Test print_skipped message."""
    xtesting_db_populate.output.print_success('test')
    out, err = capfd.readouterr()
    assert 'test' in out
    assert 'success' in out

def test_failure(capsys):
    """Test print_skipped message."""
    with pytest.raises(SystemExit) as pytest_wrapped_e:

        xtesting_db_populate.output.print_failed_and_exit('message')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 'message'

def test_print_job(capfd):
    """Test print_skipped message."""
    xtesting_db_populate.output.print_job("message")
    out, err = capfd.readouterr()
    assert 'message ' in out
