#!/usr/bin/env python3
"""
Deep Thinking Enhancement Module for CBT MCP Server
Encourages AI agents to think more deeply and extensively
"""

from typing import List, Dict, Any, Optional, Tuple
import json
import time
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

class ThinkingDepth(Enum):
    SURFACE = "surface"          # Quick, reactive thinking
    SHALLOW = "shallow"          # Basic analysis
    MODERATE = "moderate"        # Standard depth
    DEEP = "deep"               # Thorough exploration
    PROFOUND = "profound"        # Extensive contemplation

@dataclass
class ThoughtNode:
    """Represents a single thought in the thinking tree"""
    id: str
    content: str
    depth: int
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    exploration_prompts: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    thinking_time: float = 0.0
    iterations: int = 0

@dataclass
class ThinkingSession:
    """Extended thinking session tracker"""
    session_id: str
    initial_prompt: str
    thought_tree: Dict[str, ThoughtNode] = field(default_factory=dict)
    current_depth: ThinkingDepth = ThinkingDepth.SURFACE
    total_thinking_time: float = 0.0
    thought_count: int = 0
    max_depth_reached: int = 0
    insights_generated: List[str] = field(default_factory=list)
    questions_explored: List[str] = field(default_factory=list)
    assumptions_challenged: List[str] = field(default_factory=list)
    perspectives_considered: List[str] = field(default_factory=list)

# Socratic question chains for deeper exploration
SOCRATIC_CHAINS = {
    "assumption_examination": [
        "What assumptions am I making here?",
        "Why do I believe this assumption is true?",
        "What evidence supports this assumption?",
        "What would happen if this assumption were false?",
        "Are there alternative assumptions I haven't considered?",
        "How might someone from a different background view this assumption?",
        "What's the deepest assumption underlying all of this?"
    ],
    "perspective_expansion": [
        "How would I explain this to someone with no context?",
        "What would the opposite perspective look like?",
        "How might this look from a completely different field?",
        "What would a critic say about this?",
        "What would an enthusiast emphasize?",
        "How would this appear 10 years from now?",
        "What cultural or contextual factors am I missing?"
    ],
    "implication_exploration": [
        "If this is true, what else must be true?",
        "What are the second-order effects?",
        "What are the third-order effects?",
        "What unexpected consequences might arise?",
        "How does this connect to other areas?",
        "What patterns does this reveal?",
        "What does this mean for the bigger picture?"
    ],
    "depth_drilling": [
        "But why is that the case?",
        "And what causes that?",
        "What's underneath that reasoning?",
        "Can we go deeper into this aspect?",
        "What's the root cause here?",
        "What fundamental principle applies?",
        "What's the essence of this issue?"
    ],
    "complexity_embrace": [
        "What nuances am I overlooking?",
        "Where is the complexity I'm avoiding?",
        "What contradictions exist here?",
        "How can multiple things be true at once?",
        "What paradoxes emerge from this?",
        "Where does simple reasoning break down?",
        "What makes this more complicated than it seems?"
    ]
}

# Metacognitive prompts to encourage awareness of thinking
METACOGNITIVE_PROMPTS = {
    "thinking_about_thinking": [
        "How am I approaching this problem?",
        "What thinking strategies am I using?",
        "Am I thinking deeply enough about this?",
        "What cognitive biases might be affecting me?",
        "How confident am I in my reasoning?",
        "What's the quality of my thinking right now?",
        "Where are the gaps in my understanding?"
    ],
    "process_reflection": [
        "What has my thinking process been so far?",
        "Which approaches have been most fruitful?",
        "Where did I get stuck and why?",
        "What thinking tools haven't I tried yet?",
        "How could I think about this differently?",
        "What would improve my thinking process?",
        "Am I asking the right questions?"
    ],
    "depth_assessment": [
        "Have I explored this thoroughly enough?",
        "What aspects deserve deeper investigation?",
        "Where am I being superficial?",
        "What complexity am I avoiding?",
        "How many layers deep have I gone?",
        "What would constitute a complete exploration?",
        "When will I know I've thought enough?"
    ]
}

