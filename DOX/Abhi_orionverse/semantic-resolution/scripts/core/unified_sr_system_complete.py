"""
Complete Unified SR System - Integrating Assignment, Analysis, and ML Predictions
Fully integrated with existing chat_sr_assignment_interface, pattern analyzer, and new SR predictor
"""

from flask import Flask, render_template_string, request, jsonify, send_file
import os
import json
import pandas as pd
from datetime import datetime
from werkzeug.utils import secure_filename
from scripts.core.chat_sr_assignment_interface import ChatSRAssignmentInterface
from scripts.analysis.comprehensive_pattern_analyzer import ComprehensivePatternAnalyzer
from scripts.core.team_config_chatbot import TeamConfigChatbot
from scripts.utilities.people_skills_database import PeopleSkillsDatabase
from scripts.analysis.enhanced_sr_tracking_system import EnhancedSRTrackingSystem

# Import prediction system
try:
    from sr_prediction_integration import SRPredictionIntegration
    PREDICTION_AVAILABLE = True
except:
    PREDICTION_AVAILABLE = False
    print("⚠️ SR Prediction system not available. Ensure models are trained.")

app = Flask(__name__)
app.secret_key = 'unified_sr_complete_system_2024'

# Global instances
chat_sessions = {}

class CompleteUnifiedSRSystem:
    """
    Complete unified system with all features
    """
    
    def __init__(self):
        # Existing systems
        self.assignment_interface = ChatSRAssignmentInterface()
        self.pattern_analyzer = ComprehensivePatternAnalyzer()
        self.team_config_chatbot = TeamConfigChatbot()
        self.people_db = PeopleSkillsDatabase()
        self.sr_tracking = EnhancedSRTrackingSystem()
        
        # New prediction system
        self.sr_predictor = None
        self.predictor_initialized = False
        
        self.mode = 'assignment'
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
        if not PREDICTION_AVAILABLE:
            return False
            
        if self.sr_predictor is None:
            try:
                self.sr_predictor = SRPredictionIntegration()
                if self.sr_predictor.initialize():
                    self.predictor_initialized = True
                    print("✅ SR Predictor initialized")
                    return True
            except Exception as e:
                print(f"❌ Failed to initialize predictor: {str(e)}")
                return False
        return self.predictor_initialized
    
    def process_file_for_assignment(self, file_path):
        """Process file for SR assignment"""
        try:
            df = pd.read_excel(file_path)
            
            # Use existing assignment interface
            result = self.assignment_interface.assignment_system.process_batch(df)
            
            return {
                'success': True,
                'total_srs': len(df),
                'assignments': result,
                'message': f'Successfully processed {len(df)} SRs for assignment'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_file_for_analysis(self, file_path):
        """Process file for pattern analysis"""
        try:
            # Use existing pattern analyzer
            results = self.pattern_analyzer.analyze_file(file_path)
            
            return {
                'success': True,
                'analysis': results,
                'message': 'Pattern analysis completed successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Global system instance
unified_system = CompleteUnifiedSRSystem()

# Complete Enhanced HTML Template
COMPLETE_UNIFIED_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Unified SR System</title>
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
            font-size: 28px;
        }
        
        .header p {
            color: #666;
            font-size: 16px;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .tab {
            background: white;
            padding: 15px 30px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            color: #666;
            font-weight: 500;
            font-size: 15px;
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
        
        .form-group input[type="file"] {
            padding: 8px;
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
        
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
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
            font-size: 16px;
        }
        
        .success {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
            margin-bottom: 15px;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
            margin-bottom: 15px;
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
        
        pre {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 13px;
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
            <h1>🚀 Complete Unified SR System</h1>
            <p>Assignment • Analysis • ML Predictions - All in One Platform</p>
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
                                   placeholder="e.g., Provisioning">
                        </div>
                        
                        <button type="submit" class="btn">🔍 Predict Issue Type</button>
                    </form>
                </div>
                
                <div class="card">
                    <h2>📊 Prediction Results</h2>
                    <div id="predictionResults">
                        <p style="color: #999; text-align: center; padding: 40px 20px;">
                            Enter ticket details and click "Predict Issue Type"
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
                        <small>Test Set</small>
                    </div>
                    <div class="feature-box">
                        <h4>Features</h4>
                        <p>190</p>
                        <small>Engineered</small>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- SR Assignment Tab -->
        <div id="assignment-tab" class="tab-content">
            <div class="card">
                <h2>👥 Intelligent SR Assignment with Predictions</h2>
                <p style="margin-bottom: 10px;">Upload today's SR Excel file to automatically:</p>
                <ul style="margin: 0 0 20px 20px; color: #666;">
                    <li>Filter "In Progress" tickets</li>
                    <li>Predict issue type (Amdocs vs Customer) and complexity</li>
                    <li>Identify interface issues that need workarounds</li>
                    <li>Assign tickets to team members based on skills and workload</li>
                    <li>Match easy SRs to junior members, complex SRs to experienced staff</li>
                </ul>
                
                <form id="assignmentForm" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="assignment_file">Upload Today's SR Excel File (.xls or .xlsx)</label>
                        <input type="file" id="assignment_file" name="file" accept=".xls,.xlsx" required>
                    </div>
                    <button type="submit" class="btn">📤 Analyze & Assign Today's SRs</button>
                </form>
                
                <div id="assignmentResults" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <!-- Pattern Analysis Tab -->
        <div id="analysis-tab" class="tab-content">
            <div class="card">
                <h2>📊 Pattern Analysis</h2>
                <p style="margin-bottom: 20px;">Analyze patterns in your SR data to identify trends, peak times, and common issues.</p>
                
                <form id="analysisForm" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="analysis_file">Upload SR Excel File (.xls or .xlsx)</label>
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
                <h2>ℹ️ About Complete Unified SR System</h2>
                
                <h3 style="margin-top: 20px; color: #667eea;">🔮 SR Prediction (ML-Powered)</h3>
                <p>Machine Learning models trained on 15,268 historical tickets provide:</p>
                <ul style="margin: 10px 0 10px 20px;">
                    <li><strong>Issue Type Classification</strong>: Amdocs vs Customer (66.2% accuracy)</li>
                    <li><strong>Resolution Predictions</strong>: Suggested resolution categories</li>
                    <li><strong>Confidence Scores</strong>: High/Medium/Low confidence levels</li>
                    <li><strong>Real-time Analysis</strong>: Instant predictions for new tickets</li>
                </ul>
                
                <h3 style="margin-top: 20px; color: #667eea;">👥 Intelligent SR Assignment with ML</h3>
                <p>Upload today's Excel file to automatically analyze and assign "In Progress" tickets:</p>
                <ul style="margin: 10px 0 10px 20px;">
                    <li><strong>Automated Prediction</strong>: ML models predict issue type and complexity for each ticket</li>
                    <li><strong>Interface Detection</strong>: Identifies tickets likely to need workarounds (Amdocs issues)</li>
                    <li><strong>Skill-Based Assignment</strong>: Easy tickets → Junior staff, Complex tickets → Experienced staff</li>
                    <li><strong>Workload Balancing</strong>: Considers team capacity and availability</li>
                    <li><strong>Detailed Reports</strong>: Excel and JSON reports with full analysis breakdown</li>
                    <li><strong>Team Database</strong>: Integrated with People.xlsx skills database</li>
                </ul>
                
                <h3 style="margin-top: 20px; color: #667eea;">📊 Pattern Analysis</h3>
                <p>Comprehensive analysis powered by your pattern analyzer:</p>
                <ul style="margin: 10px 0 10px 20px;">
                    <li><strong>Temporal Trends</strong>: Volume patterns over time</li>
                    <li><strong>Issue Patterns</strong>: Common problem areas</li>
                    <li><strong>Resolution Analysis</strong>: Time-to-resolve metrics</li>
                    <li><strong>Visual Reports</strong>: Charts and graphs</li>
                </ul>
                
                <h3 style="margin-top: 20px; color: #667eea;">🚀 System Features</h3>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 15px;">
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
                        <strong>✅ Real-time Predictions</strong><br>
                        <small>Instant ML-based classification</small>
                    </div>
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
                        <strong>✅ Smart Assignment</strong><br>
                        <small>Optimal team member selection</small>
                    </div>
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
                        <strong>✅ Pattern Detection</strong><br>
                        <small>Identify trends and issues</small>
                    </div>
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
                        <strong>✅ Integrated Platform</strong><br>
                        <small>All features in one UI</small>
                    </div>
                </div>
                
                <h3 style="margin-top: 25px; color: #667eea;">📈 Performance Metrics</h3>
                <ul style="margin: 10px 0 10px 20px;">
                    <li><strong>Prediction Accuracy</strong>: 66.2% (primary classification)</li>
                    <li><strong>ROC AUC Score</strong>: 0.615</li>
                    <li><strong>Historical Data</strong>: 10 months (Dec 2024 - Oct 2025)</li>
                    <li><strong>Total Tickets Analyzed</strong>: 15,268</li>
                </ul>
            </div>
        </div>
    </div>
    
    <script>
        // Tab switching
        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }
        
        // Prediction examples
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
        
        // Prediction form
        document.getElementById('predictionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const resultsDiv = document.getElementById('predictionResults');
            resultsDiv.innerHTML = '<div class="loading">🔄 Analyzing ticket with ML models...</div>';
            
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
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.error) {
                    resultsDiv.innerHTML = `<div class="error">❌ ${result.error}</div>`;
                    return;
                }
                
                const rec = result.recommendation;
                const mlPred = result.ml_prediction.issue_type;
                const confidenceClass = rec.confidence_level === 'High' ? 'confidence-high' : 
                                       (rec.confidence_level === 'Medium' ? 'confidence-medium' : 'confidence-low');
                const predictionClass = rec.primary_classification === 'Amdocs' ? 'prediction-amdocs' : 'prediction-customer';
                
                resultsDiv.innerHTML = `
                    <div class="result-card ${predictionClass}">
                        <h3>🎯 Primary Classification</h3>
                        <div class="result-item"><strong>Issue Type:</strong> ${rec.primary_classification}</div>
                        <div class="result-item"><strong>Confidence:</strong> <span class="${confidenceClass}">${rec.confidence_level}</span> (${(rec.confidence_score * 100).toFixed(1)}%)</div>
                        <div class="result-item"><strong>Action:</strong> ${rec.suggested_action}</div>
                    </div>
                    <div class="result-card">
                        <h3>📊 Probabilities</h3>
                        <div class="result-item"><strong>Amdocs:</strong> ${(mlPred.probabilities.Amdocs * 100).toFixed(1)}%</div>
                        <div class="result-item"><strong>Customer:</strong> ${(mlPred.probabilities.Customer * 100).toFixed(1)}%</div>
                    </div>
                    <div class="result-card">
                        <h3>ℹ️ Info</h3>
                        <div class="result-item"><strong>ID:</strong> ${result.ticket_id}</div>
                        <div class="result-item"><strong>Time:</strong> ${new Date(result.timestamp).toLocaleString()}</div>
                    </div>
                `;
            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">❌ ${error.message}</div>`;
            }
        });
        
        // Assignment form
        document.getElementById('assignmentForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const resultsDiv = document.getElementById('assignmentResults');
            resultsDiv.innerHTML = '<div class="loading">🔄 Processing SR assignments with predictions...</div>';
            
            try {
                const response = await fetch('/api/assign', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                
                if (result.success) {
                    const summary = result.summary;
                    const assignments = result.assignments || [];
                    
                    // Build complexity breakdown
                    let complexityHtml = '';
                    for (const [complexity, count] of Object.entries(summary.by_complexity || {})) {
                        complexityHtml += `<div class="result-item"><strong>${complexity}:</strong> ${count} tickets</div>`;
                    }
                    
                    // Build prediction breakdown
                    let predictionHtml = '';
                    for (const [pred, count] of Object.entries(summary.by_prediction || {})) {
                        predictionHtml += `<div class="result-item"><strong>${pred}:</strong> ${count} tickets</div>`;
                    }
                    
                    // Build assignments table
                    let assignmentsHtml = '<table style="width: 100%; border-collapse: collapse; margin-top: 15px;">';
                    assignmentsHtml += '<tr style="background: #f8f9fa; font-weight: bold;"><th style="padding: 10px; border: 1px solid #ddd;">SR Number</th><th style="padding: 10px; border: 1px solid #ddd;">Complexity</th><th style="padding: 10px; border: 1px solid #ddd;">Prediction</th><th style="padding: 10px; border: 1px solid #ddd;">Assigned To</th><th style="padding: 10px; border: 1px solid #ddd;">Interface?</th></tr>';
                    
                    assignments.slice(0, 10).forEach(a => {
                        const isInterface = (a.operational_cat && (a.operational_cat.toLowerCase().includes('provisioning') || a.operational_cat.toLowerCase().includes('interface'))) || 
                                          (a.prediction && a.prediction.primary_classification === 'Amdocs');
                        const interfaceBadge = isInterface ? '<span style="background: #ff6b6b; color: white; padding: 2px 8px; border-radius: 3px;">⚠️ Interface</span>' : '';
                        
                        assignmentsHtml += `
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">${a.sr_number || 'N/A'}</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">${a.complexity || 'N/A'}</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">${a.prediction ? a.prediction.primary_classification : 'N/A'}</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">${a.assigned_to || 'Unassigned'}</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">${interfaceBadge}</td>
                            </tr>
                        `;
                    });
                    assignmentsHtml += '</table>';
                    
                    resultsDiv.innerHTML = `
                        <div class="success">
                            ✅ ${result.message}
                        </div>
                        <div class="feature-grid" style="margin-top: 15px;">
                            <div class="feature-box">
                                <h4>Total Tickets</h4>
                                <p>${summary.total || 0}</p>
                            </div>
                            <div class="feature-box" style="background: linear-gradient(135deg, #ff6b6b 0%, #c92a2a 100%);">
                                <h4>Interface Issues</h4>
                                <p>${summary.interface_issues || 0}</p>
                                <small>${(summary.interface_percentage || 0).toFixed(1)}% need workarounds</small>
                            </div>
                            <div class="feature-box" style="background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);">
                                <h4>Easy Tickets</h4>
                                <p>${summary.by_complexity?.Easy || 0}</p>
                                <small>For Junior Members</small>
                            </div>
                        </div>
                        <div class="result-card">
                            <h3>📊 Complexity Breakdown</h3>
                            ${complexityHtml}
                        </div>
                        <div class="result-card">
                            <h3>🎯 Prediction Breakdown</h3>
                            ${predictionHtml}
                        </div>
                        <div class="result-card">
                            <h3>👥 Assignment Preview (First 10)</h3>
                            ${assignmentsHtml}
                            ${assignments.length > 10 ? `<p style="margin-top: 10px; color: #666;"><em>...and ${assignments.length - 10} more assignments</em></p>` : ''}
                        </div>
                        ${result.reports && result.reports.excel ? `
                        <div class="result-card">
                            <h3>📥 Download Reports</h3>
                            <div class="result-item">
                                <strong>Excel Report:</strong> <a href="/${result.reports.excel}" download style="color: #667eea;">Download Assignment Report</a>
                            </div>
                            <div class="result-item">
                                <strong>JSON Report:</strong> <a href="/${result.reports.json}" download style="color: #667eea;">Download JSON Data</a>
                            </div>
                        </div>
                        ` : ''}
                    `;
                } else {
                    resultsDiv.innerHTML = `<div class="error">❌ ${result.error}${result.traceback ? '<pre style="margin-top: 10px; font-size: 11px;">' + result.traceback + '</pre>' : ''}</div>`;
                }
            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">❌ ${error.message}</div>`;
            }
        });
        
        // Analysis form
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
                
                if (result.success) {
                    resultsDiv.innerHTML = `
                        <div class="success">✅ ${result.message}</div>
                        <div class="result-card">
                            <pre>${JSON.stringify(result.analysis, null, 2)}</pre>
                        </div>
                    `;
                } else {
                    resultsDiv.innerHTML = `<div class="error">❌ ${result.error}</div>`;
                }
            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">❌ ${error.message}</div>`;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main unified interface"""
    return render_template_string(COMPLETE_UNIFIED_HTML)

@app.route('/api/predict', methods=['POST'])
def predict_sr():
    """SR Prediction endpoint"""
    try:
        ticket_data = request.json
        
        # Initialize predictor if needed
        if not unified_system.initialize_predictor():
            return jsonify({
                'error': 'Prediction system not available. Please ensure models are trained by running: python sr_prediction_model.py'
            }), 503
        
        # Make prediction
        result = unified_system.sr_predictor.predict_unified(ticket_data, include_ai_prompt=False)
        
        # Save to log
        unified_system.sr_predictor.save_prediction_log(result)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assign', methods=['POST'])
def assign_sr():
    """SR Assignment endpoint - integrated with intelligent assignment system"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
        file.save(file_path)
        
        # Import and use intelligent assignment system
        from intelligent_sr_assignment_with_prediction import IntelligentSRAssignmentWithPrediction
        
        processor = IntelligentSRAssignmentWithPrediction()
        result = processor.process_todays_file(file_path, filter_status='In Progress')
        
        if result['success']:
            # Format for web display
            summary = result['summary']
            assignments = result['assignments']
            
            # Count interface issues
            interface_count = sum(1 for a in assignments 
                                 if 'provisioning' in a['operational_cat'].lower() 
                                 or 'interface' in a['operational_cat'].lower()
                                 or (a.get('prediction') and a['prediction'].get('primary_classification') == 'Amdocs'))
            
            web_result = {
                'success': True,
                'total_tickets': result['total_tickets'],
                'summary': {
                    'total': summary['total_tickets'],
                    'by_complexity': summary['by_complexity'],
                    'by_prediction': summary.get('by_prediction', {}),
                    'interface_issues': interface_count,
                    'interface_percentage': (interface_count / summary['total_tickets'] * 100) if summary['total_tickets'] > 0 else 0
                },
                'assignments': assignments[:10],  # First 10 for display
                'reports': {
                    'json': result.get('output_file', ''),
                    'excel': result.get('excel_file', '')
                },
                'message': f'Successfully analyzed {result["total_tickets"]} tickets. {interface_count} likely need workarounds.'
            }
            
            return jsonify(web_result)
        else:
            return jsonify(result)
    
    except Exception as e:
        import traceback
        return jsonify({
            'success': False, 
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_patterns():
    """Pattern Analysis endpoint - integrated with existing system"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
        file.save(file_path)
        
        # Process with existing pattern analyzer
        result = unified_system.process_file_for_analysis(file_path)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'prediction_available': PREDICTION_AVAILABLE,
        'predictor_initialized': unified_system.predictor_initialized,
        'assignment_available': True,
        'analysis_available': True
    })

def main():
    """Main entry point"""
    print("=" * 80)
    print("COMPLETE UNIFIED SR SYSTEM")
    print("=" * 80)
    print("\n🚀 Initializing all systems...")
    print("\n📦 Available Features:")
    print("  ✅ SR Assignment (Team-based routing)")
    print("  ✅ Pattern Analysis (Trend identification)")
    if PREDICTION_AVAILABLE:
        print("  ✅ SR Prediction (ML-powered classification)")
    else:
        print("  ⚠️  SR Prediction (Not available - models not trained)")
        print("      Run: python sr_prediction_model.py")
    
    print("\n🌐 Starting web server...")
    print("📍 Access at: http://localhost:5000")
    print("\n💡 Press Ctrl+C to stop")
    print("=" * 80)
    
    # Create directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Start Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()

