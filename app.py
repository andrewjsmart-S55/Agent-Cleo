"""
AI Agent Job Management System
Main Flask Application
"""
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from models import db, Agent, Job, Activity
from agent_utils import discover_agents, scan_context_folder, monitor_output_folder
from todoist_integration import TodoistIntegration, create_task_for_andrew, create_weekly_plan_tasks

# Configuration
BASE_PATH = r"C:\Users\AndrewSmart\Claude_Projects\Agent-Cleo"
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'agents.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Initialize database
db.init_app(app)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()


# ============================================================================
# INITIALIZATION
# ============================================================================

@app.route('/api/initialize', methods=['POST'])
def initialize_system():
    """Initialize the system by discovering agents and setting up monitoring"""
    try:
        agents_data = discover_agents(BASE_PATH)

        for agent_data in agents_data:
            # Check if agent exists
            agent = Agent.query.filter_by(folder_name=agent_data['folder_name']).first()

            if not agent:
                # Create new agent
                agent = Agent(
                    name=agent_data['name'],
                    folder_name=agent_data['folder_name'],
                    path=agent_data['path'],
                    context_summary=agent_data['context_summary'],
                    is_master=agent_data['is_master']
                )
                db.session.add(agent)
            else:
                # Update existing agent
                agent.name = agent_data['name']
                agent.path = agent_data['path']
                agent.context_summary = agent_data['context_summary']
                agent.is_master = agent_data['is_master']
                agent.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Initialized {len(agents_data)} agents',
            'agents': [a['name'] for a in agents_data]
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# AGENT ROUTES
# ============================================================================

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get all agents"""
    agents = Agent.query.order_by(Agent.is_master.desc(), Agent.name).all()
    return jsonify([agent.to_dict() for agent in agents])


@app.route('/api/agents/<int:agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Get a specific agent"""
    agent = Agent.query.get_or_404(agent_id)
    return jsonify(agent.to_dict())


@app.route('/api/agents/<int:agent_id>/context', methods=['GET'])
def get_agent_context(agent_id):
    """Get agent context files"""
    agent = Agent.query.get_or_404(agent_id)
    context_path = os.path.join(agent.path, 'Context')

    files = scan_context_folder(context_path)

    return jsonify({
        'agent_id': agent_id,
        'agent_name': agent.name,
        'context_path': context_path,
        'files': files
    })


