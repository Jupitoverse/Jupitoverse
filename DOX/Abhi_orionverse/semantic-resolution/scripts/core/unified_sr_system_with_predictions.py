"""
Enhanced Unified SR System with Prediction Capabilities
Integrates SR assignment, analysis, and ML/AI-based predictions into one interface
"""

from flask import Flask, render_template_string, request, jsonify, send_file
import os
import json
import pandas as pd
from datetime import datetime
from scripts.core.chat_sr_assignment_interface import ChatSRAssignmentInterface
from scripts.analysis.comprehensive_pattern_analyzer import ComprehensivePatternAnalyzer
from scripts.core.team_config_chatbot import TeamConfigChatbot
from scripts.utilities.people_skills_database import PeopleSkillsDatabase
from scripts.analysis.sr_prediction_integration import SRPredictionIntegration

app = Flask(__name__)
app.secret_key = 'unified_sr_system_with_predictions_2024'

# Global instances
chat_sessions = {}

class UnifiedSRSystemWithPredictions:
    """
    Enhanced unified system with SR prediction capabilities
    """
    
    def __init__(self):
        self.assignment_interface = ChatSRAssignmentInterface()
        self.pattern_analyzer = ComprehensivePatternAnalyzer()
        self.team_config_chatbot = TeamConfigChatbot()
        self.people_db = PeopleSkillsDatabase()
        self.sr_predictor = None  # Will be initialized on demand
        self.mode = 'assignment'  # 'assignment', 'analysis', 'config', or 'prediction'
        self.processed_data = None
        
        # Initialize people database
        self._init_people_database()
        
    def _init_people_database(self):
        """Initialize people database from Excel if needed"""
        try:
            if os.path.exists("People.xlsx"):
                self.people_db.load_people_from_excel("People.xlsx")
                print("✅ People.xlsx loaded into database")
        except Exception as e:
            print(f"⚠️ Could not load People.xlsx: {str(e)}")
    
    def initialize_predictor(self):
        """Initialize SR predictor on demand"""
        if self.sr_predictor is None:
            try:
                self.sr_predictor = SRPredictionIntegration()
                if self.sr_predictor.initialize():
                    print("✅ SR Predictor initialized")
                    return True
            except Exception as e:
                print(f"❌ Failed to initialize predictor: {str(e)}")
                return False
        return True

# Global system instance
unified_system = UnifiedSRSystemWithPredictions()

