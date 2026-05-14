import os
from crewai import Agent, Task, Crew, Process, LLM


def run_crew(topic: str) -> str:
    llm = LLM(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"])

    # --- Agents ---
    researcher = Agent(
        role="Research Analyst",
        goal="Find accurate information about the given topic",
        backstory="You are an expert researcher who finds and summarizes facts.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    writer = Agent(
        role="Content Writer",
        goal="Write a clear, engaging summary from the research",
        backstory="You turn complex research into easy-to-read content.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # --- Tasks ---
    research_task = Task(
        description=f"Research '{topic}'. Find key facts and important points.",
        expected_output=f"A bullet-point list of at least 5 key facts about '{topic}'.",
        agent=researcher,
    )

    writing_task = Task(
        description=f"Write a 3-4 paragraph summary about '{topic}' using the research.",
        expected_output=f"A well-written, easy-to-read summary about '{topic}'.",
        agent=writer,
        context=[research_task],
    )

    # --- Run ---
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=True,
    )

    return str(crew.kickoff())
