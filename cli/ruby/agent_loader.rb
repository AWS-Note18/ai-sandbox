# Agent framework loader for Ruby CLI tools.
#
# This module provides utilities to load and use agents, tools, roles, rules,
# and templates from the main project structure.

require 'yaml'
require 'pathname'

class AgentLoader
  def initialize
    @cli_path = File.expand_path('../', __FILE__)
  end

  # Load an agent configuration by name.
  #
  # @param agent_name [String] Name of the agent (e.g., 'coder-agent')
  # @return [Hash, nil] Agent configuration or nil if not found
  def load_agent(agent_name)
    role_path = File.join(@cli_path, 'role', agent_name, 'role.yaml')

    unless File.exist?(role_path)
      puts "Error: Agent '#{agent_name}' not found at #{role_path}"
      return nil
    end

    parse_yaml(role_path)
  end

  # Load a tool configuration by name.
  #
  # @param tool_name [String] Name of the tool (e.g., 'write_python')
  # @return [Hash, nil] Tool configuration or nil if not found
  def load_tool(tool_name)
    tool_path = File.join(@cli_path, 'tool', "#{tool_name}.yaml")

    if File.exist?(tool_path)
      return parse_yaml(tool_path)
    end

    # Search recursively in tool subdirectories
    tool_dir = File.join(@cli_path, 'tool')
    files = find_yaml_files(tool_dir, tool_name)

    unless files.empty?
      return parse_yaml(files[0])
    end

    puts "Error: Tool '#{tool_name}' not found"
    nil
  end

  # List all available agents.
  #
  # @return [Array<String>] List of agent names
  def list_agents
    role_dir = File.join(@cli_path, 'role')
    agents = []

    if Dir.exist?(role_dir)
      Dir.each_child(role_dir) do |item|
        item_path = File.join(role_dir, item)
        if File.directory?(item_path) && File.exist?(File.join(item_path, 'role.yaml'))
          agents << item
        end
      end
    end

    agents.sort
  end

  # List all available tools.
  #
  # @return [Array<String>] List of tool names
  def list_tools
    tool_dir = File.join(@cli_path, 'tool')
    tools = []

    if Dir.exist?(tool_dir)
      find_all_yaml_tools(tool_dir, tools)
    end

    tools.sort.uniq
  end

  private

  # Parse a simple YAML file.
  #
  # @param file_path [String] Path to YAML file
  # @return [Hash] Parsed YAML as hash
  def parse_yaml(file_path)
    YAML.load_file(file_path) || {}
  rescue => e
    puts "Error parsing YAML at #{file_path}: #{e.message}"
    {}
  end

  # Find YAML files recursively.
  #
  # @param dir [String] Directory to search
  # @param tool_name [String] Tool name to find
  # @return [Array<String>] List of matching file paths
  def find_yaml_files(dir, tool_name)
    files = []

    return files unless Dir.exist?(dir)

    Dir.each_child(dir) do |item|
      path = File.join(dir, item)

      if File.directory?(path)
        files.concat(find_yaml_files(path, tool_name))
      elsif File.file?(path) && File.extname(path) == '.yaml'
        if File.basename(path, '.yaml') == tool_name
          files << path
        end
      end
    end

    files
  end

  # Find all YAML tool files.
  #
  # @param dir [String] Directory to search
  # @param tools [Array] Reference to tools array
  def find_all_yaml_tools(dir, tools)
    return unless Dir.exist?(dir)

    Dir.each_child(dir) do |item|
      path = File.join(dir, item)

      if File.directory?(path)
        find_all_yaml_tools(path, tools)
      elsif File.file?(path) && File.extname(path) == '.yaml'
        tools << File.basename(path, '.yaml')
      end
    end
  end
end