# ============================================================================
# JOB ROUTES
# ============================================================================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs, optionally filtered by agent"""
    agent_id = request.args.get('agent_id', type=int)

    if agent_id:
        jobs = Job.query.filter_by(agent_id=agent_id).order_by(Job.created_at.desc()).all()
    else:
        jobs = Job.query.order_by(Job.created_at.desc()).all()

    return jsonify([job.to_dict() for job in jobs])


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get a specific job"""
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict())


@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job"""
    data = request.json

    try:
        job = Job(
            agent_id=data['agent_id'],
            name=data['name'],
            description=data.get('description', ''),
            frequency=data.get('frequency', 'manual'),
            cron_expression=data.get('cron_expression'),
            sop=data.get('sop', ''),
            status='active'
        )

        # Calculate next run time based on frequency
        if job.frequency == 'daily':
            job.next_run = datetime.utcnow() + timedelta(days=1)
        elif job.frequency == 'weekly':
            job.next_run = datetime.utcnow() + timedelta(weeks=1)
        elif job.frequency == 'monthly':
            job.next_run = datetime.utcnow() + timedelta(days=30)

        db.session.add(job)
        db.session.commit()

        # Schedule the job if it has a frequency
        if job.frequency != 'manual' and job.frequency != 'once':
            schedule_job(job)

        return jsonify({'success': True, 'job': job.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Update a job"""
    job = Job.query.get_or_404(job_id)
    data = request.json

    try:
        job.name = data.get('name', job.name)
        job.description = data.get('description', job.description)
        job.frequency = data.get('frequency', job.frequency)
        job.cron_expression = data.get('cron_expression', job.cron_expression)
        job.sop = data.get('sop', job.sop)
        job.status = data.get('status', job.status)
        job.updated_at = datetime.utcnow()

        db.session.commit()

        # Reschedule if frequency changed
        if 'frequency' in data:
            unschedule_job(job_id)
            if job.frequency != 'manual' and job.frequency != 'once':
                schedule_job(job)

        return jsonify({'success': True, 'job': job.to_dict()})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job"""
    job = Job.query.get_or_404(job_id)

    try:
        unschedule_job(job_id)
        db.session.delete(job)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Job deleted'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/jobs/<int:job_id>/run', methods=['POST'])
def run_job(job_id):
    """Manually trigger a job execution"""
    job = Job.query.get_or_404(job_id)

    try:
        execute_job(job.id)
        return jsonify({'success': True, 'message': f'Job "{job.name}" executed'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ============================================================================
# ACTIVITY ROUTES
# ============================================================================

@app.route('/api/activities', methods=['GET'])
def get_activities():
    """Get all activities, optionally filtered by agent or job"""
    agent_id = request.args.get('agent_id', type=int)
    job_id = request.args.get('job_id', type=int)
    limit = request.args.get('limit', 50, type=int)

    query = Activity.query

    if agent_id:
        query = query.filter_by(agent_id=agent_id)

    if job_id:
        query = query.filter_by(job_id=job_id)

    activities = query.order_by(Activity.created_at.desc()).limit(limit).all()

    return jsonify([activity.to_dict() for activity in activities])


@app.route('/api/activities', methods=['POST'])
def create_activity():
    """Create a new activity entry"""
    data = request.json

    try:
        activity = Activity(
            agent_id=data['agent_id'],
            job_id=data.get('job_id'),
            title=data['title'],
            summary=data.get('summary', ''),
            output_files=json.dumps(data.get('output_files', [])),
            status=data.get('status', 'success')
        )

        db.session.add(activity)
        db.session.commit()

        return jsonify({'success': True, 'activity': activity.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


# ============================================================================
# FILE MONITORING
# ============================================================================

@app.route('/api/monitor/scan', methods=['POST'])
def scan_output_folders():
    """Scan all agent output folders for new files"""
    try:
        agents = Agent.query.all()
        new_activities = []

        for agent in agents:
            output_path = os.path.join(agent.path, 'Output')
            new_files = monitor_output_folder(output_path, agent.id)

            for file_info in new_files:
                # Check if activity already exists for this file
                existing = Activity.query.filter(
                    Activity.agent_id == agent.id,
                    Activity.output_files.contains(file_info['name'])
                ).first()

                if not existing:
                    activity = Activity(
                        agent_id=agent.id,
                        title=f"New output: {file_info['name']}",
                        summary=f"File created: {file_info['modified']}",
                        output_files=json.dumps([file_info]),
                        status='success'
                    )
                    db.session.add(activity)
                    new_activities.append(file_info['name'])

        db.session.commit()

        return jsonify({
            'success': True,
            'new_activities': len(new_activities),
            'files': new_activities
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


# ============================================================================
# OVERLORD ROUTES
# ============================================================================

@app.route('/api/overlord/run', methods=['POST'])
def run_overlord_task():
    """Run a task via AA-Overlord across multiple agents"""
    data = request.json

    try:
        overlord = Agent.query.filter_by(is_master=True).first()
        if not overlord:
            return jsonify({'success': False, 'error': 'AA-Overlord not found'}), 404

        target_agents = data.get('target_agents', [])  # List of agent IDs
        task_description = data.get('task_description', '')

        # Create activity for overlord task
        activity = Activity(
            agent_id=overlord.id,
            title=f"Overlord Task: {data.get('task_name', 'Multi-Agent Task')}",
            summary=f"Task across {len(target_agents)} agents: {task_description}",
            status='in_progress'
        )
        db.session.add(activity)
        db.session.commit()

        return jsonify({
            'success': True,
            'activity': activity.to_dict(),
            'message': 'Overlord task initiated'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


# ============================================================================
# TODOIST INTEGRATION ROUTES
# ============================================================================

@app.route('/api/todoist/task', methods=['POST'])
def create_todoist_task():
    """Create a single task in Todoist"""
    data = request.json

    try:
        result = create_task_for_andrew(
            content=data.get('content'),
            description=data.get('description', ''),
            project=data.get('project'),
            priority=data.get('priority', 1),
            due=data.get('due'),
            labels=data.get('labels'),
            agent=data.get('agent', 'Agent-Cleo')
        )

        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Failed to create Todoist task: {str(e)}'
        }), 500


@app.route('/api/todoist/tasks/batch', methods=['POST'])
def create_todoist_tasks_batch():
    """Create multiple tasks in Todoist"""
    data = request.json

    try:
        tasks = data.get('tasks', [])
        agent = data.get('agent', 'Agent-Cleo')

        if not tasks:
            return jsonify({
                'success': False,
                'error': 'No tasks provided'
            }), 400

        result = create_weekly_plan_tasks(tasks, agent=agent)

        return jsonify(result), 201 if result['success'] else 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Failed to create batch tasks: {str(e)}'
        }), 500


@app.route('/api/todoist/projects', methods=['GET'])
def list_todoist_projects():
    """List all Todoist projects"""
    try:
        integration = TodoistIntegration()
        projects = integration.list_projects()

        return jsonify({
            'success': True,
            'projects': projects,
            'count': len(projects)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Failed to fetch Todoist projects: {str(e)}'
        }), 500


@app.route('/api/todoist/test', methods=['GET'])
def test_todoist_integration():
    """Test Todoist integration"""
    try:
        integration = TodoistIntegration()

        # Try to list projects
        projects = integration.list_projects()

        return jsonify({
            'success': True,
            'message': 'Todoist integration is working',
            'projects_count': len(projects),
            'projects': [p['name'] for p in projects]
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Todoist integration test failed. Check TODOIST_API_TOKEN environment variable.'
        }), 500


# ============================================================================
# JOB SCHEDULING
# ============================================================================

def schedule_job(job):
    """Schedule a recurring job"""
    if job.frequency == 'daily':
        scheduler.add_job(
            func=execute_job,
            args=[job.id],
            trigger='cron',
            hour=9,
            minute=0,
            id=f'job_{job.id}',
            replace_existing=True
        )
    elif job.frequency == 'weekly':
        scheduler.add_job(
            func=execute_job,
            args=[job.id],
            trigger='cron',
            day_of_week='mon',
            hour=9,
            minute=0,
            id=f'job_{job.id}',
            replace_existing=True
        )
    elif job.frequency == 'monthly':
        scheduler.add_job(
            func=execute_job,
            args=[job.id],
            trigger='cron',
            day=1,
            hour=9,
            minute=0,
            id=f'job_{job.id}',
            replace_existing=True
        )
    elif job.cron_expression:
        scheduler.add_job(
            func=execute_job,
            args=[job.id],
            trigger=CronTrigger.from_crontab(job.cron_expression),
            id=f'job_{job.id}',
            replace_existing=True
        )


def unschedule_job(job_id):
    """Remove a job from the scheduler"""
    try:
        scheduler.remove_job(f'job_{job_id}')
    except:
        pass


def execute_job(job_id):
    """Execute a job and create activity record"""
    with app.app_context():
        job = Job.query.get(job_id)
        if not job:
            return

        job.last_run = datetime.utcnow()

        # Calculate next run
        if job.frequency == 'daily':
            job.next_run = job.last_run + timedelta(days=1)
        elif job.frequency == 'weekly':
            job.next_run = job.last_run + timedelta(weeks=1)
        elif job.frequency == 'monthly':
            job.next_run = job.last_run + timedelta(days=30)

        # Create activity record
        activity = Activity(
            agent_id=job.agent_id,
            job_id=job.id,
            title=f"Job executed: {job.name}",
            summary=f"Scheduled execution at {job.last_run.strftime('%Y-%m-%d %H:%M:%S')}",
            status='success'
        )

        db.session.add(activity)
        db.session.commit()


# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')


@app.route('/jobs')
def jobs_page():
    """Jobs management page"""
    return render_template('jobs.html')


@app.route('/activities')
def activities_page():
    """Activity feed page"""
    return render_template('activities.html')


@app.route('/overlord')
def overlord_page():
    """AA-Overlord control panel"""
    return render_template('overlord.html')


# ============================================================================
# STARTUP
# ============================================================================

def init_db():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized")


if __name__ == '__main__':
    init_db()
    print("=" * 70)
    print("AI Agent Job Management System")
    print("=" * 70)
    print(f"Base Path: {BASE_PATH}")
    print(f"Database: {DATABASE_PATH}")
    print("\nStarting server on http://localhost:5000")
    print("\nFirst-time setup:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Click 'Initialize System' to discover agents")
    print("=" * 70)

    app.run(debug=True, host='0.0.0.0', port=5000)
