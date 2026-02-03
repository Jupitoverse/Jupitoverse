"""
Chat SR Assignment Interface
Provides conversational interface for SR assignment system
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
from scripts.ml_models.enhanced_sr_assignment_system import EnhancedSRAssignmentSystem
from scripts.ml_models.enhanced_ai_nlp import enhanced_nlp
# from enhanced_mukul_sr_assignment import EnhancedMukulSRAssignment  # No longer needed - functionality integrated

class ChatSRAssignmentInterface:
    """
    Conversational interface for SR assignment system
    """
    
    def __init__(self):
        self.assignment_system = EnhancedSRAssignmentSystem()
        self.nlp_processor = enhanced_nlp  # Use singleton from enhanced_ai_nlp
        self.current_availability = None
        self.processed_file = None
        self.session_data = {}
        self.conversation_history = []
        
    def process_message(self, message: str) -> str:
        """Main message processing entry point"""
        message_lower = message.lower()
        
        # PRIORITY 1: Check if user is responding to Mukul application selection (separate from main routing)
        if hasattr(self, 'mukul_session') and self.mukul_session.get('awaiting_selection'):
            return self._handle_mukul_application_selection(message)
        
        # PRIORITY 2: Check if user is responding to legacy application selection
        if self.session_data.get('awaiting_app_selection'):
            return self._handle_mukul_assignment(message)
        
        # PRIORITY 3: Check for Mukul commands first (these don't require processed data)
        mukul_commands = [
            'process mukul', 'mukul assignment', 'assign mukul', 'process Mukul.xls',
            'enhanced mukul', 'mukul enhancement', 'assign mukul srs', 'process mukul file',
            'run mukul assignment', 'mukul sr assignment'
        ]
        
        if any(cmd in message_lower for cmd in mukul_commands):
            return self._handle_mukul_assignment(message)
        
        # Check for specific assignment commands first (regardless of availability status)
        assignment_commands = [
            'show detailed assignments', 'show assignments', 'detailed assignments',
            'show workload', 'team workload', 'show team skills', 'team skills',
            'generate html report', 'html report', 'download excel', 'export excel',
            'download assignments', 'download', 'export assignments', 'save assignments',
            'pull srs', 'pull sr', 'get srs', 'fetch srs', 'realtime pull', 'start scheduler',
            'stop scheduler', 'pull status', 'connection test', 'setup credentials',
            'p0', 'p1', 'p2', 'p3', 'p4', 'priority',  # Priority queries
            'insights', 'generate insights', 'insights report', 'show insights',  # Insights commands
            'weekly', 'week', 'weekly pattern', 'weekly analysis', 'patterns', 'trend',  # Weekly/pattern analysis
            'reassign', 're-assign', 'reprocess', 're-process', 'recalculate'  # Reassignment commands
        ]
        
        # If it's a specific assignment command and we have processed data, handle it
        if any(cmd in message_lower for cmd in assignment_commands):
            if (self.session_data.get('file_processed') or 
                self.session_data.get('processing_results') or 
                self.processed_file):
                return self.process_follow_up_command(message)
        
        # Default flow based on session state
        if not self.current_availability:
            # Check if it's clearly NOT an availability message
            if any(cmd in message_lower for cmd in assignment_commands):
                # Set default availability for assignment commands
                self.current_availability = "Default team availability - all members available"
                return self.process_follow_up_command(message)
            else:
                return self.process_availability_input(message)
        elif not self.processed_file:
            return self.process_file_input(message)
        else:
            return self.process_follow_up_command(message)
        
    def start_session(self):
        """Start a new chat session"""
        self.session_data = {
            'session_id': f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'started_at': datetime.now().isoformat(),
            'availability_set': False,
            'file_processed': False,
            'assignments_generated': False
        }
        
        welcome_message = """
🤖 Hi! I'm your SR Assignment Assistant!

I'll help you process today's Service Requests and assign them to the right team members using our ML system.

Let's start with today's team status. Just tell me who's available, who's out, etc.

For example, you can say:
• "Prateek and Smitesh are available, Anamika is on vacation"
• "Everyone is available today"
• "Prateek available, Smitesh sick, Anamika vacation"
• "All team members available except Anamika who is on training"

I'll understand and set up the assignments accordingly! 😊
"""
        
        self.conversation_history.append({
            'type': 'bot',
            'message': welcome_message,
            'timestamp': datetime.now().isoformat()
        })
        
        return welcome_message
    
    def process_availability_input(self, user_input: str) -> str:
        """Process team availability input using natural language"""
        try:
            # Simple parsing - just set everyone as available by default
            user_input_lower = user_input.lower()
            
            if "everyone" in user_input_lower or "all" in user_input_lower:
                system_format = "Everyone available"
            else:
                # For now, just accept the input as-is
                system_format = user_input
            
            # Set availability in the system
            self.assignment_system.set_daily_team_availability(system_format)
            self.current_availability = system_format
            self.session_data['availability_set'] = True
            
            # Generate friendly response
            friendly_response = f"✅ Team availability set: {system_format}"
            
            # Add next steps
            next_steps = """

🎯 What's next?
• Upload a file: "Process today's SRs" or "Upload Today_SR.xls"
• Or just say: "Process the morning file" or "Load today's data"

📁 Available files: Today_SR.xls, Dump_2025.xlsx, Aug_Dump.xlsx
"""
            
            response = friendly_response + next_steps
            
            self.conversation_history.append({
                'type': 'user',
                'message': user_input,
                'timestamp': datetime.now().isoformat()
            })
            
            self.conversation_history.append({
                'type': 'bot', 
                'message': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            error_response = f"""
😅 Something went wrong while processing that: {str(e)}

Could you try telling me the team status in a different way? 

For example:
• "Prateek is available, Anamika is on vacation"
• "Everyone is here today"
• "Prateek and Smitesh working, Anamika sick"
"""
            return error_response
    
    def process_file_input(self, user_input: str) -> str:
        """Process file upload/processing request using natural language"""
        try:
            # Extract filename from user input
            filename = None
            text = user_input.lower()
            
            # Try to extract filename directly from the message
            import re
            # Look for common file patterns: *.xls, *.xlsx, Mukul, Today_SR, etc.
            file_pattern = r'([A-Za-z0-9_-]+\.(?:xls|xlsx))|mukul|today[_\s]?sr|dump'
            matches = re.findall(file_pattern, text, re.IGNORECASE)
            
            if matches:
                # Get first match
                match = matches[0]
                if isinstance(match, tuple):
                    match = match[0] if match[0] else matches[0]
                
                # Map common references to actual filenames
                if 'mukul' in match.lower():
                    filename = 'Mukul.xls'
                elif 'today' in match.lower() or 'sr' in match.lower():
                    filename = 'Today_SR.xls'
                elif 'dump' in match.lower():
                    filename = 'Dump_2025.xlsx'
                else:
                    filename = match
            
            # If no specific file found, try common patterns
            if not filename:
                # Natural language file references
                if any(word in text for word in ['today', 'daily', 'morning', 'current']):
                    filename = 'Today_SR.xls'
                elif any(word in text for word in ['mukul']):
                    filename = 'Mukul.xls'
                elif any(word in text for word in ['dump', 'large', 'big', 'main']):
                    filename = 'Dump_2025.xlsx'
                elif any(word in text for word in ['august', 'aug', 'previous']):
                    filename = 'Aug_Dump.xlsx'
                elif any(word in text for word in ['people', 'team', 'staff']):
                    filename = 'People.xlsx'
            
            if not filename:
                return """
🤔 Which file would you like me to process?

You can say:
• "Process today's SRs" or "Load the daily file" → Today_SR.xls
• "Process the main dump" or "Load all data" → Dump_2025.xlsx  
• "Process August data" → Aug_Dump.xlsx
• Or just: "Today_SR.xls" or "Dump_2025.xlsx"

📁 Available files: Today_SR.xls, Dump_2025.xlsx, Aug_Dump.xlsx
"""
            
            # Check if file exists
            if not os.path.exists(filename):
                return f"""
❌ File '{filename}' not found.

Available files in directory:
- Today_SR.xls
- Dump_2025.xlsx
- Aug_Dump.xlsx

Please check the filename and try again.
"""
            
            # Reminder about availability if not set
            availability_reminder = ""
            if not self.current_availability or self.current_availability == "Default team availability - all members available":
                availability_reminder = """
💡 **Pro Tip:** Set team availability BEFORE processing for optimal assignments!

**Examples:**
• "Anamika is available half day today"
• "Prateek on vacation, Smitesh available"
• "Everyone available full day"

(Proceeding with default availability - all members at full capacity)

"""
            
            # Process the file with automatic assignment
            processing_results = self.assignment_system.process_excel_file(filename)
            self.processed_file = filename
            self.session_data['file_processed'] = True
            self.session_data['processing_results'] = processing_results
            
            # Automatically assign ALL SRs
            print(f"📁 Auto-assigning {processing_results['file_info']['total_srs']} SRs...")
            assignment_results = processing_results['assignment_results']
            
            # Store assignments for later retrieval
            self.daily_assignments = assignment_results.get('assignments', [])
            
            # Generate comprehensive summary response
            file_info = processing_results['file_info']
            stats = assignment_results['statistics']
            
            response = f"""{availability_reminder}✅ File '{filename}' processed and ALL SRs automatically assigned!

📊 **ASSIGNMENT RESULTS:**
- **Total SRs Processed**: {file_info['total_srs']}
- **Successfully Assigned**: {stats['successfully_assigned']}
- **No Capacity Available**: {stats['workload_exceeded']}
- **Assignment Success Rate**: {(stats['successfully_assigned']/file_info['total_srs']*100):.1f}%

👥 **TEAM WORKLOAD:**
{self._format_team_workload(stats.get('assignee_distribution', {}))}

📈 **APPLICATION BREAKDOWN:**
{self._format_application_breakdown(stats.get('application_distribution', {}))}

📊 **FILTERING SUMMARY:**
- **Total SRs Processed**: {file_info['total_srs']}
- **Eligible for Assignment**: {stats['successfully_assigned'] + stats.get('no_assignee_available', 0)}
- **Filtered Out**: {stats.get('filtered_out', 0)}

🎯 **What's Next?**
• Say "Show detailed assignments" - View assigned SRs with CAS IDs
• Say "Show filtered SRs" - View SRs that were filtered out
• Say "Filter SOM_MM assignments" - Show only SOM_MM assignments  
• Say "Filter SQO_MM assignments" - Show only SQO_MM assignments
• Say "Generate HTML report" - Create professional report
• Say "Download Excel" - Export all results including filtered SRs

🔄 **Need to Update Availability?**
• Set availability: "Anamika is available half day today"
• Then reassign: "Reassign all SRs" or "Reprocess file"

❓ **Which view would you like to see first?**
• Assigned SRs only ({stats['successfully_assigned']} SRs)
• Filtered out SRs ({stats.get('filtered_out', 0)} SRs)
• All SRs together
"""
            
            self.conversation_history.append({
                'type': 'user',
                'message': user_input,
                'timestamp': datetime.now().isoformat()
            })
            
            self.conversation_history.append({
                'type': 'bot',
                'message': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            error_response = f"""
❌ Error processing file: {str(e)}

Please check:
1. File exists and is accessible
2. File is a valid Excel format (.xlsx or .xls)
3. File contains the expected SR data columns

Try again with a different file or check the file format.
"""
            return error_response
    
    def process_follow_up_command(self, user_input: str) -> str:
        """Process follow-up commands after file processing"""
        try:
            command = user_input.lower().strip()
            
            # Check for real-time pulling commands first (these don't require processed data)
            realtime_commands = ['pull sr', 'get sr', 'fetch sr', 'start scheduler', 'stop scheduler', 'pull status', 'connection test', 'setup credential']
            if any(cmd in command for cmd in realtime_commands):
                return self._process_realtime_commands(command)
            
            # Check for processing data in multiple ways
            has_processing_data = (
                self.processed_file or 
                'processing_results' in self.session_data or
                self.session_data.get('file_processed') or
                hasattr(self, 'daily_assignments')
            )
            
            # If no session data, try to load from database
            if not has_processing_data:
                processing_results = self._try_load_from_database()
                if processing_results:
                    has_processing_data = True
                    self.session_data['processing_results'] = processing_results
                    self.session_data['file_processed'] = True
                else:
                    return "❌ Please process a file first before using follow-up commands."
            
            # Get processing results from available sources
            processing_results = self.session_data.get('processing_results')
            
            # If no processing results in session data, try to generate a basic structure
            if not processing_results and hasattr(self, 'daily_assignments'):
                # Create basic processing results from assignments
                processing_results = {
                    'assignment_results': {
                        'assignments': getattr(self, 'daily_assignments', []),
                        'statistics': {'total_srs': len(getattr(self, 'daily_assignments', []))}
                    },
                    'file_info': {'filename': 'Previously processed file'}
                }
            
            # Check for priority-based queries first
            if any(p in command for p in ['p0', 'p1', 'p2', 'p3', 'p4']) and any(word in command for word in ['show', 'assignments', 'list', 'view']):
                # Extract priority level
                priority = None
                for p in ['p0', 'p1', 'p2', 'p3', 'p4']:
                    if p in command:
                        priority = p.upper()
                        break
                if priority:
                    return self._handle_priority_filter(priority, processing_results)
            
            if 'show assignments' in command or 'detailed assignments' in command:
                # Check if we have assignment results or just pattern analysis
                if 'assignment_results' not in processing_results:
                    return self._handle_pattern_only_results(processing_results, 'assignments')
                return self._generate_detailed_assignments(processing_results)
                
            elif 'show workload' in command:
                return self._generate_workload_summary(processing_results)
                
            elif 'show patterns' in command:
                return self._generate_pattern_summary(processing_results)
            
            elif 'insights' in command or 'generate insights' in command:
                return self._generate_insights_report(processing_results)
            
            elif 'weekly' in command or 'week' in command or 'patterns' in command or 'trend' in command:
                return self._generate_weekly_patterns(processing_results)
                
            elif 'generate html report' in command or 'html report' in command:
                return self._generate_html_report_info(processing_results)
                
            elif 'download excel' in command or 'download assignments' in command or (command == 'download' or command.startswith('download ')):
                return self._generate_excel_download_info(processing_results)
                
            elif 'process new file' in command or 'new file' in command:
                return self._reset_for_new_file()
                
            elif 'reassign' in command:
                # Check if it's a full reprocess request or individual SR reassignment
                if any(word in command for word in ['all', 'reprocess', 're-process', 'recalculate', 'again', 'file']):
                    return self._handle_full_reprocess()
                else:
                    return self._handle_reassignment(command)
                
            elif 'team assignments' in command or 'show team assignments' in command:
                return self._generate_detailed_assignments(processing_results)
                
            elif 'filter' in command and ('som' in command or 'sqo' in command or 'billing' in command):
                return self._handle_application_filter(command, processing_results)
                
            elif 'filtered srs' in command or 'show filtered' in command or 'filtered out' in command:
                return self._show_filtered_srs(processing_results)
                
            elif 'export' in command and ('som' in command or 'sqo' in command or 'billing' in command):
                return self._handle_application_export(command, processing_results)
                
            elif 'show team skills' in command or 'team skills' in command:
                # Always return HTML table format for web interface
                return self._generate_team_skills_html_table()
                
            else:
                return """
🤖 **Available Commands:**

**🚀 Enhanced Assignment:**
• "Process Mukul file" - Analyze Mukul.xls with specialization matching
• "Enhanced Mukul assignment" - Run intelligent SR assignment for Mukul data
• "Mukul SR assignment" - Process Mukul SRs with load-aware assignment

**📋 View Assignments:**
• "Show detailed assignments" / "Show team assignments" - View all assignments with CAS IDs
• "Show workload" - Team capacity and distribution
• "Show team skills" - Enhanced team skills matrix with capacity analysis
• "Show team skills HTML" - Interactive HTML table format for web display
• "Process mukul file" - Interactive HTML dashboard with proper tables
• "Process mukul file text" - Text-based dashboard with ASCII tables
• "Filter SOM_MM assignments" - Show only SOM_MM assignments  
• "Filter SQO_MM assignments" - Show only SQO_MM assignments
• "Filter BILLING_MM assignments" - Show only BILLING assignments

**🔄 Manage Assignments:**
• "Reassign all SRs" / "Reprocess file" - Reassign all SRs with updated availability
• "Reassign SR-12345 to Prateek" - Move specific SR (with or without CAS ID)
• "Reassign INC000009607812 to Kiran" - Use incident number directly

**📊 Reports & Export:**
• "Generate HTML report" - Create professional report
• "Download Excel" - Export all assignments to Excel
• "Export SOM_MM Excel" - Export only SOM_MM assignments  
• "Export SQO_MM Excel" - Export only SQO_MM assignments
• "Export BILLING_MM Excel" - Export only BILLING_MM assignments
• "Show patterns" - Pattern analysis results

**⚙️ System:**
• "Process new file" - Start over with a new file
• Set availability: "Prateek available, Anamika vacation, Smitesh sick"

**💡 Examples:**
• "Process Mukul file" - Enhanced specialization-based assignment
• "Show SOM_MM assignments" 
• "Filter SQO_MM assignments"
• "Reassign INC000009607812 to Kiran Jadhav"

What would you like to do?
"""
                
        except Exception as e:
            return f"❌ Error processing command: {str(e)}"
    
    def _process_realtime_commands(self, command: str) -> str:
        """Process real-time SR pulling commands"""
        try:
            from realtime_sr_puller import realtime_puller, PullStatus
            from secure_credential_manager import SecureCredentialManager
            
            if 'pull sr' in command or 'get sr' in command or 'fetch sr' in command:
                print("🚀 Executing manual SR pull...")
                result = realtime_puller.pull_srs_once()
                
                if result.status == PullStatus.SUCCESS:
                    # Store the results so other commands can access them
                    if result.srs_retrieved > 0:
                        self.session_data['file_processed'] = True
                        self.session_data['realtime_pull_results'] = {
                            'timestamp': result.timestamp.isoformat(),
                            'srs_retrieved': result.srs_retrieved,
                            'srs_processed': result.srs_processed,
                            'srs_assigned': result.srs_assigned
                        }
                    
                    return f"""
🎉 **Real-time SR Pull Successful!**

📊 **Results:**
• Retrieved: {result.srs_retrieved} SRs from GSSUTS
• Processed: {result.srs_processed} SRs into database  
• Assigned: {result.srs_assigned} SRs to team members
• Processing time: {result.processing_time:.2f} seconds

✅ Your system is now updated with the latest SRs from GSSUTS!

🎯 **Next steps:**
• "Show detailed assignments" - View new assignments
• "Team workload status" - Check updated capacity
• "Generate HTML report" - Create assignment report
"""
                else:
                    return f"""
❌ **SR Pull Failed**

Error: {result.error_message}

🔧 **Troubleshooting:**
• "Test connection" - Check GSSUTS connectivity
• "Setup credentials" - Update login credentials  
• Check network connectivity to https://gssuts/
"""
            
            elif 'start scheduler' in command:
                realtime_puller.start_scheduler()
                status = realtime_puller.get_status()
                return f"""
🕐 **Automatic Scheduler Started!**

📋 **Configuration:**
• Pull interval: {status['config']['pull_interval_minutes']} minutes
• Auto-assign enabled: {status['config']['auto_assign_enabled']}
• Next pull: {status.get('next_scheduled_pull', 'Soon')}

✅ Your system will now automatically pull and process SRs from GSSUTS every {status['config']['pull_interval_minutes']} minutes!

🛑 Use "stop scheduler" to disable automatic pulling.
"""
            
            elif 'stop scheduler' in command:
                realtime_puller.stop_scheduler()
                return """
🛑 **Automatic Scheduler Stopped**

