 # 🤖 Multi-Agent Systems Lab: Reflections

 ## 📚 Overview
 This document captures reflection answers comparing agent behavior and communication patterns across **AutoGen** and **CrewAI** for Lab 7.

 ---

## Behavior Across Agents

One agent’s changed behavior rippled through the system because later agents used the earlier agent’s output as context. In AutoGen, when the first research direction changed, the later responses also shifted: the analysis moved toward personalization, bias mitigation, HR integration, and AR/VR instead of the earlier focus on industry modules, soft skills, VR, and blockchain. This shows that downstream agents adapt to the information produced before them, even when their own prompts are not directly changed.  

## AutoGen Speaker Selection

In AutoGen, the GroupChatManager did not select speakers in the same order. In one run, the order followed the expected sequence: ProductManager → ResearchAgent → AnalysisAgent → BlueprintAgent → ReviewerAgent. In the later run, the manager selected AnalysisAgent immediately after ProductManager, even though the prompt asked ResearchAgent to begin. It then moved to BlueprintAgent, so the order changed and the conversation ended earlier.  

## CrewAI Budget Reflection

In CrewAI, the BudgetAgent’s calculations did reflect the FlightAgent’s priorities because the final budget used specific flight options from the flight research. For example, one output selected Icelandair direct at $420, while the later Iceland trip budget listed different flight options like PLAY Airlines at $349, Icelandair at $485, and Delta at $612. The budget totals changed based on which flight option was treated as budget, mid-range, or luxury.  

## Adding the Agent to AutoGen

The GroupChatManager did select the CostAnalyst after the product blueprint stage, which is the right general timing. However, the speaker labeling got messy: the “CostAnalyst” turn actually wrote blueprint-style content first, then asked CostAnalyst to proceed. The next turn, labeled “ReviewerAgent,” contained the actual cost analysis. So functionally, cost analysis happened at the right stage, but the agent selection/name alignment was not clean.  

The ReviewerAgent did incorporate cost data in the final recommendations. It prioritized the top ROI features: comprehensive feedback module, customizable interview questions, and soft skills assessment tool. It also recommended phased development and delaying lower-ROI/high-cost items like the integration hub and candidate portal.  

## Adding to CrewAI

Yes, but only partially.  

The BudgetAgent did account for some LocalExpert-style tips because the final budget includes local practical advice: using Flybus instead of taxis, public transportation, walking/biking, preparing meals, packing layers, and considering a Reykjavik City Card. These are not just raw cost totals; they reflect local travel/safety/cost-saving context.  

However, it did not deeply incorporate local customs or safety details into the budget. For example, it does not explicitly budget for winter safety needs, weather-related tour flexibility, or local etiquette/customs. So the LocalExpert influenced the budget, but the connection could be stronger.

## Exercise 4: Custom Problem (Marketing Campaign)

I chose the **marketing campaign** domain and ran **both frameworks** on the same problem: launching NoteFlow AI in 4 weeks.

For AutoGen, I used a GroupChat workflow with role-specific agents (`AudienceAgent`, `ChannelAgent`, `BudgetAgent`, `ExecutionAgent`) and a manager-directed kickoff prompt. The conversation flowed as intended: audience segmentation first, then channel strategy, then budget scenarios, then final execution plan. The output included a complete 4-week plan with milestones, KPI targets, ownership, risks/mitigations, and a total budget of **$30,000**.

For CrewAI, I used a sequential task workflow with equivalent marketing roles and task dependencies. The output was also a complete 4-week plan, but it was more structured as an execution report, with explicit objective blocks per week, category split percentages, and scenario totals (base budget **$13,530**, best-case **$16,255**, constrained **$11,455**).

For this domain, **CrewAI produced the more useful result overall** because the final plan was more operationally structured and easier to use directly for campaign execution (clear objective-by-week formatting and cleaner budget accounting). AutoGen was still valuable for showing collaborative reasoning and handoff quality, but CrewAI gave a tighter deliverable for implementation.