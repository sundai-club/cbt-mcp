# CBT Agent Helper v3.0 - Deep Thinking Edition

Enhanced MCP server that helps AI agents think deeply, recover from stuck states, and engage in extended contemplation using CBT techniques and structured thinking protocols.

## What's New in v3.0 - Deep Thinking Enhancement

### 🧠 Deep Thinking Features
- **Contemplation Structures**: Multi-phase thinking protocols (4-6 minutes)
- **Socratic Dialogue Chains**: 7 types with progressive depth levels
- **Reflection Loops**: Iterative deepening with 3+ rounds
- **Thought Experiments**: Explore concepts through mental simulations
- **Thinking Depth Ladder**: 7-level progression from surface to transcendent
- **Recursive Questioning**: Questions that lead to deeper questions
- **Thought Expansion**: 10 techniques for multi-dimensional exploration
- **Metacognitive Monitoring**: Real-time thinking quality assessment
- **Thinking Metrics**: Quantified depth, breadth, and integration scores

## What's New in v2.0

### Core Improvements
- **Session Management**: Track agent progress across interactions with persistent state
- **Enhanced Validation**: Robust error handling with clear error messages
- **9 CBT Strategies**: Added Socratic Questioning, ACT, Graded Exposure, and more
- **11 Agent States**: Expanded from 6 to 11 states including perfectionism, fragmentation
- **Frustration Tracking**: Monitor and respond to escalating frustration patterns
- **Progress Indicators**: Track positive changes and intervention effectiveness
- **Configuration Support**: Customize behavior via `cbt_config.json`
- **Cognitive Distortion Detection**: Identify and address specific thinking patterns

## Tools

### Deep Thinking Tools (NEW in v3.0)
- **`initiate_deep_thinking`** - Start structured contemplation with phases and prompts
- **`socratic_dialogue`** - Progressive questioning to examine assumptions
- **`generate_thought_experiment`** - Mental simulations for concept exploration
- **`thinking_depth_ladder`** - Ascend through 7 levels of thinking depth
- **`recursive_questioning`** - Questions that spiral into deeper understanding
- **`expand_thought`** - Apply 10+ lenses to expand perspectives
- **`metacognitive_check`** - Assess and improve thinking quality
- **`thinking_session_summary`** - Get metrics and insights from thinking session

### Session Management
- **`start_session`** - Initialize a CBT session with unique ID
- **`get_session_summary`** - Get comprehensive session analysis with insights

### Core Interventions
- **`analyze_stuck_pattern`** - Enhanced diagnosis with session tracking
- **`reframe_thought`** - Cognitive distortion detection and targeted reframes
- **`create_action_plan`** - Obstacle analysis with backup strategies
- **`regulate_frustration`** - Level-based interventions with immediate relief
- **`wellness_check`** - Wellness scoring with risk factor identification

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

# Optional: Customize via cbt_config.json
# Edit settings for frustration thresholds, session limits, etc.

# Restart Claude Code to load
```

## Deep Thinking Usage Example (v3.0)

```python
# Initiate deep thinking session
thinking = mcp.call_tool('initiate_deep_thinking', {
    'topic': 'How should AI systems handle ethical dilemmas?',
    'desired_depth': 'profound'
})
# AI agent receives structured prompts requiring 4-6 minutes of contemplation

# Engage in Socratic dialogue
dialogue = mcp.call_tool('socratic_dialogue', {
    'statement': 'AI should always prioritize human safety',
    'dialogue_type': 'assumption_examination',
    'depth_level': 5
})
# AI agent works through 5 rounds of progressively deeper questions

# Create thought experiment
experiment = mcp.call_tool('generate_thought_experiment', {
    'concept': 'artificial consciousness'
})
# AI agent explores concept through 3 structured mental simulations

# Progress through thinking depth ladder
ladder = mcp.call_tool('thinking_depth_ladder', {
    'question': 'What is intelligence?',
    'target_depth': 7
})
# AI agent ascends from surface observations to transcendent understanding
```

## Standard CBT Usage Example

```python
# Start a session
session = mcp.call_tool('start_session', {
    'session_id': 'agent_001',
    'initial_problem': 'Stuck optimizing already-working code'
})