The system is no longer automatically pulling SRs from GSSUTS.

🔄 **Manual options:**
• "Pull SRs now" - Execute single pull
• "Start scheduler" - Resume automatic pulling
"""
            
            elif 'pull status' in command or 'realtime status' in command:
                status = realtime_puller.get_status()
                last_pull = status.get('last_pull')
                
                status_icon = "🟢" if status['current_status'] == 'success' else \
                             "🟡" if status['current_status'] == 'running' else \
                             "🔴" if status['current_status'] == 'error' else "⚪"
                
                response = f"""
{status_icon} **Real-time Pull Status**

**Current Status:** {status['current_status'].title()}
**Scheduler:** {'🟢 Running' if status['is_running'] else '🔴 Stopped'}

"""
                if last_pull:
                    response += f"""**Last Pull:**
• Time: {last_pull['timestamp'][:19]}
• Retrieved: {last_pull['srs_retrieved']} SRs
• Processed: {last_pull['srs_processed']} SRs
• Assigned: {last_pull['srs_assigned']} SRs
"""
                else:
                    response += "**Last Pull:** No pulls executed yet"
                
                if status.get('next_scheduled_pull'):
                    response += f"\n**Next Scheduled:** {status['next_scheduled_pull']}"
                
                return response
            
            elif 'test connection' in command or 'connection test' in command:
                connection_result = realtime_puller.test_connection()
                auth_result = realtime_puller.manual_authenticate()
                
                conn_icon = "✅" if connection_result.get('connection', False) else "❌"
                auth_icon = "✅" if auth_result else "❌"
                
                return f"""
🧪 **GSSUTS Connection Test**

{conn_icon} **Connection:** {'Successful' if connection_result.get('connection', False) else 'Failed'}
{auth_icon} **Authentication:** {'Successful' if auth_result else 'Failed'}
🌐 **URL:** {connection_result.get('base_url', 'Unknown')}

{'🎉 Ready for real-time SR pulling!' if (connection_result.get('connection', False) and auth_result) else '🔧 Setup required - use "Setup credentials" command'}
"""
            
            elif 'setup credential' in command:
                credential_manager = SecureCredentialManager()
                has_creds = credential_manager.test_credentials('gssuts')
                
                if has_creds:
                    return """
🔐 **Credentials Already Configured**

Your NTNET credentials are already stored securely.

🧪 **Test Commands:**
• "Test connection" - Verify GSSUTS connectivity
• "Pull SRs now" - Try pulling SRs immediately

🔄 To update credentials, use the web interface credential setup form.
"""
                else:
                    return """
🔐 **Credential Setup Required**

To enable real-time SR pulling, you need to configure your NTNET credentials.

📋 **Steps:**
1. Use the web interface credential setup form
2. Enter your NTNET username (e.g., mukulbh)
3. Enter your password
4. Test the connection

🔒 Your credentials will be encrypted and stored securely on this machine.
"""
            
            else:
                return "❌ Unknown real-time command"
                
        except Exception as e:
            return f"❌ Error processing real-time command: {str(e)}"
    
    def _generate_assignments_summary(self, processing_results: Dict) -> str:
        """Generate assignments summary"""
        assignment_results = processing_results['assignment_results']
        
        summary = f"""
📋 ASSIGNMENT SUMMARY

📊 Overall Statistics:
- Total SRs: {assignment_results['assigned_count'] + assignment_results.get('unassigned_count', 0)}
- Successfully Assigned: {assignment_results['assigned_count']}
- Assignment Rate: {assignment_results['assignment_rate']:.1%}

👥 Team Assignments:
"""
        
        if 'assignments_by_member' in assignment_results:
            for member, count in assignment_results['assignments_by_member'].items():
                summary += f"- {member}: {count} SRs\n"
        
        summary += """
📱 Applications Distribution:
"""
        
        if 'assignments_by_application' in assignment_results:
            for app, count in assignment_results['assignments_by_application'].items():
                summary += f"- {app}: {count} SRs\n"
        
        return summary
    
    def _generate_workload_summary(self, processing_results: Dict) -> str:
        """Generate workload summary based on actual assignments"""
        assignment_results = processing_results['assignment_results']
        assignee_distribution = assignment_results['statistics'].get('assignee_distribution', {})
        
        summary = """
⚖️ **TEAM WORKLOAD SUMMARY**

"""
        
        # If we have actual assignments, show them
        if assignee_distribution:
            total_assigned = sum(assignee_distribution.values())
            for assignee, count in sorted(assignee_distribution.items(), key=lambda x: x[1], reverse=True):
                # Map internal names to display names
                display_name = assignee.replace('_', ' ').title()
                percentage = (count / total_assigned * 100) if total_assigned > 0 else 0
                
                summary += f"👤 **{display_name}**:\n"
                summary += f"   📋 Assigned SRs: {count}\n"
                summary += f"   📊 Share of workload: {percentage:.1f}%\n"
                summary += f"   ✅ Status: Active\n\n"
        else:
            # Fallback to team status if no assignments
            team_status = processing_results.get('team_status', {})
            for member, status in team_status.items():
                current_load = status.get('current_workload', 0)
                max_load = status.get('max_workload', 0)
                utilization = (current_load / max_load * 100) if max_load > 0 else 0
                
                summary += f"👤 {member}:\n"
                summary += f"   Current: {current_load}/{max_load} ({utilization:.1f}%)\n"
                summary += f"   Status: {status.get('availability', 'available')}\n\n"
        
        summary += """
🎯 **Actions:**
• "Show detailed assignments" - See individual SRs per person
• "Reassign SR-12345 to [name]" - Move specific SRs
• "Generate HTML report" - Create detailed report
"""
        
        return summary
    
    def _generate_pattern_summary(self, processing_results: Dict) -> str:
        """Generate pattern analysis summary"""
        pattern_analysis = processing_results.get('pattern_analysis', {})
        
        if not pattern_analysis:
            return "⚠️ No pattern analysis data available."
        
        summary = """
🔍 PATTERN ANALYSIS SUMMARY

