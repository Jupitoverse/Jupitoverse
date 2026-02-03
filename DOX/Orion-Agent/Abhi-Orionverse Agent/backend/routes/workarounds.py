# backend/routes/workarounds.py
from flask import Blueprint, request, jsonify
import database  # Make sure you have a database.py file with the connection logic

workarounds_bp = Blueprint('workarounds', __name__)

@workarounds_bp.route('/', methods=['GET'])
def get_workarounds():
    conn = database.get_db_connection()
    cur = conn.cursor(cursor_factory=database.psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM workarounds ORDER BY created_date DESC;')
    workarounds = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(workarounds)

@workarounds_bp.route('/', methods=['POST'])
def add_workaround():
    data = request.get_json()
    conn = database.get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO workarounds (category, issue, description, created_by) VALUES (%s, %s, %s, %s) RETURNING id;',
        (data['category'], data['issue'], data['description'], data.get('created_by', 'Anonymous'))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success', 'id': new_id}), 201

@workarounds_bp.route('/<int:id>/view', methods=['POST'])
def increment_view(id):
    conn = database.get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE workarounds SET views = views + 1 WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

@workarounds_bp.route('/<int:id>/like', methods=['POST'])
def increment_like(id):
    conn = database.get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE workarounds SET likes = likes + 1 WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})


# Add these two routes to backend/routes/workarounds.py

@workarounds_bp.route('/<int:id>', methods=['PUT'])
def update_workaround_route(id):
    """Route to update a workaround."""
    data = request.get_json()
    success = database.update_workaround(id, data)
    if success:
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Workaround not found or update failed'}), 404

@workarounds_bp.route('/<int:id>', methods=['DELETE'])
def delete_workaround_route(id):
    """Route to delete a workaround."""
    success = database.delete_workaround(id)
    if success:
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Workaround not found'}), 404