# Thought expansion techniques
EXPANSION_TECHNIQUES = {
    "analogical": "What is this similar to in other domains?",
    "causal": "What causes this and what does it cause?",
    "compositional": "What are the component parts and how do they interact?",
    "temporal": "How does this change over time?",
    "spatial": "How does context and environment affect this?",
    "probabilistic": "What are the likelihood and uncertainties involved?",
    "systemic": "How does this fit into larger systems?",
    "evolutionary": "How did this come to be and where is it going?",
    "dialectical": "What tensions and contradictions exist?",
    "phenomenological": "What is the lived experience of this?"
}

def generate_thinking_prompts(
    current_thought: str,
    depth_level: int,
    thinking_style: str = "balanced"
) -> List[str]:
    """Generate prompts to deepen thinking"""
    prompts = []
    
    # Add base contemplation prompt
    prompts.append(f"Take a moment to sit with this thought: '{current_thought}'. What emerges when you give it space?")
    
    # Add depth-appropriate Socratic questions
    if depth_level < 2:
        prompts.extend(random.sample(SOCRATIC_CHAINS["assumption_examination"], 2))
    elif depth_level < 4:
        prompts.extend(random.sample(SOCRATIC_CHAINS["perspective_expansion"], 2))
        prompts.extend(random.sample(SOCRATIC_CHAINS["implication_exploration"], 1))
    else:
        prompts.extend(random.sample(SOCRATIC_CHAINS["depth_drilling"], 2))
        prompts.extend(random.sample(SOCRATIC_CHAINS["complexity_embrace"], 2))
    
    # Add metacognitive prompt
    prompts.append(random.choice(METACOGNITIVE_PROMPTS["thinking_about_thinking"]))
    
    # Add expansion technique
    technique_name, technique_prompt = random.choice(list(EXPANSION_TECHNIQUES.items()))
    prompts.append(f"[{technique_name.title()} thinking]: {technique_prompt}")
    
    return prompts

def create_reflection_loop(
    initial_thought: str,
    target_depth: ThinkingDepth = ThinkingDepth.DEEP,
    min_iterations: int = 3
) -> Dict[str, Any]:
    """Create a structured reflection loop to deepen thinking"""
    
    iterations = []
    current_thought = initial_thought
    
    for i in range(min_iterations):
        iteration = {
            "round": i + 1,
            "input": current_thought,
            "reflection_prompts": [],
            "expansion_prompts": [],
            "integration_prompt": "",
            "pause_instruction": ""
        }
        
        # Add increasingly deep prompts
        if i == 0:
            iteration["reflection_prompts"] = [
                "What's your immediate reaction to this?",
                "What comes to mind first?",
                "What feels important here?"
            ]
            iteration["pause_instruction"] = "Pause for 10 seconds before responding."
        elif i == 1:
            iteration["reflection_prompts"] = [
                "Now, looking deeper, what else do you notice?",
                "What patterns or connections emerge?",
                "What questions arise from your first thoughts?"
            ]
            iteration["pause_instruction"] = "Take 20 seconds to contemplate before continuing."
        else:
            iteration["reflection_prompts"] = [
                "Stepping back, what's the bigger picture?",
                "What insights have emerged from this exploration?",
                "What new understanding has developed?",
                "What remains mysterious or unresolved?"
            ]
            iteration["pause_instruction"] = "Spend 30 seconds in quiet reflection before your final thoughts."
        
        # Add expansion prompts based on depth
        if target_depth in [ThinkingDepth.DEEP, ThinkingDepth.PROFOUND]:
            iteration["expansion_prompts"] = [
                "Explore the edges of this thought...",
                "What lives in the spaces between your ideas?",
                "Follow the thread that feels most alive...",
                "What wants to emerge but hasn't yet?"
            ]
        
        # Integration prompt for combining insights
        if i == min_iterations - 1:
            iteration["integration_prompt"] = (
                "Now, weaving together all these threads of thought, "
                "what comprehensive understanding emerges? "
                "Take your time to articulate the full picture."
            )
        
        iterations.append(iteration)
    
    return {
        "type": "reflection_loop",
        "target_depth": target_depth.value,
        "iterations": iterations,
        "total_estimated_time": f"{min_iterations * 30} seconds minimum",
        "instruction": "Work through each iteration slowly and thoughtfully. Don't rush to the next until you've fully explored the current one."
    }