📊 Application Detection:
"""
        
        app_patterns = pattern_analysis.get('application_patterns', {})
        for app, patterns in app_patterns.items():
            if patterns:
                summary += f"- {app}: {len(patterns)} patterns detected\n"
        
        return summary
    
    def _generate_weekly_patterns(self, processing_results: Dict) -> str:
        """Generate weekly pattern analysis"""
        try:
            import sqlite3
            from datetime import datetime, timedelta
            
            conn = sqlite3.connect('sr_tracking.db')
            cursor = conn.cursor()
            
            # Get data from last 7 days
            seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT 
                    DATE(processed_date) as day,
                    COUNT(*) as total_srs,
                    application,
                    priority
                FROM sr_records
                WHERE DATE(processed_date) >= ?
                GROUP BY DATE(processed_date), application, priority
                ORDER BY DATE(processed_date) DESC
            """, (seven_days_ago,))
            
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return """
📅 **WEEKLY PATTERN ANALYSIS**

⚠️ No data available for the past 7 days.

Please process some SR files first, then try this command again.
"""
            
            # Aggregate data by day
            daily_stats = {}
            app_totals = {}
            priority_totals = {}
            
            for row in rows:
                day, count, app, priority = row
                if day not in daily_stats:
                    daily_stats[day] = {'total': 0, 'apps': {}, 'priorities': {}}
                
                daily_stats[day]['total'] += count
                daily_stats[day]['apps'][app] = daily_stats[day]['apps'].get(app, 0) + count
                daily_stats[day]['priorities'][priority] = daily_stats[day]['priorities'].get(priority, 0) + count
                
                app_totals[app] = app_totals.get(app, 0) + count
                priority_totals[priority] = priority_totals.get(priority, 0) + count
            
            total_week = sum(app_totals.values())
            
            report = f"""
📅 **WEEKLY PATTERN ANALYSIS** (Last 7 Days)
═══════════════════════════════════════════════

📊 **OVERALL SUMMARY**
• Total SRs Processed: {total_week}
• Days with Activity: {len(daily_stats)}
• Average SRs/Day: {total_week / len(daily_stats):.1f}

📈 **DAILY BREAKDOWN**
"""
            # Sort by date
            for day in sorted(daily_stats.keys(), reverse=True):
                stats = daily_stats[day]
                report += f"\n📆 **{day}** - {stats['total']} SRs\n"
                
                # Top apps for this day
                top_apps = sorted(stats['apps'].items(), key=lambda x: x[1], reverse=True)[:3]
                if top_apps:
                    report += "   Applications: " + ", ".join([f"{app}: {count}" for app, count in top_apps]) + "\n"
                
                # Priorities for this day
                priorities = sorted(stats['priorities'].items(), key=lambda x: x[1], reverse=True)
                if priorities:
                    report += "   Priorities: " + ", ".join([f"{p}: {c}" for p, c in priorities]) + "\n"
            
            report += f"""

📱 **APPLICATION TRENDS**
"""
            for app, count in sorted(app_totals.items(), key=lambda x: x[1], reverse=True):
                percentage = count / total_week * 100
                bar_length = int(percentage / 5)
                visual_bar = "█" * bar_length + "░" * (20 - bar_length)
                emoji = "🔧" if app == "SOM_MM" else "📊" if app == "SQO_MM" else "💰" if app == "BILLING_MM" else "❓"
                report += f"{emoji} {app}: {visual_bar} {count} ({percentage:.1f}%)\n"
            
            report += f"""

🎯 **PRIORITY TRENDS**
"""
            priority_order = ['P0', 'P1', 'P2', 'P3', 'P4']
            for priority in priority_order:
                if priority in priority_totals:
                    count = priority_totals[priority]
                    percentage = count / total_week * 100
                    emoji = "🚨" if priority == 'P0' else "⚡" if priority == 'P1' else "📋" if priority == 'P2' else "📝"
                    report += f"{emoji} {priority}: {count} ({percentage:.1f}%)\n"
            
            # Add insights
            report += f"""

💡 **KEY INSIGHTS**
"""
            # Busiest day
            busiest_day = max(daily_stats.items(), key=lambda x: x[1]['total'])
            report += f"• Busiest Day: {busiest_day[0]} with {busiest_day[1]['total']} SRs\n"
            
            # Most common app
            top_app = max(app_totals.items(), key=lambda x: x[1])
            report += f"• Most Common Application: {top_app[0]} ({top_app[1]} SRs, {top_app[1]/total_week*100:.1f}%)\n"
            
            # High priority count
            high_priority = sum(priority_totals.get(p, 0) for p in ['P0', 'P1', 'P2'])
            if high_priority > 0:
                report += f"• High Priority SRs (P0-P2): {high_priority} ({high_priority/total_week*100:.1f}%)\n"
            
            report += """

📋 **RECOMMENDATIONS**
• Monitor daily patterns to optimize team scheduling
• Address high-priority SRs promptly
• Consider load balancing for peak days
"""
            
            return report
            
        except Exception as e:
            return f"""
📅 **WEEKLY PATTERN ANALYSIS**

❌ Error generating weekly patterns: {str(e)}

Make sure you have processed SR files with stored data in the database.
"""
    
    def _generate_insights_report(self, processing_results: Dict) -> str:
        """Generate comprehensive insights report"""
        assignment_results = processing_results.get('assignment_results', {})
        assignments = assignment_results.get('assignments', [])
        stats = assignment_results.get('statistics', {})
        
        if not assignments:
            return "⚠️ No assignment data available for insights."
        
        # Application breakdown
        app_counts = {}
        priority_counts = {}
        assignee_counts = {}
        
        for assignment in assignments:
            app = assignment.get('detected_application', 'UNKNOWN')
            priority = assignment.get('priority', 'Unknown')
            assignee = assignment.get('assignee_name', 'Unassigned')
            
            app_counts[app] = app_counts.get(app, 0) + 1
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
            assignee_counts[assignee] = assignee_counts.get(assignee, 0) + 1
        
        total_srs = len(assignments)
        assigned = sum(1 for a in assignments if a.get('final_assignee') != 'unassigned')
        
        report = f"""
📊 **INSIGHTS REPORT**
═══════════════════════════════════════════════

📈 **OVERALL STATISTICS**
• Total SRs Processed: {total_srs}
• Successfully Assigned: {assigned} ({assigned/total_srs*100:.1f}%)
• Unassigned: {total_srs - assigned} ({(total_srs-assigned)/total_srs*100:.1f}%)

🎯 **PRIORITY BREAKDOWN**
"""
        # Sort priorities
        priority_order = ['P0', 'P1', 'P2', 'P3', 'P4', 'Unknown']
        for priority in priority_order:
            if priority in priority_counts:
                count = priority_counts[priority]
                percentage = count / total_srs * 100
                emoji = "🚨" if priority == 'P0' else "⚡" if priority == 'P1' else "📋" if priority == 'P2' else "📝"
                report += f"{emoji} {priority}: {count} SRs ({percentage:.1f}%)\n"
        
        report += f"""

📱 **APPLICATION DISTRIBUTION**
"""
        # Sort by count
        for app, count in sorted(app_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = count / total_srs * 100
            emoji = "🔧" if app == "SOM_MM" else "📊" if app == "SQO_MM" else "💰" if app == "BILLING_MM" else "❓"
            report += f"{emoji} {app}: {count} SRs ({percentage:.1f}%)\n"
        
        report += f"""

👥 **TEAM ASSIGNMENT BREAKDOWN**
"""
        # Show top assignees
        sorted_assignees = sorted(assignee_counts.items(), key=lambda x: x[1], reverse=True)
        for assignee, count in sorted_assignees[:10]:  # Top 10
            percentage = count / total_srs * 100
            emoji = "✅" if assignee != "Unassigned" else "⚠️"
            report += f"{emoji} {assignee}: {count} SRs ({percentage:.1f}%)\n"
        
        # Key insights
        report += f"""

💡 **KEY INSIGHTS**
"""
        # High priority insight
        high_priority = sum(priority_counts.get(p, 0) for p in ['P0', 'P1', 'P2'])
        if high_priority > 0:
            report += f"• {high_priority} high-priority SRs (P0-P2) require immediate attention\n"
        
        # Most common application
        if app_counts:
            top_app = max(app_counts, key=app_counts.get)
            report += f"• {top_app} is the most common application ({app_counts[top_app]} SRs)\n"
        
        # Workload distribution
        if len(assignee_counts) > 1:
            assigned_members = [k for k in assignee_counts.keys() if k != 'Unassigned']
            if assigned_members:
                avg_load = assigned / len(assigned_members) if assigned_members else 0
                report += f"• Average workload: {avg_load:.1f} SRs per team member\n"
        
        # Unassigned insight
        unassigned_count = assignee_counts.get('Unassigned', 0)
        if unassigned_count > 0:
            report += f"• ⚠️ {unassigned_count} SRs remain unassigned - consider team capacity\n"
        
        report += """

📋 **RECOMMENDED ACTIONS**
• Review high-priority (P0-P2) assignments first
• Monitor team workload for balanced distribution
• Follow up on unassigned SRs
• Use 'Show detailed assignments' for full SR list
"""
        
        return report
    
    def _generate_html_report_info(self, processing_results: Dict) -> str:
        """Generate HTML report information"""
        return """
📄 HTML REPORT GENERATION

✅ Report will include:
- Assignment summary with charts
- Team workload visualization
- Pattern analysis insights
- Detailed SR listings

📁 Report will be saved as: sr_assignment_report.html

To generate the report, use the web interface or download option.
"""
    
    def _generate_excel_download_info(self, processing_results: Dict) -> str:
        """Generate Excel download information with actual download"""
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sr_assignments_{timestamp}.xlsx"
        
        # Return message with download button HTML  
        return f"""
📊 **EXCEL DOWNLOAD**

✅ Excel file will include:
- Original SR data with assignments
- Team member assignments
- Complexity scores
- Application classifications

📁 File will be saved as: `{filename}`

<div style="margin-top: 15px;">
    <button onclick="downloadExcel()" style="padding: 12px 24px; background: linear-gradient(135deg, #4CAF50, #45a049); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 15px; font-weight: 600; box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3); transition: all 0.3s ease;">
        📥 Download Excel Report
    </button>
</div>
"""
    
    def _try_load_from_database(self):
        """Try to load the most recent SR assignments from the database"""
        try:
            import sqlite3
            conn = sqlite3.connect('sr_tracking.db')
            cursor = conn.cursor()
            
            # Get all SRs from the most recent file with assignments
            cursor.execute("""
                SELECT 
                    r.sr_id, 
                    COALESCE(r.description, r.summary, '') as description,
                    r.priority, 
                    r.application,
                    a.assignee_name,
                    a.assignment_reason,
                    a.confidence_score,
                    r.complexity_score,
                    r.source_file
                FROM sr_records r
                LEFT JOIN sr_assignments a ON r.sr_id = a.sr_id
                ORDER BY r.processed_date DESC 
                LIMIT 200
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return None
            
            # Convert to assignment format
            assignments = []
            for row in rows:
                assignee = row[4] or 'unassigned'
                assignments.append({
                    'sr_id': row[0],
                    'inc_summary': row[1] or '',
                    'priority': row[2] or 'Medium',
                    'detected_application': row[3] or 'UNKNOWN',
                    'final_assignee': assignee,
                    'assignee_name': row[4] or 'Unassigned',
                    'assignment_reason': row[5] or '',
                    'confidence': row[6] or 0.0,
                    'complexity_score': row[7] or 0.0,
                })
            
            # Create processing_results structure
            source_file = rows[0][8] if rows else 'Unknown'
            return {
                'assignment_results': {
                    'assignments': assignments,
                    'statistics': {
                        'total_srs': len(assignments),
                        'successful_assignments': sum(1 for a in assignments if a['final_assignee'] != 'unassigned'),
                        'success_rate': (sum(1 for a in assignments if a['final_assignee'] != 'unassigned') / len(assignments) * 100) if assignments else 0
                    }
                },
                'file_info': {
                    'filename': source_file,
                    'total_srs': len(assignments)
                }
            }
        except Exception as e:
            print(f"⚠️ Could not load from database: {e}")
            return None
    
    def _reset_for_new_file(self) -> str:
        """Reset session for new file processing"""
        self.processed_file = None
        self.session_data['file_processed'] = False
        
        return """
🔄 Ready for new file processing!

Available files:
- Today_SR.xls
- Dump_2025.xlsx
- Aug_Dump.xlsx

Please specify which file to process:
Example: "Process file: Today_SR.xls"
"""
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def get_session_data(self) -> Dict:
        """Get current session data"""
        return self.session_data
    
    def _format_team_workload(self, assignee_distribution):
        """Format team workload distribution for display"""
        if not assignee_distribution:
            return "No assignments recorded"
        
        lines = []
        for assignee, count in sorted(assignee_distribution.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"• **{assignee}**: {count} SRs")
        
        return '\n'.join(lines) if lines else "No assignments recorded"
    
    def _format_application_breakdown(self, app_distribution):
        """Format application distribution for display"""
        if not app_distribution:
            return "No application data available"
        
        lines = []
        total = sum(app_distribution.values())
        for app, count in sorted(app_distribution.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            lines.append(f"• **{app}**: {count} SRs ({percentage:.1f}%)")
        
        return '\n'.join(lines) if lines else "No application data available"
    
    def _format_pattern_distribution(self, pattern_results):
        """Format pattern analysis distribution for display"""
        if not pattern_results or 'application_distribution' not in pattern_results:
            return "No pattern distribution available"
        
        distribution = pattern_results['application_distribution']
        lines = []
        
        for app, percentage in distribution.items():
            lines.append(f"• **{app}**: {percentage:.1f}%")
        
        return '\n'.join(lines) if lines else "No distribution data available"
    
    def _handle_pattern_only_results(self, processing_results, requested_action):
        """Handle cases where we only have pattern analysis, not assignments"""
        total_srs = processing_results.get('file_info', {}).get('total_srs', 0)
        pattern_results = processing_results.get('insights', {})
        
        return f"""
📊 **Pattern Analysis Results Available**

🔍 **File Analysis:**
- Total SRs processed: {total_srs}
- Pattern analysis completed ✅

📈 **Application Distribution:**
{self._format_pattern_distribution(pattern_results)}

⚠️ **Assignment Data Not Available**
The file was processed for pattern analysis but not for team assignments.

🎯 **Available Actions:**
• View pattern analysis details
• Re-process file for assignments  
• Upload a new file

💡 **To get assignments:** Upload the file again and it will be processed for both pattern analysis AND team assignments.
"""

    def _generate_detailed_assignments(self, processing_results):
        """Generate detailed assignments view"""
        assignment_results = processing_results['assignment_results']
        assignments = assignment_results.get('assignments', [])
        
        if not assignments:
            return "❌ No assignments found. Please process a file first."
        
        # Group assignments by assignee
        by_assignee = {}
        unassigned = []
        
        for assignment in assignments:
            assignee = assignment.get('assignee_name', 'Unassigned')
            if assignee == 'Unassigned' or not assignee:
                unassigned.append(assignment)
            else:
                if assignee not in by_assignee:
                    by_assignee[assignee] = []
                by_assignee[assignee].append(assignment)
        
        response = f"""
📋 **DETAILED SR ASSIGNMENTS** 
Total SRs: {len(assignments)} | Assigned: {len(assignments) - len(unassigned)} | Unassigned: {len(unassigned)}

"""
        
        # Show assignments by team member
        for assignee, member_assignments in sorted(by_assignee.items()):
            response += f"""
👤 **{assignee}** ({len(member_assignments)} SRs):
"""
            for i, assignment in enumerate(member_assignments[:10], 1):  # Show first 10
                incident_id = assignment.get('sr_id', assignment.get('incident_id', 'N/A'))
                cas_id = assignment.get('cas_id', '')
                cas_display = f" (CAS: {cas_id})" if cas_id and cas_id != 'nan' else ""
                summary = assignment.get('inc_summary', 'No summary')[:80] + '...' if len(assignment.get('inc_summary', '')) > 80 else assignment.get('inc_summary', 'No summary')
                app = assignment.get('detected_application', 'Unknown')
                confidence = assignment.get('confidence', 0)
                
                response += f"""   {i}. **{incident_id}{cas_display}** - {app} (Confidence: {confidence:.2f})
      📝 {summary}
"""
            
            if len(member_assignments) > 10:
                response += f"   ... and {len(member_assignments) - 10} more SRs\n"
            
            response += "\n"
        
        # Show unassigned if any
        if unassigned:
            response += f"""
⚠️ **UNASSIGNED SRs** ({len(unassigned)}):
"""
            for i, assignment in enumerate(unassigned[:5], 1):  # Show first 5 unassigned
                incident_id = assignment.get('sr_id', assignment.get('incident_id', 'N/A'))
                cas_id = assignment.get('cas_id', '')
                cas_display = f" (CAS: {cas_id})" if cas_id and cas_id != 'nan' else ""
                summary = assignment.get('inc_summary', 'No summary')[:60] + '...' if len(assignment.get('inc_summary', '')) > 60 else assignment.get('inc_summary', 'No summary')
                reason = assignment.get('assignment_reason', 'No reason provided')
                
                response += f"""   {i}. **{incident_id}{cas_display}** - {summary}
      ❌ Reason: {reason}
"""
            
            if len(unassigned) > 5:
                response += f"   ... and {len(unassigned) - 5} more unassigned SRs\n"
        
        response += """
🎯 **Next Actions:**
• "Reassign SR-12345 to Prateek" - Reassign specific SR
• "Show team workload" - Check current capacity
• "Generate HTML report" - Create detailed report
• "Download Excel" - Export all assignments
"""
        
        return response
    
    def _handle_full_reprocess(self):
        """Handle full file reprocessing with updated availability"""
        # Check multiple sources for processed file information
        filename = None
        
        # Option 1: Check processed_file attribute
        if self.processed_file:
            filename = self.processed_file
        
        # Option 2: Check session data for processing results
        elif self.session_data.get('processing_results'):
            processing_results = self.session_data['processing_results']
            filename = processing_results.get('file_info', {}).get('filename')
        
        # Option 3: Check if we have daily_assignments (which means a file was processed)
        elif hasattr(self, 'daily_assignments') and self.daily_assignments:
            # Default to most common file
            filename = 'Mukul.xls' if os.path.exists('Mukul.xls') else 'Today_SR.xls'
        
        if not filename:
            return """
❌ **No File to Reprocess**

You need to process a file first before you can reassign all SRs.

**Quick Start:**
1. Process a file: "Process Mukul file" or "Process Today_SR.xls"
2. Set availability: "Anamika is available half day today"
3. Reassign: "Reassign all SRs"

**Or process availability first (recommended):**
1. "Anamika is available half day today"
2. "Process Mukul file"
3. Done! (Assignments already optimized)
"""
        
        try:
            # Clear previous results to force reprocessing
            if 'processing_results' in self.session_data:
                del self.session_data['processing_results']
            
            # Reprocess the file with current availability
            result = self.process_file_input(f"Process {filename}")
            
            # Add a note that this is a reprocessing
            reprocess_note = """
🔄 **File Reprocessed with Updated Availability**

The assignments above reflect your latest team availability settings.
All SRs have been redistributed based on current capacity.

"""
            return reprocess_note + result
            
        except Exception as e:
            return f"""
❌ **Error Reprocessing File**

{str(e)}

**What You Can Try:**
• "Process {filename}" - Process file manually
• "Show team workload" - Check current capacity
• "Show assignments" - View current assignments (if any)
• "Process Mukul file" - Start fresh with Mukul.xls
"""
    
    def _handle_reassignment(self, command):
        """Handle SR reassignment requests"""
        # Parse reassignment command like "Reassign SR-12345 to Prateek"
        import re
        
        # Look for SR ID and assignee name
        sr_match = re.search(r'(SR[-_]?\d+)', command, re.IGNORECASE)
        to_match = re.search(r'to\s+(\w+)', command, re.IGNORECASE)
        
        if not sr_match:
            return """
❌ Please specify an SR ID to reassign.

**Format:** "Reassign SR-12345 to Prateek"
**Examples:**
• "Reassign SR-12345 to Prateek"
• "Move SR123 to Anamika"
• "Assign SR-456 to Smitesh"
"""
        
        if not to_match:
            return """
❌ Please specify who to reassign the SR to.

**Format:** "Reassign SR-12345 to Prateek"
**Available team members:**
• Prateek Jain (prateek)
• Smitesh Kadia (smitesh)
• Anamika Thakur (anamika)
• Akshit Kaushik (akshit)
• Abhishek Agrahari (abhishek)
• Krishna Tayade (krishna)
• Dhulipalla Divya (dhulipalla)
"""
        
        sr_id = sr_match.group(1).upper()
        new_assignee = to_match.group(1).lower()
        
        # Map short names to full names
        name_mapping = {
            'prateek': 'Prateek Jain',
            'smitesh': 'Smitesh Kadia', 
            'anamika': 'Anamika Thakur',
            'akshit': 'Akshit Kaushik',
            'abhishek': 'Abhishek Agrahari',
            'krishna': 'Krishna Tayade',
            'dhulipalla': 'Dhulipalla Divya',
            'divya': 'Dhulipalla Divya'
        }
        
        full_name = name_mapping.get(new_assignee)
        if not full_name:
            # Try exact match
            full_name = new_assignee.title()
        
        # Find and update the assignment
        if hasattr(self, 'daily_assignments') and self.daily_assignments:
            for assignment in self.daily_assignments:
                if assignment.get('sr_id', '').upper() == sr_id:
                    old_assignee = assignment.get('assignee_name', 'Unassigned')
                    assignment['assignee_name'] = full_name
                    assignment['assignment_reason'] = f"Manual reassignment from {old_assignee}"
                    
                    return f"""
✅ **SR Reassignment Successful**

**SR ID:** {sr_id}
**From:** {old_assignee}
**To:** {full_name}
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 **Next steps:**
• Say "Show detailed assignments" to see updated assignments
• Say "Generate HTML report" to create updated report
• Make more reassignments as needed
"""
        
        return f"""
❌ **SR {sr_id} not found** in current assignments.

Please check:
• SR ID is correct (e.g., SR-12345)
• File has been processed and assignments made
• Use "Show detailed assignments" to see available SRs
"""
    
    def _handle_priority_filter(self, priority, processing_results):
        """Handle priority-specific filtering (e.g., P0, P1, P2)"""
        assignment_results = processing_results.get('assignment_results', {})
        assignments = assignment_results.get('assignments', [])
        
        if not assignments:
            return "❌ No assignments found. Please process a file first."
        
        # Filter assignments by priority
        filtered_assignments = [a for a in assignments if a.get('priority', '').upper() == priority]
        
        if not filtered_assignments:
            # Show available priorities
            all_priorities = set(a.get('priority', 'Unknown') for a in assignments)
            return f"""
📋 **{priority} ASSIGNMENTS**

❌ No {priority} assignments found.

📊 **Available Priorities:** {', '.join(sorted(all_priorities))}
"""
        
        # Group by assignee
        by_assignee = {}
        unassigned = []
        
        for assignment in filtered_assignments:
            assignee = assignment.get('assignee_name', 'Unassigned')
            if assignee == 'Unassigned' or not assignee:
                unassigned.append(assignment)
            else:
                if assignee not in by_assignee:
                    by_assignee[assignee] = []
                by_assignee[assignee].append(assignment)
        
        response = f"""
📋 **{priority} PRIORITY ASSIGNMENTS**
Total {priority} SRs: {len(filtered_assignments)} | Assigned: {len(filtered_assignments) - len(unassigned)} | Unassigned: {len(unassigned)}

"""
        
        # Show assignments by team member
        for assignee, member_assignments in sorted(by_assignee.items()):
            response += f"""
👤 **{assignee}** ({len(member_assignments)} SRs):
"""
            for idx, assignment in enumerate(member_assignments, 1):
                sr_id = assignment.get('sr_id', 'Unknown')
                summary = assignment.get('inc_summary', 'No description')[:80]
                app = assignment.get('detected_application', 'UNKNOWN')
                response += f"  {idx}. {sr_id} - {app} - {summary}...\n"
            response += "\n"
        
        # Show unassigned
        if unassigned:
            response += f"""
⚠️ **UNASSIGNED {priority} SRs** ({len(unassigned)}):
"""
            for idx, assignment in enumerate(unassigned, 1):
                sr_id = assignment.get('sr_id', 'Unknown')
                summary = assignment.get('inc_summary', 'No description')[:80]
                app = assignment.get('detected_application', 'UNKNOWN')
                response += f"  {idx}. {sr_id} - {app} - {summary}...\n"
        
        return response
    
    def _handle_application_filter(self, command, processing_results):
        """Handle application-specific filtering"""
        assignment_results = processing_results['assignment_results']
        assignments = assignment_results.get('assignments', [])
        
        # Determine which application to filter
        if 'som' in command.lower():
            app_filter = 'SOM_MM'
        elif 'sqo' in command.lower():
            app_filter = 'SQO_MM'
        elif 'billing' in command.lower():
            app_filter = 'BILLING_MM'
        else:
            return "❌ Please specify application: SOM_MM, SQO_MM, or BILLING_MM"
        
        # Filter assignments by application
        filtered_assignments = [a for a in assignments if a.get('detected_application') == app_filter]
        
        if not filtered_assignments:
            return f"""
📋 **{app_filter} ASSIGNMENTS**

❌ No {app_filter} assignments found.

📊 **Available Applications:**
{self._get_application_summary(assignments)}
"""
        
        # Group by assignee
        by_assignee = {}
        unassigned = []
        
        for assignment in filtered_assignments:
            assignee = assignment.get('assignee_name', 'Unassigned')
            if assignee == 'Unassigned' or not assignee:
                unassigned.append(assignment)
            else:
                if assignee not in by_assignee:
                    by_assignee[assignee] = []
                by_assignee[assignee].append(assignment)
        
        response = f"""
📋 **{app_filter} ASSIGNMENTS ONLY**
Total {app_filter} SRs: {len(filtered_assignments)} | Assigned: {len(filtered_assignments) - len(unassigned)} | Unassigned: {len(unassigned)}

"""
        
        # Show assignments by team member
        for assignee, member_assignments in sorted(by_assignee.items()):
            response += f"""
👤 **{assignee}** ({len(member_assignments)} {app_filter} SRs):
"""
            for i, assignment in enumerate(member_assignments[:8], 1):  # Show first 8
                incident_id = assignment.get('sr_id', assignment.get('incident_id', 'N/A'))
                cas_id = assignment.get('cas_id', '')
                cas_display = f" (CAS: {cas_id})" if cas_id and cas_id != 'nan' else ""
                summary = assignment.get('inc_summary', 'No summary')[:70] + '...' if len(assignment.get('inc_summary', '')) > 70 else assignment.get('inc_summary', 'No summary')
                confidence = assignment.get('confidence', 0)
                
                response += f"""   {i}. **{incident_id}{cas_display}** - Confidence: {confidence:.2f}
      📝 {summary}
"""
            
            if len(member_assignments) > 8:
                response += f"   ... and {len(member_assignments) - 8} more {app_filter} SRs\n"
            
            response += "\n"
        
        # Show unassigned if any
        if unassigned:
            response += f"""
⚠️ **UNASSIGNED {app_filter} SRs** ({len(unassigned)}):
"""
            for i, assignment in enumerate(unassigned[:5], 1):  # Show first 5 unassigned
                incident_id = assignment.get('sr_id', assignment.get('incident_id', 'N/A'))
                cas_id = assignment.get('cas_id', '')
                cas_display = f" (CAS: {cas_id})" if cas_id and cas_id != 'nan' else ""
                summary = assignment.get('inc_summary', 'No summary')[:50] + '...' if len(assignment.get('inc_summary', '')) > 50 else assignment.get('inc_summary', 'No summary')
                reason = assignment.get('assignment_reason', 'No reason provided')
                
                response += f"""   {i}. **{incident_id}{cas_display}** - {summary}
      ❌ Reason: {reason}
"""
            
            if len(unassigned) > 5:
                response += f"   ... and {len(unassigned) - 5} more unassigned {app_filter} SRs\n"
        
        response += f"""
🎯 **{app_filter} Actions:**
• "Reassign SR-12345 to [name]" - Move specific SR
• "Show all assignments" - View all applications
• "Show team workload" - Check capacity
• "Filter SOM_MM assignments" - Filter other applications
"""
        
        return response
    
    def _get_application_summary(self, assignments):
        """Get summary of applications in assignments"""
        apps = {}
        for assignment in assignments:
            app = assignment.get('detected_application', 'UNKNOWN')
            apps[app] = apps.get(app, 0) + 1
        
        lines = []
        for app, count in sorted(apps.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"• {app}: {count} SRs")
        
        return '\n'.join(lines) if lines else "No applications found"
    
    def _show_filtered_srs(self, processing_results):
        """Show SRs that were filtered out from assignment"""
        assignment_results = processing_results['assignment_results']
        assignments = assignment_results.get('assignments', [])
        
        # Get filtered SRs
        filtered_srs = [a for a in assignments if a.get('assignee_name') == 'Filtered Out']
        
        if not filtered_srs:
            return """
📋 **FILTERED SRs**

✅ No SRs were filtered out - all eligible SRs were processed for assignment.

All SRs met the criteria:
• Status = "In Progress"  
• Status_Reason ≠ "Workaround Given"
"""
        
        # Group by filter reason
        by_reason = {}
        for sr in filtered_srs:
            reason = sr.get('assignment_reason', 'Unknown filter reason')
            if reason not in by_reason:
                by_reason[reason] = []
            by_reason[reason].append(sr)
        
        response = f"""
🚫 **FILTERED SRs** 
Total Filtered: {len(filtered_srs)} SRs

"""
        
        # Show by filter reason
        for reason, srs in by_reason.items():
            response += f"""
📌 **{reason}** ({len(srs)} SRs):
"""
            for i, sr in enumerate(srs[:10], 1):  # Show first 10 per reason
                incident_id = sr.get('sr_id', 'N/A')
                cas_id = sr.get('cas_id', '')
                cas_display = f" (CAS: {cas_id})" if cas_id and cas_id != 'nan' else ""
                summary = sr.get('inc_summary', 'No summary')[:60] + '...' if len(sr.get('inc_summary', '')) > 60 else sr.get('inc_summary', 'No summary')
                status = sr.get('status', 'N/A')
                status_reason = sr.get('status_reason', 'N/A')
                
                response += f"""   {i}. **{incident_id}{cas_display}**
      📝 {summary}
      🔸 Status: {status} | Status_Reason: {status_reason}
"""
            
            if len(srs) > 10:
                response += f"   ... and {len(srs) - 10} more filtered SRs\n"
            
            response += "\n"
        
        response += """
🎯 **Actions:**
• "Show detailed assignments" - View assigned SRs only
• "Download Excel" - Export all data including filtered SRs
• "Generate HTML report" - Create comprehensive report

💡 **Note:** Filtered SRs are included in Excel export for reference but are not assigned to team members.
"""
        
        return response
    
    def _handle_application_export(self, command, processing_results):
        """Handle application-specific Excel export commands"""
        command_lower = command.lower()
        
        # Determine application type from command
        if 'som' in command_lower:
            app_type = 'SOM_MM'
            app_display = 'SOM_MM (Sales Order Management)'
        elif 'sqo' in command_lower:
            app_type = 'SQO_MM'
            app_display = 'SQO_MM (Sales Quote Operations)'
        elif 'billing' in command_lower:
            app_type = 'BILLING_MM'
            app_display = 'BILLING_MM (Billing Management)'
        else:
            return """
❌ **Export Error**

Please specify a valid application type:
• "Export SOM_MM Excel" - Export only SOM_MM assignments
• "Export SQO_MM Excel" - Export only SQO_MM assignments  
• "Export BILLING_MM Excel" - Export only BILLING_MM assignments
"""
        
        try:
            # Use the assignment system's filtered export
            if hasattr(self, 'assignment_interface') and hasattr(self.assignment_interface, 'sr_assignment_system'):
                output_file = self.assignment_interface.sr_assignment_system.export_filtered_assignments(app_type)
                
                # Get some stats for the response
                assignment_results = processing_results.get('assignment_results', {})
                assignments = assignment_results.get('assignments', [])
                
                # Count assignments for this application
                app_assignments = [a for a in assignments if a.get('detected_application') == app_type]
                assigned_count = len([a for a in app_assignments if a.get('assignee_name') != 'Filtered Out'])
                filtered_count = len([a for a in app_assignments if a.get('assignee_name') == 'Filtered Out'])
                
                return f"""
✅ **{app_display} Excel Export Complete!**

📊 **Export Summary:**
- **Application**: {app_type}
- **Total {app_type} SRs**: {len(app_assignments)}
- **Assigned**: {assigned_count} SRs
- **Filtered Out**: {filtered_count} SRs
- **File**: `{output_file}`

📋 **What's Included:**
• **{app_type}_Assignments** sheet - All SRs for this application
• **Summary** sheet - Statistics and metrics
• **Team_Workload** sheet - Who got how many SRs

🎯 **Next Actions:**
• "Export SQO_MM Excel" - Export another application
• "Show {app_type} assignments" - View these assignments
• "Generate HTML report" - Create comprehensive report

💡 **File Location**: `downloads/{output_file.split('/')[-1]}`
"""
                
            else:
                return "❌ Assignment system not available. Please process a file first."
                
        except ValueError as e:
            return f"""
❌ **Export Error**

{str(e)}

🎯 **Available Applications:**
• SOM_MM - Sales Order Management  
• SQO_MM - Sales Quote Operations
• BILLING_MM - Billing Management

Try: "Export SOM_MM Excel" or similar commands.
"""
        except Exception as e:
            return f"""
❌ **Unexpected Export Error**

{str(e)}

Please try again or contact support if the issue persists.
"""
    
    def _handle_mukul_assignment(self, command: str) -> str:
        """Handle Mukul.xls processing for enhanced SR assignment with interactive application selection"""
        try:
            if not os.path.exists('Mukul.xls'):
                return self._generate_mukul_file_not_found_response()
            
            # Ensure we have availability set for mukul processing (prevents routing issues)
            if not self.current_availability:
                self.current_availability = "Default team availability - all members available for mukul processing"
            
            # Check if user is responding to application selection (using dedicated mukul session state)
            if hasattr(self, 'mukul_session') and self.mukul_session.get('awaiting_selection'):
                return self._handle_mukul_application_selection(command)
            
            # Show application selection UI for Mukul processing
            return self._show_mukul_application_selection_ui()
            
        except FileNotFoundError:
            return """❌ **Mukul.xls File Not Found**

The Mukul.xls file is required for enhanced SR assignment but was not found in the current directory.

🔧 **How to resolve:**
1. Ensure Mukul.xls is in the sr-analyzer folder
2. Check the file name (case-sensitive)
3. Verify the file is not open in Excel
4. Try the command again

📁 **Expected location:** sr-analyzer/Mukul.xls

**Alternative:**
• Use 'upload sr file' for regular SR processing
• Check 'show team skills' for available team members
"""
        except Exception as e:
            return f"""❌ **Error Processing Mukul File**

An unexpected error occurred while processing the Mukul.xls file.

**Error details:** {str(e)}

🔧 **Troubleshooting steps:**
1. Ensure Mukul.xls has the required columns (Description, Notes)
2. Check that the file is not corrupted or open in Excel
3. Verify the people_skills.db database is accessible
4. Try processing a smaller subset of the data

**For support:** Check the error details above or contact system administrator.
"""
    
    def _show_mukul_application_selection_ui(self) -> str:
        """Show dedicated UI for Mukul application selection"""
        # Initialize mukul-specific session state (separate from main chat routing)
        if not hasattr(self, 'mukul_session'):
            self.mukul_session = {}
        
        self.mukul_session['awaiting_selection'] = True
        
        # Check available applications in the data
        try:
            import pandas as pd
            df = pd.read_excel('Mukul.xls')
            available_apps = df['Assigned Group'].unique()
            available_apps = [app for app in available_apps if pd.notna(app)]
            
            app_counts = {}
            for app in available_apps:
                count = len(df[df['Assigned Group'] == app])
                app_counts[app] = count
        except:
            app_counts = {}
        
        # Generate the dedicated UI
        selection_ui = f"""
        <div class="mukul-application-selector">
            <div class="selector-header">
                <h2>🎯 Mukul File Processing - Application Selection</h2>
                <p>Choose which application(s) to process from Mukul.xls:</p>
            </div>
            
            <div class="application-grid">
                <div class="app-card som-card">
                    <div class="app-icon">📋</div>
                    <div class="app-info">
                        <h3>SOM_MM</h3>
                        <p>Service Order Management</p>
                        <span class="sr-count">{app_counts.get('SOM_MM', 0)} SRs</span>
                    </div>
                </div>
                
                <div class="app-card sqo-card">
                    <div class="app-icon">💼</div>
                    <div class="app-info">
                        <h3>SQO_MM</h3>
                        <p>Sales Quote Management</p>
                        <span class="sr-count">{app_counts.get('SQO_MM', 0)} SRs</span>
                    </div>
                </div>
                
                <div class="app-card billing-card">
                    <div class="app-icon">💰</div>
                    <div class="app-info">
                        <h3>BILLING_MM</h3>
                        <p>Billing Management</p>
                        <span class="sr-count">{app_counts.get('BILLING_MM', 0)} SRs</span>
                    </div>
                </div>
                
                <div class="app-card all-card">
                    <div class="app-icon">📁</div>
                    <div class="app-info">
                        <h3>ALL</h3>
                        <p>Process All Applications Together</p>
                        <span class="sr-count">{sum(app_counts.values())} SRs total</span>
                    </div>
                </div>
            </div>
            
            <div class="selection-guide">
                <h4>📝 How to Select:</h4>
                <div class="selection-options">
                    <div class="option-row">
                        <span class="option-code">SOM_MM</span> → Process Service Order Management only
                    </div>
                    <div class="option-row">
                        <span class="option-code">SQO_MM</span> → Process Sales Quote Management only
                    </div>
                    <div class="option-row">
                        <span class="option-code">BILLING_MM</span> → Process Billing Management only
                    </div>
                    <div class="option-row">
                        <span class="option-code">ALL</span> → Create one combined file for all applications
                    </div>
                </div>
                
                <div class="output-info">
                    <h4>📄 Output Files:</h4>
                    <p>Each selection will create files with format:</p>
                    <code>Mukul1_enhanced_YYYYMMDD_HHMMSS_&lt;APP&gt;.xlsx</code>
                    <p><strong>Note:</strong> Only the latest file for each application type is kept.</p>
                </div>
            </div>
        </div>
        
        <style>
        .mukul-application-selector {{
            max-width: 800px;
            margin: 20px auto;
            padding: 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}
        
        .selector-header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .selector-header h2 {{
            margin: 0 0 10px 0;
            font-size: 24px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        .selector-header p {{
            margin: 0;
            opacity: 0.9;
            font-size: 16px;
        }}
        
        .application-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .app-card {{
            background: rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }}
        
        .app-card:hover {{
            background: rgba(255, 255, 255, 0.25);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        }}
        
        .app-icon {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        
        .app-info h3 {{
            margin: 0 0 8px 0;
            font-size: 18px;
            font-weight: bold;
        }}
        
        .app-info p {{
            margin: 0 0 10px 0;
            font-size: 14px;
            opacity: 0.8;
        }}
        
        .sr-count {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .selection-guide {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
        }}
        
        .selection-guide h4 {{
            margin: 0 0 15px 0;
            font-size: 16px;
        }}
        
        .selection-options {{
            margin-bottom: 20px;
        }}
        
        .option-row {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        
        .option-code {{
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 8px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            min-width: 100px;
            margin-right: 10px;
        }}
        
        .output-info {{
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            padding-top: 15px;
        }}
        
        .output-info h4 {{
            margin: 0 0 10px 0;
        }}
        
        .output-info p {{
            margin: 0 0 8px 0;
            font-size: 14px;
        }}
        
        .output-info code {{
            background: rgba(0, 0, 0, 0.3);
            padding: 4px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}
        </style>
        """
        
        return selection_ui
    
    def _handle_mukul_application_selection(self, response: str) -> str:
        """Handle user's application selection for Mukul processing"""
        response = response.strip().upper()
        
        # Clear the mukul-specific awaiting state
        if hasattr(self, 'mukul_session'):
            self.mukul_session['awaiting_selection'] = False
        
        # Valid application options
        valid_apps = ['SOM_MM', 'SQO_MM', 'BILLING_MM', 'ALL']
        
        if response not in valid_apps:
            # Invalid selection, show UI again
            if not hasattr(self, 'mukul_session'):
                self.mukul_session = {}
            self.mukul_session['awaiting_selection'] = True
            
            return f"""❌ **Invalid Selection: "{response}"**

Please enter one of these options:
• **SOM_MM** - Process Service Order Management only
• **SQO_MM** - Process Sales Quote Management only  
• **BILLING_MM** - Process Billing Management only
• **ALL** - Process all applications together in one file

{self._show_mukul_application_selection_ui()}"""
        
        # Valid selection, process with the chosen application
        if response == 'ALL':
            return self._process_all_applications_separately()
        else:
            return self._process_single_mukul_application(response)
    
    def _process_all_applications_separately(self) -> str:
        """Process all applications together and create one combined file"""
        try:
            import pandas as pd
            from datetime import datetime
            from enhanced_mukul_sr_assignment import EnhancedMukulSRAssignment
            
            df = pd.read_excel('Mukul.xls')
            available_apps = df['Assigned Group'].unique()
            available_apps = [app for app in available_apps if pd.notna(app)]
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Create the enhanced assignment processor
            enhanced_processor = EnhancedMukulSRAssignment()
            
            # Process all applications together in MIXED mode
            result_df = enhanced_processor._process_single_application(
                df, 
                'Mukul.xls', 
                f'Mukul1_enhanced_{timestamp}_ALL.xlsx',  # Single output file for ALL mode
                'MIXED',  # Process all applications together
                timestamp
            )
            
            # Count assignments per application
            app_stats = []
            total_assigned = 0
            
            for app in ['SOM_MM', 'SQO_MM', 'BILLING_MM']:
                if app in available_apps:
                    app_srs = df[df['Assigned Group'] == app]
                    assigned_srs = result_df[(result_df['Assigned Group'] == app) & (result_df['Assignee'] != '')]
                    
                    app_names = {
                        'SOM_MM': 'Service Order Management',
                        'SQO_MM': 'Sales Quote Management', 
                        'BILLING_MM': 'Billing Management'
                    }
                    
                    app_name = app_names.get(app, app)
                    app_stats.append(f"📋 **{app}** ({app_name}): {len(assigned_srs)}/{len(app_srs)} SRs assigned")
                    total_assigned += len(assigned_srs)
            
            summary = f"""
🎯 **ALL Applications Processed Together**

**Single Combined File:** Mukul1_enhanced_{timestamp}_ALL.xlsx

**Application Statistics:**
{chr(10).join(app_stats)}

**Total Assigned:** {total_assigned} SRs
**Timestamp:** {timestamp}

All applications have been processed together in a single combined file.
The file contains all SRs with assignments distributed across team members based on their application expertise.
Note: Only the latest file for each application type is kept.
"""
            return summary
            
        except Exception as e:
            return f"""❌ **Error Processing All Applications**

{str(e)}

Please check the Mukul.xls file and try again."""
    
    def _process_single_mukul_application(self, selected_app: str, timestamp: str = None) -> str:
        """Process a single application and create appropriately named file"""
        try:
            from datetime import datetime
            from enhanced_mukul_sr_assignment import EnhancedMukulSRAssignment
            import pandas as pd
            
            if timestamp is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Create the enhanced assignment processor
            enhanced_processor = EnhancedMukulSRAssignment()
            
            # Read the Mukul file
            df = pd.read_excel('Mukul.xls')
            
            # Process with the selected application using the internal method
            result_df = enhanced_processor._process_single_application(
                df, 
                'Mukul.xls', 
                None,  # Let it auto-generate output filename
                selected_app,
                timestamp
            )
            
            # Generate confirmation message
            app_names = {
                'SOM_MM': 'Service Order Management',
                'SQO_MM': 'Sales Quote Management', 
                'BILLING_MM': 'Billing Management'
            }
            
            app_name = app_names.get(selected_app, selected_app)
            app_short = selected_app.split('_')[0]
            
            confirmation = f"""
✅ **{selected_app} Processing Complete**

**Application:** {app_name}
**Output File:** Mukul1_enhanced_{timestamp}_{app_short}.xlsx
**Timestamp:** {timestamp}
**Processed SRs:** {len(result_df)} records

Processing completed successfully with application-specific filtering and assignment.
Note: Only the latest file for this application type is kept.
"""
            return confirmation
            
        except Exception as e:
            return f"""❌ **Error Processing {selected_app}**

{str(e)}

Please check the Mukul.xls file and try again."""

    def _process_mukul_with_application(self, selected_app: str, original_command: str) -> str:
        """Process Mukul file with the selected application"""
        try:
            # Show processing confirmation
            app_names = {
                'SOM_MM': 'Service Order Management',
                'SQO_MM': 'Sales Quote Management', 
                'BILLING_MM': 'Billing Management',
                'ALL': 'All Applications Separately',
                'MIXED': 'All Applications Together'
            }
            
            app_name = app_names.get(selected_app, selected_app)
            
            confirmation_html = f"""
            <div class="processing-confirmation">
                <div class="confirmation-header">
                    <h3>✅ Selection Confirmed</h3>
                    <p>Processing with: <strong>{app_name}</strong></p>
                </div>
                <div class="processing-status">
                    <div class="status-indicator">🚀</div>
                    <div class="status-text">Processing Mukul.xls...</div>
                </div>
            </div>
            
            <style>
            .processing-confirmation {{
                background: linear-gradient(135deg, #e8f5e8 0%, #f0f8ff 100%);
                border: 2px solid #27ae60;
                border-radius: 8px;
                padding: 20px;
                margin: 15px 0;
                text-align: center;
            }}
            
            .confirmation-header h3 {{
                color: #27ae60;
                margin: 0 0 5px 0;
            }}
            
            .confirmation-header p {{
                color: #2c3e50;
                margin: 0 0 15px 0;
            }}
            
            .processing-status {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }}
            
            .status-indicator {{
                font-size: 20px;
                animation: pulse 1.5s infinite;
            }}
            
            .status-text {{
                font-weight: bold;
                color: #3498db;
            }}
            
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
                100% {{ opacity: 1; }}
            }}
            </style>
            """
            
            # Initialize enhancer and process with selected application
            enhancer = EnhancedMukulSRAssignment()
            
            if selected_app == 'ALL':
                # Process all applications separately
                df = pd.read_excel('Mukul.xls')
                enhanced_df = enhancer._process_all_applications_separately(df, 'Mukul.xls')
            else:
                # Process specific application or mixed mode using the internal method
                df = pd.read_excel('Mukul.xls') 
                enhanced_df = enhancer._process_single_application(df, 'Mukul.xls', None, selected_app)
            
            # Generate results based on original format preference
            if 'text' in original_command.lower():
                results_html = self._generate_mukul_enhanced_dashboard(original_command)
            else:
                results_html = self._generate_mukul_html_dashboard(original_command)
            
            # Store results in session
            self.session_data['mukul_processed'] = True
            self.session_data['selected_application'] = selected_app
            self.session_data['mukul_results'] = {
                'application': selected_app,
                'total_srs': len(enhanced_df),
                'assigned_count': len(enhanced_df[enhanced_df['Assignee'] != '']),
                'timestamp': datetime.now().isoformat()
            }
            
            return confirmation_html + results_html
            
        except Exception as e:
            return f"""❌ **Error Processing with {app_name}**

An error occurred while processing with the selected application:

{str(e)}

Please try again or contact support if the issue persists.
"""
    
    def _generate_mukul_file_not_found_response(self) -> str:
        """Generate enhanced file not found response"""
        return """
        <div class="mukul-error-container">
            <div class="error-header">
                <h2>❌ Mukul.xls File Not Found</h2>
                <p class="error-subtitle">Please ensure the Mukul.xls file is available for processing</p>
            </div>
            
            <div class="error-details">
                <div class="detail-card">
                    <h3>📁 Expected File Location</h3>
                    <p><strong>File Name:</strong> Mukul.xls</p>
                    <p><strong>Directory:</strong> sr-analyzer folder</p>
                    <p><strong>Full Path:</strong> C:\\SR Assignment Tool\\sr-analyzer\\Mukul.xls</p>
                </div>
                
                <div class="detail-card">
                    <h3>🔧 Required File Structure</h3>
                    <table class="requirements-table">
                        <thead>
                            <tr>
                                <th>Required Column</th>
                                <th>Purpose</th>
                                <th>Example</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>QC Defect ID</td>
                                <td>Unique identifier</td>
                                <td>QC123456</td>
                            </tr>
                            <tr>
                                <td>Call ID</td>
                                <td>Service request ID</td>
                                <td>SR001234</td>
                            </tr>
                            <tr>
                                <td>Customer Priority</td>
                                <td>Priority classification</td>
                                <td>P0, P1, P2</td>
                            </tr>
                            <tr>
                                <td>Status</td>
                                <td>Current status</td>
                                <td>In Progress, New, Completed</td>
                            </tr>
                            <tr>
                                <td>Description</td>
                                <td>SR description for analysis</td>
                                <td>Network connectivity issue</td>
                            </tr>
                            <tr>
                                <td>Notes</td>
                                <td>Additional details</td>
                                <td>Customer reported timeout</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <div class="detail-card">
                    <h3>⚡ Quick Setup Steps</h3>
                    <ol class="setup-steps">
                        <li>Locate your Mukul.xls file</li>
                        <li>Copy it to the sr-analyzer directory</li>
                        <li>Ensure the file is not open in Excel</li>
                        <li>Verify it contains the required columns</li>
                        <li>Try the command again</li>
                    </ol>
                </div>
                
                <div class="detail-card">
                    <h3>🚀 Alternative Commands</h3>
                    <div class="command-buttons">
                        <button class="cmd-btn">process mukul file</button>
                        <button class="cmd-btn">enhanced mukul assignment</button>
                        <button class="cmd-btn">mukul sr assignment</button>
                        <button class="cmd-btn">show team skills</button>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
        .mukul-error-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #fef7f0 0%, #fed7aa 100%);
            border-radius: 12px;
            border-left: 5px solid #ea580c;
        }
        
        .error-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .error-header h2 {
            color: #dc2626;
            font-size: 2.2em;
            margin: 0;
        }
        
        .error-subtitle {
            color: #7c2d12;
            font-size: 1.1em;
            margin: 10px 0 0 0;
        }
        
        .error-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }
        
        .detail-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .detail-card h3 {
            color: #1f2937;
            margin: 0 0 15px 0;
            font-size: 1.3em;
        }
        
        .requirements-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        
        .requirements-table th {
            background: #f3f4f6;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #e5e7eb;
        }
        
        .requirements-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .requirements-table tr:hover {
            background-color: #f9fafb;
        }
        
        .setup-steps {
            padding-left: 20px;
        }
        
        .setup-steps li {
            margin-bottom: 8px;
            color: #374151;
        }
        
        .command-buttons {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        
        .cmd-btn {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 500;
            transition: transform 0.2s;
        }
        
        .cmd-btn:hover {
            transform: translateY(-2px);
        }
        </style>
        """
    
    def _generate_mukul_enhanced_dashboard(self, command: str) -> str:
        """Generate enhanced text-based dashboard for Mukul processing"""
        try:
            enhancer = EnhancedMukulSRAssignment()
            print("🚀 Processing Mukul.xls for Enhanced SR Assignment...")
            enhanced_df = enhancer.process_mukul_file()
            
            # Calculate comprehensive statistics
            total_srs = len(enhanced_df)
            assigned_count = len(enhanced_df[enhanced_df['Assignee'] != ''])
            assignment_rate = (assigned_count / total_srs * 100) if total_srs > 0 else 0
            unassigned_count = total_srs - assigned_count
            
            # Get assignment distribution
            assignment_dist = enhanced_df[enhanced_df['Assignee'] != '']['Assignee'].value_counts()
            
            # Get priority distribution
            priority_dist = enhanced_df['Customer Priority'].value_counts()
            
            # Find output file name
            import glob
            enhanced_files = sorted(glob.glob('Mukul1_enhanced_*.xlsx'), key=os.path.getmtime, reverse=True)
            output_file = enhanced_files[0] if enhanced_files else 'Mukul1_enhanced_[timestamp].xlsx'
            
            # Generate enhanced dashboard response
            response = """🎯 **ENHANCED MUKUL SR ASSIGNMENT DASHBOARD**
═══════════════════════════════════════════════════════════════════════════════

✅ **PROCESSING COMPLETE!** - Mukul.xls successfully processed and enhanced

📊 **PROCESSING STATISTICS:**
╔════════════════════════════════════════╗
║  Total SRs Processed: {:<16} ║
║  Successfully Assigned: {:<14} ║
║  Unassigned SRs: {:<19} ║
║  Assignment Success Rate: {:<12} ║
╚════════════════════════════════════════╝

""".format(total_srs, assigned_count, unassigned_count, f"{assignment_rate:.1f}%")
            
            # Priority Analysis
            response += "🔥 **PRIORITY DISTRIBUTION ANALYSIS:**\n"
            response += "┌─────────────┬─────────────┬─────────────────────────────┐\n"
            response += "│ Priority    │ Count       │ Visual Distribution         │\n"
            response += "├─────────────┼─────────────┼─────────────────────────────┤\n"
            
            for priority, count in priority_dist.items():
                percentage = (count / total_srs * 100) if total_srs > 0 else 0
                bar_length = int(percentage / 4)  # Scale bar to max 25 chars
                visual_bar = "█" * bar_length + "░" * (25 - bar_length)
                
                priority_emoji = "🚨" if priority in ['P0'] else "⚡" if priority in ['P1'] else "📋" if priority in ['P2'] else "📝"
                response += f"│ {priority_emoji} {priority:<8} │ {count:<11} │ {visual_bar} {percentage:.1f}% │\n"
            
            response += "└─────────────┴─────────────┴─────────────────────────────┘\n\n"
            
            # Team Assignment Distribution Table
            if assigned_count > 0:
                response += "👥 **TEAM ASSIGNMENT DISTRIBUTION:**\n"
                response += "┌─────────────────────┬─────────────┬─────────────┬─────────────────────────────┐\n"
                response += "│ Team Member         │ Assigned    │ Percentage  │ Load Distribution           │\n"
                response += "├─────────────────────┼─────────────┼─────────────┼─────────────────────────────┤\n"
                
                for assignee, count in assignment_dist.items():
                    percentage = (count / assigned_count * 100) if assigned_count > 0 else 0
                    bar_length = int(percentage / 4)  # Scale bar to max 25 chars
                    visual_bar = "█" * bar_length + "░" * (25 - bar_length)
                    
                    # Determine performance indicator
                    if percentage >= 40:
                        indicator = "🔥 HIGH"
                    elif percentage >= 20:
                        indicator = "⚡ MED"
                    else:
                        indicator = "📋 LOW"
                    
                    response += f"│ {assignee:<19} │ {count:<11} │ {percentage:>6.1f}%    │ {visual_bar} {indicator:<6} │\n"
                
                response += "└─────────────────────┴─────────────┴─────────────┴─────────────────────────────┘\n\n"
            
            # Application Distribution
            app_dist = enhanced_df[enhanced_df['Assignment_Application'] != '']['Assignment_Application'].value_counts()
            if len(app_dist) > 0:
                response += "🏢 **APPLICATION AREA DISTRIBUTION:**\n"
                response += "┌─────────────────┬─────────────┬─────────────────────────────┐\n"
                response += "│ Application     │ Assignments │ Coverage Distribution       │\n"
                response += "├─────────────────┼─────────────┼─────────────────────────────┤\n"
                
                for app, count in app_dist.items():
                    percentage = (count / assigned_count * 100) if assigned_count > 0 else 0
                    bar_length = int(percentage / 4)
                    visual_bar = "█" * bar_length + "░" * (25 - bar_length)
                    
                    app_emoji = "🌐" if "SOM" in app else "💰" if "SQO" in app else "💳" if "BILLING" in app else "📱"
                    response += f"│ {app_emoji} {app:<12} │ {count:<11} │ {visual_bar} {percentage:.1f}% │\n"
                
                response += "└─────────────────┴─────────────┴─────────────────────────────┘\n\n"
            
            # Sample Assignments Table
            if assigned_count > 0:
                response += "🎯 **SAMPLE ASSIGNMENTS (Top 5):**\n"
                response += "┌──────────────┬─────────────────────┬──────────────┬───────┬─────────────────────────────────────┐\n"
                response += "│ Call ID      │ Assignee            │ Application  │ Score │ Key Specializations                 │\n"
                response += "├──────────────┼─────────────────────┼──────────────┼───────┼─────────────────────────────────────┤\n"
                
                sample_assignments = enhanced_df[enhanced_df['Assignee'] != ''].head(5)
                for idx, row in sample_assignments.iterrows():
                    call_id = str(row.get('Call ID', 'Unknown'))[:12]
                    assignee = str(row['Assignee'])[:19]
                    score = row.get('Assignment_Score', 0.0)
                    app = str(row.get('Assignment_Application', ''))[:12]
                    specializations = str(row.get('Extracted_Specializations', ''))[:35]
                    
                    score_indicator = "🏆" if score >= 0.8 else "⭐" if score >= 0.6 else "📋"
                    response += f"│ {call_id:<12} │ {assignee:<19} │ {app:<12} │ {score_indicator}{score:<4.2f} │ {specializations:<35} │\n"
                
                response += "└──────────────┴─────────────────────┴──────────────┴───────┴─────────────────────────────────────┘\n\n"
            
            # Enhanced File Information
            response += f"💾 **ENHANCED FILE DETAILS:**\n"
            response += f"   📁 **Output File**: {output_file}\n"
            response += f"   🔄 **File Management**: Automatic cleanup of older enhanced files\n"
            response += f"   📊 **Size**: {total_srs} rows with enhanced columns\n"
            response += f"   ⏰ **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # New Columns Added
            response += f"📋 **NEW ENHANCEMENT COLUMNS:**\n"
            response += f"   🏷️  **Assignee** - Team member names based on specialization matching\n"
            response += f"   📊 **Assignment_Score** - Confidence scores (0.0-1.0) for assignment quality\n"
            response += f"   🏢 **Assignment_Application** - Application areas (SOM_MM/SQO_MM/BILLING_MM)\n"
            response += f"   🔍 **Extracted_Specializations** - AI-detected specializations with confidence\n"
            response += f"   💭 **Assignment_Reasoning** - Detailed assignment explanations\n\n"
            
            # Performance Insights
            response += "💡 **PERFORMANCE INSIGHTS:**\n"
            if assignment_rate >= 80:
                response += "   ✅ **Excellent Assignment Rate** - Most SRs successfully matched to team expertise\n"
            elif assignment_rate >= 60:
                response += "   ⚡ **Good Assignment Rate** - Majority of SRs assigned with some optimization opportunities\n"
            else:
                response += "   ⚠️  **Room for Improvement** - Consider expanding team specializations or SR descriptions\n"
            
            if unassigned_count > 0:
                response += f"   📝 **{unassigned_count} Unassigned SRs** - May require manual review or specialized skills\n"
            
            # Next Steps
            response += f"\n🚀 **RECOMMENDED NEXT STEPS:**\n"
            response += f"   1. 📊 Open **{output_file}** to review all assignments\n"
            response += f"   2. 🔍 Check **Assignment_Reasoning** column for assignment logic\n"
            response += f"   3. ⚡ Use **'show team workload'** to verify current capacity\n"
            response += f"   4. 📈 Use **'show team skills'** to view team expertise matrix\n"
            response += f"   5. 🔄 Process additional SR files for comprehensive assignment\n\n"
            
            # Command Suggestions
            response += "🎯 **QUICK ACTIONS:**\n"
            response += "   • **'show team workload'** - View current team capacity utilization\n"
            response += "   • **'show detailed assignments'** - See all current assignments\n"
            response += "   • **'show team skills'** - Display team skills matrix\n"
            response += "   • **'process mukul file'** - Generate HTML dashboard with proper tables (default)\n"
            
            response += "\n" + "═" * 80 + "\n"
            response += f"✅ **Enhancement Complete!** Ready for team assignment and review.\n"
            
            # Update session data
            self.session_data['mukul_processed'] = True
            self.session_data['mukul_results'] = {
                'total_srs': total_srs,
                'assigned_count': assigned_count,
                'assignment_rate': assignment_rate,
                'output_file': output_file,
                'priority_distribution': dict(priority_dist),
                'assignment_distribution': dict(assignment_dist)
            }
            
            return response
            
        except Exception as e:
            return f"""❌ **Error Processing Mukul File**

An unexpected error occurred while processing the Mukul.xls file.

**Error details:** {str(e)}

🔧 **Troubleshooting steps:**
1. Ensure Mukul.xls has the required columns (Description, Notes, Status, Customer Priority)
2. Check that the file is not corrupted or open in Excel
3. Verify the people_skills.db database is accessible
4. Try processing a smaller subset of the data

**For support:** Check the error details above or contact system administrator.
"""
    
    def _generate_mukul_html_dashboard(self, command: str) -> str:
        """Generate comprehensive HTML dashboard for Mukul processing results"""
        try:
            # Check if we have a selected application from the session
            selected_app = self.session_data.get('selected_application', 'MIXED')
            
            enhancer = EnhancedMukulSRAssignment()
            print("🚀 Processing Mukul.xls for Enhanced SR Assignment...")
            
            # Use the selected application if available
            if selected_app and selected_app != 'MIXED':
                enhanced_df = enhancer.process_mukul_file(interactive=False, selected_app=selected_app)
            else:
                enhanced_df = enhancer.process_mukul_file(interactive=False)
            
            # Calculate statistics
            total_srs = len(enhanced_df)
            assigned_count = len(enhanced_df[enhanced_df['Assignee'] != ''])
            assignment_rate = (assigned_count / total_srs * 100) if total_srs > 0 else 0
            unassigned_count = total_srs - assigned_count
            
            # Get distributions
            assignment_dist = enhanced_df[enhanced_df['Assignee'] != '']['Assignee'].value_counts()
            priority_dist = enhanced_df['Customer Priority'].value_counts()
            app_dist = enhanced_df[enhanced_df['Assignment_Application'] != '']['Assignment_Application'].value_counts()
            
            # Find output file
            import glob
            enhanced_files = sorted(glob.glob('Mukul1_enhanced_*.xlsx'), key=os.path.getmtime, reverse=True)
            output_file = enhanced_files[0] if enhanced_files else 'Mukul1_enhanced_[timestamp].xlsx'
            
            # Generate application info
            app_names = {
                'SOM_MM': 'Service Order Management',
                'SQO_MM': 'Sales Quote Management', 
                'BILLING_MM': 'Billing Management',
                'ALL': 'All Applications Separately',
                'MIXED': 'All Applications Together'
            }
            app_display = app_names.get(selected_app, selected_app)
            
            # Generate HTML dashboard
            html_content = f"""
            <div class="mukul-dashboard">
                <div class="dashboard-header">
                    <h1>🎯 Mukul SR Assignment Dashboard</h1>
                    <p class="subtitle">Enhanced processing results with comprehensive analysis</p>
                    <div class="app-selection-info">
                        <span class="app-label">Application:</span>
                        <span class="app-value">{app_display}</span>
                    </div>
                </div>
                
                <!-- Processing Status Banner -->
                <div class="status-banner success">
                    <div class="status-icon">✅</div>
                    <div class="status-content">
                        <h3>Processing Complete!</h3>
                        <p>Mukul.xls successfully processed and enhanced with AI-powered assignments</p>
                    </div>
                </div>
                
                <!-- Key Metrics Cards -->
                <div class="metrics-grid">
                    <div class="metric-card total">
                        <div class="metric-icon">📊</div>
                        <div class="metric-content">
                            <div class="metric-value">{total_srs}</div>
                            <div class="metric-label">Total SRs Processed</div>
                        </div>
                    </div>
                    <div class="metric-card assigned">
                        <div class="metric-icon">✅</div>
                        <div class="metric-content">
                            <div class="metric-value">{assigned_count}</div>
                            <div class="metric-label">Successfully Assigned</div>
                        </div>
                    </div>
                    <div class="metric-card rate">
                        <div class="metric-icon">📈</div>
                        <div class="metric-content">
                            <div class="metric-value">{assignment_rate:.1f}%</div>
                            <div class="metric-label">Assignment Success Rate</div>
                        </div>
                    </div>
                    <div class="metric-card unassigned">
                        <div class="metric-icon">⚠️</div>
                        <div class="metric-content">
                            <div class="metric-value">{unassigned_count}</div>
                            <div class="metric-label">Require Manual Review</div>
                        </div>
                    </div>
                </div>
                
                <!-- Assignment Distribution Table -->
                <div class="table-section">
                    <h3>👥 Team Assignment Distribution</h3>
                    <div class="table-responsive">
                        <table class="assignment-table">
                            <thead>
                                <tr>
                                    <th>Team Member</th>
                                    <th>Assignments</th>
                                    <th>Percentage</th>
                                    <th>Load Distribution</th>
                                    <th>Performance</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            
            # Add assignment distribution rows
            for assignee, count in assignment_dist.items():
                percentage = (count / assigned_count * 100) if assigned_count > 0 else 0
                
                # Performance classification
                if percentage >= 40:
                    perf_class = "high"
                    perf_text = "🔥 High Load"
                elif percentage >= 20:
                    perf_class = "medium"
                    perf_text = "⚡ Balanced"
                else:
                    perf_class = "low"
                    perf_text = "📋 Light Load"
                
                html_content += f"""
                                <tr class="assignment-row">
                                    <td class="member-name"><strong>{assignee}</strong></td>
                                    <td class="assignment-count">{count}</td>
                                    <td class="assignment-percentage">{percentage:.1f}%</td>
                                    <td class="load-bar">
                                        <div class="progress-bar">
                                            <div class="progress-fill {perf_class}" style="width: {percentage}%"></div>
                                        </div>
                                    </td>
                                    <td class="performance-indicator {perf_class}">{perf_text}</td>
                                </tr>
                """
            
            # Priority Distribution
            html_content += """
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Priority Analysis -->
                <div class="priority-section">
                    <h3>🔥 Priority Distribution Analysis</h3>
                    <div class="priority-grid">
            """
            
            for priority, count in priority_dist.items():
                percentage = (count / total_srs * 100) if total_srs > 0 else 0
                
                priority_config = {
                    'P0': {'icon': '🚨', 'class': 'critical', 'label': 'Critical'},
                    'P1': {'icon': '⚡', 'class': 'high', 'label': 'High'},
                    'P2': {'icon': '📋', 'class': 'medium', 'label': 'Medium'},
                    'P3': {'icon': '📝', 'class': 'low', 'label': 'Standard'}
                }
                
                config = priority_config.get(priority, {'icon': '📝', 'class': 'low', 'label': 'Standard'})
                
                html_content += f"""
                        <div class="priority-card {config['class']}">
                            <div class="priority-icon">{config['icon']}</div>
                            <div class="priority-content">
                                <div class="priority-name">{priority} - {config['label']}</div>
                                <div class="priority-count">{count} SRs</div>
                                <div class="priority-percentage">{percentage:.1f}% of total</div>
                            </div>
                        </div>
                """
            
            # Sample Assignments
            sample_assignments = enhanced_df[enhanced_df['Assignee'] != ''].head(5)
            
            html_content += f"""
                    </div>
                </div>
                
                <!-- Sample Assignments -->
                <div class="sample-section">
                    <h3>🎯 Sample Assignments</h3>
                    <div class="table-responsive">
                        <table class="sample-table">
                            <thead>
                                <tr>
                                    <th>Call ID</th>
                                    <th>Assignee</th>
                                    <th>Application</th>
                                    <th>Score</th>
                                    <th>Key Specializations</th>
                                    <th>Priority</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            
            for idx, row in sample_assignments.iterrows():
                call_id = str(row.get('Call ID', 'Unknown'))
                assignee = str(row['Assignee'])
                score = row.get('Assignment_Score', 0.0)
                app = str(row.get('Assignment_Application', ''))
                specializations = str(row.get('Extracted_Specializations', ''))[:30]
                priority = str(row.get('Customer Priority', ''))
                
                score_class = "excellent" if score >= 0.8 else "good" if score >= 0.6 else "fair"
                score_icon = "🏆" if score >= 0.8 else "⭐" if score >= 0.6 else "📋"
                
                html_content += f"""
                                <tr class="sample-row">
                                    <td class="call-id">{call_id}</td>
                                    <td class="assignee-name">{assignee}</td>
                                    <td class="application">{app}</td>
                                    <td class="score {score_class}">{score_icon} {score:.2f}</td>
                                    <td class="specializations">{specializations}</td>
                                    <td class="priority">{priority}</td>
                                </tr>
                """
            
            # Complete the HTML
            html_content += f"""
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- File Details -->
                <div class="file-details-section">
                    <h3>💾 Enhanced File Information</h3>
                    <div class="details-grid">
                        <div class="detail-item">
                            <span class="detail-label">📁 Output File:</span>
                            <span class="detail-value">{output_file}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">📊 File Size:</span>
                            <span class="detail-value">{total_srs} rows with enhanced columns</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">⏰ Generated:</span>
                            <span class="detail-value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">🔄 Management:</span>
                            <span class="detail-value">Auto-cleanup of older files</span>
                        </div>
                    </div>
                </div>
                
                <!-- Enhanced Columns -->
                <div class="columns-section">
                    <h3>📋 New Enhancement Columns</h3>
                    <div class="columns-grid">
                        <div class="column-card">
                            <h4>🏷️ Assignee</h4>
                            <p>Team member names based on AI specialization matching</p>
                        </div>
                        <div class="column-card">
                            <h4>📊 Assignment_Score</h4>
                            <p>Confidence scores (0.0-1.0) for assignment quality assessment</p>
                        </div>
                        <div class="column-card">
                            <h4>🏢 Assignment_Application</h4>
                            <p>Application areas: SOM_MM, SQO_MM, or BILLING_MM</p>
                        </div>
                        <div class="column-card">
                            <h4>🔍 Extracted_Specializations</h4>
                            <p>AI-detected specializations with confidence scores</p>
                        </div>
                        <div class="column-card">
                            <h4>💭 Assignment_Reasoning</h4>
                            <p>Detailed explanations for assignment decisions</p>
                        </div>
                    </div>
                </div>
                
                <!-- Quick Actions -->
                <div class="actions-section">
                    <h3>🚀 Quick Actions</h3>
                    <div class="action-buttons">
                        <button class="action-btn primary" onclick="openFile()">
                            📊 Open Enhanced File
                        </button>
                        <button class="action-btn secondary" onclick="showWorkload()">
                            ⚡ View Team Workload
                        </button>
                        <button class="action-btn info" onclick="showSkills()">
                            🔧 Team Skills Matrix
                        </button>
                        <button class="action-btn success" onclick="showAssignments()">
                            📋 Detailed Assignments
                        </button>
                    </div>
                </div>
                
                <div class="footer-info">
                    <p>✅ Enhancement Complete! Ready for team assignment and review.</p>
                </div>
            </div>
            
            <style>
            .mukul-dashboard {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                border-radius: 15px;
            }}
            
            .dashboard-header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            
            .dashboard-header h1 {{
                color: #0f172a;
                font-size: 2.5em;
                margin: 0;
                font-weight: 700;
            }}
            
            .subtitle {{
                color: #64748b;
                font-size: 1.1em;
                margin: 10px 0 0 0;
            }}
            
            .app-selection-info {{
                margin-top: 15px;
                padding: 10px 20px;
                background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
                border-radius: 25px;
                border: 1px solid #0ea5e9;
                display: inline-block;
            }}
            
            .app-label {{
                color: #0369a1;
                font-weight: 600;
                margin-right: 8px;
            }}
            
            .app-value {{
                color: #0c4a6e;
                font-weight: 700;
                background: rgba(255, 255, 255, 0.7);
                padding: 4px 12px;
                border-radius: 15px;
                font-size: 0.95em;
            }}
            
            .status-banner {{
                display: flex;
                align-items: center;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            .status-banner.success {{
                background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
                border-left: 5px solid #22c55e;
            }}
            
            .status-icon {{
                font-size: 2.5em;
                margin-right: 20px;
            }}
            
            .status-content h3 {{
                margin: 0;
                color: #15803d;
                font-size: 1.4em;
            }}
            
            .status-content p {{
                margin: 5px 0 0 0;
                color: #166534;
            }}
            
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .metric-card {{
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                display: flex;
                align-items: center;
                border-left: 4px solid;
            }}
            
            .metric-card.total {{ border-left-color: #3b82f6; }}
            .metric-card.assigned {{ border-left-color: #22c55e; }}
            .metric-card.rate {{ border-left-color: #f59e0b; }}
            .metric-card.unassigned {{ border-left-color: #ef4444; }}
            
            .metric-icon {{
                font-size: 2.5em;
                margin-right: 20px;
            }}
            
            .metric-value {{
                font-size: 2.2em;
                font-weight: bold;
                color: #1e40af;
                line-height: 1;
            }}
            
            .metric-label {{
                color: #64748b;
                font-size: 0.9em;
                margin-top: 5px;
            }}
            
            .table-section, .priority-section, .sample-section, .file-details-section, .columns-section, .actions-section {{
                background: white;
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 25px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            .table-section h3, .priority-section h3, .sample-section h3, .file-details-section h3, .columns-section h3, .actions-section h3 {{
                margin: 0 0 20px 0;
                color: #1f2937;
                font-size: 1.5em;
            }}
            
            .table-responsive {{
                overflow-x: auto;
            }}
            
            .assignment-table, .sample-table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
            }}
            
            .assignment-table th, .sample-table th {{
                background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                color: white;
                padding: 15px 12px;
                text-align: left;
                font-weight: 600;
                border: none;
            }}
            
            .assignment-table td, .sample-table td {{
                padding: 12px;
                border-bottom: 1px solid #e5e7eb;
                vertical-align: middle;
            }}
            
            .assignment-row:hover, .sample-row:hover {{
                background-color: #f9fafb;
            }}
            
            .member-name {{
                font-weight: 600;
                color: #1f2937;
            }}
            
            .load-bar {{
                width: 120px;
            }}
            
            .progress-bar {{
                width: 100%;
                height: 8px;
                background-color: #e5e7eb;
                border-radius: 4px;
                overflow: hidden;
            }}
            
            .progress-fill {{
                height: 100%;
                border-radius: 4px;
                transition: width 0.3s ease;
            }}
            
            .progress-fill.high {{ background-color: #ef4444; }}
            .progress-fill.medium {{ background-color: #f59e0b; }}
            .progress-fill.low {{ background-color: #22c55e; }}
            
            .performance-indicator.high {{ color: #dc2626; font-weight: 600; }}
            .performance-indicator.medium {{ color: #d97706; font-weight: 600; }}
            .performance-indicator.low {{ color: #16a34a; font-weight: 600; }}
            
            .priority-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
            }}
            
            .priority-card {{
                display: flex;
                align-items: center;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid;
            }}
            
            .priority-card.critical {{ background: #fef2f2; border-left-color: #dc2626; }}
            .priority-card.high {{ background: #fffbeb; border-left-color: #f59e0b; }}
            .priority-card.medium {{ background: #f0f9ff; border-left-color: #3b82f6; }}
            .priority-card.low {{ background: #f9fafb; border-left-color: #6b7280; }}
            
            .priority-icon {{
                font-size: 2em;
                margin-right: 15px;
            }}
            
            .priority-name {{
                font-weight: 600;
                color: #1f2937;
            }}
            
            .priority-count {{
                font-size: 1.3em;
                font-weight: bold;
                color: #3b82f6;
            }}
            
            .priority-percentage {{
                font-size: 0.9em;
                color: #6b7280;
            }}
            
            .score.excellent {{ color: #16a34a; font-weight: 600; }}
            .score.good {{ color: #d97706; font-weight: 600; }}
            .score.fair {{ color: #dc2626; font-weight: 600; }}
            
            .details-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 15px;
            }}
            
            .detail-item {{
                display: flex;
                justify-content: space-between;
                padding: 10px;
                background: #f8fafc;
                border-radius: 6px;
            }}
            
            .detail-label {{
                font-weight: 600;
                color: #374151;
            }}
            
            .detail-value {{
                color: #1f2937;
            }}
            
            .columns-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }}
            
            .column-card {{
                padding: 20px;
                background: #f8fafc;
                border-radius: 10px;
                border-left: 4px solid #3b82f6;
            }}
            
            .column-card h4 {{
                margin: 0 0 10px 0;
                color: #1f2937;
                font-size: 1.1em;
            }}
            
            .column-card p {{
                margin: 0;
                color: #6b7280;
                font-size: 0.9em;
            }}
            
            .action-buttons {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
            }}
            
            .action-btn {{
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 15px 20px;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                color: white;
                font-size: 1em;
            }}
            
            .action-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}
            
            .action-btn.primary {{ background: linear-gradient(135deg, #3b82f6, #1d4ed8); }}
            .action-btn.secondary {{ background: linear-gradient(135deg, #6b7280, #374151); }}
            .action-btn.info {{ background: linear-gradient(135deg, #0ea5e9, #0284c7); }}
            .action-btn.success {{ background: linear-gradient(135deg, #10b981, #059669); }}
            
            .footer-info {{
                text-align: center;
                margin-top: 20px;
                padding: 20px;
                background: #f0f9ff;
                border-radius: 10px;
                color: #1e40af;
                font-weight: 600;
            }}
            
            @media (max-width: 768px) {{
                .metrics-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
                
                .action-buttons {{
                    grid-template-columns: 1fr;
                }}
            }}
            </style>
            """
            
            # Update session data
            self.session_data['mukul_processed'] = True
            self.session_data['mukul_results'] = {
                'total_srs': total_srs,
                'assigned_count': assigned_count,
                'assignment_rate': assignment_rate,
                'output_file': output_file,
                'priority_distribution': dict(priority_dist),
                'assignment_distribution': dict(assignment_dist)
            }
            
            return html_content
            
        except Exception as e:
            return f"""
            <div class="error-container">
                <h3>❌ Error Processing Mukul File</h3>
                <p>An unexpected error occurred while processing the Mukul.xls file.</p>
                <p><strong>Error details:</strong> {str(e)}</p>
                <div class="troubleshooting">
                    <strong>Troubleshooting steps:</strong>
                    <ul>
                        <li>Ensure Mukul.xls has the required columns</li>
                        <li>Check that the file is not corrupted or open in Excel</li>
                        <li>Verify the people_skills.db database is accessible</li>
                    </ul>
                </div>
            </div>
            """
    
    def _generate_enhanced_team_skills(self) -> str:
        """Generate enhanced team skills display with improved UI"""
        try:
            from people_skills_database import PeopleSkillsDatabase
            
            # Initialize database connection
            db = PeopleSkillsDatabase()
            config = db.get_team_configuration()
            
            if not config:
                return "❌ No team configuration found. Please ensure the People.xlsx file has been loaded."
            
            # Generate enhanced response with improved formatting
            response = "🎯 **ENHANCED TEAM SKILLS MATRIX**\n"
            response += "=" * 60 + "\n\n"
            
            # Team overview statistics
            total_members = len(config)
            total_applications = set()
            total_specializations = set()
            
            for member_data in config.values():
                for app in member_data['applications'].keys():
                    total_applications.add(app)
                for app_data in member_data['applications'].values():
                    total_specializations.update(app_data['specializations'])
            
            response += f"📊 **TEAM OVERVIEW:**\n"
            response += f"   • Active Members: **{total_members}**\n"
            response += f"   • Applications Covered: **{len(total_applications)}** ({', '.join(sorted(total_applications))})\n"
            response += f"   • Total Specializations: **{len(total_specializations)}**\n\n"
            
            # Capacity Analysis
            response += "⚡ **CAPACITY ANALYSIS:**\n"
            capacity_data = []
            total_capacity = 0
            
            for member_name, member_data in config.items():
                member_capacity = 0
                for app_data in member_data['applications'].values():
                    member_capacity = max(member_capacity, app_data['max_load'])
                capacity_data.append((member_name, member_capacity))
                total_capacity += member_capacity
            
            capacity_data.sort(key=lambda x: x[1], reverse=True)
            
            for name, capacity in capacity_data:
                utilization_indicator = "🟢 HIGH" if capacity >= 15 else "🟡 MED" if capacity >= 10 else "🔴 LOW"
                response += f"   • **{name}**: {capacity} SRs max {utilization_indicator}\n"
            
            response += f"\n   📈 **Total Team Capacity**: {total_capacity} SRs\n\n"
            
            # Team Skills Table
            response += "🔧 **TEAM SKILLS TABLE:**\n"
            response += "=" * 120 + "\n"
            
            # Create team skills table
            response += self._create_team_skills_table(config)
            
            # Individual Member Details
            response += "\n\n📋 **DETAILED MEMBER PROFILES:**\n"
            response += "=" * 80 + "\n\n"
            
            for member_name, member_data in config.items():
                # Member header with status
                status_emoji = "✅" if member_data['status'] == 'active' else "❌"
                response += f"{status_emoji} **{member_name}** ({member_data['status'].upper()})\n"
                
                # Create individual member table
                response += self._create_member_skills_table(member_name, member_data)
                response += "\n" + "-" * 80 + "\n\n"
            
            # Application Coverage Table
            response += "🏢 **APPLICATION COVERAGE TABLE:**\n"
            response += "=" * 100 + "\n"
            response += self._create_application_coverage_table(config, total_applications)
            response += "\n"
            
            # Actionable Insights
            response += "💡 **ACTIONABLE INSIGHTS:**\n"
            response += "-" * 60 + "\n"
            
            # Find skill gaps
            skill_gaps = []
            for app in total_applications:
                experts = sum(1 for member_data in config.values() 
                            if app in member_data['applications'] and member_data['applications'][app]['skill_level'] >= 4.0)
                if experts == 0:
                    skill_gaps.append(app)
            
            if skill_gaps:
                response += f"🔴 **Skill Gaps**: {', '.join(skill_gaps)} need expert-level members (4.0+ skill)\n"
            
            # Find capacity bottlenecks
            low_capacity_apps = []
            for app in total_applications:
                total_app_capacity = sum(member_data['applications'][app]['max_load'] 
                                       for member_data in config.values() 
                                       if app in member_data['applications'])
                if total_app_capacity < 30:  # Threshold for low capacity
                    low_capacity_apps.append(f"{app} ({total_app_capacity} SRs)")
            
            if low_capacity_apps:
                response += f"⚠️ **Capacity Bottlenecks**: {', '.join(low_capacity_apps)}\n"
            
            # Training recommendations
            response += f"📚 **Training Recommendations**: Focus on upskilling in {', '.join(skill_gaps[:2])} applications\n"
            response += f"🎯 **Optimal Team Load**: {int(total_capacity * 0.8)} SRs (80% of max capacity)\n\n"
            
            # Quick Actions
            response += "⚡ **QUICK ACTIONS:**\n"
            response += "   • `Update [Name] [App] skill to [Level]` - Update skill levels\n"
            response += "   • `Set [Name] [App] load to [Number]` - Adjust capacity\n"
            response += "   • `Show skill evolution` - View ML learning progress\n"
            response += "   • `Export config` - Download team configuration\n\n"
            
            # Footer
            response += "=" * 60 + "\n"
            response += f"📅 **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            response += "🔄 **Auto-updated** by ML learning from assignment performance\n"
            
            # Add HTML table option note
            response += "\n💡 **Enhanced View Options:**\n"
            response += "   • Current: 📊 Text-based table format\n"
            response += "   • Available: 🌐 HTML table format (for web interface)\n"
            response += "   • Use `Show team skills HTML` for interactive web tables\n"
            
            return response
            
        except Exception as e:
            return f"""❌ **Error Loading Team Skills**

An error occurred while retrieving team skills configuration.

**Error details:** {str(e)}

🔧 **Troubleshooting:**
1. Ensure People.xlsx has been loaded into the database
2. Check database connectivity
3. Verify team configuration is properly set up

**Alternative commands:**
• `Load People.xlsx` - Reload team configuration  
• `Show team` - Basic team overview
• `View [Member Name]` - Individual member details
"""
    
    def _create_team_skills_table(self, config: dict) -> str:
        """Create a formatted table showing team skills overview"""
        try:
            # Collect all team data for table
            table_data = []
            applications = set()
            
            for member_name, member_data in config.items():
                for app in member_data['applications'].keys():
                    applications.add(app)
            
            applications = sorted(applications)
            
            # Create table header
            table = "\n"
            table += f"{'MEMBER':<20} | {'STATUS':<8} | "
            for app in applications:
                table += f"{app:<12} | "
            table += f"{'CAPACITY':<10} | {'OVERALL':<15}\n"
            
            table += "-" * (20 + 11 + len(applications) * 15 + 12 + 17) + "\n"
            
            # Add team member rows
            for member_name, member_data in config.items():
                status_indicator = "✅ ACTIVE" if member_data['status'] == 'active' else "❌ INACTIVE"
                
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
                row = f"{member_name:<20} | {status_indicator:<8} | "
                
                # Add skill levels for each application
                for app in applications:
                    if app in member_data['applications']:
                        skill_level = member_data['applications'][app]['skill_level']
                        if skill_level >= 4.0:
                            app_skill = f"🏆 {skill_level:.1f}/5"
                        elif skill_level >= 3.0:
                            app_skill = f"⭐ {skill_level:.1f}/5"
                        elif skill_level >= 2.0:
                            app_skill = f"📘 {skill_level:.1f}/5"
                        else:
                            app_skill = f"🌱 {skill_level:.1f}/5"
                        row += f"{app_skill:<12} | "
                    else:
                        row += f"{'N/A':<12} | "
                
                # Add capacity and overall
                capacity_indicator = "🔥" if max_capacity >= 15 else "⚡" if max_capacity >= 10 else "🔋"
                row += f"{capacity_indicator} {max_capacity:<6} | {overall:<15}\n"
                
                table += row
            
            # Add summary row
            table += "-" * (20 + 11 + len(applications) * 15 + 12 + 17) + "\n"
            
            # Calculate totals
            total_capacity = sum(
                max(app_data['max_load'] for app_data in member_data['applications'].values())
                for member_data in config.values()
            )
            
            total_avg_skill = sum(
                sum(app_data['skill_level'] for app_data in member_data['applications'].values()) / len(member_data['applications'])
                for member_data in config.values()
            ) / len(config)
            
            summary_row = f"{'TEAM TOTALS':<20} | {'SUMMARY':<8} | "
            
            # Application averages
            for app in applications:
                app_skills = [
                    member_data['applications'][app]['skill_level']
                    for member_data in config.values()
                    if app in member_data['applications']
                ]
                if app_skills:
                    avg_app_skill = sum(app_skills) / len(app_skills)
                    summary_row += f"{'📊 ' + str(avg_app_skill)[:3]:<12} | "
                else:
                    summary_row += f"{'N/A':<12} | "
            
            summary_row += f"{'📈 ' + str(total_capacity):<10} | {'📊 ' + str(total_avg_skill)[:3]:<15}\n"
            table += summary_row
            
            return table
            
        except Exception as e:
            return f"Error creating team skills table: {str(e)}\n"
    
    def _create_member_skills_table(self, member_name: str, member_data: dict) -> str:
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
            
            table = f"\n📈 **Overall**: {avg_skill:.1f}/5 {skill_indicator} | Confidence: {avg_confidence:.2f} {confidence_indicator} | Capacity: {max_capacity} SRs\n\n"
            
            # Skills table header
            table += f"{'APPLICATION':<15} | {'SKILL LEVEL':<15} | {'CONFIDENCE':<12} | {'CAPACITY':<12} | {'TOP SPECIALIZATIONS':<40}\n"
            table += "-" * 95 + "\n"
            
            # Application rows
            for app, app_data in member_data['applications'].items():
                skill_level = app_data['skill_level']
                confidence = app_data['confidence_score']
                max_load = app_data['max_load']
                
                # Skill level with emoji
                if skill_level >= 4.5:
                    skill_display = f"🏆 {skill_level:.1f}/5"
                elif skill_level >= 3.5:
                    skill_display = f"⭐ {skill_level:.1f}/5"
                elif skill_level >= 2.5:
                    skill_display = f"📘 {skill_level:.1f}/5"
                elif skill_level >= 1.5:
                    skill_display = f"🌱 {skill_level:.1f}/5"
                else:
                    skill_display = f"🆕 {skill_level:.1f}/5"
                
                # Confidence with emoji
                confidence_emoji = "🎯" if confidence >= 0.8 else "🔍" if confidence >= 0.6 else "⚠️"
                confidence_display = f"{confidence_emoji} {confidence:.2f}"
                
                # Capacity with emoji
                load_emoji = "🔥" if max_load >= 15 else "⚡" if max_load >= 10 else "🔋"
                capacity_display = f"{load_emoji} {max_load} SRs"
                
                # Top specializations (truncate if too long)
                specs = app_data['specializations'][:3]  # Top 3
                specs_display = ', '.join(specs) if specs else "None defined"
                if len(specs_display) > 38:
                    specs_display = specs_display[:35] + "..."
                
                table += f"{app:<15} | {skill_display:<15} | {confidence_display:<12} | {capacity_display:<12} | {specs_display:<40}\n"
            
            return table
            
        except Exception as e:
            return f"Error creating member skills table: {str(e)}\n"
    
    def _create_application_coverage_table(self, config: dict, applications: set) -> str:
        """Create a table showing application coverage and capacity analysis"""
        try:
            table = "\n"
            
            # Table header
            table += f"{'APPLICATION':<15} | {'TOTAL CAPACITY':<15} | {'EXPERTS':<8} | {'SENIORS':<8} | {'COVERAGE':<10} | {'EXPERT TEAM':<45}\n"
            table += "-" * 105 + "\n"
            
            for app in sorted(applications):
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
                            experts.append(f"{member_name}({skill_level:.1f})")
                        elif skill_level >= 3.0:
                            seniors.append(f"{member_name}({skill_level:.1f})")
                
                # Coverage indicator
                if len(experts) >= 2:
                    coverage = "🟢 STRONG"
                elif len(experts) == 1 or len(seniors) >= 2:
                    coverage = "🟡 ADEQUATE"
                else:
                    coverage = "🔴 WEAK"
                
                # Expert team display (truncate if too long)
                expert_team = ", ".join(experts + seniors) if experts or seniors else "None"
                if len(expert_team) > 43:
                    expert_team = expert_team[:40] + "..."
                
                # Capacity indicator
                capacity_emoji = "🔥" if app_capacity >= 50 else "⚡" if app_capacity >= 30 else "🔋"
                capacity_display = f"{capacity_emoji} {app_capacity} SRs"
                
                table += f"{app:<15} | {capacity_display:<15} | {len(experts):<8} | {len(seniors):<8} | {coverage:<10} | {expert_team:<45}\n"
            
            # Summary row
            table += "-" * 105 + "\n"
            
            total_experts = sum(
                sum(1 for app_data in member_data['applications'].values() if app_data['skill_level'] >= 4.0)
                for member_data in config.values()
            )
            
            total_seniors = sum(
                sum(1 for app_data in member_data['applications'].values() if 3.0 <= app_data['skill_level'] < 4.0)
                for member_data in config.values()
            )
            
            total_capacity = sum(
                sum(app_data['max_load'] for app_data in member_data['applications'].values())
                for member_data in config.values()
            )
            
            summary_row = f"{'TOTALS':<15} | {'📈 ' + str(total_capacity) + ' SRs':<15} | {total_experts:<8} | {total_seniors:<8} | {'📊 SUMMARY':<10} | {'Team-wide coverage analysis':<45}\n"
            table += summary_row
            
            return table
            
        except Exception as e:
            return f"Error creating application coverage table: {str(e)}\n"
    
    def _create_html_team_skills_table(self, config: dict) -> str:
        """Create an HTML table for team skills (for web interface)"""
        try:
            # Collect applications
            applications = set()
            for member_data in config.values():
                for app in member_data['applications'].keys():
                    applications.add(app)
            applications = sorted(applications)
            
            html = """
            <div class="team-skills-table">
                <h3>🎯 Team Skills Matrix</h3>
                <table class="skills-table">
                    <thead>
                        <tr>
                            <th>Member</th>
                            <th>Status</th>"""
            
            for app in applications:
                html += f"<th>{app}</th>"
            
            html += """
                            <th>Capacity</th>
                            <th>Overall</th>
                        </tr>
                    </thead>
                    <tbody>"""
            
            # Add member rows
            for member_name, member_data in config.items():
                status_class = "active" if member_data['status'] == 'active' else "inactive"
                status_icon = "✅" if member_data['status'] == 'active' else "❌"
                
                # Calculate overall metrics
                skill_levels = [app_data['skill_level'] for app_data in member_data['applications'].values()]
                avg_skill = sum(skill_levels) / len(skill_levels) if skill_levels else 0
                max_capacity = max((app_data['max_load'] for app_data in member_data['applications'].values()), default=0)
                
                # Overall skill class
                if avg_skill >= 4.0:
                    overall_class = "expert"
                    overall_text = "🚀 EXPERT"
                elif avg_skill >= 3.0:
                    overall_class = "senior"
                    overall_text = "⭐ SENIOR"
                elif avg_skill >= 2.0:
                    overall_class = "mid"
                    overall_text = "📘 MID"
                else:
                    overall_class = "junior"
                    overall_text = "🌱 JUNIOR"
                
                html += f"""
                        <tr class="member-row {status_class}">
                            <td class="member-name"><strong>{member_name}</strong></td>
                            <td class="status {status_class}">{status_icon} {member_data['status'].upper()}</td>"""
                
                # Add skill levels for each application
                for app in applications:
                    if app in member_data['applications']:
                        skill_level = member_data['applications'][app]['skill_level']
                        
                        # Determine skill class and icon
                        if skill_level >= 4.0:
                            skill_class = "expert"
                            skill_icon = "🏆"
                        elif skill_level >= 3.0:
                            skill_class = "senior"
                            skill_icon = "⭐"
                        elif skill_level >= 2.0:
                            skill_class = "mid"
                            skill_icon = "📘"
                        else:
                            skill_class = "junior"
                            skill_icon = "🌱"
                        
                        html += f'<td class="skill-cell {skill_class}">{skill_icon} {skill_level:.1f}/5</td>'
                    else:
                        html += '<td class="skill-cell na">N/A</td>'
                
                # Capacity cell
                capacity_class = "high" if max_capacity >= 15 else "medium" if max_capacity >= 10 else "low"
                capacity_icon = "🔥" if max_capacity >= 15 else "⚡" if max_capacity >= 10 else "🔋"
                
                html += f"""
                            <td class="capacity {capacity_class}">{capacity_icon} {max_capacity} SRs</td>
                            <td class="overall {overall_class}">{overall_text}</td>
                        </tr>"""
            
            html += """
                    </tbody>
                </table>
            </div>
            
            <style>
            .team-skills-table {
                margin: 20px 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .skills-table {
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .skills-table th {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 8px;
                text-align: center;
                font-weight: 600;
                font-size: 0.9em;
            }
            
            .skills-table td {
                padding: 10px 8px;
                text-align: center;
                border-bottom: 1px solid #eee;
                font-size: 0.85em;
            }
            
            .member-row:hover {
                background-color: #f8f9ff;
            }
            
            .member-name {
                text-align: left !important;
                font-weight: 600;
            }
            
            .status.active { color: #22c55e; }
            .status.inactive { color: #ef4444; }
            
            .skill-cell.expert { background-color: #dcfce7; color: #15803d; }
            .skill-cell.senior { background-color: #fef3c7; color: #d97706; }
            .skill-cell.mid { background-color: #dbeafe; color: #2563eb; }
            .skill-cell.junior { background-color: #f3e8ff; color: #7c3aed; }
            .skill-cell.na { background-color: #f9fafb; color: #6b7280; }
            
            .capacity.high { background-color: #fee2e2; color: #dc2626; }
            .capacity.medium { background-color: #fef3c7; color: #d97706; }
            .capacity.low { background-color: #ecfdf5; color: #059669; }
            
            .overall.expert { background-color: #dcfce7; color: #15803d; font-weight: 600; }
            .overall.senior { background-color: #fef3c7; color: #d97706; font-weight: 600; }
            .overall.mid { background-color: #dbeafe; color: #2563eb; font-weight: 600; }
            .overall.junior { background-color: #f3e8ff; color: #7c3aed; font-weight: 600; }
            </style>"""
            
            return html
            
        except Exception as e:
            return f"<div class='error'>Error creating HTML table: {str(e)}</div>"
    
    def _generate_enhanced_team_skills_html(self) -> str:
        """Generate enhanced team skills display in HTML format"""
        try:
            from people_skills_database import PeopleSkillsDatabase
            
            # Initialize database connection
            db = PeopleSkillsDatabase()
            config = db.get_team_configuration()
            
            if not config:
                return "❌ No team configuration found. Please ensure the People.xlsx file has been loaded."
            
            # Generate HTML response
            html_content = """
            <div class="enhanced-team-skills">
                <h2>🎯 Enhanced Team Skills Matrix</h2>
                <div class="team-overview">
                    <h3>📊 Team Overview</h3>
            """
            
            # Team statistics
            total_members = len(config)
            total_applications = set()
            total_specializations = set()
            total_capacity = 0
            
            for member_data in config.values():
                for app, app_data in member_data['applications'].items():
                    total_applications.add(app)
                    total_specializations.update(app_data['specializations'])
                    total_capacity += app_data['max_load']
            
            html_content += f"""
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h4>👥 Active Members</h4>
                            <div class="stat-value">{total_members}</div>
                        </div>
                        <div class="stat-card">
                            <h4>🏢 Applications</h4>
                            <div class="stat-value">{len(total_applications)}</div>
                            <div class="stat-detail">{', '.join(sorted(total_applications))}</div>
                        </div>
                        <div class="stat-card">
                            <h4>⚡ Total Capacity</h4>
                            <div class="stat-value">{total_capacity} SRs</div>
                        </div>
                        <div class="stat-card">
                            <h4>🔧 Specializations</h4>
                            <div class="stat-value">{len(total_specializations)}</div>
                        </div>
                    </div>
                </div>
                
                <div class="team-skills-matrix">
            """
            
            # Add the HTML table
            html_content += self._create_html_team_skills_table(config)
            
            # Add application coverage table
            html_content += """
                </div>
                
                <div class="application-coverage">
                    <h3>🏢 Application Coverage Analysis</h3>
            """
            
            # Create application coverage HTML table
            html_content += self._create_html_application_coverage_table(config, total_applications)
            
            # Add insights and quick actions
            html_content += f"""
                </div>
                
                <div class="insights-section">
                    <h3>💡 Key Insights</h3>
                    <div class="insights-grid">
                        <div class="insight-card success">
                            <h4>🎯 Optimal Load</h4>
                            <p>{int(total_capacity * 0.8)} SRs (80% capacity)</p>
                        </div>
                        <div class="insight-card warning">
                            <h4>⚠️ Capacity Planning</h4>
                            <p>Monitor load distribution across applications</p>
                        </div>
                        <div class="insight-card info">
                            <h4>📈 ML Learning</h4>
                            <p>Auto-updated from assignment performance</p>
                        </div>
                    </div>
                </div>
                
                <div class="quick-actions">
                    <h3>⚡ Quick Actions</h3>
                    <div class="action-buttons">
                        <button class="action-btn" onclick="updateSkills()">📝 Update Skills</button>
                        <button class="action-btn" onclick="adjustCapacity()">⚡ Adjust Capacity</button>
                        <button class="action-btn" onclick="showEvolution()">📊 Skill Evolution</button>
                        <button class="action-btn" onclick="exportConfig()">📤 Export Config</button>
                    </div>
                </div>
                
                <div class="footer">
                    <p>📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>🔄 Auto-updated by ML learning from assignment performance</p>
                </div>
            </div>
            
            <style>
            .enhanced-team-skills {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                border-radius: 12px;
            }}
            
            .enhanced-team-skills h2 {{
                color: #2d3748;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2em;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }}
            
            .stat-card h4 {{
                margin: 0 0 10px 0;
                color: #4a5568;
                font-size: 0.9em;
            }}
            
            .stat-value {{
                font-size: 2em;
                font-weight: bold;
                color: #2b6cb0;
                margin-bottom: 5px;
            }}
            
            .stat-detail {{
                font-size: 0.8em;
                color: #718096;
            }}
            
            .insights-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }}
            
            .insight-card {{
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid;
            }}
            
            .insight-card.success {{
                background: #f0fff4;
                border-color: #38a169;
            }}
            
            .insight-card.warning {{
                background: #fffbf0;
                border-color: #d69e2e;
            }}
            
            .insight-card.info {{
                background: #ebf8ff;
                border-color: #3182ce;
            }}
            
            .action-buttons {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 10px;
                margin-bottom: 20px;
            }}
            
            .action-btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 16px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                transition: transform 0.2s;
            }}
            
            .action-btn:hover {{
                transform: translateY(-2px);
            }}
            
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
                color: #718096;
                font-size: 0.9em;
            }}
            </style>
            """
            
            return html_content
            
        except Exception as e:
            return f"""<div class='error-container'>
                <h3>❌ Error Loading Team Skills</h3>
                <p>An error occurred while retrieving team skills configuration.</p>
                <p><strong>Error details:</strong> {str(e)}</p>
            </div>"""
    
    def _create_html_application_coverage_table(self, config: dict, applications: set) -> str:
        """Create HTML table for application coverage"""
        try:
            html = """
            <div class="table-responsive coverage-table-container">
                <table class="coverage-table">
                <thead>
                    <tr>
                        <th>Application</th>
                        <th>Total Capacity</th>
                        <th>Experts</th>
                        <th>Seniors</th>
                        <th>Coverage</th>
                        <th>Expert Team</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for app in sorted(applications):
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
                            experts.append(f"{member_name}({skill_level:.1f})")
                        elif skill_level >= 3.0:
                            seniors.append(f"{member_name}({skill_level:.1f})")
                
                # Coverage status
                if len(experts) >= 2:
                    coverage_class = "strong"
                    coverage_text = "🟢 STRONG"
                elif len(experts) == 1 or len(seniors) >= 2:
                    coverage_class = "adequate"
                    coverage_text = "🟡 ADEQUATE"
                else:
                    coverage_class = "weak"
                    coverage_text = "🔴 WEAK"
                
                expert_team = ", ".join(experts + seniors) if experts or seniors else "None"
                
                html += f"""
                    <tr>
                        <td class="app-name">{app}</td>
                        <td class="capacity">{app_capacity} SRs</td>
                        <td class="expert-count">{len(experts)}</td>
                        <td class="senior-count">{len(seniors)}</td>
                        <td class="coverage {coverage_class}">{coverage_text}</td>
                        <td class="expert-team">{expert_team}</td>
                    </tr>
                """
            
            html += """
                </tbody>
            </table>
            </div>
            
            <style>
            .coverage-table-container {{
                position: relative;
            }}
            
            .coverage-table-container::after {{
                content: '← Scroll horizontally for complete analysis →';
                position: absolute;
                top: 10px;
                right: 10px;
                font-size: 0.7em;
                font-weight: 400;
                color: #94a3b8;
                font-style: italic;
                background: rgba(255,255,255,0.9);
                padding: 5px 10px;
                border-radius: 4px;
                white-space: nowrap;
                z-index: 10;
            }}
            
            @media (max-width: 768px) {{
                .coverage-table-container::after {{
                    content: '← Scroll →';
                    font-size: 0.6em;
                    padding: 3px 6px;
                }}
            }}
            
            
            .coverage-table {
                width: 100%;
                min-width: 1200px;
                border-collapse: collapse;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin: 20px 0;
                table-layout: fixed;
            }
            
            .coverage-table th {
                background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
                color: white;
                padding: 15px 20px;
                text-align: left;
                font-weight: 600;
                font-size: 0.95em;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            .coverage-table td {
                padding: 15px 20px;
                border-bottom: 1px solid #e2e8f0;
                vertical-align: middle;
                font-size: 0.9em;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            .coverage-table th:first-child,
            .coverage-table td:first-child {
                width: 220px;
                white-space: normal;
                word-wrap: break-word;
                font-weight: 600;
                text-overflow: initial;
                overflow: visible;
            }
            
            .coverage-table th:nth-child(2),
            .coverage-table td:nth-child(2) {
                width: 160px;
                text-align: center;
                white-space: nowrap;
            }
            
            .coverage-table th:nth-child(3),
            .coverage-table td:nth-child(3) {
                width: 140px;
                text-align: center;
                white-space: nowrap;
            }
            
            .coverage-table th:nth-child(4),
            .coverage-table td:nth-child(4) {
                width: 140px;
                text-align: center;
                white-space: nowrap;
            }
            
            .coverage-table th:nth-child(5),
            .coverage-table td:nth-child(5) {
                width: 180px;
                text-align: center;
                white-space: nowrap;
            }
            
            .coverage-table th:nth-child(6),
            .coverage-table td:nth-child(6) {
                width: 280px;
                white-space: normal;
                word-wrap: break-word;
                text-overflow: initial;
                overflow: visible;
            }
            
            .coverage-table tr:hover {
                background-color: #f7fafc;
            }
            
            .app-name { font-weight: 600; }
            .coverage.strong { color: #38a169; font-weight: 600; }
            .coverage.adequate { color: #d69e2e; font-weight: 600; }
            .coverage.weak { color: #e53e3e; font-weight: 600; }
            </style>
            """
            
            return html
            
        except Exception as e:
            return f"<div class='error'>Error creating coverage table: {str(e)}</div>"
    
    def _generate_team_skills_html_table(self) -> str:
        """Generate team skills display with proper HTML tables for web interface"""
        try:
            from people_skills_database import PeopleSkillsDatabase
            
            # Initialize database connection
            db = PeopleSkillsDatabase()
            config = db.get_team_configuration()
            
            if not config:
                return """
                <div class="alert alert-warning">
                    <h4>❌ No Team Configuration Found</h4>
                    <p>Please ensure the People.xlsx file has been loaded into the database.</p>
                </div>
                """
            
            # Calculate team statistics
            total_members = len(config)
            total_applications = set()
            total_specializations = set()
            total_capacity = 0
            
            for member_data in config.values():
                for app, app_data in member_data['applications'].items():
                    total_applications.add(app)
                    total_specializations.update(app_data['specializations'])
                    total_capacity += app_data['max_load']
            
            applications = sorted(total_applications)
            
            # Generate complete HTML response
            html_response = f"""
            <div class="team-skills-response">
                <div class="response-header">
                    <h3>🎯 Team Skills Matrix</h3>
                    <p class="subtitle">Complete team skills overview with capacity analysis</p>
                </div>
                
                <!-- Team Overview Cards -->
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
                        <div class="stat-icon">🔧</div>
                        <div class="stat-content">
                            <div class="stat-number">{len(total_specializations)}</div>
                            <div class="stat-label">Specializations</div>
                        </div>
                    </div>
                </div>
                
                <!-- Main Team Skills Table -->
                <div class="table-container">
                    <h3>📊 Team Skills Overview</h3>
                    <div class="table-responsive">
                        <table class="team-skills-table">
                            <thead>
                                <tr>
                                    <th class="member-col">Team Member</th>
                                    <th class="status-col">Status</th>
            """
            
            # Add application columns
            for app in applications:
                html_response += f'<th class="skill-col">{app}</th>'
            
            html_response += """
                                    <th class="capacity-col">Max Capacity</th>
                                    <th class="overall-col">Overall Level</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            
            # Add team member rows
            for member_name, member_data in config.items():
                status_class = "active" if member_data['status'] == 'active' else "inactive"
                status_text = "✅ Active" if member_data['status'] == 'active' else "❌ Inactive"
                
                # Calculate overall metrics
                skill_levels = [app_data['skill_level'] for app_data in member_data['applications'].values()]
                avg_skill = sum(skill_levels) / len(skill_levels) if skill_levels else 0
                max_capacity = max((app_data['max_load'] for app_data in member_data['applications'].values()), default=0)
                
                # Overall skill classification
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
                
                html_response += f"""
                                <tr class="member-row {status_class}">
                                    <td class="member-col member-name">
                                        <div class="member-info">
                                            <strong>{member_name}</strong>
                                            <small>Avg: {avg_skill:.1f}/5</small>
                                        </div>
                                    </td>
                                    <td class="status-col status-cell {status_class}">{status_text}</td>
                """
                
                # Add skill cells for each application
                for app in applications:
                    if app in member_data['applications']:
                        app_data = member_data['applications'][app]
                        skill_level = app_data['skill_level']
                        confidence = app_data['confidence_score']
                        
                        # Determine skill class and styling
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
                        elif skill_level >= 2.5:
                            skill_class = "mid-plus"
                            skill_icon = "📘"
                        elif skill_level >= 2.0:
                            skill_class = "mid"
                            skill_icon = "🔹"
                        else:
                            skill_class = "junior"
                            skill_icon = "🌱"
                        
                        html_response += f"""
                                    <td class="skill-col skill-cell {skill_class}">
                                        <div class="skill-content">
                                            <span class="skill-icon">{skill_icon}</span>
                                            <span class="skill-value">{skill_level:.1f}/5</span>
                                            <small class="confidence">({confidence:.2f})</small>
                                        </div>
                                    </td>
                        """
                    else:
                        html_response += '<td class="skill-col skill-cell na">N/A</td>'
                
                # Capacity and overall cells
                capacity_class = "high" if max_capacity >= 15 else "medium" if max_capacity >= 10 else "low"
                capacity_icon = "🔥" if max_capacity >= 15 else "⚡" if max_capacity >= 10 else "🔋"
                
                html_response += f"""
                                    <td class="capacity-col capacity-cell {capacity_class}">
                                        <span class="capacity-icon">{capacity_icon}</span>
                                        <span class="capacity-value">{max_capacity} SRs</span>
                                    </td>
                                    <td class="overall-col overall-cell {overall_class}">{overall_text}</td>
                                </tr>
                """
            
            html_response += """
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Individual Member Details -->
                <div class="member-details-section">
                    <h3>👤 Individual Member Details</h3>
                    <div class="member-cards">
            """
            
            # Add individual member detail cards
            for member_name, member_data in config.items():
                status_class = "active" if member_data['status'] == 'active' else "inactive"
                
                # Calculate member metrics
                skill_levels = [app_data['skill_level'] for app_data in member_data['applications'].values()]
                avg_skill = sum(skill_levels) / len(skill_levels)
                avg_confidence = sum(app_data['confidence_score'] for app_data in member_data['applications'].values()) / len(member_data['applications'])
                max_capacity = max(app_data['max_load'] for app_data in member_data['applications'].values())
                
                html_response += f"""
                        <div class="member-card {status_class}">
                            <div class="member-header">
                                <h4>{member_name}</h4>
                                <span class="member-status {status_class}">{member_data['status'].title()}</span>
                            </div>
                            <div class="member-summary">
                                <div class="summary-item">
                                    <span class="label">Overall Skill:</span>
                                    <span class="value">{avg_skill:.1f}/5</span>
                                </div>
                                <div class="summary-item">
                                    <span class="label">Confidence:</span>
                                    <span class="value">{avg_confidence:.2f}</span>
                                </div>
                                <div class="summary-item">
                                    <span class="label">Max Capacity:</span>
                                    <span class="value">{max_capacity} SRs</span>
                                </div>
                            </div>
                            <div class="member-skills-table">
                                <table class="mini-skills-table">
                                    <thead>
                                        <tr>
                                            <th>Application</th>
                                            <th>Skill</th>
                                            <th>Confidence</th>
                                            <th>Load</th>
                                            <th>Top Skills</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                """
                
                # Add application rows for this member
                for app, app_data in member_data['applications'].items():
                    skill_level = app_data['skill_level']
                    confidence = app_data['confidence_score']
                    max_load = app_data['max_load']
                    
                    # Get top specializations
                    specs = app_data['specializations'][:2]
                    specs_text = ', '.join(specs) if specs else 'None'
                    if len(specs_text) > 20:
                        specs_text = specs_text[:17] + '...'
                    
                    # Skill styling
                    if skill_level >= 4.0:
                        skill_class = "expert"
                        skill_display = f"🏆 {skill_level:.1f}/5"
                    elif skill_level >= 3.0:
                        skill_class = "senior"
                        skill_display = f"⭐ {skill_level:.1f}/5"
                    elif skill_level >= 2.0:
                        skill_class = "mid"
                        skill_display = f"📘 {skill_level:.1f}/5"
                    else:
                        skill_class = "junior"
                        skill_display = f"🌱 {skill_level:.1f}/5"
                    
                    html_response += f"""
                                        <tr>
                                            <td class="app-name">{app}</td>
                                            <td class="skill-value {skill_class}">{skill_display}</td>
                                            <td class="confidence-value">{confidence:.2f}</td>
                                            <td class="load-value">{max_load}</td>
                                            <td class="specs-value">{specs_text}</td>
                                        </tr>
                    """
                
                html_response += """
                                    </tbody>
                                </table>
                            </div>
                        </div>
                """
            
            # Application Coverage Analysis Table
            html_response += """
                    </div>
                </div>
                
                <!-- Application Coverage Analysis -->
                <div class="coverage-analysis-section">
                    <h3>🏢 Application Coverage Analysis</h3>
                    <div class="table-responsive">
                        <table class="coverage-table">
                            <thead>
                                <tr>
                                    <th>Application</th>
                                    <th>Total Capacity</th>
                                    <th>Expert Count</th>
                                    <th>Senior Count</th>
                                    <th>Coverage Status</th>
                                    <th>Expert Team</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            
            # Add coverage analysis rows
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
                
                # Determine coverage status
                if len(experts) >= 2:
                    coverage_class = "strong"
                    coverage_text = "🟢 Strong"
                elif len(experts) == 1 or len(seniors) >= 2:
                    coverage_class = "adequate"
                    coverage_text = "🟡 Adequate"
                else:
                    coverage_class = "weak"
                    coverage_text = "🔴 Needs Support"
                
                expert_team = ', '.join(experts + seniors[:2]) if experts or seniors else 'None'
                if len(expert_team) > 50:
                    expert_team = expert_team[:47] + '...'
                
                html_response += f"""
                                <tr class="coverage-row {coverage_class}">
                                    <td class="app-name"><strong>{app}</strong></td>
                                    <td class="capacity-value">{app_capacity} SRs</td>
                                    <td class="expert-count">{len(experts)}</td>
                                    <td class="senior-count">{len(seniors)}</td>
                                    <td class="coverage-status {coverage_class}">{coverage_text}</td>
                                    <td class="expert-team">{expert_team}</td>
                                </tr>
                """
            
            # Complete the HTML with insights and styling
            html_response += f"""
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Key Insights -->
                <div class="insights-section">
                    <h3>💡 Key Insights</h3>
                    <div class="insights-grid">
                        <div class="insight-card success">
                            <div class="insight-icon">🎯</div>
                            <div class="insight-content">
                                <h4>Optimal Team Load</h4>
                                <p>{int(total_capacity * 0.8)} SRs (80% of total capacity)</p>
                            </div>
                        </div>
                        <div class="insight-card info">
                            <div class="insight-icon">📈</div>
                            <div class="insight-content">
                                <h4>Average Skill Level</h4>
                                <p>{sum(sum(app_data['skill_level'] for app_data in member_data['applications'].values()) / len(member_data['applications']) for member_data in config.values()) / len(config):.1f}/5 across all applications</p>
                            </div>
                        </div>
                        <div class="insight-card warning">
                            <div class="insight-icon">⚠️</div>
                            <div class="insight-content">
                                <h4>Capacity Planning</h4>
                                <p>Monitor load distribution and skill development</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Quick Actions -->
                <div class="actions-section">
                    <h3>⚡ Quick Actions</h3>
                    <div class="action-buttons">
                        <button class="action-btn primary" onclick="updateSkills()">
                            <span class="btn-icon">📝</span>
                            Update Skills
                        </button>
                        <button class="action-btn secondary" onclick="adjustCapacity()">
                            <span class="btn-icon">⚡</span>
                            Adjust Capacity
                        </button>
                        <button class="action-btn info" onclick="showEvolution()">
                            <span class="btn-icon">📊</span>
                            Skill Evolution
                        </button>
                        <button class="action-btn success" onclick="exportConfig()">
                            <span class="btn-icon">📤</span>
                            Export Config
                        </button>
                    </div>
                </div>
                
                <div class="footer-info">
                    <p>📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 🔄 Auto-updated by ML learning</p>
                </div>
            </div>
            
            <style>
            .team-skills-response {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                width: 100%;
                max-width: 100%;
                max-height: 80vh;
                margin: 0;
                padding: 15px;
                background: #f8fafc;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
                box-sizing: border-box;
                overflow-y: auto;
                overflow-x: hidden;
                position: relative;
                display: block;
                contain: layout style;
            }}
            
            .response-header {{
                text-align: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #e2e8f0;
            }}
            
            .response-header h3 {{
                color: #1a202c;
                font-size: 1.4em;
                margin: 0;
                font-weight: 600;
            }}
            
            .subtitle {{
                color: #64748b;
                font-size: 0.9em;
                margin: 5px 0 0 0;
            }}
            
            .stats-overview {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 12px;
                margin-bottom: 20px;
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
                contain: layout;
            }}
            
            .stat-card {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                display: flex;
                align-items: center;
                border-left: 4px solid #3b82f6;
                min-height: 60px;
            }}
            
            .stat-icon {{
                font-size: 2.5em;
                margin-right: 20px;
            }}
            
            .stat-number {{
                font-size: 2.2em;
                font-weight: bold;
                color: #1e40af;
                line-height: 1;
            }}
            
            .stat-label {{
                color: #64748b;
                font-size: 0.9em;
                margin-top: 5px;
            }}
            
            .table-container {{
                background: white;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
                contain: layout;
                position: relative;
            }}
            
            .table-container::after {{
                content: '';
                position: absolute;
                top: 15px;
                right: 15px;
                width: 20px;
                height: 100%;
                background: linear-gradient(to left, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 100%);
                pointer-events: none;
                opacity: 0.7;
                border-radius: 0 8px 8px 0;
            }}
            
            .table-container h3 {{
                margin: 0 0 15px 0;
                color: #1a202c;
                font-size: 1.2em;
                font-weight: 600;
                position: relative;
            }}
            
            .table-container h3::after {{
                content: '← Scroll horizontally to view all columns →';
                position: absolute;
                right: 0;
                top: 50%;
                transform: translateY(-50%);
                font-size: 0.7em;
                font-weight: 400;
                color: #94a3b8;
                font-style: italic;
                white-space: nowrap;
            }}
            
            @media (max-width: 768px) {{
                .table-container h3::after {{
                    content: '← Scroll →';
                    font-size: 0.6em;
                }}
            }}
            
            .table-responsive {{
                overflow-x: auto;
                overflow-y: hidden;
                max-width: 100%;
                width: 100%;
                box-sizing: border-box;
                scrollbar-width: thin;
                scrollbar-color: #cbd5e1 #f1f5f9;
                border-radius: 8px;
            }}
            
            .table-responsive::-webkit-scrollbar {{
                height: 12px;
            }}
            
            .table-responsive::-webkit-scrollbar-track {{
                background: #f1f5f9;
                border-radius: 6px;
                margin: 0 5px;
            }}
            
            .table-responsive::-webkit-scrollbar-thumb {{
                background: linear-gradient(45deg, #cbd5e1, #94a3b8);
                border-radius: 6px;
                border: 1px solid #e2e8f0;
            }}
            
            .table-responsive::-webkit-scrollbar-thumb:hover {{
                background: linear-gradient(45deg, #94a3b8, #64748b);
            }}
            
            .table-responsive::-webkit-scrollbar-corner {{
                background: #f1f5f9;
            }}
            
            .team-skills-table {{
                width: 100%;
                min-width: 1000px;
                border-collapse: collapse;
                background: white;
                table-layout: auto;
            }}
            
            .team-skills-table th {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 10px;
                text-align: left;
                font-weight: 600;
                font-size: 0.85em;
                border: none;
                white-space: normal;
                word-wrap: break-word;
                min-width: 100px;
                max-width: 180px;
                overflow-wrap: break-word;
                hyphens: auto;
                line-height: 1.3;
            }}
            
            .team-skills-table td {{
                padding: 10px;
                border-bottom: 1px solid #e2e8f0;
                vertical-align: middle;
                font-size: 0.9em;
                white-space: normal;
                word-wrap: break-word;
                min-width: 100px;
                max-width: 180px;
                overflow-wrap: break-word;
                hyphens: auto;
                line-height: 1.4;
            }}
            
            .team-skills-table th.member-col,
            .team-skills-table td.member-col {{
                min-width: 150px;
                max-width: 200px;
                font-weight: 600;
            }}
            
            .team-skills-table th.status-col,
            .team-skills-table td.status-col {{
                min-width: 100px;
                max-width: 120px;
                text-align: center;
            }}
            
            .team-skills-table th.skill-col,
            .team-skills-table td.skill-col {{
                min-width: 120px;
                max-width: 160px;
                text-align: center;
            }}
            
            .team-skills-table th.capacity-col,
            .team-skills-table td.capacity-col,
            .team-skills-table th.overall-col,
            .team-skills-table td.overall-col {{
                min-width: 110px;
                max-width: 140px;
                text-align: center;
            }}
            
            .member-row:hover {{
                background-color: #f1f5f9;
            }}
            
            .member-name {{
                font-weight: 600;
                min-width: 150px;
            }}
            
            .member-info small {{
                display: block;
                color: #64748b;
                font-size: 0.8em;
                margin-top: 2px;
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
                min-width: 100px;
            }}
            
            .skill-content {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 2px;
            }}
            
            .skill-icon {{
                font-size: 1.2em;
            }}
            
            .skill-value {{
                font-weight: 600;
                font-size: 0.9em;
            }}
            
            .confidence {{
                color: #64748b;
                font-size: 0.7em;
            }}
            
            .skill-cell.expert-plus {{ background-color: #fef3c7; color: #92400e; }}
            .skill-cell.expert {{ background-color: #dcfce7; color: #166534; }}
            .skill-cell.senior-plus {{ background-color: #fef3c7; color: #d97706; }}
            .skill-cell.senior {{ background-color: #dbeafe; color: #1d4ed8; }}
            .skill-cell.mid-plus {{ background-color: #ede9fe; color: #7c3aed; }}
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
            }}
            
            .overall-cell.expert {{ background-color: #dcfce7; color: #166534; }}
            .overall-cell.senior {{ background-color: #fef3c7; color: #d97706; }}
            .overall-cell.mid {{ background-color: #dbeafe; color: #1d4ed8; }}
            .overall-cell.junior {{ background-color: #f3e8ff; color: #7c3aed; }}
            
            .member-details-section {{
                margin-bottom: 15px;
            }}
            
            .member-details-section h3 {{
                color: #1a202c;
                margin-bottom: 12px;
                font-size: 1.2em;
                font-weight: 600;
            }}
            
            .member-cards {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 15px;
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
                contain: layout;
            }}
            
            .member-card {{
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                border-left: 4px solid #3b82f6;
            }}
            
            .member-card.inactive {{
                border-left-color: #ef4444;
                opacity: 0.8;
            }}
            
            .member-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }}
            
            .member-header h4 {{
                margin: 0;
                color: #1a202c;
            }}
            
            .member-status {{
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: 600;
            }}
            
            .member-status.active {{
                background-color: #dcfce7;
                color: #166534;
            }}
            
            .member-status.inactive {{
                background-color: #fee2e2;
                color: #dc2626;
            }}
            
            .member-summary {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin-bottom: 15px;
            }}
            
            .summary-item {{
                text-align: center;
                padding: 10px;
                background: #f8fafc;
                border-radius: 8px;
            }}
            
            .summary-item .label {{
                display: block;
                font-size: 0.8em;
                color: #64748b;
                margin-bottom: 5px;
            }}
            
            .summary-item .value {{
                font-weight: 600;
                color: #1e40af;
                font-size: 1.1em;
            }}
            
            .mini-skills-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 0.85em;
            }}
            
            .mini-skills-table th {{
                background: #f1f5f9;
                padding: 8px 6px;
                text-align: left;
                font-weight: 600;
                color: #374151;
                font-size: 0.8em;
            }}
            
            .mini-skills-table td {{
                padding: 6px;
                border-bottom: 1px solid #f1f5f9;
            }}
            
            .coverage-analysis-section {{
                background: white;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
                contain: layout;
                position: relative;
            }}
            
            .coverage-analysis-section::after {{
                content: '';
                position: absolute;
                top: 15px;
                right: 15px;
                width: 20px;
                height: 100%;
                background: linear-gradient(to left, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 100%);
                pointer-events: none;
                opacity: 0.7;
                border-radius: 0 8px 8px 0;
            }}
            
            .coverage-analysis-section h3 {{
                margin: 0 0 12px 0;
                color: #1a202c;
                font-size: 1.2em;
                font-weight: 600;
                position: relative;
            }}
            
            .coverage-analysis-section h3::after {{
                content: '← Scroll horizontally for complete coverage analysis →';
                position: absolute;
                right: 0;
                top: 50%;
                transform: translateY(-50%);
                font-size: 0.7em;
                font-weight: 400;
                color: #94a3b8;
                font-style: italic;
                white-space: nowrap;
            }}
            
            @media (max-width: 768px) {{
                .coverage-analysis-section h3::after {{
                    content: '← Scroll for details →';
                    font-size: 0.6em;
                }}
            }}
            
            .coverage-table {{
                width: 100%;
                min-width: 1200px;
                border-collapse: collapse;
                background: white;
                table-layout: fixed;
            }}
            
            .coverage-table th {{
                background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
                color: white;
                padding: 15px 20px;
                text-align: left;
                font-weight: 600;
                font-size: 0.95em;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            
            .coverage-table td {{
                padding: 15px 20px;
                border-bottom: 1px solid #e2e8f0;
                vertical-align: middle;
                font-size: 0.9em;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            
            .coverage-table th:first-child,
            .coverage-table td:first-child {{
                width: 220px;
                white-space: normal;
                word-wrap: break-word;
                font-weight: 600;
                text-overflow: initial;
                overflow: visible;
            }}
            
            .coverage-table th:nth-child(2),
            .coverage-table td:nth-child(2) {{
                width: 160px;
                text-align: center;
                white-space: nowrap;
            }}
            
            .coverage-table th:nth-child(3),
            .coverage-table td:nth-child(3) {{
                width: 140px;
                text-align: center;
                white-space: nowrap;
            }}
            
            .coverage-table th:nth-child(4),
            .coverage-table td:nth-child(4) {{
                width: 140px;
                text-align: center;
                white-space: nowrap;
            }}
            
            .coverage-table th:nth-child(5),
            .coverage-table td:nth-child(5) {{
                width: 180px;
                text-align: center;
                white-space: nowrap;
            }}
            
            .coverage-table th:nth-child(6),
            .coverage-table td:nth-child(6) {{
                width: 280px;
                white-space: normal;
                word-wrap: break-word;
                text-overflow: initial;
                overflow: visible;
            }}
            
            .coverage-row:hover {{
                background-color: #f7fafc;
            }}
            
            .coverage-status.strong {{ color: #059669; font-weight: 600; }}
            .coverage-status.adequate {{ color: #d97706; font-weight: 600; }}
            .coverage-status.weak {{ color: #dc2626; font-weight: 600; }}
            
            .insights-section {{
                margin-bottom: 30px;
            }}
            
            .insights-section h3 {{
                color: #1a202c;
                margin-bottom: 20px;
                font-size: 1.5em;
            }}
            
            .insights-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }}
            
            .insight-card {{
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                display: flex;
                align-items: center;
            }}
            
            .insight-card.success {{ border-left: 4px solid #059669; }}
            .insight-card.info {{ border-left: 4px solid #0ea5e9; }}
            .insight-card.warning {{ border-left: 4px solid #d97706; }}
            
            .insight-icon {{
                font-size: 2em;
                margin-right: 15px;
            }}
            
            .insight-content h4 {{
                margin: 0 0 5px 0;
                color: #1a202c;
                font-size: 1.1em;
            }}
            
            .insight-content p {{
                margin: 0;
                color: #64748b;
                font-size: 0.9em;
            }}
            
            .actions-section {{
                margin-bottom: 30px;
            }}
            
            .actions-section h3 {{
                color: #1a202c;
                margin-bottom: 20px;
                font-size: 1.5em;
            }}
            
            .action-buttons {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
            }}
            
            .action-btn {{
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                color: white;
            }}
            
            .action-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            }}
            
            .action-btn.primary {{ background: linear-gradient(135deg, #3b82f6, #1d4ed8); }}
            .action-btn.secondary {{ background: linear-gradient(135deg, #6b7280, #374151); }}
            .action-btn.info {{ background: linear-gradient(135deg, #0ea5e9, #0284c7); }}
            .action-btn.success {{ background: linear-gradient(135deg, #10b981, #059669); }}
            
            .btn-icon {{
                margin-right: 8px;
                font-size: 1.1em;
            }}
            
            .footer-info {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
                color: #64748b;
                font-size: 0.9em;
            }}
            
            @media (max-width: 768px) {{
                .stats-overview {{
                    grid-template-columns: repeat(2, 1fr);
                    gap: 8px;
                }}
                
                .stat-card {{
                    padding: 10px;
                    min-height: 50px;
                }}
                
                .member-cards {{
                    grid-template-columns: 1fr;
                    gap: 10px;
                }}
                
                .team-skills-table th,
                .team-skills-table td {{
                    padding: 6px 4px;
                    font-size: 0.8em;
                }}
                
                .response-header h3 {{
                    font-size: 1.1em;
                }}
                
                .table-container {{
                    padding: 10px;
                }}
                
                .insights-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .action-buttons {{
                    grid-template-columns: repeat(2, 1fr);
                }}
            }}
            
            @media (max-width: 480px) {{
                .team-skills-response {{
                    padding: 10px;
                }}
                
                .stats-overview {{
                    grid-template-columns: 1fr;
                    gap: 6px;
                }}
                
                .stat-card {{
                    padding: 8px;
                    min-height: 45px;
                }}
                
                .stat-icon {{
                    font-size: 1.8em;
                    margin-right: 10px;
                }}
                
                .member-cards {{
                    grid-template-columns: 1fr;
                }}
                
                .response-header h3 {{
                    font-size: 1.1em;
                }}
            }}
            </style>
            """
            
            return html_response
            
        except Exception as e:
            return f"""
            <div class="alert alert-danger">
                <h4>❌ Error Loading Team Skills</h4>
                <p>An error occurred while retrieving team skills configuration.</p>
                <p><strong>Error details:</strong> {str(e)}</p>
                <div class="mt-3">
                    <strong>Troubleshooting:</strong>
                    <ul>
                        <li>Ensure People.xlsx has been loaded into the database</li>
                        <li>Check database connectivity</li>
                        <li>Verify team configuration is properly set up</li>
                    </ul>
                </div>
            </div>
            """
