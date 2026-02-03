#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON Workaround Module
Provides historical workaround search by description and RCA

This module is self-contained to avoid merge conflicts with existing code.
"""

from json_workaround.routes import workaround_bp
from json_workaround.data_handler import WorkaroundDataHandler

__all__ = ['workaround_bp', 'WorkaroundDataHandler']
__version__ = '1.0.0'

