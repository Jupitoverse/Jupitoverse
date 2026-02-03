#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workaround Routes Blueprint
Flask routes for historical workaround search functionality

This module is self-contained to avoid merge conflicts.
"""

import sys
import os

# Add parent directory to path for imports
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(MODULE_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Blueprint, render_template, request, jsonify
import logging

from json_workaround.data_handler import get_workaround_handler

logger = logging.getLogger(__name__)

# Create Blueprint with unique name
workaround_bp = Blueprint(
    'json_workaround',
    __name__,
    url_prefix='/workaround',
    template_folder='templates'
)


@workaround_bp.route('/', methods=['GET'])
@workaround_bp.route('/search', methods=['GET', 'POST'])
def workaround_search():
    """
    Main workaround page.
    Shows ALL workarounds by default, with optional search/filter.
    """
    results = []
    description_query = ''
    rca_query = ''
    is_filtered = False
    error = None
    
    try:
        handler = get_workaround_handler()
        stats = handler.get_stats()
        
        if request.method == 'POST':
            description_query = request.form.get('description', '').strip()
            rca_query = request.form.get('rca', '').strip()
            
            if description_query or rca_query:
                # Filter results based on search
                results = handler.search_combined(
                    description_query=description_query,
                    rca_query=rca_query,
                    limit=100
                )
                is_filtered = True
            else:
                # No filter - show all
                results = handler.get_all_workarounds()
        else:
            # GET request - show all workarounds by default
            results = handler.get_all_workarounds()
        
    except Exception as e:
        logger.error(f"Error in workaround search: {e}")
        error = f"An error occurred: {str(e)}"
        stats = {'total_records': 0, 'data_loaded': False}
    
    return render_template(
        'json_workaround/workaround_search.html',
        results=results,
        description_query=description_query,
        rca_query=rca_query,
        is_filtered=is_filtered,
        error=error,
        stats=stats
    )


@workaround_bp.route('/api/search', methods=['POST'])
def api_search():
    """
    API endpoint for workaround search.
    Returns JSON results for AJAX requests.
    """
    try:
        data = request.get_json() or {}
        description_query = data.get('description', '').strip()
        rca_query = data.get('rca', '').strip()
        limit = min(int(data.get('limit', 50)), 100)  # Cap at 100
        
        if not description_query and not rca_query:
            return jsonify({
                'success': False,
                'error': 'Please provide at least one search term',
                'results': []
            })
        
        handler = get_workaround_handler()
        results = handler.search_combined(
            description_query=description_query,
            rca_query=rca_query,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        logger.error(f"API search error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'results': []
        }), 500


@workaround_bp.route('/api/stats', methods=['GET'])
def api_stats():
    """Get statistics about loaded workaround data."""
    try:
        handler = get_workaround_handler()
        stats = handler.get_stats()
        return jsonify({
            'success': True,
            **stats
        })
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@workaround_bp.route('/api/reload', methods=['POST'])
def api_reload():
    """Reload workaround data from JSON file."""
    try:
        data = request.get_json() or {}
        json_file = data.get('json_file')
        
        handler = get_workaround_handler()
        handler.reload_data(json_file)
        stats = handler.get_stats()
        
        return jsonify({
            'success': True,
            'message': 'Data reloaded successfully',
            **stats
        })
    except Exception as e:
        logger.error(f"Reload error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@workaround_bp.route('/detail/<sr_id>', methods=['GET'])
def workaround_detail(sr_id: str):
    """
    View detailed information for a specific workaround by SR ID.
    """
    try:
        handler = get_workaround_handler()
        record = handler.get_by_sr_id(sr_id)
        
        if not record:
            return render_template(
                'json_workaround/workaround_search.html',
                results=[],
                search_performed=False,
                error=f"No workaround found for SR ID: {sr_id}",
                stats=handler.get_stats()
            )
        
        return render_template(
            'json_workaround/workaround_detail.html',
            record=record,
            sr_id=sr_id
        )
        
    except Exception as e:
        logger.error(f"Detail view error: {e}")
        return render_template(
            'json_workaround/workaround_search.html',
            results=[],
            search_performed=False,
            error=f"Error loading workaround: {str(e)}",
            stats={'total_records': 0, 'data_loaded': False}
        )

