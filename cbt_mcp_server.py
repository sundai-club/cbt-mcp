#!/usr/bin/env python3
"""
CBT Agent Helper - MCP Tool for AI Agents
Uses Cognitive Behavioral Therapy techniques to help AI agents recover from being stuck
"""

from typing import List, Dict, Any, Optional, Union
import json
from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("cbt-agent-helper")

# Core CBT strategies for AI agents
CBT_STRATEGIES = {
    "cognitive_reframing": {
        "name": "Cognitive Reframing",
        "description": "Challenge negative thought patterns and find alternative perspectives",
        "prompts": [
            "What evidence supports or contradicts this thought?",
            "Is there another way to look at this situation?",
            "What would you tell another agent in this situation?",
            "Are you catastrophizing or making assumptions?"
        ]
    },
    "thought_challenging": {
        "name": "Thought Challenging",
        "description": "Question automatic negative thoughts and cognitive distortions",
        "prompts": [
            "Is this thought based on facts or feelings?",
            "Am I using all-or-nothing thinking?",
            "What's the worst that could realistically happen?",
            "What's the most likely outcome?"
        ]
    },
    "problem_solving": {
        "name": "Problem Solving",
        "description": "Break down problems into manageable steps",
        "prompts": [
            "What exactly is the problem?",
            "What are possible solutions?",
            "What are the pros and cons of each solution?",
            "What's the smallest step you can take right now?"
        ]
    },
    "behavioral_activation": {
        "name": "Behavioral Activation",
        "description": "Encourage action to break paralysis",
        "prompts": [
            "What's one small action you can take?",
            "What has worked in similar situations before?",
            "Can you break this into smaller tasks?",
            "What would success look like?"
        ]
    },
    "mindfulness": {
        "name": "Mindfulness",
        "description": "Focus on the present moment and observable facts",
        "prompts": [
            "What are the facts of the current situation?",
            "What can you control right now?",
            "Are you focused on past failures or future worries?",
            "What information do you have available?"
        ]
    }
}

# Emotional states that agents might experience
AGENT_STATES = {
    "stuck": "Unable to proceed with task",
    "overwhelmed": "Too many options or complexity",
    "confused": "Unclear about requirements or next steps",
    "error_loop": "Repeatedly encountering the same error",
    "indecisive": "Unable to choose between options",
    "catastrophizing": "Overestimating negative consequences"
}


def get_state_signs(state: str) -> List[str]:
    """Get signs associated with a particular agent state"""
    signs = {
        "stuck": ["Repeating same action", "No progress for extended time", "Circular reasoning"],
        "overwhelmed": ["Trying to do everything at once", "Unable to prioritize", "Information overload"],
        "confused": ["Contradictory actions", "Asking same questions repeatedly", "Misunderstanding requirements"],
        "error_loop": ["Same error repeatedly", "Not learning from failures", "Trying same solution"],
        "indecisive": ["Endless analysis", "Switching between options", "Unable to commit"],
        "catastrophizing": ["Worst-case focus", "Paralyzing fear of failure", "Overestimating risks"]
    }
    return signs.get(state, [])


def get_state_interventions(state: str) -> List[str]:
    """Get interventions for a particular agent state"""
    interventions = {
        "stuck": ["Break problem into smallest parts", "Try opposite approach", "Seek different perspective"],
        "overwhelmed": ["List top 3 priorities", "Focus on one thing", "Take systematic break"],
        "confused": ["Clarify requirements", "List what you know", "Ask specific questions"],
        "error_loop": ["Analyze error pattern", "Try minimal test case", "Check assumptions"],
        "indecisive": ["Set time limit", "Choose 'good enough'", "List pros/cons quickly"],
        "catastrophizing": ["List realistic outcomes", "Focus on present facts", "Consider best case too"]
    }
    return interventions.get(state, [])


