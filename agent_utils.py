"""
Utility functions for agent discovery, context scanning, and output monitoring
"""
import os
from pathlib import Path
from datetime import datetime


def discover_agents(base_path):
    """
    Discover all agent folders in the base directory

    Args:
        base_path: Path to the Agent-Cleo directory

    Returns:
        List of agent dictionaries with metadata
    """
    agents = []

    if not os.path.exists(base_path):
        raise ValueError(f"Base path does not exist: {base_path}")

    # Get all subdirectories
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)

        if os.path.isdir(item_path):
            # Check if it has Context and Output folders
            context_path = os.path.join(item_path, 'Context')
            output_path = os.path.join(item_path, 'Output')

            if os.path.exists(context_path) and os.path.exists(output_path):
                # This is a valid agent folder
                is_master = item == 'AA-Overlord'

                # Read context summary
                context_summary = read_context_summary(context_path)

                agent_name = item.replace('-', ' ').replace('_', ' ')

                agents.append({
                    'name': agent_name,
                    'folder_name': item,
                    'path': item_path,
                    'context_summary': context_summary,
                    'is_master': is_master
                })

    return agents


def read_context_summary(context_path):
    """
    Read and summarize the context files in an agent's Context folder

    Args:
        context_path: Path to the Context folder

    Returns:
        String summary of context files
    """
    if not os.path.exists(context_path):
        return "No context folder found"

    files = []
    total_size = 0

    try:
        for item in os.listdir(context_path):
            item_path = os.path.join(context_path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                files.append({
                    'name': item,
                    'size': size,
                    'modified': datetime.fromtimestamp(os.path.getmtime(item_path))
                })
                total_size += size

        if not files:
            return "Context folder is empty"

        # Create summary
        summary_parts = [
            f"{len(files)} file(s)",
            f"Total size: {format_file_size(total_size)}"
        ]

        # List file names
        file_names = [f['name'] for f in files[:5]]  # First 5 files
        if len(files) > 5:
            file_names.append(f"... and {len(files) - 5} more")

        summary = f"{', '.join(summary_parts)}\nFiles: {', '.join(file_names)}"

        return summary

    except Exception as e:
        return f"Error reading context: {str(e)}"


def scan_context_folder(context_path):
    """
    Get detailed information about files in the Context folder

    Args:
        context_path: Path to the Context folder

    Returns:
        List of file information dictionaries
    """
    if not os.path.exists(context_path):
        return []

    files = []

    try:
        for item in os.listdir(context_path):
            item_path = os.path.join(context_path, item)

            if os.path.isfile(item_path):
                stat = os.stat(item_path)
                files.append({
                    'name': item,
                    'path': item_path,
                    'size': stat.st_size,
                    'size_formatted': format_file_size(stat.st_size),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'extension': os.path.splitext(item)[1]
                })

        # Sort by modified date, newest first
        files.sort(key=lambda x: x['modified'], reverse=True)

    except Exception as e:
        print(f"Error scanning context folder: {e}")

    return files


def monitor_output_folder(output_path, agent_id):
    """
    Monitor an agent's Output folder for files

    Args:
        output_path: Path to the Output folder
        agent_id: ID of the agent

    Returns:
        List of file information dictionaries
    """
    if not os.path.exists(output_path):
        return []

    files = []

    try:
        for item in os.listdir(output_path):
            item_path = os.path.join(output_path, item)

            if os.path.isfile(item_path):
                stat = os.stat(item_path)
                files.append({
                    'name': item,
                    'path': item_path,
                    'size': stat.st_size,
                    'size_formatted': format_file_size(stat.st_size),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'extension': os.path.splitext(item)[1],
                    'agent_id': agent_id
                })

        # Sort by modified date, newest first
        files.sort(key=lambda x: x['modified'], reverse=True)

    except Exception as e:
        print(f"Error monitoring output folder: {e}")

    return files


def format_file_size(size_bytes):
    """
    Format file size in human-readable format

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def read_file_content(file_path, max_chars=5000):
    """
    Read file content with size limit

    Args:
        file_path: Path to the file
        max_chars: Maximum number of characters to read

    Returns:
        File content as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(max_chars)
            return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


def get_recent_outputs(output_path, hours=24):
    """
    Get files created/modified in the last N hours

    Args:
        output_path: Path to the Output folder
        hours: Number of hours to look back

    Returns:
        List of recent file information
    """
    if not os.path.exists(output_path):
        return []

    cutoff_time = datetime.now().timestamp() - (hours * 3600)
    recent_files = []

    try:
        for item in os.listdir(output_path):
            item_path = os.path.join(output_path, item)

            if os.path.isfile(item_path):
                mtime = os.path.getmtime(item_path)

                if mtime >= cutoff_time:
                    stat = os.stat(item_path)
                    recent_files.append({
                        'name': item,
                        'path': item_path,
                        'size': stat.st_size,
                        'size_formatted': format_file_size(stat.st_size),
                        'modified': datetime.fromtimestamp(mtime).isoformat(),
                        'extension': os.path.splitext(item)[1]
                    })

        # Sort by modified date, newest first
        recent_files.sort(key=lambda x: x['modified'], reverse=True)

    except Exception as e:
        print(f"Error getting recent outputs: {e}")

    return recent_files