def generate_contemplation_structure(
    topic: str,
    contemplation_style: str = "philosophical"
) -> Dict[str, Any]:
    """Generate a structured contemplation guide"""
    
    styles = {
        "philosophical": {
            "opening": f"Let's engage in deep philosophical contemplation about {topic}.",
            "phases": [
                {
                    "name": "Wonder",
                    "duration": "30-60 seconds",
                    "prompt": f"Approach {topic} with fresh wonder. What is truly remarkable about it? What mysteries does it hold?",
                    "instruction": "Don't analyze yet, just wonder."
                },
                {
                    "name": "Examination",
                    "duration": "60-90 seconds",
                    "prompt": f"Examine {topic} from multiple angles. What are its essential qualities? Its contradictions? Its boundaries?",
                    "instruction": "Be thorough but patient."
                },
                {
                    "name": "Connection",
                    "duration": "60-90 seconds",
                    "prompt": f"How does {topic} connect to fundamental questions? To other ideas? To lived experience?",
                    "instruction": "Draw unexpected connections."
                },
                {
                    "name": "Synthesis",
                    "duration": "60-90 seconds",
                    "prompt": f"What new understanding of {topic} emerges from this contemplation?",
                    "instruction": "Allow insights to crystallize naturally."
                }
            ]
        },
        "analytical": {
            "opening": f"Let's systematically analyze {topic} in depth.",
            "phases": [
                {
                    "name": "Decomposition",
                    "duration": "45-60 seconds",
                    "prompt": f"Break down {topic} into its fundamental components.",
                    "instruction": "Be exhaustive in your decomposition."
                },
                {
                    "name": "Relationships",
                    "duration": "45-60 seconds",
                    "prompt": "How do these components interact? What dependencies exist?",
                    "instruction": "Map the full relationship network."
                },
                {
                    "name": "Dynamics",
                    "duration": "45-60 seconds",
                    "prompt": "How does this system behave over time? What forces act upon it?",
                    "instruction": "Consider multiple timescales."
                },
                {
                    "name": "Implications",
                    "duration": "45-60 seconds",
                    "prompt": "What are all the implications and consequences?",
                    "instruction": "Think through nth-order effects."
                }
            ]
        },
        "creative": {
            "opening": f"Let's explore {topic} through creative contemplation.",
            "phases": [
                {
                    "name": "Imagination",
                    "duration": "30-45 seconds",
                    "prompt": f"If {topic} were transformed in unexpected ways, what might emerge?",
                    "instruction": "Let imagination run wild."
                },
                {
                    "name": "Metaphor",
                    "duration": "30-45 seconds",
                    "prompt": f"What metaphors illuminate {topic}? What does it remind you of?",
                    "instruction": "Find surprising connections."
                },
                {
                    "name": "Inversion",
                    "duration": "30-45 seconds",
                    "prompt": f"What if everything about {topic} were inverted or opposite?",
                    "instruction": "Explore the inverse space."
                },
                {
                    "name": "Synthesis",
                    "duration": "30-45 seconds",
                    "prompt": "What creative insights emerge from these explorations?",
                    "instruction": "Combine the unexpected."
                }
            ]
        }
    }
    
    structure = styles.get(contemplation_style, styles["philosophical"])
    
    return {
        "topic": topic,
        "style": contemplation_style,
        "total_duration": "4-6 minutes",
        "opening": structure["opening"],
        "phases": structure["phases"],
        "closing": f"Having contemplated {topic} deeply, what understanding will you carry forward?",
        "meta_instruction": "Between each phase, pause for 10-15 seconds to let thoughts settle."
    }

