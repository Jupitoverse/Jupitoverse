# 2. LangChain, LangGraph, Agentic AI & MCP – Interview Guide

---

## 📋 Quick Reference

| Concept | One-Liner |
|---------|-----------|
| LangChain | Framework for chaining LLMs with tools, memory, and data (prompts, retrievers, agents) |
| LangGraph | Extension for multi-step, stateful, cyclic workflows (graphs with conditional edges) |
| Agent | LLM that decides which tools to call and in what order to accomplish a goal |
| Agentic AI | Systems where an agent plans, uses tools, and iterates (e.g. ReAct, tool use) |
| MCP | Model Context Protocol – standard way for AI apps to connect to external data/tools |

---

## 🔑 Core Concepts

### 1. LangChain

- Purpose: Compose LLM apps with reusable building blocks: prompts, chains, retrievers, agents, memory.
- Key abstractions: `LCEL` (LangChain Expression Language), `Runnable` interfaces, `ChatModel`, `Retriever`, `Tool`, `AgentExecutor`.
- Typical use: RAG (vector store + retriever + prompt + LLM), chatbots with memory, tool-calling agents.

```python
# Conceptual RAG with LangChain
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=retriever)
result = qa.invoke({"query": "What is the workaround for X?"})
```

### 2. LangGraph

- Purpose: Build stateful, multi-step workflows with branching and cycles (e.g. agent loops, human-in-the-loop).
- Concepts: Nodes (functions), edges (conditional or fixed), state schema, checkpoints (for persistence).
- When to use: When you need loops (agent retrying tools), conditional routing, or explicit state (e.g. plan → execute → reflect).

```python
# Conceptual: graph with conditional edge
from langgraph.graph import StateGraph, END

workflow = StateGraph(StateSchema)
workflow.add_node("plan", plan_node)
workflow.add_node("execute", execute_node)
workflow.add_conditional_edges("plan", route_by_intent)
workflow.add_edge("execute", END)
app = workflow.compile()
```

### 3. Agentic AI

- Definition: AI that uses tools, plans steps, and can iterate (e.g. search, code, DB, API) instead of one-shot generation.
- Patterns: ReAct (reason + act), tool-calling (function calling), plan-and-execute, multi-agent.
- Use cases: Research assistants, coding agents, support bots that query KB and ticketing systems.

### 4. MCP (Model Context Protocol)

- Purpose: Standard protocol so AI applications can discover and use external data sources and tools (files, DBs, APIs) in a uniform way.
- Benefits: One integration pattern; tools/servers can be developed once and used by multiple AI clients (e.g. Cursor, other IDEs/agents).
- Concepts: MCP servers expose resources (read-only) and tools (actions). Clients connect and call them; context is passed to the model.

---

## 💡 Top 15 Interview Q&A – LangChain / LangGraph / Agents / MCP

Q1: What is LangChain and when do you use it?
> "LangChain is a framework for building LLM applications with chains, retrievers, tools, and memory. I use it when I need RAG, tool-calling agents, or reusable prompt/retriever components without wiring everything from scratch."

Q2: What is LCEL?
> "LangChain Expression Language – a way to compose runnables with pipe (|) operators. For example: prompt | llm | output_parser. It makes chains streamable and batchable."

Q3: LangChain vs custom RAG?
> "LangChain gives built-in retriever/chain abstractions and many integrations (vector stores, LLMs). Custom RAG gives full control and fewer dependencies. I use LangChain for speed and consistency; custom when we need very specific behavior or minimal stack."

Q4: What is LangGraph and how is it different from LangChain?
> "LangGraph adds graph-based workflows with state and cycles. LangChain chains are mostly linear. LangGraph is for multi-step flows with branching, loops (e.g. agent retries), and explicit state – like a state machine for LLM workflows."

Q5: When would you choose LangGraph over a simple chain?
> "When I need conditional routing (e.g. by intent or tool result), loops (agent calling tools until done), human-in-the-loop, or persistent state across steps. Simple chains are for linear prompt → LLM → parse flows."

Q6: What is an agent in the context of LLMs?
> "An agent is an LLM that receives a goal, can call tools (search, API, DB, code), and decides the next action based on tool results. It iterates until the task is done or a limit is reached."

Q7: What is ReAct?
> "Reasoning + Acting: the model outputs a thought, then an action (e.g. which tool and with what input), gets the observation, and repeats. It combines reasoning traces with tool use in a loop."

Q8: How do you prevent agents from looping forever?
> "Set max_iterations or max_steps; use timeouts; design tools to return clear terminal states; add a node that detects 'task done' and routes to END; optionally add a budget for tool calls."

Q9: What is MCP and why is it useful?
> "Model Context Protocol – a standard for connecting AI applications to external data and tools. MCP servers expose resources and tools; clients (e.g. Cursor) use them so the model gets context and can perform actions. One protocol, many integrations."

Q10: How does MCP differ from a normal API?
> "MCP is designed for AI use: standardized discovery of resources/tools, and passing context to the model. A normal API is general-purpose; MCP is specifically for AI agents and IDEs to plug in data and tools in a consistent way."

Q11: What is a LangChain "tool" and how does the LLM use it?
> "A tool is a callable (function) with a name and description. The LLM sees tool names and descriptions, and can request a call with arguments (e.g. via function calling). The agent executor runs the tool and returns the result to the LLM for the next step."

Q12: How do you handle errors in a LangChain/LangGraph pipeline?
> "Use try/except around tool calls and LLM calls; return structured error messages to the agent; add fallback nodes or default responses; use retries with backoff for transient failures; log and monitor for debugging."

Q13: What is "memory" in LangChain?
> "Memory stores conversation or context across turns – e.g. buffer (last K messages), summary, or entity memory. It’s injected into the prompt so the LLM has history. I choose type based on window size and cost."

Q14: How would you implement human-in-the-loop with LangGraph?
> "Add a node that pauses and waits for human input (e.g. approval, correction), stores it in state, and then continues. Use interrupt_before or interrupt_after on that node; resume when the user responds."

Q15: What is the difference between an agent and a chain?
> "A chain is a fixed sequence (e.g. prompt → LLM → parse). An agent decides dynamically which tool to call next based on the goal and previous results. Use chains for deterministic flows; agents when the path depends on content or external data."

---

## 📊 Key Talking Points

- LangChain: Chains, retrievers, tools, memory; LCEL for composition; good for RAG and simple agents.
- LangGraph: Stateful graphs, conditional edges, cycles; use for complex flows and agentic loops.
- Agents: LLM + tools + loop; ReAct and function-calling; control loops and costs with max steps and timeouts.
- MCP: Standard protocol for AI apps to use external data and tools; servers expose resources/tools; clients (e.g. Cursor) consume them.

---

## 📁 See Also

- [1_Core_GenAI_RAG_LLM.md](1_Core_GenAI_RAG_LLM.md) – RAG/LLM fundamentals  
- [0_GEN_AI_MASTER_INDEX.md](0_GEN_AI_MASTER_INDEX.md) – Master index  
