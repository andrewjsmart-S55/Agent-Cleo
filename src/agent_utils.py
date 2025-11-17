"""
Agent discovery and management utilities
Enhanced for 4-tier architecture
"""
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


def discover_agents(base_path: str) -> List[Dict[str, Any]]:
    """
    Discover all agents from the filesystem
    Identifies agents by tier based on folder structure and naming

    Args:
        base_path: Base path of Agent-Cleo project

    Returns:
        List of agent dictionaries with metadata
    """
    agents = []

    # Tier mappings based on folder structure
    tier_folders = {
        "Personal Agents": "personal",
        "Team Agents": "team",
        "Worker Agents": "worker",
        "Expert Agents": "expert"
    }

    # Check for master agent (Agent-Cleo in root)
    master_folder = os.path.join(base_path, "Agent-Cleo")
    if os.path.exists(master_folder) and _is_agent_folder(master_folder):
        agents.append(_create_agent_data(
            master_folder,
            "Agent-Cleo",
            "master",
            "Master orchestration agent coordinating all other agents"
        ))

    # Discover agents in tier folders
    for tier_folder, tier_name in tier_folders.items():
        tier_path = os.path.join(base_path, tier_folder)

        if not os.path.exists(tier_path):
            continue

        for item in os.listdir(tier_path):
            item_path = os.path.join(tier_path, item)

            if os.path.isdir(item_path) and _is_agent_folder(item_path):
                agents.append(_create_agent_data(
                    item_path,
                    item,
                    tier_name,
                    _get_agent_description(tier_name, item)
                ))

    return agents


def _is_agent_folder(path: str) -> bool:
    """Check if folder is a valid agent folder (has Context and Output folders)"""
    context_path = os.path.join(path, "Context")
    output_path = os.path.join(path, "Output")
    return os.path.exists(context_path) and os.path.exists(output_path)


def _create_agent_data(
    path: str,
    folder_name: str,
    tier: str,
    description: str
) -> Dict[str, Any]:
    """Create agent data dictionary"""
    context_path = os.path.join(path, "Context")
    context_summary = _read_context_summary(context_path)

    # Extract agent name (remove prefixes and clean up)
    name = _clean_agent_name(folder_name)

    # Determine capabilities based on tier
    capabilities = _get_tier_capabilities(tier, folder_name)

    return {
        "name": name,
        "folder_name": folder_name,
        "path": path,
        "tier": tier,
        "description": description,
        "context_summary": context_summary,
        "capabilities": capabilities
    }


def _clean_agent_name(folder_name: str) -> str:
    """Clean up agent folder name to display name"""
    name = folder_name

    # Remove common prefixes
    prefixes = ["Agent-", "Expert-", "Worker-"]
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]

    # Remove common suffixes
    suffixes = ["-MD"]
    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[:-len(suffix)]

    # Replace hyphens and underscores with spaces
    name = name.replace("-", " ").replace("_", " ")

    # Capitalize words
    name = " ".join(word.capitalize() for word in name.split())

    return name


def _get_agent_description(tier: str, folder_name: str) -> str:
    """Get agent description based on tier and name"""
    descriptions = {
        "master": "Master orchestration agent coordinating all other agents",
        "personal": "Personal development and coaching agent",
        "team": f"Team managing director for {_clean_agent_name(folder_name)}",
        "worker": f"Executive specialist handling {_clean_agent_name(folder_name)} tasks",
        "expert": f"Subject matter expert in {_clean_agent_name(folder_name)}"
    }
    return descriptions.get(tier, "Specialized AI agent")


def _get_tier_capabilities(tier: str, folder_name: str) -> List[str]:
    """Get capabilities based on agent tier"""
    base_capabilities = {
        "master": [
            "Strategic orchestration",
            "Agent coordination",
            "Task routing",
            "System oversight"
        ],
        "personal": [
            "Personal coaching",
            "Goal setting",
            "Habit tracking",
            "Development planning"
        ],
        "team": [
            "Team management",
            "Resource allocation",
            "Project oversight",
            "Reporting"
        ],
        "worker": [
            "Task execution",
            "Specialized operations",
            "Deliverable creation",
            "Process management"
        ],
        "expert": [
            "Expert consultation",
            "Analysis",
            "Recommendations",
            "Knowledge sharing"
        ]
    }

    capabilities = base_capabilities.get(tier, ["General tasks"]).copy()

    # Add specific capabilities based on agent name
    name_lower = folder_name.lower()

    if "cmo" in name_lower or "marketing" in name_lower:
        capabilities.extend(["Marketing strategy", "Campaign management"])
    elif "legal" in name_lower:
        capabilities.extend(["Legal analysis", "Compliance review"])
    elif "finance" in name_lower or "fd" in name_lower:
        capabilities.extend(["Financial analysis", "Budget management"])
    elif "data" in name_lower:
        capabilities.extend(["Data analysis", "Statistical modeling"])
    elif "cyber" in name_lower or "security" in name_lower:
        capabilities.extend(["Security assessment", "Threat analysis"])

    return capabilities


def _read_context_summary(context_path: str) -> str:
    """Read and summarize context folder contents"""
    if not os.path.exists(context_path):
        return "No context folder found"

    try:
        files = []
        total_size = 0

        for item in os.listdir(context_path):
            item_path = os.path.join(context_path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                files.append(item)
                total_size += size

        if not files:
            return "Context folder is empty"

        file_list = ", ".join(files[:5])
        if len(files) > 5:
            file_list += f" ... and {len(files) - 5} more"

        return f"{len(files)} file(s) - {file_list}"

    except Exception as e:
        return f"Error reading context: {str(e)}"


def scan_context_folder(context_path: str) -> List[Dict[str, Any]]:
    """Get detailed file information from context folder"""
    if not os.path.exists(context_path):
        return []

    files = []
    try:
        for item in os.listdir(context_path):
            item_path = os.path.join(context_path, item)
            if os.path.isfile(item_path):
                stat = os.stat(item_path)
                files.append({
                    "name": item,
                    "path": item_path,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

        files.sort(key=lambda x: x["modified"], reverse=True)
    except Exception as e:
        print(f"Error scanning context: {e}")

    return files


def monitor_output_folder(output_path: str, agent_id: int) -> List[Dict[str, Any]]:
    """Monitor output folder for new files"""
    if not os.path.exists(output_path):
        return []

    files = []
    try:
        for item in os.listdir(output_path):
            item_path = os.path.join(output_path, item)
            if os.path.isfile(item_path):
                stat = os.stat(item_path)
                files.append({
                    "name": item,
                    "path": item_path,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "agent_id": agent_id
                })

        files.sort(key=lambda x: x["modified"], reverse=True)
    except Exception as e:
        print(f"Error monitoring output: {e}")

    return files