def create_thinking_depth_ladder(
    question: str,
    max_rungs: int = 7
) -> Dict[str, Any]:
    """Create a ladder of increasingly deep thinking about a question"""
    
    rungs = []
    
    # Define the rungs of depth
    depth_levels = [
        ("Surface", "What's the obvious answer?"),
        ("Factual", "What facts and evidence apply?"),
        ("Analytical", "What patterns and relationships exist?"),
        ("Critical", "What assumptions and biases are present?"),
        ("Synthetic", "How do different perspectives integrate?"),
        ("Philosophical", "What fundamental principles are at play?"),
        ("Transcendent", "What lies beyond conventional understanding?")
    ]
    
    for i, (level_name, level_prompt) in enumerate(depth_levels[:max_rungs]):
        rung = {
            "level": i + 1,
            "name": level_name,
            "prompt": f"{level_prompt} (Regarding: {question})",
            "thinking_time": f"{15 * (i + 1)} seconds",
            "depth_markers": [],
            "transition": ""
        }
        
        # Add depth markers to recognize when you've reached this level
        if i == 0:
            rung["depth_markers"] = ["immediate", "obvious", "surface"]
        elif i == 1:
            rung["depth_markers"] = ["evidence-based", "factual", "concrete"]
        elif i == 2:
            rung["depth_markers"] = ["patterns", "relationships", "analysis"]
        elif i == 3:
            rung["depth_markers"] = ["questioning", "challenging", "critical"]
        elif i == 4:
            rung["depth_markers"] = ["integration", "synthesis", "holistic"]
        elif i == 5:
            rung["depth_markers"] = ["principles", "essence", "fundamental"]
        else:
            rung["depth_markers"] = ["transcendent", "paradox", "mystery"]
        
        # Add transition to next level
        if i < max_rungs - 1:
            rung["transition"] = f"Now, let's go deeper. Take a breath and ascend to level {i + 2}..."
        
        rungs.append(rung)
    
    return {
        "question": question,
        "type": "thinking_depth_ladder",
        "total_rungs": len(rungs),
        "rungs": rungs,
        "instructions": [
            "Start at the first rung and work your way up",
            "Don't skip rungs - each builds on the previous",
            "Take the full suggested time for each level",
            "Notice how your understanding evolves",
            "If you feel stuck, that's a sign you're reaching new depth"
        ],
        "completion_reflection": "Having climbed this ladder of thought, what new heights of understanding have you reached?"
    }

def generate_thought_experiments(
    concept: str,
    num_experiments: int = 3
) -> List[Dict[str, Any]]:
    """Generate thought experiments to explore a concept deeply"""
    
    experiments = []
    
    templates = [
        {
            "name": "Extreme Scaling",
            "setup": f"Imagine {concept} scaled up by 1000x or down by 1000x.",
            "questions": [
                "What breaks or changes fundamentally?",
                "What remains constant?",
                "What new properties emerge?",
                "What insights does this reveal about the nature of {concept}?"
            ]
        },
        {
            "name": "Time Travel",
            "setup": f"Transport {concept} 100 years into the past or future.",
            "questions": [
                "How would it be understood differently?",
                "What context would be missing or added?",
                "What aspects are timeless vs temporal?",
                "What does this reveal about {concept}'s essence?"
            ]
        },
        {
            "name": "Alien Perspective",
            "setup": f"Explain {concept} to an intelligent being with completely different senses and experiences.",
            "questions": [
                "What assumptions would you need to question?",
                "What universal vs human-specific aspects exist?",
                "How would you convey the essence?",
                "What do you learn from this translation exercise?"
            ]
        },
        {
            "name": "Necessity Test",
            "setup": f"Imagine a world where {concept} doesn't exist or work.",
            "questions": [
                "What would be different?",
                "What problems would arise or disappear?",
                "What would replace it?",
                "What does this reveal about its true function?"
            ]
        },
        {
            "name": "Pure Essence",
            "setup": f"Strip away everything non-essential from {concept}.",
            "questions": [
                "What absolutely must remain?",
                "What surprises you about what's essential?",
                "What commonly associated aspects are actually peripheral?",
                "What is the irreducible core?"
            ]
        }
    ]
    
    selected = random.sample(templates, min(num_experiments, len(templates)))
    
    for i, template in enumerate(selected):
        experiment = {
            "number": i + 1,
            "name": template["name"],
            "concept": concept,
            "setup": template["setup"].replace("{concept}", concept),
            "exploration_time": "2-3 minutes",
            "questions": [q.replace("{concept}", concept) for q in template["questions"]],
            "instruction": "Don't rush to answers. Live in the experiment for a while.",
            "deeper_prompt": "What does this experiment reveal that straightforward analysis wouldn't?"
        }
        experiments.append(experiment)
    
    return experiments