# Enhanced HTML Template with Prediction Tab
ENHANCED_UNIFIED_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unified SR System with Predictions</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .tab {
            background: white;
            padding: 15px 30px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            color: #666;
            font-weight: 500;
        }
        
        .tab:hover {
            background: #f8f9fa;
            transform: translateY(-2px);
        }
        
        .tab.active {
            background: #667eea;
            color: white;
            box-shadow: 0 4px 6px rgba(102, 126, 234, 0.4);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .card h2 {
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        
        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 500;
        }
        
        .form-group input,
        .form-group textarea,
        .form-group select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-family: inherit;
            font-size: 14px;
        }
        
        .form-group textarea {
            min-height: 100px;
            resize: vertical;
        }
        
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: background 0.3s;
        }
        
        .btn:hover {
            background: #5568d3;
        }
        
        .btn-secondary {
            background: #6c757d;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
        }
        
        .result-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }
        
        .result-card h3 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .result-item {
            margin: 8px 0;
            color: #555;
        }
        
        .result-item strong {
            color: #333;
        }
        
        .confidence-high {
            color: #28a745;
            font-weight: bold;
        }
        
        .confidence-medium {
            color: #ffc107;
            font-weight: bold;
        }
        
        .confidence-low {
            color: #dc3545;
            font-weight: bold;
        }
        
        .prediction-amdocs {
            background: #fff3cd;
            border-left-color: #ffc107;
        }
        
        .prediction-customer {
            background: #d1ecf1;
            border-left-color: #17a2b8;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        
        .quick-fill {
            margin-bottom: 15px;
        }
        
        .quick-fill button {
            margin-right: 10px;
            margin-bottom: 10px;
            padding: 8px 15px;
            background: #6c757d;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 13px;
        }
        
        .quick-fill button:hover {
            background: #5a6268;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .feature-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        
        .feature-box h4 {
            font-size: 14px;
            margin-bottom: 10px;
            opacity: 0.9;
        }
        
        .feature-box p {
            font-size: 24px;
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .two-column {
                grid-template-columns: 1fr;
            }
            
            .feature-grid {
                grid-template-columns: 1fr;
            }
            
            .tabs {
                flex-wrap: wrap;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Unified SR System with AI Predictions</h1>
            <p>Complete SR Management: Assignment, Analysis, and Intelligent Predictions</p>
        </div>
        
        <div class="tabs">
            <div class="tab active" onclick="switchTab('prediction')">
                🔮 SR Prediction
            </div>
            <div class="tab" onclick="switchTab('assignment')">
                👥 SR Assignment
            </div>
            <div class="tab" onclick="switchTab('analysis')">
                📊 Pattern Analysis
            </div>
            <div class="tab" onclick="switchTab('about')">
                ℹ️ About
            </div>
        </div>
        
        <!-- SR Prediction Tab -->
        <div id="prediction-tab" class="tab-content active">
            <div class="two-column">
                <div class="card">
                    <h2>🔮 Predict SR Classification</h2>
                    
                    <div class="quick-fill">
                        <button onclick="fillPredictionExample1()">Example: System Error</button>
                        <button onclick="fillPredictionExample2()">Example: User Issue</button>
                        <button onclick="clearPredictionForm()">Clear</button>
                    </div>
                    
                    <form id="predictionForm">
                        <div class="form-group">
                            <label for="pred_incident_id">Incident ID</label>
                            <input type="text" id="pred_incident_id" name="incident_id" 
                                   placeholder="INC000009999999">
                        </div>
                        
                        <div class="form-group">
                            <label for="pred_summary">Summary *</label>
                            <input type="text" id="pred_summary" name="summary" required 
                                   placeholder="Brief summary of the issue">
                        </div>
                        
                        <div class="form-group">
                            <label for="pred_description">Description *</label>
                            <textarea id="pred_description" name="description" required 
                                      placeholder="Detailed description of the issue"></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="pred_priority">Priority</label>
                            <select id="pred_priority" name="priority">
                                <option value="Low">Low</option>
                                <option value="Medium">Medium</option>
                                <option value="High">High</option>
                                <option value="Critical">Critical</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="pred_product">Product Categorization</label>
                            <select id="pred_product" name="product">
                                <option value="SOM">SOM</option>
                                <option value="SQO_MM">SQO_MM</option>
                                <option value="Invoicing_MM">Invoicing_MM</option>
                                <option value="ADH_MM">ADH_MM</option>
                                <option value="Unknown">Unknown</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="pred_operational">Operational Categorization</label>
                            <input type="text" id="pred_operational" name="operational" 
                                   placeholder="e.g., Provisioning, Install and activation">
                        </div>
                        
                        <button type="submit" class="btn">🔍 Predict Issue Type</button>
                    </form>
                </div>
                
                <div class="card">
                    <h2>📊 Prediction Results</h2>
                    <div id="predictionResults">
                        <p style="color: #999; text-align: center; padding: 40px 20px;">
                            Enter ticket details and click "Predict Issue Type" to see results
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>📈 Model Performance</h2>
                <div class="feature-grid">
                    <div class="feature-box">
                        <h4>Training Data</h4>
                        <p>15,268</p>
                        <small>Historical Tickets</small>
                    </div>
                    <div class="feature-box">
                        <h4>Model Accuracy</h4>
                        <p>66.2%</p>
                        <small>Test Set Performance</small>
                    </div>
                    <div class="feature-box">
                        <h4>Features Used</h4>
                        <p>190</p>
                        <small>Text + Categorical</small>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- SR Assignment Tab -->
        <div id="assignment-tab" class="tab-content">
            <div class="card">
                <h2>👥 SR Assignment System</h2>
                <p>Upload SR Excel file to get intelligent assignment recommendations</p>
                <form id="assignmentForm" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="sr_file">Upload SR Excel File</label>
                        <input type="file" id="sr_file" name="file" accept=".xls,.xlsx" required>
                    </div>
                    <button type="submit" class="btn">📤 Process & Assign</button>
                </form>
                <div id="assignmentResults" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <!-- Pattern Analysis Tab -->
        <div id="analysis-tab" class="tab-content">
            <div class="card">
                <h2>📊 Pattern Analysis</h2>
                <p>Analyze patterns in your SR data to identify trends and insights</p>
                <form id="analysisForm" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="analysis_file">Upload SR Excel File</label>
                        <input type="file" id="analysis_file" name="file" accept=".xls,.xlsx" required>
                    </div>
                    <button type="submit" class="btn">📊 Analyze Patterns</button>
                </form>
                <div id="analysisResults" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <!-- About Tab -->
        <div id="about-tab" class="tab-content">
            <div class="card">
                <h2>ℹ️ About This System</h2>
                
                <h3 style="margin-top: 20px;">🔮 SR Prediction</h3>
                <p>Uses Machine Learning models trained on 15,268 historical tickets to predict:</p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li><strong>Issue Type</strong>: Amdocs Issue vs Customer Issue (66.2% accuracy)</li>
                    <li><strong>Resolution Categories</strong>: Predicted resolution paths</li>
                    <li><strong>Confidence Scores</strong>: High/Medium/Low confidence levels</li>
                </ul>
                
                <h3 style="margin-top: 20px;">👥 SR Assignment</h3>
                <p>Intelligent assignment recommendations based on:</p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>Team member skills and expertise</li>
                    <li>Current workload and availability</li>
                    <li>Priority and complexity of tickets</li>
                </ul>
                
                <h3 style="margin-top: 20px;">📊 Pattern Analysis</h3>
                <p>Comprehensive analysis including:</p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>Temporal trends and seasonality</li>
                    <li>Common issue patterns</li>
                    <li>Resolution time analysis</li>
                </ul>
                
                <h3 style="margin-top: 20px;">🚀 Features</h3>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>✅ Real-time predictions</li>
                    <li>✅ Confidence-based recommendations</li>
                    <li>✅ Historical pattern analysis</li>
                    <li>✅ Team workload optimization</li>
                    <li>✅ Integrated dashboard</li>
                </ul>
            </div>
        </div>
    </div>
    
    <script>
        // Tab switching
        function switchTab(tabName) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Remove active class from all tabs
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab content
            document.getElementById(tabName + '-tab').classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }
        
        // Prediction form examples
        function fillPredictionExample1() {
            document.getElementById('pred_incident_id').value = 'INC000001234567';
            document.getElementById('pred_summary').value = 'DCP provision failed with timeout error';
            document.getElementById('pred_description').value = 'Customer site provisioning task is failing in DCP with error code 503. The system shows timeout after 60 seconds. This has been occurring for the past 2 hours. Backend logs show connection issues to the provisioning service.';
            document.getElementById('pred_priority').value = 'High';
            document.getElementById('pred_product').value = 'SOM';
            document.getElementById('pred_operational').value = 'Provisioning';
        }
        
        function fillPredictionExample2() {
            document.getElementById('pred_incident_id').value = 'INC000007654321';
            document.getElementById('pred_summary').value = 'User unable to submit proposal in quote system';
            document.getElementById('pred_description').value = 'User reports they cannot find the submit button in the proposal workflow. After review, the button is visible but user was looking in wrong section. User education on proper workflow needed.';
            document.getElementById('pred_priority').value = 'Low';
            document.getElementById('pred_product').value = 'SQO_MM';
            document.getElementById('pred_operational').value = 'ProposalFlow';
        }
        
        function clearPredictionForm() {
            document.getElementById('predictionForm').reset();
        }
        
        // Prediction form submission
        document.getElementById('predictionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const resultsDiv = document.getElementById('predictionResults');
            resultsDiv.innerHTML = '<div class="loading">🔄 Analyzing ticket...</div>';
            
            const formData = {
                'Incident ID': document.getElementById('pred_incident_id').value || 'N/A',
                'Summary*': document.getElementById('pred_summary').value,
                'Description*': document.getElementById('pred_description').value,
                'Priority': document.getElementById('pred_priority').value,
                'Product Categorization*': document.getElementById('pred_product').value,
                'Operational Categorization*': document.getElementById('pred_operational').value,
                'Status*': 'In Progress',
                'Assigned Group*': 'SOM_MM',
                'Reported Date': new Date().toISOString()
            };
            
            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.error) {
                    resultsDiv.innerHTML = `<div style="background:#f8d7da;color:#721c24;padding:15px;border-radius:5px;">❌ Error: ${result.error}</div>`;
                    return;
                }
                
                // Display results
                const rec = result.recommendation;
                const mlPred = result.ml_prediction.issue_type;
                
                const confidenceClass = rec.confidence_level === 'High' ? 'confidence-high' : 
                                       (rec.confidence_level === 'Medium' ? 'confidence-medium' : 'confidence-low');
                
                const predictionClass = rec.primary_classification === 'Amdocs' ? 'prediction-amdocs' : 'prediction-customer';
                
                resultsDiv.innerHTML = `
                    <div class="result-card ${predictionClass}">
                        <h3>🎯 Primary Classification</h3>
                        <div class="result-item">
                            <strong>Issue Type:</strong> ${rec.primary_classification}
                        </div>
                        <div class="result-item">
                            <strong>Confidence:</strong> <span class="${confidenceClass}">${rec.confidence_level}</span> (${(rec.confidence_score * 100).toFixed(1)}%)
                        </div>
                        <div class="result-item">
                            <strong>Suggested Action:</strong> ${rec.suggested_action}
                        </div>
                    </div>
                    
                    <div class="result-card">
                        <h3>📊 Detailed Probabilities</h3>
                        <div class="result-item">
                            <strong>Amdocs Issue:</strong> ${(mlPred.probabilities.Amdocs * 100).toFixed(1)}%
                        </div>
                        <div class="result-item">
                            <strong>Customer Issue:</strong> ${(mlPred.probabilities.Customer * 100).toFixed(1)}%
                        </div>
                    </div>
                    
                    <div class="result-card">
                        <h3>ℹ️ Ticket Information</h3>
                        <div class="result-item">
                            <strong>Ticket ID:</strong> ${result.ticket_id}
                        </div>
                        <div class="result-item">
                            <strong>Analysis Time:</strong> ${new Date(result.timestamp).toLocaleString()}
                        </div>
                    </div>
                `;
                
            } catch (error) {
                resultsDiv.innerHTML = `<div style="background:#f8d7da;color:#721c24;padding:15px;border-radius:5px;">❌ Error: ${error.message}</div>`;
            }
        });
        
        // Assignment form submission  
        document.getElementById('assignmentForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const resultsDiv = document.getElementById('assignmentResults');
            resultsDiv.innerHTML = '<div class="loading">🔄 Processing assignments...</div>';
            
            try {
                const response = await fetch('/api/assign', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                resultsDiv.innerHTML = `<div class="result-card"><pre>${JSON.stringify(result, null, 2)}</pre></div>`;
            } catch (error) {
                resultsDiv.innerHTML = `<div style="background:#f8d7da;color:#721c24;padding:15px;border-radius:5px;">❌ Error: ${error.message}</div>`;
            }
        });
        
        // Analysis form submission
        document.getElementById('analysisForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const resultsDiv = document.getElementById('analysisResults');
            resultsDiv.innerHTML = '<div class="loading">🔄 Analyzing patterns...</div>';
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                resultsDiv.innerHTML = `<div class="result-card"><pre>${JSON.stringify(result, null, 2)}</pre></div>`;
            } catch (error) {
                resultsDiv.innerHTML = `<div style="background:#f8d7da;color:#721c24;padding:15px;border-radius:5px;">❌ Error: ${error.message}</div>`;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main unified interface"""
    return render_template_string(ENHANCED_UNIFIED_HTML)

@app.route('/api/predict', methods=['POST'])
def predict_sr():
    """SR Prediction endpoint"""
    try:
        ticket_data = request.json
        
        # Initialize predictor if needed
        if not unified_system.initialize_predictor():
            return jsonify({'error': 'Prediction system not available. Please ensure models are trained.'}), 503
        
        # Make prediction
        result = unified_system.sr_predictor.predict_unified(ticket_data, include_ai_prompt=False)
        
        # Save to log
        unified_system.sr_predictor.save_prediction_log(result)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assign', methods=['POST'])
def assign_sr():
    """SR Assignment endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        # Process assignment (simplified - integrate with your existing logic)
        return jsonify({
            'status': 'success',
            'message': 'Assignment functionality - integrate with existing assignment system',
            'filename': file.filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_patterns():
    """Pattern Analysis endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        # Process analysis (simplified - integrate with your existing logic)
        return jsonify({
            'status': 'success',
            'message': 'Analysis functionality - integrate with existing analysis system',
            'filename': file.filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'predictor_initialized': unified_system.sr_predictor is not None and unified_system.sr_predictor.is_initialized
    })

def main():
    """Main entry point"""
    print("=" * 80)
    print("ENHANCED UNIFIED SR SYSTEM WITH PREDICTIONS")
    print("=" * 80)
    print("\n🚀 Starting unified system...")
    print("\n📍 Features available:")
    print("  - 🔮 SR Prediction (ML-based classification)")
    print("  - 👥 SR Assignment (Team-based routing)")
    print("  - 📊 Pattern Analysis (Trend identification)")
    print("\n🌐 Access the dashboard at: http://localhost:5000")
    print("\n💡 Use Ctrl+C to stop the server")
    print("=" * 80)
    
    # Start Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()