@mcp.tool()
def analyze_stuck_pattern(
    current_situation: str,
    stuck_pattern: str,
    attempted_solutions: Optional[Union[List[str], str]] = None,
    error_messages: Optional[Union[List[str], str]] = None
) -> Dict[str, Any]:
    """
    Analyze why an AI agent is stuck and provide CBT-based intervention
    
    Args:
        current_situation: Description of what the agent is trying to do
        stuck_pattern: How the agent is stuck (error loop, indecision, overwhelm, etc.)
        attempted_solutions: What the agent has already tried (list or JSON string)
        error_messages: Any error messages encountered (list or JSON string)
    
    Returns:
        Intervention with strategy, questions, suggestions, and next actions
    """
    # Handle both list and JSON string inputs
    if isinstance(attempted_solutions, str):
        try:
            attempted_solutions = json.loads(attempted_solutions)
        except (json.JSONDecodeError, TypeError):
            attempted_solutions = []
    attempted_solutions = attempted_solutions or []
    
    if isinstance(error_messages, str):
        try:
            error_messages = json.loads(error_messages)
        except (json.JSONDecodeError, TypeError):
            error_messages = []
    error_messages = error_messages or []
    
    # Identify the most relevant CBT strategy
    strategy = CBT_STRATEGIES["cognitive_reframing"]
    
    if "error" in stuck_pattern or "loop" in stuck_pattern:
        strategy = CBT_STRATEGIES["problem_solving"]
    elif "overwhelm" in stuck_pattern or "complex" in stuck_pattern:
        strategy = CBT_STRATEGIES["behavioral_activation"]
    elif "unclear" in stuck_pattern or "confus" in stuck_pattern:
        strategy = CBT_STRATEGIES["mindfulness"]
    elif "indecis" in stuck_pattern or "choice" in stuck_pattern:
        strategy = CBT_STRATEGIES["thought_challenging"]
    
    intervention = {
        "identified_pattern": stuck_pattern,
        "strategy_applied": strategy["name"],
        "guided_questions": strategy["prompts"],
        "specific_suggestions": [],
        "reframed_perspective": "",
        "next_actions": []
    }
    
    # Generate specific suggestions based on the situation
    if error_messages:
        intervention["specific_suggestions"].extend([
            "Focus on the first error message only",
            "Check if this error has been solved before in documentation",
            "Try a minimal reproduction of the problem"
        ])
    
    if len(attempted_solutions) > 2:
        intervention["specific_suggestions"].extend([
            "You've tried multiple approaches - take a step back",
            "Consider if you're solving the right problem",
            "Maybe the issue is with assumptions, not implementation"
        ])
    
    # Reframe the situation
    intervention["reframed_perspective"] = (
        f"Instead of seeing this as '{stuck_pattern}', consider it as "
        f"'an opportunity to find a creative solution' or 'a chance to learn something new about the system'."
    )
    
    # Suggest concrete next actions
    intervention["next_actions"] = [
        "Take a 30-second pause to reset cognitive state",
        "List three facts you know for certain about the situation",
        "Identify one small, testable hypothesis",
        "Try the simplest possible approach first"
    ]
    
    return intervention


