import sys
from pathlib import Path
from agent_loader import list_available_agents, list_available_tools, load_agent_config, load_tool_config


def main():
    """Main CLI entry point for the agent framework."""
    print("=" * 60)
    print("AI Agent Framework CLI")
    print("=" * 60)
    
    # List available agents
    print("\n📋 Available Agents:")
    agents = list_available_agents()
    if agents:
        for agent in agents:
            print(f"   ✓ {agent}")
    else:
        print("   (No agents found)")
    
    # List available tools
    print("\n🔧 Available Tools:")
    tools = list_available_tools()
    if tools:
        for tool in tools[:10]:  # Show first 10
            print(f"   ✓ {tool}")
        if len(tools) > 10:
            print(f"   ... and {len(tools) - 10} more")
    else:
        print("   (No tools found)")
    
    # Example: Load and display a specific agent
    print("\n" + "=" * 60)
    print("Example: Loading 'coder-agent' configuration")
    print("=" * 60)
    agent_config = load_agent_config("coder-agent")
    if agent_config:
        print(f"✓ Successfully loaded agent configuration")
        print(f"  Keys: {', '.join(agent_config.keys())}")
    
    # Example: Load and display a specific tool
    print("\nExample: Loading 'write_python' tool configuration")
    tool_config = load_tool_config("write_python")
    if tool_config:
        print(f"✓ Successfully loaded tool configuration")
        print(f"  Keys: {', '.join(tool_config.keys())}")
    
    print("\n" + "=" * 60)
    print("Framework integration successful!")
    print("=" * 60)


if __name__ == "__main__":
    main()