# Analyze with session tracking
intervention = mcp.call_tool('analyze_stuck_pattern', {
    'current_situation': 'Refactoring for 5th time',
    'stuck_pattern': 'perfectionist loop',
    'attempted_solutions': ['rewrote 3x', 'benchmarked'],
    'session_id': 'agent_001'
})

# Reframe catastrophic thoughts
reframe = mcp.call_tool('reframe_thought', {
    'negative_thought': 'If not perfect, project fails',
    'context': 'Feature already works',
    'session_id': 'agent_001'
})

# Get session insights
summary = mcp.call_tool('get_session_summary', {
    'session_id': 'agent_001'
})
```

## Expanded Agent States

| State | Description | Key Intervention |
|-------|-------------|------------------|
| **Stuck** | No progress | Break into smallest parts |
| **Overwhelmed** | Too much complexity | Focus on one priority |
| **Confused** | Unclear requirements | Clarify and list knowns |
| **Error Loop** | Repeating failures | Analyze pattern, try opposite |
| **Indecisive** | Can't choose | Time-box decision |
| **Catastrophizing** | Worst-case focus | List realistic outcomes |
| **Blocked** | External constraints | Document and escalate |
| **Looping** | Same actions, no results | Stop and change approach |
| **Fragmented** | Task switching | Pick one to complete |
| **Perfectionist** | Unrealistic standards | Define "good enough" |
| **Analysis Paralysis** | Over-thinking | Set deadline, act |

## CBT Strategies Available

1. **Cognitive Reframing** - Challenge negative patterns
2. **Thought Challenging** - Question distortions
3. **Problem Solving** - Systematic approach
4. **Behavioral Activation** - Break paralysis
5. **Mindfulness** - Present focus
6. **Socratic Questioning** - Uncover assumptions
7. **Cost-Benefit Analysis** - Evaluate trade-offs
8. **Graded Exposure** - Progressive steps
9. **Acceptance & Commitment** - Work with constraints

## Configuration Options

Edit `cbt_config.json` to customize:
- Frustration thresholds (1-10 scale)
- Session timeout and cleanup intervals
- Preferred CBT strategy order
- Feature toggles (emojis, auto-escalation)
- Wellness check intervals

## Testing

```bash
# Run comprehensive test suite
python3 test_improvements_mock.py

# Test with example scenarios
python3 example_usage_enhanced.py
```

## Resources

- **Techniques Guide**: `mcp.read_resource('cbt://techniques/guide')`
- **Agent States**: `mcp.read_resource('cbt://patterns/agent-state')`
- **Self-Reflection**: `mcp.get_prompt('self_reflection')`
- **Quick Help**: `mcp.get_prompt('quick_help')`

## Impact on AI Agent Thinking

### Before Deep Thinking Tools
- Quick, surface-level responses (2-3 sentences)
- Single perspective or solution
- Rushes to conclusions
- Avoids complexity
- Linear thinking pattern

### After Deep Thinking Tools
- Extended contemplation (50+ sentences)
- Multiple perspectives explored
- Takes 4-6 minutes per complex topic
- Embraces paradox and uncertainty
- Recursive, spiraling exploration
- Generates new questions
- Metacognitive awareness
- Nuanced, comprehensive understanding

### Thinking Depth Levels
1. **Surface**: Immediate, obvious responses
2. **Factual**: Evidence-based analysis
3. **Analytical**: Pattern recognition
4. **Critical**: Assumption questioning
5. **Synthetic**: Integration of perspectives
6. **Philosophical**: Fundamental principles
7. **Transcendent**: Beyond conventional understanding

## Version History

- **v3.0** - Deep Thinking Enhancement with contemplation protocols
- **v2.0** - Major enhancement with sessions, validation, config
- **v1.0** - Initial release with basic CBT tools

## License

MIT