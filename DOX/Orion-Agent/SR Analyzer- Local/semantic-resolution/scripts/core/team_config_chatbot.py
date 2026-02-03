"""
Team Configuration Chatbot
Natural language interface for managing team skills and configurations
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from scripts.utilities.people_skills_database import PeopleSkillsDatabase
from datetime import datetime
import json

class TeamConfigChatbot:
    """
    Natural language chatbot for team configuration management
    """
    
    def __init__(self, db_path: str = "people_skills.db"):
        self.db = PeopleSkillsDatabase(db_path)
        self.current_member = None
        self.conversation_context = {}
        
        # Command patterns for natural language processing
        self.command_patterns = {
            'view_team': [
                r'show\s+team',
                r'list\s+team',
                r'view\s+team',
                r'who\s+is\s+on\s+team',
                r'team\s+members',
                r'show\s+team\s+skills',
                r'team\s+skills',
                r'team\s+configuration',
                r'team\s+matrix'
            ],
            'view_member': [
                r'show\s+(?P<name>[\w\s]+)\s+skills?',
                r'(?P<name>[\w\s]+)\s+details',
                r'view\s+(?P<name>[\w\s]+)',
                r'info\s+(?P<name>[\w\s]+)'
            ],
            'update_skill': [
                r'set\s+(?P<name>[\w\s]+?)\s+(?P<app>\w+)\s+skill\s+to\s+(?P<level>[\d.]+)',
                r'update\s+(?P<name>[\w\s]+?)\s+(?P<app>\w+)\s+level\s+(?P<level>[\d.]+)',
                r'(?P<name>[\w\s]+?)\s+(?P<app>\w+)\s+skill\s+(?P<level>[\d.]+)',
                r'change\s+(?P<name>[\w\s]+?)\s+(?P<app>\w+)\s+skill\s+to\s+(?P<level>[\d.]+)'
            ],
            'update_load': [
                r'set\s+(?P<name>[\w\s]+?)\s+(?P<app>\w+)\s+max\s+load\s+to\s+(?P<load>\d+)',
                r'change\s+(?P<name>[\w\s]+?)\s+(?P<app>\w+)\s+load\s+to\s+(?P<load>\d+)',
                r'set\s+(?P<name>[\w\s]+?)\s+(?P<app>\w+)\s+load\s+to\s+(?P<load>\d+)',
                r'update\s+(?P<name>[\w\s]+?)\s+(?P<app>\w+)\s+load\s+(?P<load>\d+)',
                r'(?P<name>[\w\s]+?)\s+(?P<app>\w+)\s+max\s+load\s+(?P<load>\d+)',
                r'update\s+(?P<name>[\w\s]+?)\s+(?P<app>\w+)\s+capacity\s+(?P<load>\d+)'
            ],
            'add_specialization': [
                r'add\s+(?P<spec>[\w\s-]+)\s+to\s+(?P<name>[\w\s]+)\s+(?P<app>\w+)',
                r'(?P<name>[\w\s]+)\s+(?P<app>\w+)\s+add\s+(?P<spec>[\w\s-]+)',
                r'give\s+(?P<name>[\w\s]+)\s+(?P<spec>[\w\s-]+)\s+skill'
            ],
            'skill_evolution': [
                r'show\s+skill\s+changes',
                r'evolution\s+report',
                r'ml\s+updates',
                r'learning\s+progress'
            ],
            'export_config': [
                r'export\s+config',
                r'download\s+team\s+config',
                r'save\s+configuration'
            ]
        }
        
        # Name mappings for flexible recognition
        self.name_mappings = {
            'prateek': 'Prateek Jain',
            'prateek jain': 'Prateek Jain',
            'akshit': 'Akshit Kaushik',
            'akshit kaushik': 'Akshit Kaushik',
            'anamika': 'Anamika Thakur',
            'anamika thakur': 'Anamika Thakur',
            'smitesh': 'Smitesh Kadia',
            'smitesh kadia': 'Smitesh Kadia',
            'vidit': 'Vidit Nayal',
            'vidit nayal': 'Vidit Nayal'
        }
        
        # Application mappings
        self.app_mappings = {
            'som': 'SOM_MM',
            'som_mm': 'SOM_MM',
            'sqo': 'SQO_MM',
            'sqo_mm': 'SQO_MM',
            'billing': 'BILLING_MM',
            'billing_mm': 'BILLING_MM'
        }
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process natural language message and return response"""
        message_lower = message.lower().strip()
        
        # Identify command type and extract parameters
        command_type, params = self._parse_command(message_lower)
        
        if command_type == 'view_team':
            return self._handle_view_team()
        
        elif command_type == 'view_member':
            return self._handle_view_member(params)
        
        elif command_type == 'update_skill':
            return self._handle_update_skill(params)
        
        elif command_type == 'update_load':
            return self._handle_update_load(params)
        
        elif command_type == 'add_specialization':
            return self._handle_add_specialization(params)
        
        elif command_type == 'skill_evolution':
            return self._handle_skill_evolution()
        
        elif command_type == 'export_config':
            return self._handle_export_config()
        
        else:
            return self._handle_unknown_command(message)
    
    def _parse_command(self, message: str) -> Tuple[str, Dict[str, Any]]:
        """Parse natural language command"""
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    params = match.groupdict() if hasattr(match, 'groupdict') else {}
                    
                    # Clean and map names
                    if 'name' in params:
                        params['name'] = self._clean_name(params['name'])
                    
                    # Clean and map applications
                    if 'app' in params:
                        params['app'] = self._clean_app(params['app'])
                    
                    return command_type, params
        
        return 'unknown', {}
    
    def _clean_name(self, name: str) -> str:
        """Clean and standardize member names"""
        name_clean = name.strip().lower()
        return self.name_mappings.get(name_clean, name.title())
    
    def _clean_app(self, app: str) -> str:
        """Clean and standardize application names"""
        app_clean = app.strip().lower()
        return self.app_mappings.get(app_clean, app.upper())
    
    def _handle_view_team(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle team viewing commands with enhanced UI"""
        try:
            config = self.db.get_team_configuration()
            
            if not config:
                return {
                    'response': "❌ No team configuration found. Please ensure the People.xlsx file has been loaded.",
                    'type': 'error'
                }
            
            # Generate enhanced team overview
            response = "🎯 **TEAM CONFIGURATION OVERVIEW**\n"
            response += "=" * 50 + "\n\n"
            
            # Team Statistics
            total_members = len(config)
            applications = set()
            total_capacity = 0
            
            for member_data in config.values():
                for app, app_data in member_data['applications'].items():
                    applications.add(app)
                    total_capacity += app_data['max_load']
            
            response += f"📊 **TEAM STATS:**\n"
            response += f"   • Members: **{total_members}** active\n"
            response += f"   • Applications: **{len(applications)}** ({', '.join(sorted(applications))})\n"
            response += f"   • Total Capacity: **{total_capacity} SRs**\n\n"
            
            # Return HTML table for web interface
            return self._create_html_team_skills_display(config, applications)
            
            # Application Coverage Analysis
            response += "🏢 **APPLICATION COVERAGE:**\n"
            response += "-" * 50 + "\n\n"
            
            for app in sorted(applications):
                experts = []
                total_app_capacity = 0
                
                for member_name, member_data in config.items():
                    if app in member_data['applications']:
                        app_data = member_data['applications'][app]
                        skill_level = app_data['skill_level']
                        max_load = app_data['max_load']
                        total_app_capacity += max_load
                        
                        if skill_level >= 3.5:
                            experts.append(f"{member_name} ({skill_level:.1f}/5)")
                
                coverage_indicator = "🟢" if len(experts) >= 2 else "🟡" if len(experts) == 1 else "🔴"
                
                response += f"📱 **{app}**: {total_app_capacity} SRs capacity {coverage_indicator}\n"
                
                if experts:
                    response += f"   • Experts: {', '.join(experts)}\n"
                else:
                    response += f"   • ⚠️ No expert-level members (3.5+ skill)\n"
                
                response += "\n"
            
            # Quick Actions
            response += "⚡ **QUICK ACTIONS:**\n"
            response += "   • View individual: `Show [Name] skills`\n"
            response += "   • Update skills: `Set [Name] [App] skill to [Level]`\n"
            response += "   • Adjust capacity: `Update [Name] [App] load [Number]`\n"
            response += "   • Track progress: `Show skill evolution`\n\n"
            
            response += "=" * 50 + "\n"
            response += f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            return {
                'response': response,
                'type': 'enhanced_team_overview',
                'data': config,
                'suggestions': [
                    'Show Prateek Jain skills',
                    'Update skill levels',
                    'Show skill evolution',
                    'Export configuration',
                    'View capacity analysis'
                ]
            }
            
        except Exception as e:
            return {
                'response': f"❌ Error retrieving team configuration: {str(e)}",
                'type': 'error'
            }
    
    def _create_team_skills_table(self, config: dict, applications: set) -> str:
        """Create a formatted table showing team skills overview"""
        try:
            table = "\n"
            applications = sorted(applications)
            
            # Table header
            table += f"{'MEMBER':<18} | {'STATUS':<8} | "
            for app in applications:
                table += f"{app:<10} | "
            table += f"{'CAPACITY':<10} | {'OVERALL':<12}\n"
            
            table += "-" * (18 + 11 + len(applications) * 13 + 12 + 14) + "\n"
            
            # Member rows
            for member_name, member_data in config.items():
                status_indicator = "✅ ACT" if member_data['status'] == 'active' else "❌ INA"
                
                # Calculate overall metrics
                skill_levels = [app_data['skill_level'] for app_data in member_data['applications'].values()]
                avg_skill = sum(skill_levels) / len(skill_levels) if skill_levels else 0
                max_capacity = max((app_data['max_load'] for app_data in member_data['applications'].values()), default=0)
                
                # Overall indicator
                if avg_skill >= 4.0:
                    overall = "🚀 EXPERT"
                elif avg_skill >= 3.0:
                    overall = "⭐ SENIOR"
                elif avg_skill >= 2.0:
                    overall = "📘 MID"
                else:
                    overall = "🌱 JUNIOR"
                
                # Start row
                row = f"{member_name:<18} | {status_indicator:<8} | "
                
                # Add skill levels for each application
                for app in applications:
                    if app in member_data['applications']:
                        skill_level = member_data['applications'][app]['skill_level']
                        if skill_level >= 4.0:
                            app_skill = f"🏆 {skill_level:.1f}"
                        elif skill_level >= 3.0:
                            app_skill = f"⭐ {skill_level:.1f}"
                        elif skill_level >= 2.0:
                            app_skill = f"📘 {skill_level:.1f}"
                        else:
                            app_skill = f"🌱 {skill_level:.1f}"
                        row += f"{app_skill:<10} | "
                    else:
                        row += f"{'N/A':<10} | "
                
                # Add capacity and overall
                capacity_indicator = "🔥" if max_capacity >= 15 else "⚡" if max_capacity >= 10 else "🔋"
                row += f"{capacity_indicator} {max_capacity:<6} | {overall:<12}\n"
                
                table += row
            
            return table
            
        except Exception as e:
            return f"Error creating team skills table: {str(e)}\n"
    
    def _create_individual_member_table(self, member_name: str, member_data: dict) -> str:
        """Create a detailed skills table for an individual member"""
        try:
            # Calculate overall metrics
            skill_levels = [app_data['skill_level'] for app_data in member_data['applications'].values()]
            avg_skill = sum(skill_levels) / len(skill_levels)
            avg_confidence = sum(app_data['confidence_score'] for app_data in member_data['applications'].values()) / len(member_data['applications'])
            max_capacity = max(app_data['max_load'] for app_data in member_data['applications'].values())
            
            # Member summary
            skill_indicator = "🚀 EXPERT" if avg_skill >= 4.0 else "⭐ SENIOR" if avg_skill >= 3.0 else "📘 MID" if avg_skill >= 2.0 else "🌱 JUNIOR"
            confidence_indicator = "🎯 HIGH" if avg_confidence >= 0.8 else "🔍 MED" if avg_confidence >= 0.6 else "⚠️ LOW"
            
            table = f"📈 Overall: {avg_skill:.1f}/5 {skill_indicator} | Confidence: {avg_confidence:.2f} {confidence_indicator} | Capacity: {max_capacity} SRs\n\n"
            
            # Skills table header
            table += f"{'APP':<12} | {'SKILL':<12} | {'CONFIDENCE':<10} | {'CAPACITY':<10} | {'KEY SPECIALIZATIONS':<30}\n"
            table += "-" * 75 + "\n"
            
            # Application rows
            for app, app_data in member_data['applications'].items():
                skill_level = app_data['skill_level']
                confidence = app_data['confidence_score']
                max_load = app_data['max_load']
                
                # Skill level with emoji
                if skill_level >= 4.0:
                    skill_display = f"🏆 {skill_level:.1f}/5"
                elif skill_level >= 3.0:
                    skill_display = f"⭐ {skill_level:.1f}/5"
                elif skill_level >= 2.0:
                    skill_display = f"📘 {skill_level:.1f}/5"
                else:
                    skill_display = f"🌱 {skill_level:.1f}/5"
                
                # Confidence with emoji
                confidence_emoji = "🎯" if confidence >= 0.8 else "🔍" if confidence >= 0.6 else "⚠️"
                confidence_display = f"{confidence_emoji} {confidence:.2f}"
                
                # Capacity with emoji
                load_emoji = "🔥" if max_load >= 15 else "⚡" if max_load >= 10 else "🔋"
                capacity_display = f"{load_emoji} {max_load}"
                
                # Top specializations (truncate if too long)
                specs = app_data['specializations'][:2]  # Top 2
                specs_display = ', '.join(specs) if specs else "None"
                if len(specs_display) > 28:
                    specs_display = specs_display[:25] + "..."
                
                table += f"{app:<12} | {skill_display:<12} | {confidence_display:<10} | {capacity_display:<10} | {specs_display:<30}\n"
            
            return table
            
        except Exception as e:
            return f"Error creating member skills table: {str(e)}\n"
    
    def _create_html_team_skills_display(self, config: dict, applications: set) -> dict:
        """Create comprehensive HTML team skills display for web interface"""
        try:
            # Calculate team statistics
            total_members = len(config)
            total_capacity = sum(
                max(app_data['max_load'] for app_data in member_data['applications'].values())
                for member_data in config.values()
            )
            
            applications = sorted(applications)
            
            # Generate HTML response
            html_content = f"""
            <div class="team-config-dashboard">
                <div class="dashboard-header">
                    <h2>🎯 Team Configuration Overview</h2>
                    <p class="subtitle">Comprehensive team skills and capacity analysis</p>
                </div>
                
                <!-- Team Statistics Cards -->
                <div class="stats-overview">
                    <div class="stat-card">
                        <div class="stat-icon">👥</div>
                        <div class="stat-content">
                            <div class="stat-number">{total_members}</div>
                            <div class="stat-label">Active Members</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">🏢</div>
                        <div class="stat-content">
                            <div class="stat-number">{len(applications)}</div>
                            <div class="stat-label">Applications</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">⚡</div>
                        <div class="stat-content">
                            <div class="stat-number">{total_capacity}</div>
                            <div class="stat-label">Total Capacity</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">📊</div>
                        <div class="stat-content">
                            <div class="stat-number">{total_capacity // total_members}</div>
                            <div class="stat-label">Avg per Member</div>
                        </div>
                    </div>
                </div>
                
                <!-- Main Skills Matrix Table -->
                <div class="table-section">
                    <h3>🔧 Team Skills Matrix</h3>
                    <div class="table-responsive">
                        <table class="skills-matrix-table">
                            <thead>
                                <tr>
                                    <th class="member-header">Team Member</th>
                                    <th class="status-header">Status</th>
            """
            
            # Add dynamic application headers
            for app in applications:
                html_content += f'<th class="app-header">{app}</th>'
            
            html_content += """
                                    <th class="capacity-header">Max Capacity</th>
                                    <th class="overall-header">Overall</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            
            # Add team member rows
            for member_name, member_data in config.items():
                status_class = "active" if member_data['status'] == 'active' else "inactive"
                status_display = "✅ Active" if member_data['status'] == 'active' else "❌ Inactive"
                
                # Calculate member metrics
                skill_levels = [app_data['skill_level'] for app_data in member_data['applications'].values()]
                avg_skill = sum(skill_levels) / len(skill_levels) if skill_levels else 0
                max_capacity = max((app_data['max_load'] for app_data in member_data['applications'].values()), default=0)
                
                # Overall classification
                if avg_skill >= 4.0:
                    overall_class = "expert"
                    overall_text = "🏆 Expert"
                elif avg_skill >= 3.0:
                    overall_class = "senior"
                    overall_text = "⭐ Senior"
                elif avg_skill >= 2.0:
                    overall_class = "mid"
                    overall_text = "📘 Mid-Level"
                else:
                    overall_class = "junior"
                    overall_text = "🌱 Junior"
                
                html_content += f"""
                                <tr class="member-row {status_class}">
                                    <td class="member-cell">
                                        <div class="member-info">
                                            <strong>{member_name}</strong>
                                            <div class="member-avg">Avg: {avg_skill:.1f}/5</div>
                                        </div>
                                    </td>
                                    <td class="status-cell {status_class}">{status_display}</td>
                """
                
                # Add skill cells for each application
                for app in applications:
                    if app in member_data['applications']:
                        app_data = member_data['applications'][app]
                        skill_level = app_data['skill_level']
                        confidence = app_data['confidence_score']
                        
                        # Skill level styling
                        if skill_level >= 4.5:
                            skill_class = "expert-plus"
                            skill_icon = "🏆"
                        elif skill_level >= 4.0:
                            skill_class = "expert"
                            skill_icon = "🥇"
                        elif skill_level >= 3.5:
                            skill_class = "senior-plus"
                            skill_icon = "⭐"
                        elif skill_level >= 3.0:
                            skill_class = "senior"
                            skill_icon = "🔸"
                        elif skill_level >= 2.0:
                            skill_class = "mid"
                            skill_icon = "📘"
                        else:
                            skill_class = "junior"
                            skill_icon = "🌱"
                        
                        html_content += f"""
                                    <td class="skill-cell {skill_class}">
                                        <div class="skill-info">
                                            <span class="skill-icon">{skill_icon}</span>
                                            <span class="skill-level">{skill_level:.1f}/5</span>
                                            <small class="confidence">({confidence:.2f})</small>
                                        </div>
                                    </td>
                        """
                    else:
                        html_content += '<td class="skill-cell na">N/A</td>'
                
                # Capacity and overall cells
                capacity_class = "high" if max_capacity >= 15 else "medium" if max_capacity >= 10 else "low"
                capacity_icon = "🔥" if max_capacity >= 15 else "⚡" if max_capacity >= 10 else "🔋"
                
                html_content += f"""
                                    <td class="capacity-cell {capacity_class}">
                                        <span class="capacity-icon">{capacity_icon}</span>
                                        <span class="capacity-value">{max_capacity} SRs</span>
                                    </td>
                                    <td class="overall-cell {overall_class}">{overall_text}</td>
                                </tr>
                """
            
            # Complete the skills matrix table
            html_content += """
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Application Coverage Analysis -->
                <div class="coverage-section">
                    <h3>🏢 Application Coverage Analysis</h3>
                    <div class="table-responsive">
                        <table class="coverage-analysis-table">
                            <thead>
                                <tr>
                                    <th>Application</th>
                                    <th>Total Capacity</th>
                                    <th>Expert Count</th>
                                    <th>Senior Count</th>
                                    <th>Coverage Status</th>
                                    <th>Key Personnel</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            
            # Add application coverage rows
            for app in applications:
                experts = []
                seniors = []
                app_capacity = 0
                
                for member_name, member_data in config.items():
                    if app in member_data['applications']:
                        app_data = member_data['applications'][app]
                        skill_level = app_data['skill_level']
                        max_load = app_data['max_load']
                        app_capacity += max_load
                        
                        if skill_level >= 4.0:
                            experts.append(f"{member_name} ({skill_level:.1f})")
                        elif skill_level >= 3.0:
                            seniors.append(f"{member_name} ({skill_level:.1f})")
                
                # Coverage assessment
                if len(experts) >= 2:
                    coverage_class = "strong"
                    coverage_text = "🟢 Strong"
                elif len(experts) == 1 or len(seniors) >= 2:
                    coverage_class = "adequate"
                    coverage_text = "🟡 Adequate"
                else:
                    coverage_class = "weak"
                    coverage_text = "🔴 At Risk"
                
                key_personnel = ', '.join((experts + seniors)[:3]) if experts or seniors else 'None'
                if len(key_personnel) > 40:
                    key_personnel = key_personnel[:37] + '...'
                
                html_content += f"""
                                <tr class="coverage-row {coverage_class}">
                                    <td class="app-name"><strong>{app}</strong></td>
                                    <td class="capacity-value">{app_capacity} SRs</td>
                                    <td class="expert-count">{len(experts)}</td>
                                    <td class="senior-count">{len(seniors)}</td>
                                    <td class="coverage-status {coverage_class}">{coverage_text}</td>
                                    <td class="personnel-list">{key_personnel}</td>
                                </tr>
                """
            
            # Complete the HTML with styling
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            html_content += f"""
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Quick Actions Panel -->
                <div class="actions-panel">
                    <h3>⚡ Quick Actions</h3>
                    <div class="action-grid">
                        <button class="action-btn primary" onclick="updateMemberSkill()">
                            <span class="btn-icon">📝</span>
                            Update Member Skills
                        </button>
                        <button class="action-btn secondary" onclick="adjustCapacity()">
                            <span class="btn-icon">⚡</span>
                            Adjust Capacity
                        </button>
                        <button class="action-btn info" onclick="viewMemberDetails()">
                            <span class="btn-icon">👤</span>
                            View Member Details
                        </button>
                        <button class="action-btn success" onclick="exportTeamConfig()">
                            <span class="btn-icon">📊</span>
                            Export Configuration
                        </button>
                    </div>
                </div>
                
                <div class="footer-timestamp">
                    <p>📅 Generated: {current_time} | 🔄 Real-time team configuration</p>
                </div>
            </div>
            
            <style>
            .team-config-dashboard {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                border-radius: 15px;
            }}
            
            .dashboard-header {{
                text-align: center;
                margin-bottom: 35px;
            }}
            
            .dashboard-header h2 {{
                color: #1a202c;
                font-size: 2.8em;
                margin: 0;
                font-weight: 700;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .subtitle {{
                color: #64748b;
                font-size: 1.2em;
                margin: 10px 0 0 0;
                font-weight: 300;
            }}
            
            .stats-overview {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 25px;
                margin-bottom: 40px;
            }}
            
            .stat-card {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                display: flex;
                align-items: center;
                border-left: 5px solid #3b82f6;
                transition: transform 0.3s ease;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
            }}
            
            .stat-icon {{
                font-size: 3em;
                margin-right: 25px;
                opacity: 0.8;
            }}
            
            .stat-number {{
                font-size: 2.5em;
                font-weight: bold;
                color: #1e40af;
                line-height: 1;
            }}
            
            .stat-label {{
                color: #64748b;
                font-size: 1em;
                margin-top: 8px;
                font-weight: 500;
            }}
            
            .table-section, .coverage-section {{
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            }}
            
            .table-section h3, .coverage-section h3 {{
                margin: 0 0 25px 0;
                color: #1a202c;
                font-size: 1.8em;
                font-weight: 600;
            }}
            
            .table-responsive {{
                overflow-x: auto;
            }}
            
            .skills-matrix-table, .coverage-analysis-table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 10px;
                overflow: hidden;
            }}
            
            .skills-matrix-table th, .coverage-analysis-table th {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 18px 15px;
                text-align: left;
                font-weight: 600;
                font-size: 1em;
                border: none;
            }}
            
            .skills-matrix-table td, .coverage-analysis-table td {{
                padding: 15px;
                border-bottom: 1px solid #e2e8f0;
                vertical-align: middle;
            }}
            
            .member-row:hover {{
                background-color: #f1f5f9;
            }}
            
            .member-cell {{
                min-width: 180px;
            }}
            
            .member-info strong {{
                font-size: 1.1em;
                color: #1a202c;
            }}
            
            .member-avg {{
                color: #64748b;
                font-size: 0.85em;
                margin-top: 3px;
            }}
            
            .status-cell.active {{
                color: #059669;
                font-weight: 600;
            }}
            
            .status-cell.inactive {{
                color: #dc2626;
                font-weight: 600;
            }}
            
            .skill-cell {{
                text-align: center;
                min-width: 110px;
            }}
            
            .skill-info {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 3px;
            }}
            
            .skill-icon {{
                font-size: 1.3em;
            }}
            
            .skill-level {{
                font-weight: 600;
                font-size: 0.95em;
            }}
            
            .confidence {{
                color: #64748b;
                font-size: 0.75em;
            }}
            
            .skill-cell.expert-plus {{ background-color: #fef3c7; color: #92400e; }}
            .skill-cell.expert {{ background-color: #dcfce7; color: #166534; }}
            .skill-cell.senior-plus {{ background-color: #fef3c7; color: #d97706; }}
            .skill-cell.senior {{ background-color: #dbeafe; color: #1d4ed8; }}
            .skill-cell.mid {{ background-color: #f0f9ff; color: #0369a1; }}
            .skill-cell.junior {{ background-color: #f9fafb; color: #374151; }}
            .skill-cell.na {{ background-color: #f9fafb; color: #9ca3af; }}
            
            .capacity-cell {{
                text-align: center;
                font-weight: 600;
            }}
            
            .capacity-cell.high {{ color: #dc2626; }}
            .capacity-cell.medium {{ color: #d97706; }}
            .capacity-cell.low {{ color: #059669; }}
            
            .overall-cell {{
                text-align: center;
                font-weight: 600;
                border-radius: 8px;
            }}
            
            .overall-cell.expert {{ background-color: #dcfce7; color: #166534; }}
            .overall-cell.senior {{ background-color: #fef3c7; color: #d97706; }}
            .overall-cell.mid {{ background-color: #dbeafe; color: #1d4ed8; }}
            .overall-cell.junior {{ background-color: #f3e8ff; color: #7c3aed; }}
            
            .coverage-row:hover {{
                background-color: #f7fafc;
            }}
            
            .coverage-status.strong {{ color: #059669; font-weight: 600; }}
            .coverage-status.adequate {{ color: #d97706; font-weight: 600; }}
            .coverage-status.weak {{ color: #dc2626; font-weight: 600; }}
            
            .actions-panel {{
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            }}
            
            .actions-panel h3 {{
                margin: 0 0 25px 0;
                color: #1a202c;
                font-size: 1.8em;
                font-weight: 600;
            }}
            
            .action-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
            }}
            
            .action-btn {{
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 15px 25px;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                color: white;
                font-size: 1em;
            }}
            
            .action-btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            }}
            
            .action-btn.primary {{ background: linear-gradient(135deg, #3b82f6, #1d4ed8); }}
            .action-btn.secondary {{ background: linear-gradient(135deg, #6b7280, #374151); }}
            .action-btn.info {{ background: linear-gradient(135deg, #0ea5e9, #0284c7); }}
            .action-btn.success {{ background: linear-gradient(135deg, #10b981, #059669); }}
            
            .btn-icon {{
                margin-right: 10px;
                font-size: 1.2em;
            }}
            
            .footer-timestamp {{
                text-align: center;
                margin-top: 30px;
                padding-top: 25px;
                border-top: 2px solid #e2e8f0;
                color: #64748b;
                font-size: 1em;
                font-weight: 500;
            }}
            
            @media (max-width: 768px) {{
                .stats-overview {{
                    grid-template-columns: repeat(2, 1fr);
                }}
                
                .action-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .dashboard-header h2 {{
                    font-size: 2.2em;
                }}
            }}
            </style>
            """
            
            return {
                'response': html_content,
                'type': 'enhanced_team_overview',
                'suggestions': [
                    'Update member skills',
                    'Adjust capacity limits',
                    'View individual member details',
                    'Analyze skill gaps',
                    'Export team configuration'
                ]
            }
            
        except Exception as e:
            return {
                'response': f"""
                <div class="alert alert-danger">
                    <h4>❌ Error Loading Team Configuration</h4>
                    <p>An error occurred while retrieving team configuration data.</p>
                    <p><strong>Error details:</strong> {str(e)}</p>
                    <div class="mt-3">
                        <strong>Troubleshooting steps:</strong>
                        <ul>
                            <li>Ensure People.xlsx has been loaded into the database</li>
                            <li>Check database connectivity and table structure</li>
                            <li>Verify team configuration data integrity</li>
                            <li>Try reloading the People.xlsx file</li>
                            <li>Check if the database file exists and is accessible</li>
                        </ul>
                    </div>
                </div>
                """,
                'type': 'error'
            }
    
    def _handle_view_member(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle member detail viewing"""
        member_name = params.get('name', '')
        
        if not member_name:
            return {
                'response': "❌ Please specify a team member name.",
                'type': 'error',
                'suggestions': ['Show Prateek Jain skills', 'View Akshit Kaushik']
            }
        
        try:
            config = self.db.get_team_configuration()
            
            if member_name not in config:
                available_members = ', '.join(config.keys())
                return {
                    'response': f"❌ Member '{member_name}' not found.\n\nAvailable members: {available_members}",
                    'type': 'error',
                    'suggestions': [f'View {name}' for name in list(config.keys())[:3]]
                }
            
            member_data = config[member_name]
            
            response = f"👤 **{member_name}** Details\n\n"
            response += f"Status: {member_data['status']}\n\n"
            
            for app, app_data in member_data['applications'].items():
                response += f"**{app} Application:**\n"
                response += f"  • Skill Level: {app_data['skill_level']:.1f}/5\n"
                response += f"  • Max Load: {app_data['max_load']} SRs\n"
                response += f"  • ML Confidence: {app_data['confidence_score']:.2f}\n"
                response += f"  • Last Updated: {app_data['last_updated']}\n"
                
                specializations = app_data['specializations']
                if specializations:
                    response += f"  • Specializations:\n"
                    for spec in specializations:
                        response += f"    - {spec}\n"
                
                response += "\n"
            
            return {
                'response': response,
                'type': 'member_details',
                'data': {member_name: member_data},
                'suggestions': [
                    f'Update {member_name} SOM_MM skill to 4.5',
                    f'Set {member_name} SOM_MM load to 15',
                    f'Add Provisioning to {member_name} SOM_MM',
                    'Show skill evolution'
                ]
            }
            
        except Exception as e:
            return {
                'response': f"❌ Error retrieving member details: {str(e)}",
                'type': 'error'
            }
    
    def _handle_update_skill(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle skill level updates"""
        member_name = params.get('name', '')
        application = params.get('app', '')
        skill_level = params.get('level', '')
        
        if not all([member_name, application, skill_level]):
            return {
                'response': "❌ Please specify: member name, application, and skill level.\n\nExample: 'Set Prateek Jain SOM_MM skill to 4.5'",
                'type': 'error',
                'suggestions': [
                    'Set Prateek Jain SOM_MM skill to 4.5',
                    'Update Akshit Kaushik SQO_MM level 3.8'
                ]
            }
        
        try:
            skill_level_float = float(skill_level)
            if not (1.0 <= skill_level_float <= 5.0):
                return {
                    'response': "❌ Skill level must be between 1.0 and 5.0",
                    'type': 'error'
                }
            
            # Get current skill level for comparison
            config = self.db.get_team_configuration()
            if member_name not in config:
                return {
                    'response': f"❌ Member '{member_name}' not found.",
                    'type': 'error'
                }
            
            if application not in config[member_name]['applications']:
                return {
                    'response': f"❌ Application '{application}' not found for {member_name}.",
                    'type': 'error'
                }
            
            old_level = config[member_name]['applications'][application]['skill_level']
            
            # Update skill level
            updates = {
                'application': application,
                'skill_level': skill_level_float
            }
            
            success = self.db.update_member_config_via_chat(member_name, updates, "CHATBOT")
            
            if success:
                change = skill_level_float - old_level
                change_text = f"(+{change:.1f})" if change > 0 else f"({change:.1f})"
                
                response = f"✅ **Skill Updated Successfully!**\n\n"
                response += f"👤 **{member_name}**\n"
                response += f"📱 **{application}**\n"
                response += f"📊 **Skill Level:** {old_level:.1f} → {skill_level_float:.1f} {change_text}\n\n"
                response += "✅ **Database updated:** Skills table record modified\n"
                response += "✅ **Excel updated:** People.xlsx file synchronized\n\n"
                response += "The change has been logged and will be considered by the ML learning system."
                
                return {
                    'response': response,
                    'type': 'skill_updated',
                    'data': {
                        'member': member_name,
                        'application': application,
                        'old_level': old_level,
                        'new_level': skill_level_float
                    },
                    'suggestions': [
                        f'Update {member_name} max load',
                        f'Add specialization to {member_name}',
                        'Show team overview',
                        'Export configuration'
                    ]
                }
            else:
                return {
                    'response': "❌ Failed to update skill level. Please try again.",
                    'type': 'error'
                }
                
        except ValueError:
            return {
                'response': f"❌ Invalid skill level '{skill_level}'. Please use a number between 1.0 and 5.0",
                'type': 'error'
            }
        except Exception as e:
            return {
                'response': f"❌ Error updating skill: {str(e)}",
                'type': 'error'
            }
    
    def _handle_update_load(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle max load updates"""
        member_name = params.get('name', '')
        application = params.get('app', '')
        max_load = params.get('load', '')
        
        if not all([member_name, application, max_load]):
            return {
                'response': "❌ Please specify: member name, application, and max load.\n\nExample: 'Set Prateek Jain SOM_MM load to 15'",
                'type': 'error'
            }
        
        try:
            max_load_int = int(max_load)
            if not (1 <= max_load_int <= 50):
                return {
                    'response': "❌ Max load must be between 1 and 50",
                    'type': 'error'
                }
            
            # Get current load for comparison
            config = self.db.get_team_configuration()
            if member_name not in config or application not in config[member_name]['applications']:
                return {
                    'response': f"❌ {member_name} {application} configuration not found.",
                    'type': 'error'
                }
            
            old_load = config[member_name]['applications'][application]['max_load']
            
            # Update max load
            updates = {
                'application': application,
                'max_load': max_load_int
            }
            
            success = self.db.update_member_config_via_chat(member_name, updates, "CHATBOT")
            
            if success:
                change = max_load_int - old_load
                change_text = f"(+{change})" if change > 0 else f"({change})"
                
                response = f"✅ **Max Load Updated Successfully!**\n\n"
                response += f"👤 **{member_name}**\n"
                response += f"📱 **{application}**\n"
                response += f"📊 **Max Load:** {old_load} → {max_load_int} {change_text}\n\n"
                response += "✅ **Database updated:** Skills table record modified\n"
                response += "✅ **Excel updated:** People.xlsx file synchronized\n\n"
                response += "The capacity change will be reflected in future assignments."
                
                return {
                    'response': response,
                    'type': 'load_updated',
                    'data': {
                        'member': member_name,
                        'application': application,
                        'old_load': old_load,
                        'new_load': max_load_int
                    },
                    'suggestions': [
                        f'Update {member_name} skill level',
                        f'View {member_name} details',
                        'Show team overview'
                    ]
                }
            else:
                return {
                    'response': "❌ Failed to update max load. Please try again.",
                    'type': 'error'
                }
                
        except ValueError:
            return {
                'response': f"❌ Invalid max load '{max_load}'. Please use a whole number.",
                'type': 'error'
            }
        except Exception as e:
            return {
                'response': f"❌ Error updating max load: {str(e)}",
                'type': 'error'
            }
    
    def _handle_add_specialization(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle adding specializations"""
        member_name = params.get('name', '')
        application = params.get('app', '')
        specialization = params.get('spec', '')
        
        if not all([member_name, application, specialization]):
            return {
                'response': "❌ Please specify: member name, application, and specialization.\n\nExample: 'Add Provisioning to Prateek Jain SOM_MM'",
                'type': 'error'
            }
        
        try:
            specialization = specialization.strip().title()
            
            # Update specialization
            updates = {
                'application': application,
                'add_specialization': specialization
            }
            
            success = self.db.update_member_config_via_chat(member_name, updates, "CHATBOT")
            
            if success:
                response = f"✅ **Specialization Added Successfully!**\n\n"
                response += f"👤 **{member_name}**\n"
                response += f"📱 **{application}**\n"
                response += f"🎯 **Added:** {specialization}\n\n"
                response += "The new specialization will be used in future SR assignments."
                
                return {
                    'response': response,
                    'type': 'specialization_added',
                    'data': {
                        'member': member_name,
                        'application': application,
                        'specialization': specialization
                    },
                    'suggestions': [
                        f'View {member_name} details',
                        f'Add another specialization to {member_name}',
                        'Show team overview'
                    ]
                }
            else:
                return {
                    'response': "❌ Failed to add specialization. It may already exist.",
                    'type': 'error'
                }
                
        except Exception as e:
            return {
                'response': f"❌ Error adding specialization: {str(e)}",
                'type': 'error'
            }
    
    def _handle_skill_evolution(self) -> Dict[str, Any]:
        """Handle skill evolution reports"""
        try:
            evolution = self.db.get_skill_evolution_report(days=30)
            
            if evolution['total_changes'] == 0:
                return {
                    'response': "📈 **No skill evolution in the last 30 days.**\n\nThe system is ready to learn from new assignment data.",
                    'type': 'evolution_report',
                    'suggestions': [
                        'Process some SRs to generate learning data',
                        'Manually update skills',
                        'View team overview'
                    ]
                }
            
            response = f"📈 **Skill Evolution Report (Last 30 Days)**\n\n"
            response += f"📊 **Summary:**\n"
            response += f"  • Total Changes: {evolution['total_changes']}\n"
            response += f"  • ML Updates: {evolution['summary']['ml_updates']}\n"
            response += f"  • User Updates: {evolution['summary']['user_updates']}\n"
            response += f"  • Avg Confidence: {evolution['summary']['avg_confidence']:.2f}\n\n"
            
            response += f"🔄 **Recent Changes:**\n"
            for change in evolution['changes'][:5]:  # Show last 5 changes
                change_symbol = "📈" if change['change'] > 0 else "📉"
                response += f"{change_symbol} **{change['member']}** {change['application']}: "
                response += f"{change['old_level']:.1f} → {change['new_level']:.1f} "
                response += f"({change['updated_by']})\n"
                response += f"   Reason: {change['reason'][:50]}...\n\n"
            
            return {
                'response': response,
                'type': 'evolution_report',
                'data': evolution,
                'suggestions': [
                    'Export current configuration',
                    'View team overview',
                    'Update skill levels manually'
                ]
            }
            
        except Exception as e:
            return {
                'response': f"❌ Error generating evolution report: {str(e)}",
                'type': 'error'
            }
    
    def _handle_export_config(self) -> Dict[str, Any]:
        """Handle configuration export"""
        try:
            filename = f"team_config_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            success = self.db.export_current_config_to_excel(filename)
            
            if success:
                response = f"✅ **Configuration Exported Successfully!**\n\n"
                response += f"📁 **File:** {filename}\n"
                response += f"📊 **Contains:** Current team skills, loads, and specializations\n"
                response += f"🤖 **ML Confidence:** Included for each skill assessment\n\n"
                response += "You can now download and share the configuration file."
                
                return {
                    'response': response,
                    'type': 'config_exported',
                    'data': {'filename': filename},
                    'suggestions': [
                        'View team overview',
                        'Show skill evolution',
                        'Update team skills'
                    ]
                }
            else:
                return {
                    'response': "❌ Failed to export configuration. Please try again.",
                    'type': 'error'
                }
                
        except Exception as e:
            return {
                'response': f"❌ Error exporting configuration: {str(e)}",
                'type': 'error'
            }
    
    def _handle_unknown_command(self, message: str) -> Dict[str, Any]:
        """Handle unknown commands with helpful suggestions"""
        response = "🤔 **I didn't understand that command.**\n\n"
        response += "Here's what I can help you with:\n\n"
        response += "👥 **Team Management:**\n"
        response += "  • 'Show team' - View all team members\n"
        response += "  • 'View Prateek Jain' - Show member details\n\n"
        response += "🔧 **Configuration Updates:**\n"
        response += "  **Skill Levels (updates both database and Excel):**\n"
        response += "  • 'Set Prateek Jain SOM_MM skill to 4.5'\n"
        response += "  • 'Update Prateek Jain SOM_MM level 4.8'\n\n"
        response += "  **Max Load (updates both database and Excel):**\n"
        response += "  • 'Update Akshit Kaushik SOM_MM load 15'\n"
        response += "  • 'Set Prateek Jain SOM_MM load to 12'\n"
        response += "  • 'Prateek Jain SOM_MM max load 18'\n\n"
        response += "  **Specializations:**\n"
        response += "  • 'Add Provisioning to Prateek Jain SOM_MM'\n\n"
        response += "📊 **Reports:**\n"
        response += "  • 'Show skill evolution' - ML learning progress\n"
        response += "  • 'Export config' - Download team configuration\n"
        
        return {
            'response': response,
            'type': 'help',
            'suggestions': [
                'Show team',
                'View Prateek Jain skills',
                'Show skill evolution',
                'Export config'
            ]
        }

def demo_team_config_chatbot():
    """Demonstrate the team configuration chatbot"""
    print("💬 Team Configuration Chatbot Demo")
    print("=" * 60)
    
    # Initialize chatbot
    chatbot = TeamConfigChatbot()
    
    # Test commands
    test_commands = [
        "show team",
        "view prateek jain",
        "set prateek jain som_mm skill to 4.8",
        "update akshit kaushik som_mm load 12",
        "add billing to prateek jain som_mm",
        "show skill evolution",
        "export config"
    ]
    
    for command in test_commands:
        print(f"\n👤 USER: {command}")
        result = chatbot.process_message(command)
        print(f"🤖 BOT: {result['response'][:200]}...")
        if result.get('suggestions'):
            print(f"💡 Suggestions: {result['suggestions'][:2]}")

if __name__ == "__main__":
    demo_team_config_chatbot()
