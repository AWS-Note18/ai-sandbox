"""Agent framework loader for CLI tools.

This module provides utilities to load and use agents, tools, roles, rules,
and templates from the main project structure via symlinks.
"""

from pathlib import Path


def load_agent_config(agent_name: str):
    """Load an agent configuration by name.
    
    Args:
        agent_name: Name of the agent (e.g., 'coder-agent', 'tutor-agent')
        
    Returns:
        Dictionary containing agent configuration
    """
    cli_dir = Path(__file__).resolve().parent.parent
    role_file = cli_dir / "role" / agent_name / "role.yaml"
    
    if not role_file.exists():
        print(f"Error loading agent '{agent_name}': File not found at {role_file}")
        return None
    
    return _parse_yaml(role_file)


def load_tool_config(tool_name: str):
    """Load a tool configuration by name.
    
    Args:
        tool_name: Name of the tool (e.g., 'write_python', 'analyze_code')
        
    Returns:
        Dictionary containing tool configuration
    """
    cli_dir = Path(__file__).resolve().parent.parent
    tool_file = cli_dir / "tool" / f"{tool_name}.yaml"
    
    if tool_file.exists():
        return _parse_yaml(tool_file)
    
    # Search recursively
    tool_dir = cli_dir / "tool"
    if tool_dir.exists():
        for yaml_file in tool_dir.rglob(f"{tool_name}.yaml"):
            return _parse_yaml(yaml_file)
    
    print(f"Error loading tool '{tool_name}': File not found")
    return None


def list_available_agents():
    """List all available agents in the project."""
    cli_dir = Path(__file__).resolve().parent.parent
    role_dir = cli_dir / "role"
    
    if not role_dir.exists():
        return []
    
    agents = []
    for agent_dir in role_dir.iterdir():
        if agent_dir.is_dir() and (agent_dir / "role.yaml").exists():
            agents.append(agent_dir.name)
    return sorted(agents)


def list_available_tools():
    """List all available tools in the project."""
    cli_dir = Path(__file__).resolve().parent.parent
    tool_dir = cli_dir / "tool"
    
    if not tool_dir.exists():
        return []
    
    tools = []
    for yaml_file in tool_dir.rglob("*.yaml"):
        tool_name = yaml_file.stem
        if tool_name not in tools:
            tools.append(tool_name)
    return sorted(tools)


def _parse_yaml(file_path):
    """Simple YAML parser for basic key-value pairs."""
    try:
        import yaml
        with open(file_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # Fallback without yaml library
        result = {}
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip()
        return result


if __name__ == "__main__":
    print("Available Agents:")
    for agent in list_available_agents():
        print(f"  - {agent}")
    
    print("\nAvailable Tools:")
    for tool in list_available_tools():
        print(f"  - {tool}")