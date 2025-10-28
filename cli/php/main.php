<?php

require_once __DIR__ . '/AgentLoader.php';

/**
 * Main CLI entry point for the agent framework (PHP).
 */

$loader = new AgentLoader();

echo str_repeat("=", 60) . "\n";
echo "AI Agent Framework CLI (PHP)\n";
echo str_repeat("=", 60) . "\n";

// List available agents
echo "\n📋 Available Agents:\n";
$agents = $loader->listAgents();
if (!empty($agents)) {
    foreach ($agents as $agent) {
        echo "   ✓ {$agent}\n";
    }
} else {
    echo "   (No agents found)\n";
}

// List available tools
echo "\n🔧 Available Tools:\n";
$tools = $loader->listTools();
if (!empty($tools)) {
    $displayTools = array_slice($tools, 0, 10);
    foreach ($displayTools as $tool) {
        echo "   ✓ {$tool}\n";
    }
    if (count($tools) > 10) {
        echo "   ... and " . (count($tools) - 10) . " more\n";
    }
} else {
    echo "   (No tools found)\n";
}

// Example: Load and display a specific agent
echo "\n" . str_repeat("=", 60) . "\n";
echo "Example: Loading 'coder-agent' configuration\n";
echo str_repeat("=", 60) . "\n";
$agentConfig = $loader->loadAgent('coder-agent');
if ($agentConfig) {
    echo "✓ Successfully loaded agent configuration\n";
    echo "  Keys: " . implode(', ', array_keys($agentConfig)) . "\n";
}

// Example: Load and display a specific tool
echo "\nExample: Loading 'write_python' tool configuration\n";
$toolConfig = $loader->loadTool('write_python');
if ($toolConfig) {
    echo "✓ Successfully loaded tool configuration\n";
    echo "  Keys: " . implode(', ', array_keys($toolConfig)) . "\n";
}

echo "\n" . str_repeat("=", 60) . "\n";
echo "Framework integration successful!\n";
echo str_repeat("=", 60) . "\n";

?>