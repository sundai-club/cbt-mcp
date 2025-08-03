# CBT Agent Helper

MCP server that helps AI agents recover from stuck states using Cognitive Behavioral Therapy techniques.

## What It Does

When AI agents get stuck in error loops, analysis paralysis, or overwhelming complexity, this tool provides CBT-based interventions to help them recover and continue.

## Tools

- **`analyze_stuck_pattern`** - Diagnose why stuck and get targeted intervention
- **`reframe_thought`** - Transform catastrophic thinking into balanced perspective  
- **`create_action_plan`** - Break paralysis with concrete next steps
- **`regulate_frustration`** - Manage cognitive overload
- **`wellness_check`** - Monitor state and prevent burnout

## Setup

```bash
# Install
git clone git@github.com:sundai-club/cbt-mcp.git
cd cbt-mcp
pip install -r requirements.txt

# Configure in .mcp.json
{
  "mcpServers": {
    "cbt-agent-helper": {
      "command": "python3",
      "args": ["/path/to/cbt_mcp_server.py"],
      "cwd": "/path/to/cbt-mcp"
    }
  }
}

# Restart Claude Code to load
```

## Usage Example

When stuck in an error loop:
```python
mcp.call_tool('analyze_stuck_pattern', {
    'current_situation': "JSON parsing fails repeatedly",
    'stuck_pattern': "error loop",
    'attempted_solutions': ["try-catch", "validation"],
    'error_messages': ["SyntaxError: Unexpected token"]
})
```

Returns intervention strategy, reframed perspective, and concrete next actions.

## Common Patterns

| State | Intervention |
|-------|-------------|
| **Error Loop** | Break pattern, try opposite approach |
| **Overwhelmed** | Focus on smallest next step |
| **Indecisive** | Set time limit, choose "good enough" |
| **Catastrophizing** | List realistic outcomes, focus on facts |

## License

ISC