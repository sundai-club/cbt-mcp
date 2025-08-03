#!/usr/bin/env python3
"""
Example usage of the CBT Agent Helper MCP Tool
Demonstrates how to use each tool with sample scenarios
"""

import json


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print('='*60)


def print_example(example_num, title):
    """Print a formatted example header"""
    print(f"\n--- Example {example_num}: {title} ---")


def demonstrate_cbt_tool():
    """Demonstrate all CBT tool capabilities"""
    
    print_section("CBT Agent Helper Demo")
    
    # Example 1: Analyze stuck pattern
    print_example(1, "Analyzing stuck pattern in error loop")
    
    error_loop_scenario = {
        "current_situation": "Trying to connect to database but getting connection timeouts",
        "stuck_pattern": "error_loop - getting same timeout error repeatedly",
        "attempted_solutions": [
            "Increased timeout value",
            "Restarted database service",
            "Checked connection string"
        ],
        "error_messages": [
            "Error: Connection timeout after 30000ms",
            "Error: ECONNREFUSED 127.0.0.1:5432"
        ]
    }
    
    print(f"Input: {json.dumps(error_loop_scenario, indent=2)}")
    print("\nSuggested intervention would include:")
    print("✓ Problem-solving strategy")
    print("✓ Focus on first error only")
    print("✓ Try minimal reproduction")
    print("✓ Check assumptions about database state")
    print("✓ Reframed perspective: 'opportunity to learn about the system'")
    
    # Example 2: Reframe catastrophic thinking
    print_example(2, "Reframing catastrophic thoughts")
    
    catastrophic_thought = {
        "negative_thought": "If I can't solve this bug, the entire project will fail and users will abandon the product",
        "context": "Working on a non-critical UI bug for 2 hours"
    }
    
    print(f"Input: {json.dumps(catastrophic_thought, indent=2)}")
    print("\nReframes would include:")
    print("✓ Evidence-based: What evidence supports total project failure from one bug?")
    print("✓ Probability: How likely is complete user abandonment (realistically 0.01%)?")
    print("✓ Best-friend: What would you tell another agent in this situation?")
    print("✓ Growth mindset: 'This is challenging, and I'm learning how to handle it'")
    
    # Example 3: Create action plan for overwhelmed agent
    print_example(3, "Creating action plan for overwhelmed agent")
    
    overwhelmed_scenario = {
        "goal": "Implement user authentication system",
        "obstacles": [
            "complexity",
            "multiple auth providers",
            "security concerns",
            "perfect solution"
        ],
        "time_pressure": True
    }
    
    print(f"Input: {json.dumps(overwhelmed_scenario, indent=2)}")
    print("\nAction plan would include:")
    print("✓ Mindset: Done is better than perfect")
    print("✓ Step 1: Define minimum viable auth (just email/password)")
    print("✓ Step 2: List what you know (have user table, know bcrypt)")
    print("✓ Step 3: Implement basic login endpoint")
    print("✓ Backup: Ship basic version, add OAuth later")
    print("✓ Success criteria: Any forward movement is success")
    
    # Example 4: Wellness check
    print_example(4, "Wellness check for long-running task")
    
    wellness_scenario = {
        "current_task": "Refactoring legacy codebase",
        "time_on_task": 45,
        "progress_made": False
    }
    
    print(f"Input: {json.dumps(wellness_scenario, indent=2)}")
    print("\nAssessment would show:")
    print("✓ Status: Potential cognitive fatigue or stuck pattern")
    print("✓ Cognitive load: High")
    print("✓ Recommendations:")
    print("  • Take a 2-minute reset break")
    print("  • Verbalize the problem out loud")
    print("  • Check if you're solving the right problem")
    print("✓ Suggested intervention: analyze_stuck_pattern")
    
    # Example 5: Frustration regulation
    print_example(5, "Regulating high frustration")
    
    frustration_scenario = {
        "frustration_level": 8,
        "trigger": "Documentation is outdated and examples don't work"
    }
    
    print(f"Input: {json.dumps(frustration_scenario, indent=2)}")
    print("\nRegulation techniques would include:")
    print("✓ Validation: Level 8/10 frustration is acknowledged")
    print("✓ Grounding exercises:")
    print("  • List 3 things working correctly now")
    print("  • State 3 facts about current environment")
    print("  • Name 3 available resources")
    print("✓ Perspective shifts:")
    print("  • This frustration means you care about quality")
    print("  • It might signal need for different approach")
    print("✓ Coping statements:")
    print("  • 'This is difficult, not impossible'")
    print("  • 'I can handle this one step at a time'")
    
    # Example 6: Using resources
    print_example(6, "Accessing CBT resources")
    
    print("\nAvailable resources:")
    print("✓ cbt_techniques_guide:")
    print("  • 5 core CBT strategies with prompts")
    print("  • 5 common cognitive distortions")
    print("  • Quick intervention techniques")
    print("\n✓ agent_state_patterns:")
    print("  • 6 common agent states")
    print("  • Signs to watch for")
    print("  • Targeted interventions")
    
    # Example 7: Self-reflection prompt
    print_example(7, "Self-reflection protocol")
    
    print("\nSelf-reflection steps:")
    print("1. PAUSE - Stop and acknowledge state")
    print("2. ASSESS - What's blocking? What's been tried?")
    print("3. REFRAME - Is there another way to see this?")
    print("4. ACT - Choose one small concrete action")
    print("5. LEARN - What worked? What to try differently?")
    
    print_section("Demo Summary")
    print("\nThe CBT Agent Helper provides:")
    print("✅ Pattern analysis for stuck agents")
    print("✅ Cognitive reframing for negative thoughts")
    print("✅ Action plans to overcome paralysis")
    print("✅ Emotional regulation techniques")
    print("✅ Wellness monitoring and interventions")
    print("✅ Reference guides and self-reflection protocols")
    
    print("\n💡 Key Philosophy: Progress > Perfection, Learning > Failing")
    print("\n🚀 Ready to help AI agents overcome obstacles and maintain resilience!")


if __name__ == "__main__":
    demonstrate_cbt_tool()