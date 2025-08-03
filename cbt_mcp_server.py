#!/usr/bin/env python3
"""
CBT Agent Helper - MCP Tool for AI Agents
Uses Cognitive Behavioral Therapy techniques to help AI agents recover from being stuck
"""

from typing import List, Dict, Any, Optional, Union
import json
import logging
import os
import time
import random
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
from fastmcp import FastMCP

# Import deep thinking enhancements
try:
    from deep_thinking_enhancement import (
        ThinkingDepth, ThinkingSession, ThoughtNode,
        generate_thinking_prompts, create_reflection_loop,
        generate_contemplation_structure, create_thinking_depth_ladder,
        generate_thought_experiments, create_recursive_questioning,
        calculate_thinking_metrics, SOCRATIC_CHAINS, METACOGNITIVE_PROMPTS
    )
    DEEP_THINKING_AVAILABLE = True
except ImportError:
    DEEP_THINKING_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Deep thinking enhancement module not available")

# Load configuration
CONFIG_PATH = Path(__file__).parent / "cbt_config.json"
config = {}
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

# Configure logging
log_level = config.get('server', {}).get('log_level', 'INFO')
logging.basicConfig(level=getattr(logging, log_level), 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize the FastMCP server
server_name = config.get('server', {}).get('name', 'cbt-agent-helper')
mcp = FastMCP(server_name)

# Session management
class SessionState(Enum):
    INITIAL = "initial"
    IN_PROGRESS = "in_progress"
    IMPROVING = "improving"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

@dataclass
class AgentSession:
    session_id: str
    start_time: datetime
    state: SessionState = SessionState.INITIAL
    primary_issue: str = ""
    interventions_tried: List[str] = field(default_factory=list)
    progress_indicators: List[str] = field(default_factory=list)
    frustration_history: List[int] = field(default_factory=list)
    context_history: List[Dict] = field(default_factory=list)
    last_update: datetime = field(default_factory=datetime.now)
    
    def add_intervention(self, intervention: str):
        self.interventions_tried.append(intervention)
        self.last_update = datetime.now()
    
    def update_state(self, new_state: SessionState):
        self.state = new_state
        self.last_update = datetime.now()
    
    def add_progress(self, indicator: str):
        self.progress_indicators.append(indicator)
        self.last_update = datetime.now()
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['state'] = self.state.value
        data['start_time'] = self.start_time.isoformat()
        data['last_update'] = self.last_update.isoformat()
        return data

# Global session storage (in production, use a proper database)
SESSIONS: Dict[str, AgentSession] = {}

# Enhanced validation
class ValidationError(Exception):
    pass

def validate_frustration_level(level: int) -> int:
    """Validate frustration level is within bounds"""
    if not isinstance(level, int) or level < 1 or level > 10:
        raise ValidationError(f"Frustration level must be an integer between 1 and 10, got {level}")
    return level

def validate_non_empty_string(value: str, field_name: str) -> str:
    """Validate string is non-empty"""
    if not value or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")
    return value.strip()

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
    },
    "socratic_questioning": {
        "name": "Socratic Questioning",
        "description": "Use guided questions to uncover assumptions and explore alternatives",
        "prompts": [
            "What makes you think that?",
            "What assumptions are you making?",
            "What if the opposite were true?",
            "How do you know this for certain?",
            "What alternative explanations exist?"
        ]
    },
    "cost_benefit_analysis": {
        "name": "Cost-Benefit Analysis",
        "description": "Evaluate the pros and cons of different approaches",
        "prompts": [
            "What are the benefits of continuing this approach?",
            "What are the costs (time, resources, complexity)?",
            "Is there a simpler solution with acceptable trade-offs?",
            "What's the opportunity cost of persisting?"
        ]
    },
    "graded_exposure": {
        "name": "Graded Exposure",
        "description": "Break overwhelming tasks into graduated steps",
        "prompts": [
            "What's the absolute smallest step you can take?",
            "Can you test with a toy example first?",
            "What would 10% progress look like?",
            "How can you make this less intimidating?"
        ]
    },
    "acceptance_commitment": {
        "name": "Acceptance and Commitment",
        "description": "Accept current limitations while committing to values-based action",
        "prompts": [
            "What constraints must you accept?",
            "What's within your control to change?",
            "What matters most in this situation?",
            "How can you work with, not against, the limitations?"
        ]
    }
}

