<?php

/**
 * Agent framework loader for PHP CLI tools.
 *
 * This class provides utilities to load and use agents, tools, roles, rules,
 * and templates from the main project structure via symlinks.
 */

class AgentLoader {
    private $cliPath;
    
    public function __construct() {
        $this->cliPath = dirname(__FILE__) . '/..';
    }
    
    /**
     * Load an agent configuration by name.
     *
     * @param string $agentName Name of the agent (e.g., 'coder-agent')
     * @return array|null Agent configuration or null if not found
     */
    public function loadAgent($agentName) {
        $rolePath = $this->cliPath . '/role/' . $agentName . '/role.yaml';

        if (!file_exists($rolePath)) {
            echo "Error: Agent '{$agentName}' not found at {$rolePath}\n";
            return null;
        }

        return $this->parseYaml($rolePath);
    }
    
    /**
     * Load a tool configuration by name.
     *
     * @param string $toolName Name of the tool (e.g., 'write_python')
     * @return array|null Tool configuration or null if not found
     */
    public function loadTool($toolName) {
        $toolPath = $this->cliPath . '/tool/' . $toolName . '.yaml';

        if (file_exists($toolPath)) {
            return $this->parseYaml($toolPath);
        }

        // Search recursively in tool subdirectories
        $toolDir = $this->cliPath . '/tool';
        $files = $this->findYamlFiles($toolDir, $toolName);

        if (!empty($files)) {
            return $this->parseYaml($files[0]);
        }

        echo "Error: Tool '{$toolName}' not found\n";
        return null;
    }
    
    /**
     * List all available agents.
     *
     * @return array List of agent names
     */
    public function listAgents() {
        $roleDir = $this->cliPath . '/role';
        $agents = [];

        if (is_dir($roleDir)) {
            foreach (scandir($roleDir) as $item) {
                if ($item !== '.' && $item !== '..' && is_dir($roleDir . '/' . $item)) {
                    if (file_exists($roleDir . '/' . $item . '/role.yaml')) {
                        $agents[] = $item;
                    }
                }
            }
        }

        sort($agents);
        return $agents;
    }
    
    /**
     * List all available tools.
     *
     * @return array List of tool names
     */
    public function listTools() {
        $toolDir = $this->cliPath . '/tool';
        $tools = [];

        if (is_dir($toolDir)) {
            $this->findAllYamlTools($toolDir, $tools);
        }

        sort($tools);
        return array_unique($tools);
    }
    
    /**
     * Parse a simple YAML file.
     * 
     * @param string $filePath Path to YAML file
     * @return array Parsed YAML as associative array
     */
    private function parseYaml($filePath) {
        $content = file_get_contents($filePath);
        $lines = explode("\n", $content);
        $result = [];
        
        foreach ($lines as $line) {
            $line = trim($line);
            if (empty($line) || strpos($line, '#') === 0) {
                continue;
            }
            
            if (strpos($line, ':') !== false) {
                list($key, $value) = explode(':', $line, 2);
                $result[trim($key)] = trim($value);
            }
        }
        
        return $result;
    }
    
    /**
     * Find YAML files recursively.
     * 
     * @param string $dir Directory to search
     * @param string $toolName Tool name to find
     * @return array List of matching file paths
     */
    private function findYamlFiles($dir, $toolName) {
        $files = [];
        
        if (!is_dir($dir)) {
            return $files;
        }
        
        foreach (scandir($dir) as $item) {
            if ($item === '.' || $item === '..') {
                continue;
            }
            
            $path = $dir . '/' . $item;
            
            if (is_dir($path)) {
                $files = array_merge($files, $this->findYamlFiles($path, $toolName));
            } elseif (is_file($path) && pathinfo($path, PATHINFO_EXTENSION) === 'yaml') {
                if (pathinfo($path, PATHINFO_FILENAME) === $toolName . '.yaml') {
                    $files[] = $path;
                }
            }
        }
        
        return $files;
    }
    
    /**
     * Find all YAML tool files.
     * 
     * @param string $dir Directory to search
     * @param array &$tools Reference to tools array
     */
    private function findAllYamlTools($dir, &$tools) {
        if (!is_dir($dir)) {
            return;
        }
        
        foreach (scandir($dir) as $item) {
            if ($item === '.' || $item === '..') {
                continue;
            }
            
            $path = $dir . '/' . $item;
            
            if (is_dir($path)) {
                $this->findAllYamlTools($path, $tools);
            } elseif (is_file($path) && pathinfo($path, PATHINFO_EXTENSION) === 'yaml') {
                $tools[] = pathinfo($path, PATHINFO_FILENAME);
            }
        }
    }
}

?>
