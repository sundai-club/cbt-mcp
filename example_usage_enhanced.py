#!/usr/bin/env python3
"""
Enhanced example usage of the CBT Agent Helper MCP Server
Demonstrates all new features including sessions, validation, and enhanced CBT techniques
"""

import asyncio
import json
from typing import Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_cbt_tools():
    """Test the enhanced CBT tools with session management"""
    
    # Connect to the MCP server
    async with stdio_client(StdioServerParameters(
        command="python",
        args=["cbt_mcp_server.py"]
    )) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the session
            await session.initialize()
            
            print("=" * 60)
            print("CBT AGENT HELPER - ENHANCED DEMONSTRATION")
            print("=" * 60)
            
            # Test 1: Start a new session
            print("\n1. STARTING A NEW SESSION")
            print("-" * 40)
            result = await session.call_tool(
                "start_session",
                arguments={
                    "session_id": "demo_session_001",
                    "initial_problem": "I'm stuck in an infinite loop trying to optimize code that's already working"
                }
            )
            print(f"Session started: {json.dumps(result, indent=2)}")
            session_id = result.get("session_id")
            
            # Test 2: Analyze stuck pattern with session tracking
            print("\n2. ANALYZING STUCK PATTERN (Perfectionism)")
            print("-" * 40)
            result = await session.call_tool(
                "analyze_stuck_pattern",
                arguments={
                    "current_situation": "Refactoring working code for the 5th time",
                    "stuck_pattern": "perfectionist loop - code works but I keep optimizing",
                    "attempted_solutions": [
                        "Rewrote the function 3 times",
                        "Added more type hints",
                        "Tried different design patterns",
                        "Benchmarked performance (already fast enough)"
                    ],
                    "error_messages": [],
                    "session_id": session_id
                }
            )
            print(f"Analysis: {json.dumps(result, indent=2)}")
            
            # Test 3: Reframe catastrophic thinking
            print("\n3. REFRAMING CATASTROPHIC THOUGHTS")
            print("-" * 40)
            result = await session.call_tool(
                "reframe_thought",
                arguments={
                    "negative_thought": "If this code isn't perfect, the entire project will fail and everyone will think I'm incompetent",
                    "context": "Working on a feature that's already functional",
                    "session_id": session_id
                }
            )
            print(f"Reframed thought: {json.dumps(result, indent=2)}")
            
            # Test 4: Create action plan to break paralysis
            print("\n4. CREATING ACTION PLAN")
            print("-" * 40)
            result = await session.call_tool(
                "create_action_plan",
                arguments={
                    "goal": "Ship the feature and move on to the next task",
                    "obstacles": [
                        "Fear of criticism",
                        "Perfectionist tendencies",
                        "Uncertainty about edge cases"
                    ],
                    "time_pressure": True,
                    "session_id": session_id
                }
            )
            print(f"Action plan: {json.dumps(result, indent=2)}")
            
            # Test 5: Regulate high frustration
            print("\n5. REGULATING FRUSTRATION (High Level)")
            print("-" * 40)
            result = await session.call_tool(
                "regulate_frustration",
                arguments={
                    "frustration_level": 8,
                    "trigger": "Can't get the code to be 'perfect' despite it working fine",
                    "session_id": session_id
                }
            )
            print(f"Frustration regulation: {json.dumps(result, indent=2)}")
            
            # Test 6: Wellness check after extended work
            print("\n6. WELLNESS CHECK")
            print("-" * 40)
            result = await session.call_tool(
                "wellness_check",
                arguments={
                    "current_task": "Still optimizing the same function",
                    "time_on_task": 90,
                    "progress_made": False,
                    "session_id": session_id
                }
            )
            print(f"Wellness assessment: {json.dumps(result, indent=2)}")
            
            # Test 7: Get session summary
            print("\n7. SESSION SUMMARY")
            print("-" * 40)
            result = await session.call_tool(
                "get_session_summary",
                arguments={
                    "session_id": session_id
                }
            )
            print(f"Session summary: {json.dumps(result, indent=2)}")
            
            # Test 8: Error handling - invalid input
            print("\n8. TESTING ERROR HANDLING")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "regulate_frustration",
                    arguments={
                        "frustration_level": 15,  # Invalid: > 10
                        "trigger": "",  # Invalid: empty
                        "session_id": session_id
                    }
                )
                print(f"Result: {json.dumps(result, indent=2)}")
            except Exception as e:
                print(f"Error caught (expected): {e}")
            
            # Test 9: Complex scenario - Error loop with escalating frustration
            print("\n9. COMPLEX SCENARIO: ERROR LOOP WITH ESCALATION")
            print("-" * 40)
            
            # Simulate escalating frustration
            for i, level in enumerate([3, 5, 7, 9], 1):
                print(f"\n  Iteration {i} - Frustration Level: {level}")
                result = await session.call_tool(
                    "regulate_frustration",
                    arguments={
                        "frustration_level": level,
                        "trigger": f"Same error appearing for the {i}th time",
                        "session_id": session_id
                    }
                )
                if "immediate_relief" in result:
                    print(f"  Immediate relief suggested: {result['immediate_relief'][0]}")
                if "recommended_action" in result:
                    print(f"  Recommended: {result['recommended_action']}")
            
            # Test 10: Get resources
            print("\n10. ACCESSING CBT RESOURCES")
            print("-" * 40)
            
            # Get CBT techniques guide
            resources = await session.list_resources()
            for resource in resources:
                if "techniques" in resource.uri:
                    result = await session.read_resource(resource.uri)
                    print(f"CBT Techniques Available: {len(result['techniques'])}")
                    for technique in result['techniques'][:3]:
                        print(f"  - {technique['name']}: {technique['description']}")
            
            # Test 11: Get prompts for self-help
            print("\n11. SELF-HELP PROMPTS")
            print("-" * 40)
            
            prompts = await session.list_prompts()
            for prompt in prompts:
                if prompt.name == "quick_help":
                    result = await session.get_prompt(prompt.name)
                    print("Quick Help Protocol:")
                    print(result['messages'][0]['content'][:500] + "...")
            
            print("\n" + "=" * 60)
            print("DEMONSTRATION COMPLETE")
            print("=" * 60)
            print("\nKey Improvements Demonstrated:")
            print("✓ Session management for tracking progress")
            print("✓ Enhanced error handling and validation")
            print("✓ More CBT techniques (Socratic questioning, ACT, etc.)")
            print("✓ Frustration escalation detection")
            print("✓ Wellness scoring system")
            print("✓ Cognitive distortion detection")
            print("✓ Emergency quick-help protocols")
            print("✓ Session summaries with insights")

def main():
    """Run the enhanced demonstration"""
    print("\nStarting Enhanced CBT Agent Helper Demo...")
    print("This demonstrates all new features and improvements\n")
    
    try:
        asyncio.run(test_cbt_tools())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError running demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()