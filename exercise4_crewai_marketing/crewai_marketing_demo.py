"""
Exercise 4 (CrewAI only): Marketing Campaign Planning
======================================================

This is a brand-new workflow in a new folder.
It does NOT modify the original autogen/ or crewai/ demos.

Domain:
- Marketing campaign for a new AI note-taking app.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

from crewai import Agent, Task, Crew
from crewai.tools import tool

# Import shared configuration from repo root
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared_config import Config, validate_config


@tool
def research_audience(product_name: str) -> str:
    """Return audience research insights for the product."""
    return (
        f"Audience research for {product_name}:\n"
        "- Primary audience: college students and early-career professionals\n"
        "- Top pain points: scattered notes, missed deadlines, poor revision workflows\n"
        "- Purchase triggers: clarity, productivity gains, affordable pricing\n"
        "- Preferred messaging: 'study smarter', 'capture ideas instantly', 'organized in one place'\n"
    )


@tool
def propose_channels(target_segment: str) -> str:
    """Return channel recommendations with rationale and budget ranges."""
    return (
        f"Channel strategy for {target_segment}:\n"
        "- TikTok/Reels: strong reach for students, short demos, $1.5k-$3k pilot\n"
        "- YouTube creators: product walkthroughs and productivity reviews, $2k-$5k\n"
        "- Reddit communities: trust-building and feedback loops, $300-$800 promoted posts\n"
        "- Campus ambassadors: high conversion in local clusters, $1k-$2k starter program\n"
    )


@tool
def estimate_campaign_budget(campaign_scope: str) -> str:
    """Return budget assumptions for a 4-week launch campaign."""
    return (
        f"4-week campaign budget model for {campaign_scope} (USD):\n"
        "- Content production: $2,000\n"
        "- Paid social ads: $4,500\n"
        "- Creator partnerships: $3,500\n"
        "- Community + campus program: $1,500\n"
        "- Analytics + tooling: $800\n"
        "- Contingency (10%): $1,230\n"
        "Estimated total: $13,530\n"
    )


def create_audience_agent() -> Agent:
    return Agent(
        role="Audience Research Specialist",
        goal="Identify the highest-value audience segments and message angles.",
        backstory=(
            "You are a market researcher who specializes in early-stage product launches. "
            "You focus on behavior, intent, and clear segment priorities."
        ),
        tools=[research_audience],
        verbose=True,
        allow_delegation=False,
    )


def create_channel_agent() -> Agent:
    return Agent(
        role="Channel Strategy Specialist",
        goal="Recommend the best marketing channels for each audience segment.",
        backstory=(
            "You are a growth strategist experienced with social, creator, and community channels. "
            "You optimize for practical launch outcomes, not vanity metrics."
        ),
        tools=[propose_channels],
        verbose=True,
        allow_delegation=False,
    )


def create_budget_agent() -> Agent:
    return Agent(
        role="Campaign Budget Planner",
        goal="Build a realistic campaign budget and tie spend to expected outcomes.",
        backstory=(
            "You are a finance-minded marketing planner. "
            "You produce clear, defensible budgets and tradeoff recommendations."
        ),
        tools=[estimate_campaign_budget],
        verbose=True,
        allow_delegation=False,
    )


def create_execution_agent() -> Agent:
    return Agent(
        role="Campaign Execution Lead",
        goal="Synthesize all inputs into a 4-week launch plan with weekly milestones.",
        backstory=(
            "You are a marketing program lead who turns strategy into execution. "
            "You prioritize clarity, sequence, and measurable outcomes."
        ),
        verbose=True,
        allow_delegation=False,
    )


def main(product_name: str = "NoteFlow AI", duration: str = "4 weeks"):
    print("=" * 80)
    print("Exercise 4 - CrewAI Marketing Campaign Demo")
    print("=" * 80)
    print(f"Product: {product_name}")
    print(f"Campaign Duration: {duration}")
    print()

    if not validate_config():
        print("Configuration invalid. Please set OPENAI_API_KEY in .env")
        raise SystemExit(1)

    os.environ["OPENAI_API_KEY"] = Config.API_KEY
    os.environ["OPENAI_API_BASE"] = Config.API_BASE
    if Config.USE_GROQ:
        os.environ["OPENAI_MODEL_NAME"] = Config.OPENAI_MODEL

    audience_agent = create_audience_agent()
    channel_agent = create_channel_agent()
    budget_agent = create_budget_agent()
    execution_agent = create_execution_agent()

    audience_task = Task(
        description=(
            f"Research the best audience for launching {product_name}. "
            "Provide top 3 segments, their pain points, and 2 message angles per segment."
        ),
        expected_output=(
            "A concise audience report with segment ranking, pain points, and message angles."
        ),
        agent=audience_agent,
    )

    channel_task = Task(
        description=(
            "Using the audience report, recommend channel mix and rationale for each segment. "
            "Include one low-cost test plan for week 1."
        ),
        expected_output="Channel mix strategy with priority channels, rationale, and week 1 tests.",
        agent=channel_agent,
    )

    budget_task = Task(
        description=(
            "Create a 4-week campaign budget split by channel and activities. "
            "Include a best-case and constrained-budget scenario."
        ),
        expected_output="A budget plan with totals, category split, and two scenario options.",
        agent=budget_agent,
    )

    execution_task = Task(
        description=(
            f"Create a complete {duration} marketing launch plan for {product_name}. "
            "Use prior task outputs to produce weekly milestones, KPIs, and risk mitigations."
        ),
        expected_output=(
            "Final launch plan with timeline, KPI targets, ownership notes, and risk mitigations."
        ),
        agent=execution_agent,
    )

    crew = Crew(
        agents=[audience_agent, channel_agent, budget_agent, execution_agent],
        tasks=[audience_task, channel_task, budget_task, execution_task],
        process="sequential",
        verbose=True,
    )

    result = crew.kickoff(inputs={"product_name": product_name, "duration": duration})
    print("\n" + "=" * 80)
    print("FINAL CAMPAIGN PLAN")
    print("=" * 80)
    print(result)

    output_path = Path(__file__).parent / "marketing_campaign_output.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("Exercise 4 - CrewAI Marketing Campaign Output\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now()}\n\n")
        f.write(str(result))
        f.write("\n")
    print(f"\nSaved output to: {output_path.name}")


if __name__ == "__main__":
    product = "NoteFlow AI"
    campaign_duration = "4 weeks"
    if len(sys.argv) > 1:
        product = sys.argv[1]
    if len(sys.argv) > 2:
        campaign_duration = sys.argv[2]
    main(product_name=product, duration=campaign_duration)