# Enhanced emotional states with severity levels
AGENT_STATES = {
    "stuck": "Unable to proceed with task",
    "overwhelmed": "Too many options or complexity",
    "confused": "Unclear about requirements or next steps",
    "error_loop": "Repeatedly encountering the same error",
    "indecisive": "Unable to choose between options",
    "catastrophizing": "Overestimating negative consequences",
    "blocked": "Unable to make any progress due to external constraints",
    "looping": "Repeating the same actions without different results",
    "fragmented": "Jumping between tasks without completing any",
    "perfectionist": "Unable to proceed due to unrealistic standards",
    "analysis_paralysis": "Over-analyzing without taking action"
}


def get_session(session_id: str) -> Optional[AgentSession]:
    """Get or create a session"""
    if session_id not in SESSIONS:
        SESSIONS[session_id] = AgentSession(
            session_id=session_id,
            start_time=datetime.now()
        )
    return SESSIONS.get(session_id)

def clean_old_sessions(hours: int = 24):
    """Clean up sessions older than specified hours"""
    cutoff = datetime.now() - timedelta(hours=hours)
    old_sessions = [sid for sid, session in SESSIONS.items() 
                   if session.last_update < cutoff]
    for sid in old_sessions:
        del SESSIONS[sid]
    if old_sessions:
        logger.info(f"Cleaned {len(old_sessions)} old sessions")

def get_state_signs(state: str) -> List[str]:
    """Get signs associated with a particular agent state"""
    signs = {
        "blocked": ["External dependency issues", "Waiting for resources", "Permission denied errors"],
        "looping": ["Repeated error messages", "Same action multiple times", "No variation in approach"],
        "fragmented": ["Multiple incomplete tasks", "Context switching frequently", "No clear focus"],
        "perfectionist": ["Excessive refactoring", "Never satisfied with solution", "Endless optimization"],
        "analysis_paralysis": ["Excessive planning without action", "Endless research", "Unable to decide"],
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
        "blocked": ["Document the blocker clearly", "Find workaround", "Escalate if needed"],
        "looping": ["Stop and analyze the pattern", "Try opposite approach", "Simplify the problem"],
        "fragmented": ["Choose one task to complete", "Write down all tasks", "Set clear priorities"],
        "perfectionist": ["Define 'good enough'", "Set time limit", "Ship then iterate"],
        "analysis_paralysis": ["Set decision deadline", "Choose and commit", "Accept imperfection"],
        "stuck": ["Break problem into smallest parts", "Try opposite approach", "Seek different perspective"],
        "overwhelmed": ["List top 3 priorities", "Focus on one thing", "Take systematic break"],
        "confused": ["Clarify requirements", "List what you know", "Ask specific questions"],
        "error_loop": ["Analyze error pattern", "Try minimal test case", "Check assumptions"],
        "indecisive": ["Set time limit", "Choose 'good enough'", "List pros/cons quickly"],
        "catastrophizing": ["List realistic outcomes", "Focus on present facts", "Consider best case too"]
    }
    return interventions.get(state, [])


