#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Test cases for Foma Python bindings.

english.bin is taken from https://fomafst.github.io/morphtut.html
"""

import pytest
from src.foma_with_lib.foma import FST
import os

def test_load_fst():
    dir_path, _ = os.path.split(os.path.realpath(__file__))
    foma_script_path = os.path.join(dir_path, 'english.bin')
    fst = FST.load(foma_script_path)
    assert isinstance(fst, FST)


def test_apply_fst(eat_fst):
    result, = eat_fst.apply_up('cat')
    assert result == 'cat+N+Sg'


def test_apply_down(eat_fst):
    result, = eat_fst.apply_down('fox+N+Sg')
    assert result == 'fox'


@pytest.fixture
def eat_fst():
    dir_path, _ = os.path.split(os.path.realpath(__file__))
    foma_script_path = os.path.join(dir_path, 'english.bin')
    return FST.load(foma_script_path)