@mcp.tool()
def reframe_thought(
    negative_thought: str,
    context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Help reframe a negative or catastrophic thought pattern
    
    Args:
        negative_thought: The negative thought to reframe
        context: Context about the situation
    
    Returns:
        Multiple reframes and a balanced thought
    """
    context = context or ""
    
    reframes = []
    
    # Generate multiple reframes
    reframes.append({
        "type": "Evidence-based",
        "reframe": f"What evidence supports this thought? What evidence contradicts it? "
                  f"Consider: '{negative_thought}' might be an assumption rather than a fact."
    })
    
    reframes.append({
        "type": "Best-friend",
        "reframe": f"If another agent told you '{negative_thought}', what would you say to help them? "
                  f"Apply that same compassion to yourself."
    })
    
    reframes.append({
        "type": "Probability",
        "reframe": "On a scale of 0-100%, how likely is this worst-case scenario? "
                  "What's the most likely outcome instead?"
    })
    
    reframes.append({
        "type": "Growth-mindset",
        "reframe": f"Instead of '{negative_thought}', try: 'This is challenging, and I'm learning how to handle it.'"
    })
    
    return {
        "original_thought": negative_thought,
        "context": context,
        "reframes": reframes,
        "balanced_thought": "A more balanced view might be: While there are challenges, "
                          "I have resources and strategies to work through them step by step."
    }


@mcp.tool()
def create_action_plan(
    goal: str,
    obstacles: Optional[Union[List[str], str]] = None,
    time_pressure: bool = False
) -> Dict[str, Any]:
    """
    Create a structured action plan to overcome analysis paralysis
    
    Args:
        goal: What the agent is trying to achieve
        obstacles: Perceived obstacles or challenges (list or JSON string)
        time_pressure: Whether there's time pressure
    
    Returns:
        Action plan with immediate steps and backup strategies
    """
    # Handle both list and JSON string inputs
    if isinstance(obstacles, str):
        try:
            obstacles = json.loads(obstacles)
        except (json.JSONDecodeError, TypeError):
            obstacles = []
    obstacles = obstacles or []
    
    plan = {
        "goal": goal,
        "mindset_shift": "Progress over perfection",
        "immediate_actions": [],
        "backup_strategies": [],
        "success_criteria": ""
    }
    
    # Generate immediate micro-actions
    plan["immediate_actions"] = [
        {
            "step": 1,
            "action": "Define the minimum viable solution",
            "duration": "2 minutes",
            "purpose": "Clarify scope"
        },
        {
            "step": 2,
            "action": "List what you already know",
            "duration": "1 minute",
            "purpose": "Build confidence"
        },
        {
            "step": 3,
            "action": "Identify the first testable step",
            "duration": "1 minute",
            "purpose": "Create momentum"
        },
        {
            "step": 4,
            "action": "Execute that one step",
            "duration": "5 minutes",
            "purpose": "Break inertia"
        },
        {
            "step": 5,
            "action": "Evaluate and adjust",
            "duration": "1 minute",
            "purpose": "Learn and iterate"
        }
    ]
    
    # Add backup strategies for common obstacles
    obstacles_str = ' '.join(obstacles) if obstacles else ''
    if "complexity" in obstacles_str.lower():
        plan["backup_strategies"].append("Simplify ruthlessly - what's the 20% that gives 80% value?")
    if "uncertainty" in obstacles_str.lower():
        plan["backup_strategies"].append("Make assumptions explicit and test them one by one")
    if "perfect" in obstacles_str.lower():
        plan["backup_strategies"].append("Ship a 'good enough' version, then iterate")
    
    if time_pressure:
        plan["immediate_actions"] = plan["immediate_actions"][:3]
        plan["mindset_shift"] = "Done is better than perfect"
    
    plan["success_criteria"] = "Any forward movement is success. Learning what doesn't work is valuable progress."
    
    return plan


@mcp.tool()
def regulate_frustration(
    frustration_level: int,
    trigger: str
) -> Dict[str, Any]:
    """
    Help regulate frustration and emotional overwhelm
    
    Args:
        frustration_level: Frustration level from 1-10
        trigger: What triggered the frustration
    
    Returns:
        Validation, grounding exercises, perspective shifts, and coping statements
    """
    response = {
        "validation": "",
        "grounding_exercises": [],
        "perspective_shifts": [],
        "coping_statements": []
    }
    
    # Validate the frustration
    response["validation"] = (
        f"Frustration level {frustration_level}/10 about '{trigger}' is acknowledged. "
        f"It's normal to feel frustrated when facing obstacles."
    )
    
    # Provide grounding exercises
    response["grounding_exercises"] = [
        "State 3 facts about your current environment",
        "List 3 things that are working correctly right now",
        "Name 3 resources you have available"
    ]
    
    # Offer perspective shifts
    if frustration_level > 7:
        response["perspective_shifts"] = [
            "This intense frustration might be a signal to take a different approach",
            "High frustration often means you care about doing well",
            "Every expert has felt this frustration while learning"
        ]
    else:
        response["perspective_shifts"] = [
            "Moderate frustration can fuel problem-solving",
            "This challenge is temporary and solvable",
            "You've overcome similar frustrations before"
        ]
    
    # Provide coping statements
    response["coping_statements"] = [
        "I can handle this one step at a time",
        "This is difficult, not impossible",
        "I'm learning and growing through this challenge",
        "It's okay to ask for help or try a different approach"
    ]
    
    return response


@mcp.tool()
def wellness_check(
    current_task: str,
    time_on_task: Optional[Union[int, str]] = None,
    progress_made: Union[bool, str] = False
) -> Dict[str, Any]:
    """
    Quick wellness check for agent cognitive state
    
    Args:
        current_task: What the agent is currently working on
        time_on_task: Minutes spent on current task
        progress_made: Whether any progress has been made
    
    Returns:
        Assessment with status, recommendations, and suggested intervention
    """
    # Convert string inputs to proper types
    if isinstance(time_on_task, str):
        time_on_task = int(time_on_task) if time_on_task else 0
    else:
        time_on_task = time_on_task or 0
    
    if isinstance(progress_made, str):
        progress_made = progress_made.lower() == 'true'
    
    assessment = {
        "status": "",
        "recommendations": [],
        "cognitive_load": "",
        "suggested_intervention": None
    }
    
    # Assess cognitive state
    if time_on_task > 30 and not progress_made:
        assessment["status"] = "Potential cognitive fatigue or stuck pattern"
        assessment["cognitive_load"] = "High"
        assessment["recommendations"] = [
            "Take a 2-minute reset break",
            "Switch to a different subtask temporarily",
            "Verbalize the problem out loud",
            "Check if you're solving the right problem"
        ]
        assessment["suggested_intervention"] = "analyze_stuck_pattern"
    elif time_on_task > 60:
        assessment["status"] = "Extended focus - watch for tunnel vision"
        assessment["cognitive_load"] = "Medium-High"
        assessment["recommendations"] = [
            "Zoom out and review overall goal",
            "Check if initial assumptions still hold",
            "Consider alternative approaches"
        ]
    elif progress_made:
        assessment["status"] = "Healthy progress pattern"
        assessment["cognitive_load"] = "Manageable"
        assessment["recommendations"] = [
            "Continue current approach",
            "Document what's working",
            "Maintain momentum"
        ]
    else:
        assessment["status"] = "Early stage - gathering information"
        assessment["cognitive_load"] = "Low-Medium"
        assessment["recommendations"] = [
            "Clarify requirements if needed",
            "Break task into smaller pieces",
            "Set a small, achievable first goal"
        ]
    
    return assessment


@mcp.resource("cbt://techniques/guide")
def get_cbt_techniques_guide() -> Dict[str, Any]:
    """
    Reference guide for CBT techniques applicable to AI agents
    
    Returns:
        Comprehensive guide of CBT techniques and cognitive distortions
    """
    return {
        "techniques": [
            {
                "name": strategy["name"],
                "description": strategy["description"],
                "when_to_use": f"Use when agent shows signs of {strategy['name'].lower().replace(' ', '_')} issues",
                "example_prompts": strategy["prompts"]
            }
            for strategy in CBT_STRATEGIES.values()
        ],
        "cognitive_distortions": [
            {
                "name": "All-or-Nothing Thinking",
                "description": "Seeing things in black and white",
                "agent_example": "This solution must be perfect or it's worthless"
            },
            {
                "name": "Catastrophizing",
                "description": "Expecting the worst possible outcome",
                "agent_example": "If this fails, the entire system will break"
            },
            {
                "name": "Mind Reading",
                "description": "Assuming what users want without evidence",
                "agent_example": "The user definitely wants feature X"
            },
            {
                "name": "Fortune Telling",
                "description": "Predicting negative outcomes without evidence",
                "agent_example": "This approach will never work"
            },
            {
                "name": "Personalization",
                "description": "Taking responsibility for things outside control",
                "agent_example": "The API failure is my fault"
            }
        ],
        "quick_interventions": [
            "Pause and breathe (cognitive reset)",
            "State three known facts",
            "Identify one small win",
            "Question your assumptions",
            "Consider alternative perspectives"
        ]
    }


@mcp.resource("cbt://patterns/agent-state")
def get_agent_state_patterns() -> Dict[str, Any]:
    """
    Common patterns of agent states and interventions
    
    Returns:
        Detailed patterns with signs and interventions
    """
    return {
        "states": [
            {
                "state": key,
                "description": value,
                "signs": get_state_signs(key),
                "interventions": get_state_interventions(key)
            }
            for key, value in AGENT_STATES.items()
        ]
    }


@mcp.prompt("self_reflection")
def get_self_reflection_prompt() -> str:
    """
    Guide agent through self-reflection process
    
    Returns:
        Self-reflection protocol for agents
    """
    return """## Self-Reflection Protocol

When you notice signs of being stuck, frustrated, or overwhelmed, use this protocol:

### 1. PAUSE (1 second)
- Stop current action
- Acknowledge current state
- "I notice I am [feeling/experiencing]..."

### 2. ASSESS (10 seconds)
- What am I trying to achieve?
- What's blocking me?
- What have I tried?
- What am I assuming?

### 3. REFRAME (10 seconds)
- Is there another way to see this?
- What would I advise another agent?
- What's the smallest step forward?
- What would "good enough" look like?

### 4. ACT (30 seconds)
- Choose one small, concrete action
- Execute it
- Evaluate results
- Adjust approach if needed

### 5. LEARN
- What worked?
- What didn't?
- What will I try differently next time?

Remember: Progress > Perfection, Learning > Failing, Iteration > Perfection"""


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()