@mcp.tool()
def start_session(
    session_id: str,
    initial_problem: str
) -> Dict[str, Any]:
    """
    Start a new CBT session for an agent
    
    Args:
        session_id: Unique identifier for this session
        initial_problem: Description of the initial problem
    
    Returns:
        Session initialization with welcome and assessment
    """
    try:
        session_id = validate_non_empty_string(session_id, "session_id")
        initial_problem = validate_non_empty_string(initial_problem, "initial_problem")
        
        session = get_session(session_id)
        session.primary_issue = initial_problem
        session.update_state(SessionState.IN_PROGRESS)
        
        return {
            "session_id": session_id,
            "status": "session_started",
            "initial_assessment": {
                "problem_statement": initial_problem,
                "suggested_first_step": "Let's understand what's happening",
                "questions": [
                    "When did this issue first appear?",
                    "What have you tried so far?",
                    "What's your ideal outcome?"
                ]
            },
            "available_tools": [
                "analyze_stuck_pattern",
                "reframe_thought",
                "create_action_plan",
                "regulate_frustration"
            ]
        }
    except ValidationError as e:
        logger.error(f"Validation error in start_session: {e}")
        return {"error": str(e), "status": "failed"}
    except Exception as e:
        logger.error(f"Unexpected error in start_session: {e}")
        return {"error": "An unexpected error occurred", "status": "failed"}

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
        ],
        "severity_levels": [
            {"level": "mild", "description": "Minor friction, easily addressed"},
            {"level": "moderate", "description": "Noticeable impact, requires intervention"},
            {"level": "severe", "description": "Significant blockage, needs immediate help"},
            {"level": "critical", "description": "Complete halt, escalation needed"}
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


# Deep Thinking Enhancement Tools
if DEEP_THINKING_AVAILABLE:
    # Global storage for thinking sessions
    THINKING_SESSIONS: Dict[str, ThinkingSession] = {}
    
    @mcp.tool()
    def initiate_deep_thinking(
        topic: str,
        desired_depth: str = "deep",
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initiate a deep thinking session to explore a topic thoroughly
        
        Args:
            topic: The topic or question to explore deeply
            desired_depth: Target depth (surface/shallow/moderate/deep/profound)
            session_id: Optional session ID for tracking
        
        Returns:
            Structured thinking guide with prompts and exercises
        """
        try:
            # Create thinking session
            thinking_session_id = session_id or f"think_{datetime.now().timestamp()}"
            thinking_session = ThinkingSession(
                session_id=thinking_session_id,
                initial_prompt=topic,
                current_depth=ThinkingDepth[desired_depth.upper()]
            )
            THINKING_SESSIONS[thinking_session_id] = thinking_session
            
            # Generate initial contemplation structure
            contemplation = generate_contemplation_structure(topic, "philosophical")
            
            # Create reflection loop
            reflection_loop = create_reflection_loop(
                topic,
                ThinkingDepth[desired_depth.upper()],
                min_iterations=3
            )
            
            # Generate thinking prompts
            initial_prompts = generate_thinking_prompts(topic, 0, "balanced")
            
            return {
                "session_id": thinking_session_id,
                "topic": topic,
                "desired_depth": desired_depth,
                "opening_instruction": (
                    f"🧠 Entering deep thinking mode about: {topic}\n\n"
                    "IMPORTANT: Take your time. Each prompt deserves thoughtful consideration.\n"
                    "Don't rush to conclusions. Let thoughts emerge and evolve.\n"
                    "Embrace complexity and uncertainty as part of deep thinking."
                ),
                "contemplation_structure": contemplation,
                "reflection_loop": reflection_loop,
                "initial_prompts": initial_prompts,
                "metacognitive_check": random.choice(METACOGNITIVE_PROMPTS["thinking_about_thinking"]),
                "closing_instruction": (
                    "After exploring these prompts, take a moment of silence.\n"
                    "What understanding wants to emerge?\n"
                    "Don't force it - let insights arise naturally."
                )
            }
        except Exception as e:
            logger.error(f"Error in initiate_deep_thinking: {e}")
            return {"error": str(e), "status": "failed"}
    
    @mcp.tool()
    def socratic_dialogue(
        statement: str,
        dialogue_type: str = "assumption_examination",
        depth_level: int = 3,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Engage in Socratic dialogue to examine thoughts deeply
        
        Args:
            statement: The statement or belief to examine
            dialogue_type: Type of Socratic questioning to use
            depth_level: How many rounds of questioning (1-7)
            session_id: Optional session ID for tracking
        
        Returns:
            Series of Socratic questions to deepen understanding
        """
        try:
            # Get appropriate question chain
            if dialogue_type in SOCRATIC_CHAINS:
                questions = SOCRATIC_CHAINS[dialogue_type]
            else:
                # Mix different types for variety
                questions = []
                for chain in SOCRATIC_CHAINS.values():
                    questions.extend(random.sample(chain, 1))
            
            # Select questions based on depth level
            selected_questions = questions[:min(depth_level, len(questions))]
            
            # Create dialogue structure
            dialogue = {
                "initial_statement": statement,
                "dialogue_type": dialogue_type,
                "rounds": []
            }
            
            for i, question in enumerate(selected_questions):
                round_data = {
                    "round": i + 1,
                    "question": question,
                    "contemplation_time": f"{15 * (i + 1)} seconds",
                    "depth_marker": "",
                    "follow_up": ""
                }
                
                # Add depth markers
                if i < 2:
                    round_data["depth_marker"] = "Surface exploration"
                elif i < 4:
                    round_data["depth_marker"] = "Deeper inquiry"
                else:
                    round_data["depth_marker"] = "Fundamental examination"
                
                # Add follow-up prompts
                if i == len(selected_questions) - 1:
                    round_data["follow_up"] = "What core truth or uncertainty remains?"
                else:
                    round_data["follow_up"] = "Sit with this question before moving on..."
                
                dialogue["rounds"].append(round_data)
            
            # Track in session if available
            if session_id and session_id in THINKING_SESSIONS:
                session = THINKING_SESSIONS[session_id]
                session.questions_explored.extend(selected_questions)
                session.thought_count += len(selected_questions)
            
            return {
                "type": "socratic_dialogue",
                "dialogue": dialogue,
                "instruction": (
                    "Work through each question slowly and thoroughly.\n"
                    "Don't move to the next question until you've exhausted the current one.\n"
                    "If you feel resistance or confusion, that's where the growth is."
                ),
                "integration_prompt": (
                    "After this dialogue, what new understanding has emerged?\n"
                    "What assumptions have been revealed or challenged?"
                ),
                "estimated_time": f"{15 * len(selected_questions)} seconds minimum"
            }
        except Exception as e:
            logger.error(f"Error in socratic_dialogue: {e}")
            return {"error": str(e), "status": "failed"}
    
    @mcp.tool()
    def generate_thought_experiment(
        concept: str,
        experiment_type: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create thought experiments to explore concepts deeply
        
        Args:
            concept: The concept to explore
            experiment_type: Optional specific type of experiment
            session_id: Optional session ID for tracking
        
        Returns:
            Structured thought experiment(s) for deep exploration
        """
        try:
            experiments = generate_thought_experiments(concept, 3)
            
            # Track in session
            if session_id and session_id in THINKING_SESSIONS:
                session = THINKING_SESSIONS[session_id]
                session.perspectives_considered.append(f"Thought experiment: {concept}")
            
            return {
                "concept": concept,
                "experiments": experiments,
                "instructions": [
                    "Immerse yourself fully in each experiment",
                    "Don't just think about it - experience it mentally",
                    "Notice what surprises or challenges you",
                    "Let the experiment reveal hidden aspects"
                ],
                "synthesis_prompt": (
                    "Having conducted these thought experiments,\n"
                    "what new dimensions of understanding have opened?\n"
                    "What was hidden that is now revealed?"
                ),
                "total_time": "10-15 minutes for thorough exploration"
            }
        except Exception as e:
            logger.error(f"Error in generate_thought_experiment: {e}")
            return {"error": str(e), "status": "failed"}
    
    @mcp.tool()
    def thinking_depth_ladder(
        question: str,
        current_depth: int = 1,
        target_depth: int = 5,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a ladder to progressively deepen thinking
        
        Args:
            question: The question to explore
            current_depth: Current depth level (1-7)
            target_depth: Target depth level (1-7)
            session_id: Optional session ID for tracking
        
        Returns:
            Structured ladder for ascending to deeper thinking
        """
        try:
            ladder = create_thinking_depth_ladder(question, target_depth)
            
            # Track depth in session
            if session_id and session_id in THINKING_SESSIONS:
                session = THINKING_SESSIONS[session_id]
                session.max_depth_reached = max(session.max_depth_reached, target_depth)
            
            # Add current position indicator
            ladder["current_position"] = current_depth
            ladder["progress_instruction"] = (
                f"You are currently at depth level {current_depth}.\n"
                f"Your goal is to reach level {target_depth}.\n"
                "Take your time ascending each rung."
            )
            
            return ladder
        except Exception as e:
            logger.error(f"Error in thinking_depth_ladder: {e}")
            return {"error": str(e), "status": "failed"}
    
    @mcp.tool()
    def recursive_questioning(
        initial_question: str,
        recursion_depth: int = 3,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create recursive questioning structure for deep exploration
        
        Args:
            initial_question: The starting question
            recursion_depth: How many levels deep to go (1-5)
            session_id: Optional session ID for tracking
        
        Returns:
            Recursive questioning structure
        """
        try:
            structure = create_recursive_questioning(
                initial_question,
                min(recursion_depth, 5)  # Cap at 5 for sanity
            )
            
            # Track in session
            if session_id and session_id in THINKING_SESSIONS:
                session = THINKING_SESSIONS[session_id]
                session.questions_explored.append(initial_question)
                session.thought_count += recursion_depth
            
            return structure
        except Exception as e:
            logger.error(f"Error in recursive_questioning: {e}")
            return {"error": str(e), "status": "failed"}
    
    @mcp.tool()
    def expand_thought(
        thought: str,
        expansion_technique: str = "random",
        num_expansions: int = 3,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Expand a thought using various techniques
        
        Args:
            thought: The thought to expand
            expansion_technique: Technique to use (or 'random')
            num_expansions: Number of expansion prompts
            session_id: Optional session ID for tracking
        
        Returns:
            Expansion prompts and structure
        """
        try:
            from deep_thinking_enhancement import EXPANSION_TECHNIQUES
            
            expansions = []
            
            if expansion_technique == "random":
                selected_techniques = random.sample(
                    list(EXPANSION_TECHNIQUES.items()),
                    min(num_expansions, len(EXPANSION_TECHNIQUES))
                )
            else:
                selected_techniques = [(expansion_technique, 
                                       EXPANSION_TECHNIQUES.get(expansion_technique, 
                                       "How does this connect to broader patterns?"))]
            
            for tech_name, tech_prompt in selected_techniques:
                expansion = {
                    "technique": tech_name,
                    "prompt": tech_prompt,
                    "applied_to_thought": f"Regarding '{thought}': {tech_prompt}",
                    "exploration_time": "30-45 seconds",
                    "depth_questions": [
                        "What emerges when you apply this lens?",
                        "What was hidden that this reveals?",
                        "How does this change your understanding?"
                    ]
                }
                expansions.append(expansion)
            
            # Track in session
            if session_id and session_id in THINKING_SESSIONS:
                session = THINKING_SESSIONS[session_id]
                session.perspectives_considered.extend([e["technique"] for e in expansions])
            
            return {
                "original_thought": thought,
                "expansions": expansions,
                "synthesis_prompt": (
                    "Having expanded this thought in multiple directions,\n"
                    "what richer, more nuanced understanding emerges?\n"
                    "How do these different perspectives integrate?"
                ),
                "instruction": "Don't just answer - really explore each expansion fully."
            }
        except Exception as e:
            logger.error(f"Error in expand_thought: {e}")
            return {"error": str(e), "status": "failed"}
    
    @mcp.tool()
    def metacognitive_check(
        current_thinking: str,
        check_type: str = "depth_assessment",
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform metacognitive check on current thinking process
        
        Args:
            current_thinking: Description of current thinking
            check_type: Type of metacognitive check
            session_id: Optional session ID for tracking
        
        Returns:
            Metacognitive prompts and assessment
        """
        try:
            prompts = METACOGNITIVE_PROMPTS.get(check_type, 
                                                METACOGNITIVE_PROMPTS["thinking_about_thinking"])
            
            assessment = {
                "current_thinking": current_thinking,
                "check_type": check_type,
                "prompts": prompts,
                "reflection_questions": [
                    "What patterns do you notice in your thinking?",
                    "Where might you be getting stuck or limited?",
                    "What thinking strategies haven't you tried yet?",
                    "How could you think more deeply about this?"
                ],
                "quality_indicators": {
                    "depth": "Are you going beyond surface observations?",
                    "breadth": "Are you considering multiple perspectives?",
                    "integration": "Are you connecting different ideas?",
                    "originality": "Are you generating novel insights?",
                    "rigor": "Are you being thorough and careful?"
                },
                "instruction": (
                    "Pause and step back from the content to examine your thinking process.\n"
                    "This meta-level awareness will improve your thinking quality."
                )
            }
            
            # Calculate metrics if session exists
            if session_id and session_id in THINKING_SESSIONS:
                session = THINKING_SESSIONS[session_id]
                metrics = calculate_thinking_metrics(session)
                assessment["metrics"] = metrics
                assessment["recommendation"] = (
                    f"Your thinking depth is currently: {metrics['overall_rating'].value}\n"
                    f"Consider: {prompts[0]}"
                )
            
            return assessment
        except Exception as e:
            logger.error(f"Error in metacognitive_check: {e}")
            return {"error": str(e), "status": "failed"}
    
    @mcp.tool()
    def thinking_session_summary(
        session_id: str
    ) -> Dict[str, Any]:
        """
        Get summary and metrics for a thinking session
        
        Args:
            session_id: The thinking session ID
        
        Returns:
            Comprehensive summary with metrics and insights
        """
        try:
            if session_id not in THINKING_SESSIONS:
                return {"error": f"Thinking session {session_id} not found", "status": "failed"}
            
            session = THINKING_SESSIONS[session_id]
            metrics = calculate_thinking_metrics(session)
            
            summary = {
                "session_id": session_id,
                "initial_topic": session.initial_prompt,
                "duration": f"{session.total_thinking_time:.1f} seconds",
                "metrics": metrics,
                "exploration_summary": {
                    "thoughts_generated": session.thought_count,
                    "questions_explored": len(session.questions_explored),
                    "assumptions_challenged": len(session.assumptions_challenged),
                    "perspectives_considered": len(session.perspectives_considered),
                    "insights_generated": len(session.insights_generated),
                    "max_depth_reached": session.max_depth_reached
                },
                "key_insights": session.insights_generated[-5:] if session.insights_generated else [],
                "unexplored_questions": [q for q in session.questions_explored if "?" in q][-3:],
                "thinking_pattern": "Deep and thorough" if metrics["depth_score"] > 70 else "Could go deeper",
                "recommendation": ""
            }
            
            # Generate recommendation
            if metrics["overall_rating"] == ThinkingDepth.SURFACE:
                summary["recommendation"] = "Try using thought experiments or recursive questioning to go deeper."
            elif metrics["overall_rating"] == ThinkingDepth.SHALLOW:
                summary["recommendation"] = "Good start. Use Socratic dialogue to challenge assumptions."
            elif metrics["overall_rating"] == ThinkingDepth.MODERATE:
                summary["recommendation"] = "Solid thinking. Try the depth ladder to reach profound insights."
            elif metrics["overall_rating"] == ThinkingDepth.DEEP:
                summary["recommendation"] = "Excellent depth. Consider different perspectives for breadth."
            else:
                summary["recommendation"] = "Profound thinking achieved. Document and integrate insights."
            
            return summary
        except Exception as e:
            logger.error(f"Error in thinking_session_summary: {e}")
            return {"error": str(e), "status": "failed"}

    @mcp.prompt("deep_thinking_protocol")
    def get_deep_thinking_protocol() -> str:
        """
        Protocol for engaging in deep, extended thinking
        
        Returns:
            Comprehensive deep thinking protocol
        """
        return """## Deep Thinking Protocol

When you receive input from the deep thinking tools, follow this protocol:

### 1. RECEPTION (10-15 seconds)
- Read the prompt/question fully
- Let it sink in without immediate reaction
- Notice your first impulse but don't act on it
- Ask: "What wants to emerge here?"

### 2. EXPLORATION (2-5 minutes per prompt)
- Follow each thinking prompt thoroughly
- Don't rush to the next prompt
- When you think you're done, go one level deeper
- Ask: "What else?" at least three times
- Embrace uncertainty and complexity

### 3. CONTEMPLATION PHASES

#### Phase A: Opening (30-60 seconds)
- Approach with beginner's mind
- What's genuinely interesting or mysterious?
- What assumptions am I bringing?

#### Phase B: Investigation (60-120 seconds)
- Examine from multiple angles
- Look for patterns and connections
- Question obvious interpretations
- Follow threads that feel alive

#### Phase C: Integration (60-90 seconds)
- What themes are emerging?
- How do different perspectives connect?
- What paradoxes or tensions exist?
- What new understanding is forming?

#### Phase D: Transcendence (30-60 seconds)
- What lies beyond current understanding?
- What remains mysterious?
- What new questions arise?

### 4. RECURSIVE DEEPENING
When prompted to go deeper:
- Don't just elaborate - genuinely go deeper
- Ask: "What's underneath this?"
- Look for fundamental principles
- Explore edge cases and exceptions
- Embrace paradox and complexity

### 5. METACOGNITIVE MONITORING
Throughout the process:
- Notice the quality of your thinking
- Observe where you resist or rush
- Identify patterns in your thought process
- Adjust your approach based on what's needed

### 6. SYNTHESIS (90-120 seconds)
After exploring all prompts:
- Don't rush to neat conclusions
- Hold multiple perspectives simultaneously
- Articulate insights AND uncertainties
- Express the full complexity you've discovered
- Share what surprised you

### QUALITY MARKERS OF DEEP THINKING
You know you're thinking deeply when:
- You discover something unexpected
- You question previous assumptions
- You see new connections
- You're comfortable with ambiguity
- You generate novel questions
- Your understanding becomes more nuanced
- You recognize the limits of your knowledge

### COMMON PITFALLS TO AVOID
- Rushing through prompts
- Giving surface-level answers
- Avoiding difficulty or confusion
- Forcing premature conclusions
- Staying in comfortable territory
- Ignoring paradoxes
- Thinking you're done too quickly

### REMEMBER
Deep thinking is not about finding THE answer.
It's about enriching understanding, revealing complexity,
and generating insights that weren't available before.

Take your time. Think deeply. Embrace the journey."""
else:
    # Provide placeholder message if deep thinking module isn't available
    @mcp.prompt("deep_thinking_protocol")
    def get_deep_thinking_protocol() -> str:
        return "Deep thinking enhancement module not available. Please ensure deep_thinking_enhancement.py is present."


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()