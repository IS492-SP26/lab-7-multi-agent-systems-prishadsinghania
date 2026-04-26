"""
Exercise 4 (AutoGen): Marketing Campaign Planning
==================================================

This is a separate AutoGen implementation for the same custom problem
used in the CrewAI Exercise 4 workflow (marketing campaign domain).
"""

import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import autogen
except ImportError:
    print("ERROR: pyautogen is not installed in this Python environment.")
    print("Use the same Python where requirements were installed.")
    raise SystemExit(1)

# Import shared config from project root
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared_config import Config


class GroupChatMarketingCampaign:
    """AutoGen GroupChat workflow for marketing campaign planning."""

    def __init__(self):
        if not Config.validate():
            print("ERROR: Configuration validation failed.")
            raise SystemExit(1)

        self.config_list = [
            {
                "model": Config.OPENAI_MODEL,
                "api_key": Config.API_KEY,
                "base_url": Config.API_BASE,
            }
        ]
        self.llm_config = {
            "config_list": self.config_list,
            "temperature": Config.AGENT_TEMPERATURE,
            "timeout": Config.AGENT_TIMEOUT,
            "max_tokens": Config.AGENT_MAX_TOKENS,
        }
        self._create_agents()
        self._setup_groupchat()

    def _create_agents(self):
        self.user_proxy = autogen.UserProxyAgent(
            name="MarketingManager",
            system_message="You initiate and coordinate a campaign planning discussion.",
            human_input_mode="NEVER",
            code_execution_config=False,
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
        )

        self.audience_agent = autogen.AssistantAgent(
            name="AudienceAgent",
            llm_config=self.llm_config,
            system_message=(
                "You are an audience researcher. Start by identifying 3 high-value segments for "
                "NoteFlow AI (students, professionals, researchers), with pain points and messaging."
                " Keep it concise and invite ChannelAgent next."
            ),
        )

        self.channel_agent = autogen.AssistantAgent(
            name="ChannelAgent",
            llm_config=self.llm_config,
            system_message=(
                "You are a channel strategist. Based on audience findings, recommend channel mix, "
                "message-channel fit, and week-1 test plan. Invite BudgetAgent next."
            ),
        )

        self.budget_agent = autogen.AssistantAgent(
            name="BudgetAgent",
            llm_config=self.llm_config,
            system_message=(
                "You are a budget planner. Propose a 4-week budget by category, plus best-case and "
                "constrained scenarios. Invite ExecutionAgent next."
            ),
        )

        self.execution_agent = autogen.AssistantAgent(
            name="ExecutionAgent",
            llm_config=self.llm_config,
            system_message=(
                "You are a campaign execution lead. Synthesize prior inputs into a 4-week launch plan "
                "with weekly milestones, KPI targets, ownership, risks, and mitigations. End with TERMINATE."
            ),
        )

    def _setup_groupchat(self):
        self.groupchat = autogen.GroupChat(
            agents=[
                self.user_proxy,
                self.audience_agent,
                self.channel_agent,
                self.budget_agent,
                self.execution_agent,
            ],
            messages=[],
            max_round=10,
            speaker_selection_method="auto",
            allow_repeat_speaker=False,
            send_introductions=True,
        )

        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config=self.llm_config,
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
        )

    def run(self):
        print("=" * 80)
        print("AUTOGEN GROUPCHAT - EXERCISE 4 MARKETING CAMPAIGN")
        print("=" * 80)
        print(f"Model: {Config.OPENAI_MODEL}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        initial_message = (
            "Team, create a 4-week marketing launch plan for NoteFlow AI.\n"
            "1) AudienceAgent: identify top segments and messaging\n"
            "2) ChannelAgent: recommend channels and tests\n"
            "3) BudgetAgent: provide budget and scenarios\n"
            "4) ExecutionAgent: provide final integrated launch plan\n\n"
            "AudienceAgent, please start."
        )

        chat_result = self.user_proxy.initiate_chat(
            self.manager,
            message=initial_message,
            summary_method="reflection_with_llm",
            summary_args={
                "summary_prompt": (
                    "Summarize the final marketing launch plan, including audience segments, "
                    "channel strategy, budget allocations, KPIs, and risks."
                )
            },
        )

        output_file = self._save_results(chat_result)
        print(f"Saved output to: {output_file}")

    def _save_results(self, chat_result):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path(__file__).parent / f"autogen_marketing_output_{timestamp}.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("AUTOGEN GROUPCHAT - EXERCISE 4 MARKETING CAMPAIGN OUTPUT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Model: {Config.OPENAI_MODEL}\n")
            f.write(f"Turns: {len(self.groupchat.messages)}\n\n")
            f.write("CONVERSATION:\n")
            f.write("-" * 80 + "\n")
            for idx, msg in enumerate(self.groupchat.messages, 1):
                speaker = msg.get("name", "Unknown")
                content = msg.get("content", "")
                f.write(f"--- Turn {idx}: {speaker} ---\n{content}\n\n")
            if chat_result and getattr(chat_result, "summary", None):
                f.write("-" * 80 + "\n")
                f.write("SUMMARY:\n")
                f.write(str(chat_result.summary))
                f.write("\n")
        return output_file.name


if __name__ == "__main__":
    workflow = GroupChatMarketingCampaign()
    workflow.run()