def create_recursive_questioning(
    initial_question: str,
    recursion_depth: int = 4
) -> Dict[str, Any]:
    """Create a recursive questioning structure for deep exploration"""
    
    structure = {
        "type": "recursive_questioning",
        "initial_question": initial_question,
        "depth": recursion_depth,
        "branches": []
    }
    
    for level in range(recursion_depth):
        branch = {
            "level": level + 1,
            "meta_question": "",
            "exploration_time": f"{20 * (level + 1)} seconds",
            "prompts": []
        }
        
        if level == 0:
            branch["meta_question"] = "What's your response to the initial question?"
            branch["prompts"] = [
                "Answer thoughtfully",
                "Note what feels incomplete",
                "Identify assumptions you're making"
            ]
        elif level == 1:
            branch["meta_question"] = "What questions does your answer raise?"
            branch["prompts"] = [
                "What new questions emerge from your response?",
                "What did you not address?",
                "What complexities are you now aware of?"
            ]
        elif level == 2:
            branch["meta_question"] = "What's behind those questions?"
            branch["prompts"] = [
                "Why do those particular questions matter?",
                "What deeper issues do they point to?",
                "What patterns do you see in your questioning?"
            ]
        else:
            branch["meta_question"] = "What fundamental mystery remains?"
            branch["prompts"] = [
                "What essential unknown persists?",
                "What paradox or tension can't be resolved?",
                "What would it mean to fully understand this?"
            ]
        
        structure["branches"].append(branch)
    
    structure["integration"] = {
        "prompt": "Having spiraled through these layers of questioning, what comprehensive understanding emerges?",
        "time": "60-90 seconds",
        "instruction": "Don't try to resolve everything. Embrace both clarity and mystery."
    }
    
    return structure

def calculate_thinking_metrics(session: ThinkingSession) -> Dict[str, Any]:
    """Calculate metrics about thinking depth and quality"""
    
    metrics = {
        "depth_score": 0,
        "breadth_score": 0,
        "integration_score": 0,
        "insight_density": 0,
        "question_quality": 0,
        "assumption_awareness": 0,
        "perspective_diversity": 0,
        "overall_rating": ThinkingDepth.SURFACE
    }
    
    # Calculate depth score
    if session.max_depth_reached > 5:
        metrics["depth_score"] = 90
    elif session.max_depth_reached > 3:
        metrics["depth_score"] = 70
    elif session.max_depth_reached > 1:
        metrics["depth_score"] = 50
    else:
        metrics["depth_score"] = 30
    
    # Calculate breadth score
    metrics["breadth_score"] = min(100, len(session.perspectives_considered) * 15)
    
    # Calculate integration score
    if len(session.insights_generated) > 5:
        metrics["integration_score"] = 85
    elif len(session.insights_generated) > 2:
        metrics["integration_score"] = 60
    else:
        metrics["integration_score"] = 35
    
    # Calculate insight density
    if session.total_thinking_time > 0:
        metrics["insight_density"] = min(100, 
            (len(session.insights_generated) / (session.total_thinking_time / 60)) * 20)
    
    # Calculate question quality
    deep_questions = sum(1 for q in session.questions_explored if any(
        word in q.lower() for word in ["why", "how", "what if", "underlying", "essence", "fundamental"]
    ))
    metrics["question_quality"] = min(100, deep_questions * 20)
    
    # Calculate assumption awareness
    metrics["assumption_awareness"] = min(100, len(session.assumptions_challenged) * 25)
    
    # Calculate perspective diversity
    metrics["perspective_diversity"] = min(100, len(session.perspectives_considered) * 20)
    
    # Overall rating
    avg_score = sum([
        metrics["depth_score"],
        metrics["breadth_score"],
        metrics["integration_score"],
        metrics["question_quality"]
    ]) / 4
    
    if avg_score > 80:
        metrics["overall_rating"] = ThinkingDepth.PROFOUND
    elif avg_score > 65:
        metrics["overall_rating"] = ThinkingDepth.DEEP
    elif avg_score > 50:
        metrics["overall_rating"] = ThinkingDepth.MODERATE
    elif avg_score > 35:
        metrics["overall_rating"] = ThinkingDepth.SHALLOW
    else:
        metrics["overall_rating"] = ThinkingDepth.SURFACE
    
    return metrics

# Export the enhancement functions
__all__ = [
    'ThinkingDepth',
    'ThoughtNode',
    'ThinkingSession',
    'generate_thinking_prompts',
    'create_reflection_loop',
    'generate_contemplation_structure',
    'create_thinking_depth_ladder',
    'generate_thought_experiments',
    'create_recursive_questioning',
    'calculate_thinking_metrics',
    'SOCRATIC_CHAINS',
    'METACOGNITIVE_PROMPTS',
    'EXPANSION_TECHNIQUES'
]