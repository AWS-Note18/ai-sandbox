require_relative 'agent_loader'

# Main CLI entry point for the agent framework (Ruby)

loader = AgentLoader.new

puts "=" * 60
puts "AI Agent Framework CLI (Ruby)"
puts "=" * 60

# List available agents
puts "\n📋 Available Agents:"
agents = loader.list_agents
if agents.any?
  agents.each { |agent| puts "   ✓ #{agent}" }
else
  puts "   (No agents found)"
end

# List available tools
puts "\n🔧 Available Tools:"
tools = loader.list_tools
if tools.any?
  display_tools = tools.first(10)
  display_tools.each { |tool| puts "   ✓ #{tool}" }
  puts "   ... and #{tools.length - 10} more" if tools.length > 10
else
  puts "   (No tools found)"
end

# Example: Load and display a specific agent
puts "\n" + "=" * 60
puts "Example: Loading 'coder-agent' configuration"
puts "=" * 60
agent_config = loader.load_agent('coder-agent')
if agent_config
  puts "✓ Successfully loaded agent configuration"
  puts "  Keys: #{agent_config.keys.join(', ')}"
end

# Example: Load and display a specific tool
puts "\nExample: Loading 'write_python' tool configuration"
tool_config = loader.load_tool('write_python')
if tool_config
  puts "✓ Successfully loaded tool configuration"
  puts "  Keys: #{tool_config.keys.join(', ')}"
end

puts "\n" + "=" * 60
puts "Framework integration successful!"
puts "=" * 60