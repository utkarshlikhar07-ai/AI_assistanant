# JARVIS AI — Just A Rather Very Intelligent System
### Intelligent Personal Assistant & Interactive AI Problem-Solving System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-3.5%20Flash-4285F4.svg?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.24+-499848.svg?style=flat&logo=gunicorn&logoColor=white)](https://www.uvicorn.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063.svg?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-68%20Passed-brightgreen.svg?style=flat&logo=pytest&logoColor=white)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete%20%26%20Operational-success.svg)]()

> **JARVIS AI** is a fully functional, dual-mode Intelligent Personal Assistant powered by Google's Gemini Large Language Model (`google-genai` SDK) and tightly integrated with an interactive Artificial Intelligence Algorithms Laboratory. Designed to bridge foundational computer science algorithms with modern generative AI architecture, JARVIS serves as the central intelligence orchestrator capable of conversational dialogue, autonomous tool-calling execution of 13 university-level AI algorithms, and step-by-step problem explanations. If Gemini is offline or unconfigured, JARVIS seamlessly falls back to a 100% local deterministic intent engine without disruption.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Objectives](#2-project-objectives)
3. [Features & Capabilities](#3-features--capabilities)
4. [Complete Technology Stack](#4-complete-technology-stack)
5. [System Architecture](#5-system-architecture)
6. [Directory Structure](#6-directory-structure)
7. [Explanation of All Implemented AI Algorithms](#7-explanation-of-all-implemented-ai-algorithms)
   - [Module 1: Breadth-First Search (BFS)](#module-1--breadth-first-search-bfs)
   - [Module 2: Depth-First Search (DFS)](#module-2--depth-first-search-dfs)
   - [Module 3: Iterative Deepening DFS (IDDFS)](#module-3--iterative-deepening-depth-first-search-iddfs)
   - [Module 4: Simulated Annealing](#module-4--simulated-annealing)
   - [Module 5: Hill Climbing](#module-5--hill-climbing)
   - [Module 6: A* Search Algorithm](#module-6--a-search-algorithm)
   - [Module 7: D* Lite Dynamic Pathfinding](#module-7--d-lite-dynamic-pathfinding)
   - [Module 8: Wumpus World Knowledge-Based Agent](#module-8--wumpus-world)
   - [Module 9: 8-Puzzle Problem Solver](#module-9--8-puzzle-solver)
   - [Module 10: Towers of Hanoi](#module-10--towers-of-hanoi)
   - [Module 11: Bayesian Network Inference](#module-11--bayesian-network)
   - [Module 12: Expectation-Maximization (EM) Algorithm](#module-12--expectation-maximization-algorithm)
   - [Module 13: Hidden Markov Model (HMM)](#module-13--hidden-markov-model)
8. [Virtual Assistant Functionality](#8-virtual-assistant-functionality)
   - [Google Gemini Large Language Model Integration](#google-gemini-large-language-model-integration)
   - [Local Intent Recognition & Slot Filling](#local-intent-recognition--slot-filling-offline-fallback-engine)
   - [Tool Dispatching & Execution Engine](#tool-dispatching--execution-engine)
   - [Voice Processing (Speech-to-Text & Text-to-Speech)](#voice-processing)
9. [Installation Instructions for Windows](#9-installation-instructions-for-windows)
10. [Dependencies & Requirements](#10-dependencies--requirements)
11. [Exact Commands to Run the Application](#11-exact-commands-to-run-the-application)
12. [Screenshots & UI Showcase](#12-screenshots--ui-showcase)
13. [Testing & Verification](#13-testing--verification)
14. [Future Enhancements](#14-future-enhancements)

---

## 1. Project Overview

In standard computer science laboratory coursework, algorithms such as search strategies, game agents, heuristic optimizers, and probabilistic models are typically implemented as fragmented, disconnected script demonstrations. 

**JARVIS AI (Just A Rather Very Intelligent System)** solves this by unifying all prescribed Artificial Intelligence topics under a single, cohesive, production-grade software application. JARVIS functions as a central conversational assistant where the user can ask domain questions, issue commands in natural language, or execute algorithms directly. 

When a user requests an operation (e.g., *"Find the shortest route from A to G using BFS"* or *"Solve this 8-puzzle with Manhattan distance"*), JARVIS:
1. Recognizes the user's intent and extracts relevant parameters/entities.
2. Dispatches the request to the genuine backend Python algorithm engine.
3. Computes the exact traversal, steps, mathematical optimization, or inference.
4. Returns a natural language response summarizing results and key metrics.
5. Seamlessly navigates to the visualizer panel or renders interactive step-by-step Canvas/Chart animations.

The application operates **100% offline** without mandatory third-party LLM API keys, runs locally on Windows, and provides complete transparency into algorithmic mechanics.

---

## 2. Project Objectives

1. **Integrated Virtual Assistant**: Develop an intelligent, conversational assistant with a distinct JARVIS personality capable of general conversation, factual explanations, mathematical calculations, and automated system routing.
2. **Complete Syllabus Coverage**: Implement genuine, mathematically rigorous Python implementations for all prescribed university AI lab topics:
   - *Topic 1:* BFS, DFS, IDDFS, Simulated Annealing.
   - *Topic 2:* Wumpus World, 8-Puzzle, Towers of Hanoi.
   - *Topic 3:* A\*, D\* Lite, Hill Climbing.
   - *Topic 4:* Bayesian Networks, EM Algorithm with GMM, Hidden Markov Models.
   - *Topic 5:* Intelligent Virtual Assistant.
3. **Live Interactive Visualizations**: Render high-DPI HTML5 Canvas 2D and Chart.js animations displaying nodes visited, open/closed sets, replanned grid paths, cluster contour ellipses, and state transitions.
4. **Zero-Fabrication Guarantee**: Guarantee that no outputs or execution steps are hardcoded or pre-recorded; all results are computed live through backend execution.
5. **Robust Engineering**: Deliver modular, maintainable code with strict Pydantic v2 input validation, graceful exception handling, automated Pytest coverage (58/58 tests passing), and a one-click Windows startup script (`start.bat`).

---

## 3. Features & Capabilities

- **Futuristic HUD Glassmorphism UI**: High-tech sci-fi theme utilizing dark navy/charcoal backgrounds (`#0a0e1a`), electric cyan (`#00d4ff`) and purple (`#7c3aed`) accents, responsive glass cards, and status telemetry.
- **Conversational Chat Interface**: Real-time message streaming, typing indicator, quick prompt chips, auto-scrolling, clipboard copying, and contextual inline algorithm result cards.
- **Browser-Native Voice Engine**: Integrated Web Speech API support for hands-free microphone input (speech-to-text) and natural voice responses (text-to-speech) with customizable speech rate and voice pitch.
- **Heuristic Search Laboratory**: Dedicated modules for BFS, DFS, IDDFS, A\*, D\* Lite, Hill Climbing, and Simulated Annealing with customizable graphs, heuristics, and execution controls.
- **Classic AI Puzzle Solvers**:
  - Interactive 3×3 sliding **8-Puzzle** solver featuring solvable board generation, move animations, and heuristic selection.
  - Interactive **Towers of Hanoi** solver with disk configuration controls, animated disk transfers, and recursion tracking.
  - Interactive **Wumpus World** cave simulation with fog-of-war grid, live hazard detection, arrow mechanics, and logical knowledge-base inference.
- **Probabilistic Reasoning Laboratory**:
  - Exact **Bayesian Network** posterior probability inference via variable enumeration.
  - Mathematical **Expectation-Maximization (EM)** algorithm clustering 2D Gaussian mixtures from scratch with log-likelihood convergence graphs.
  - **Hidden Markov Model (HMM)** dynamic programming executing both the Forward evaluation algorithm and the Viterbi state decoder.
- **Activity Logging & Settings**: Persistent local activity tracker, customizable theme modes, configurable API base endpoint, animation speed sliders, and session history export (JSON).

---

## 4. Complete Technology Stack

### Backend Technologies
| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.9 – 3.14+ | Core programming language for all algorithms and backend services |
| **Google GenAI** | >= 3.0.0 | Official Google Gemini LLM SDK (`google-genai`) with autonomous tool calling |
| **FastAPI** | >= 0.104.1 | High-speed asynchronous REST API framework |
| **Uvicorn** | >= 0.24.0 | ASGI production web server supporting asynchronous workers and auto-reload |
| **Pydantic** | >= 2.5.0 | Data validation, request payload parsing, and response serialization |
| **NumPy** | >= 1.26.0 | Vectorized numerical operations, matrix transformations, and mathematical modeling |
| **SciPy** | >= 1.11.0 | Scientific mathematical utilities and statistical density calculations |
| **Scikit-Learn** | >= 1.3.0 | Supplementary machine learning utilities |
| **NetworkX** | >= 3.2.0 | Graph data structure representations and topological validation |
| **Python-Dotenv**| >= 1.0.0 | Secure environment variable management for API keys (.env) |
| **Pytest** | >= 7.4.0 | Unit, integration, and regression testing framework |
| **HTTPX** | >= 0.25.0 | High-performance asynchronous HTTP client for integration testing |

### Frontend Technologies
| Technology | Purpose |
|---|---|
| **HTML5** | Semantic markup structuring the Single-Page Application (SPA) dashboard |
| **CSS3** | Modern responsive glassmorphism styles, CSS Grid/Flexbox, and neon keyframe animations |
| **Vanilla JavaScript (ES6+)** | Client-side application controllers, DOM events, and asynchronous API calls |
| **HTML5 Canvas 2D API** | High-performance graphics rendering for graphs, grid worlds, pegs, and clusters |
| **Chart.js** | Interactive charting for optimization landscapes and EM log-likelihood curves |
| **Web Speech API** | Browser-native `SpeechRecognition` (STT) and `SpeechSynthesis` (TTS) |

---

## 5. System Architecture

The application follows a clean **Separation of Concerns (SoC)** architecture consisting of client presentation, API gateway, central assistant orchestration, and independent algorithmic modules:

```text
+---------------------------------------------------------------------------------------+
|                                  JARVIS AI CLIENT (SPA)                               |
|                                                                                       |
|   +--------------------------+   +-----------------------+   +--------------------+   |
|   |  Conversational Agent UI |   |  Visualizer Subsystems|   |  Voice Engine      |   |
|   |  - Real-time chat stream |   |  - Canvas 2D Graphs   |   |  - Web Speech STT  |   |
|   |  - Inline result cards   |   |  - Grid & Peg Engines |   |  - Web Speech TTS  |   |
|   |  - Suggested prompts     |   |  - Chart.js Plots     |   |  - Mic indicator   |   |
|   +------------+-------------+   +-----------+-----------+   +---------+----------+   |
+----------------|-----------------------------|-------------------------|--------------+
                 | HTTP POST /api/assistant    | HTTP POST /api/...      |
                 v                             v                         v
+---------------------------------------------------------------------------------------+
|                                FASTAPI APPLICATION GATEWAY                            |
|                                                                                       |
|   - CORS Middleware (Allow All)          - Static File Server (/css, /js, /assets)    |
|   - JSON Request Validation (Pydantic)   - Root Index Delivery (/)                    |
+---------------------------------------------------------------------------------------+
        |                                 |                             |
        v                                 v                             v
+-----------------------+      +--------------------+       +-----------------------+
|   ASSISTANT SERVICE   |      |  ALGORITHMS ROUTER |       |   PUZZLES & PROB.     |
|                       |      |                    |       |                       |
| - Intent Recognition  |      | - /bfs, /dfs       |       | - /eight-puzzle       |
| - Slot / Entity Match |      | - /iddfs, /astar   |       | - /hanoi, /wumpus     |
| - Response Engine     |      | - /dstar           |       | - /bayesian, /em      |
| - Navigation Dispatch |      | - /hill-climbing   |       | - /hmm                |
| - Tool Invoker        |      | - /simulated-ann.  |       |                       |
+-----------+-----------+      +----------+---------+       +-----------+-----------+
            |                             |                             |
            +-----------------------------+-----------------------------+
                                          |
                                          v
+---------------------------------------------------------------------------------------+
|                                ALGORITHMIC CORE ENGINES                               |
|                                                                                       |
|   [ algorithms/ ]              [ problems/ ]                [ probabilistic/ ]        |
|   - bfs.py (Queue)             - eight_puzzle.py (A*)       - bayesian_network.py     |
|   - dfs.py (Stack)             - towers_of_hanoi.py (Rec.)  - em_algorithm.py (GMM)   |
|   - iddfs.py (Depth-Limited)   - wumpus_world.py (Agent)    - hmm.py (Forward/Viterbi)|
|   - astar.py (Heapq Priority)                                                         |
|   - dstar.py (D* Lite Replanner)                                                      |
|   - hill_climbing.py (Steepest)                                                       |
|   - simulated_annealing.py (Metropolis)                                               |
+---------------------------------------------------------------------------------------+
```

---

## 6. Directory Structure

```text
e:\mini_project\
│
├── backend\                           # Python FastAPI Application Core
│   ├── __init__.py                    # Backend package initializer
│   ├── main.py                        # FastAPI entrypoint, router mounts, static files
│   │
│   ├── algorithms\                    # Search and Optimization Implementations
│   │   ├── __init__.py                # Algorithms package exports
│   │   ├── astar.py                   # A* Heuristic Search (heapq, g/h/f tracking)
│   │   ├── bfs.py                     # Breadth-First Search (collections.deque)
│   │   ├── dfs.py                     # Depth-First Search (Iterative LIFO stack)
│   │   ├── dstar.py                   # D* Lite Dynamic Replanning on Grid
│   │   ├── hill_climbing.py           # Continuous Steepest-Ascent Hill Climbing
│   │   ├── iddfs.py                   # Iterative Deepening Depth-First Search
│   │   └── simulated_annealing.py     # Simulated Annealing with Boltzmann criterion
│   │
│   ├── api\                           # REST API Endpoints & Routers
│   │   ├── __init__.py                # Router aggregation and fallback exports
│   │   ├── algorithms.py              # Endpoints for search & optimization algorithms
│   │   ├── assistant.py               # Endpoints for chat assistant & system capabilities
│   │   ├── llm.py                     # Endpoints for Google Gemini status, config & test
│   │   ├── probabilistic.py           # Endpoints for Bayesian, EM, and HMM modules
│   │   └── puzzles.py                 # Endpoints for 8-Puzzle, Hanoi, and Wumpus World
│   │
│   ├── core\                          # Local Virtual Assistant Intelligence
│   │   ├── __init__.py                # Core package initializer
│   │   ├── intent_recognition.py      # Rule-based & keyword intent classifier (19 intents)
│   │   └── response_engine.py         # Conversational response synthesis & prompt generator
│   │
│   ├── models\                        # Data Models and Pydantic Schemas
│   │   ├── __init__.py                # Models package initializer
│   │   └── schemas.py                 # 24 Pydantic v2 request/response schemas
│   │
│   ├── probabilistic\                 # Probabilistic & Uncertainty AI Modules
│   │   ├── __init__.py                # Probabilistic package exports
│   │   ├── bayesian_network.py        # Exact Bayesian inference by joint enumeration
│   │   └── em_algorithm.py            # Gaussian Mixture Model Expectation-Maximization
│   │   └── hmm.py                     # Hidden Markov Model (Forward & Viterbi algorithms)
│   │
│   ├── problems\                      # Classical Problem Solvers & Environments
│   │   ├── __init__.py                # Problems package exports
│   │   ├── eight_puzzle.py            # 8-Puzzle solver with Manhattan & Misplaced heuristics
│   │   ├── towers_of_hanoi.py         # Recursive Towers of Hanoi solver
│   │   └── wumpus_world.py            # Wumpus World environment simulation & knowledge base
│   │
│   └── services\                      # Orchestration & Integration Services
│       ├── __init__.py                # Services package initializer
│       ├── assistant_service.py       # Central orchestrator connecting chat to AI tools
│       └── llm_service.py             # Google Gemini LLM SDK client & 13 algorithm tools
│
├── frontend\                          # Web Client Interface (Single-Page App)
│   ├── index.html                     # Main dashboard, HUD cards, visualizer layouts
│   ├── assets\                        # Static multimedia and icons placeholder
│   │   └── README.txt
│   ├── css\
│   │   ├── animations.css             # Neon pulses, glowing text, and card transitions
│   │   └── style.css                  # Sci-Fi glassmorphism theme and responsive grid
│   └── js\
│       ├── algorithms.js              # Controllers for search and optimization tabs
│       ├── app.js                     # Global SPA navigation, toasts, and API helper
│       ├── chat.js                    # Chat UI, Web Speech recognition, and synthesis
│       ├── gemini.js                  # Gemini LLM status telemetry & config modal
│       ├── probabilistic.js           # Bayesian bars, EM curves, and HMM sequences
│       ├── puzzles.js                 # 8-Puzzle grid and Towers of Hanoi visualizers
│       ├── visualizations.js          # Canvas 2D graph renderer and Chart.js plotter
│       └── wumpus.js                  # Wumpus World 4x4 grid and movement controls
│
├── tests\                             # Automated Pytest Suite (68 Tests)
│   ├── __init__.py                    # Test package initializer
│   ├── test_api.py                    # End-to-end FastAPI endpoint integration tests
│   ├── test_llm.py                    # Google Gemini LLM tool & fallback test suite
│   ├── test_probabilistic.py          # Math verification for Bayesian, EM, and HMM
│   ├── test_puzzles.py                # Tests for 8-Puzzle, Hanoi, and Wumpus World
│   └── test_search.py                 # Tests for BFS, DFS, IDDFS, A*, D*, HC, SA
│
├── .env                               # Local environment configuration (Git-ignored)
├── .env.example                       # Template for environment variables
├── .gitignore                         # Git ignore configuration (caches, venvs, envs)
├── PROJECT_REPORT.md                  # Comprehensive academic project report
├── README.md                          # Primary project documentation
├── requirements.txt                   # Production Python package dependencies
├── setup.bat                          # One-time automated environment setup script
└── start.bat                          # One-click Windows initialization and startup script
```

---

## 7. Explanation of All Implemented AI Algorithms

### Module 1 — Breadth-First Search (BFS)
- **Concept**: Uninformed graph search exploring all neighbor vertices at the present depth level before moving deeper.
- **Implementation**: Implemented in [`backend/algorithms/bfs.py`](file:///e:/mini_project/backend/algorithms/bfs.py) using a FIFO `collections.deque`. Maintains parent mappings for path reconstruction and logs queue snapshots at each step.
- **Guarantees**: Guarantees the shortest path on unweighted graphs.
- **Complexity**: Time $O(V + E)$, Space $O(V)$.

### Module 2 — Depth-First Search (DFS)
- **Concept**: Uninformed search progressing as deep as possible along each branch before backtracking.
- **Implementation**: Implemented in [`backend/algorithms/dfs.py`](file:///e:/mini_project/backend/algorithms/dfs.py) using an explicit LIFO stack to prevent call-stack overflow on deep graphs. Captures visited sets, traversal ordering, and stack states.
- **Complexity**: Time $O(V + E)$, Space $O(V)$.

### Module 3 — Iterative Deepening Depth-First Search (IDDFS)
- **Concept**: Combines the linear space-efficiency of DFS with the completeness and optimality of BFS by incrementally increasing the search depth limit ($d = 0, 1, 2, \dots, d_{max}$).
- **Implementation**: Implemented in [`backend/algorithms/iddfs.py`](file:///e:/mini_project/backend/algorithms/iddfs.py). Tracks nodes explored in each iteration and returns the discovery depth upon reaching the goal.
- **Complexity**: Time $O(b^d)$, Space $O(bd)$.

### Module 4 — Simulated Annealing
- **Concept**: Stochastic local search designed to escape local optima by probabilistically accepting worse solutions based on the physical annealing process of metallurgy.
- **Implementation**: Implemented in [`backend/algorithms/simulated_annealing.py`](file:///e:/mini_project/backend/algorithms/simulated_annealing.py). Uses the Boltzmann acceptance criterion:
  $$P(\text{accept}) = \exp\left(\frac{\Delta E}{T}\right)$$
  Supports geometric cooling schedules ($T_{k+1} = \alpha T_k$) across multi-modal and quadratic mathematical landscapes.
- **Complexity**: Time $O(\text{iterations})$, Space $O(1)$.

### Module 5 — Hill Climbing
- **Concept**: Local search optimization that continually moves in the direction of increasing elevation (steepest ascent) to find the peak of a mathematical function.
- **Implementation**: Implemented in [`backend/algorithms/hill_climbing.py`](file:///e:/mini_project/backend/algorithms/hill_climbing.py). Explores adjacent neighbors within a step size $\epsilon$. Includes detection and reporting for when the algorithm gets trapped at local maxima.
- **Complexity**: Time $O(\text{iterations})$, Space $O(1)$.

### Module 6 — A* Search Algorithm
- **Concept**: Heuristic-guided best-first search evaluating candidate nodes using:
  $$f(n) = g(n) + h(n)$$
  where $g(n)$ is the exact cost from the start node to $n$, and $h(n)$ is the estimated heuristic cost to the goal.
- **Implementation**: Implemented in [`backend/algorithms/astar.py`](file:///e:/mini_project/backend/algorithms/astar.py) using `heapq`. Guarantees optimal pathfinding provided $h(n)$ is admissible ($h(n) \le h^*(n)$).
- **Complexity**: Time $O(b^d)$, Space $O(b^d)$.

### Module 7 — D* Lite Dynamic Pathfinding
- **Concept**: Incremental heuristic search algorithm developed by Sven Koenig and Maxim Likhachev for goal-directed pathfinding in dynamic or partially known environments.
- **Implementation**: Implemented in [`backend/algorithms/dstar.py`](file:///e:/mini_project/backend/algorithms/dstar.py) as a full `DStarLite` class. Rather than planning from scratch when an obstacle appears, it maintains one-step lookahead values ($rhs$) and a key modifier ($k_m$) to update only affected nodes.
- **Complexity**: Re-planning complexity is significantly lower than full $A^*$ re-computation.

### Module 8 — Wumpus World
- **Concept**: Classical knowledge-based agent environment where an agent explores a dark 4×4 cave containing deadly pits, a hungry Wumpus, and a pot of gold.
- **Implementation**: Implemented in [`backend/problems/wumpus_world.py`](file:///e:/mini_project/backend/problems/wumpus_world.py). Features:
  - Percepts: *Stench* (adjacent to Wumpus), *Breeze* (adjacent to Pit), *Glitter* (in Gold cell), *Bump* (walking into wall), *Scream* (Wumpus slain by arrow).
  - Actions: Move forward, turn left/right, grab gold, shoot arrow, climb out.
  - Knowledge Base: Deduces guaranteed safe cells and hazard locations from accumulated percepts.

### Module 9 — 8-Puzzle Solver
- **Concept**: A 3×3 grid containing 8 numbered tiles and an empty space. The goal is to slide tiles until reaching the ordered state `[1, 2, 3, 4, 5, 6, 7, 8, Blank]`.
- **Implementation**: Implemented in [`backend/problems/eight_puzzle.py`](file:///e:/mini_project/backend/problems/eight_puzzle.py). Uses $A^*$ search with:
  1. *Manhattan Distance Heuristic*: Sum of absolute horizontal and vertical distances of tiles from their target positions.
  2. *Misplaced Tiles Heuristic*: Count of tiles currently out of place.
  - Validates solvability in $O(1)$ by computing inversion parity before launching the search.

### Module 10 — Towers of Hanoi
- **Concept**: Classic recursive mathematical puzzle involving 3 pegs and $n$ disks of varying sizes. Rules dictate moving one disk at a time and never placing a larger disk atop a smaller one.
- **Implementation**: Implemented in [`backend/problems/towers_of_hanoi.py`](file:///e:/mini_project/backend/problems/towers_of_hanoi.py). Solves the puzzle in the minimal theoretical move count:
  $$\text{Total Moves} = 2^n - 1$$
  Tracks full disk snapshots for pegs A, B, and C after each individual move.

### Module 11 — Bayesian Network
- **Concept**: Directed Acyclic Graph (DAG) representing conditional dependencies between variables under uncertainty.
- **Implementation**: Implemented in [`backend/probabilistic/bayesian_network.py`](file:///e:/mini_project/backend/probabilistic/bayesian_network.py) modeling the classic Rain / Sprinkler / Wet Grass problem:
  - Nodes: `Cloudy`, `Rain`, `Sprinkler`, `WetGrass`.
  - Calculates exact posterior marginal distributions given observed evidence using full joint enumeration:
    $$P(X \mid e) = \alpha \sum_{Y} P(X, Y, e)$$
  - No hardcoded probabilities; values are computed dynamically.

### Module 12 — Expectation-Maximization (EM) Algorithm
- **Concept**: Iterative optimization algorithm for finding Maximum Likelihood Estimates in parametric statistical models involving unobserved latent variables.
- **Implementation**: Implemented completely from scratch in [`backend/probabilistic/em_algorithm.py`](file:///e:/mini_project/backend/probabilistic/em_algorithm.py) for Gaussian Mixture Models (GMM):
  - **E-Step (Expectation)**: Computes soft responsibilities $\gamma_{ik}$ representing the posterior probability that sample $i$ belongs to cluster $k$.
  - **M-Step (Maximization)**: Re-estimates means $\mu_k$, covariance matrices $\Sigma_k$, and mixture weights $\pi_k$.
  - Tracks log-likelihood ascent to monitor numerical convergence.

### Module 13 — Hidden Markov Model (HMM)
- **Concept**: Statistical Markov model in which the system being modeled is assumed to be a Markov process with unobservable (hidden) states.
- **Implementation**: Implemented from scratch in [`backend/probabilistic/hmm.py`](file:///e:/mini_project/backend/probabilistic/hmm.py) modeling Weather (`Sunny`, `Rainy`) and Activities (`Walk`, `Shop`, `Clean`):
  - **Forward Algorithm**: Dynamic programming evaluation calculating the total probability of an observation sequence $P(O \mid \lambda)$.
  - **Viterbi Algorithm**: Dynamic programming decoder finding the single most likely hidden state trajectory:
    $$Q^* = \arg\max_Q P(Q, O \mid \lambda)$$

---

## 8. Virtual Assistant Functionality

### Intent Recognition & Slot Filling
The virtual assistant uses a local, deterministic intent classifier in [`backend/core/intent_recognition.py`](file:///e:/mini_project/backend/core/intent_recognition.py). It operates entirely offline without requiring external API calls.

Supported Intents:
1. `GREETING` — User greetings and welcomes.
2. `GENERAL_QUERY` — Factual inquiries about AI, JARVIS, or computer science.
3. `CALCULATION` — Mathematical arithmetic operations.
4. `EXPLAIN_ALGORITHM` — Technical conceptual explanations of all 13 algorithms.
5. `BFS_REQUEST`, `DFS_REQUEST`, `IDDFS_REQUEST` — Graph traversal requests.
6. `ASTAR_REQUEST`, `DSTAR_REQUEST` — Heuristic and dynamic pathfinding requests.
7. `HILL_CLIMBING_REQUEST`, `SIMULATED_ANNEALING_REQUEST`, `OPTIMIZATION_REQUEST` — Optimization calls.
8. `PUZZLE_8_REQUEST` — 8-Puzzle solving requests.
9. `WUMPUS_REQUEST` — Wumpus World environment operations.
10. `HANOI_REQUEST` — Tower of Hanoi puzzle solving.
11. `PROBABILITY_REQUEST` — Bayesian inference queries.
12. `EM_REQUEST` — Gaussian mixture clustering commands.
13. `HMM_REQUEST` — State sequence decoding requests.
14. `HELP` — System capability discovery.

**Entity Extraction**: Automatically extracts single-letter graph node names (`from A to G`), numeric parameters (`3 disks`, `10 iterations`), and target algorithm types from natural language input.

### Google Gemini Large Language Model Integration
JARVIS AI is powered by Google's Gemini Large Language Model via the modern Python SDK (`google-genai`). The assistant combines high-level reasoning and conversational intelligence with deterministic execution of the 13 lab algorithms:

- **Official Modern SDK**: Uses `from google import genai` and `from google.genai import types` (version `google-genai>=3.0.0`), strictly avoiding deprecated packages.
- **Autonomous Tool / Function Calling**: 13 real Python algorithm tool declarations are registered with the Gemini client:
  1. `execute_bfs(start_node, goal_node)` — Invokes `backend.algorithms.bfs.bfs`
  2. `execute_dfs(start_node, goal_node)` — Invokes `backend.algorithms.dfs.dfs`
  3. `execute_iddfs(start_node, goal_node, max_depth)` — Invokes `backend.algorithms.iddfs.iddfs`
  4. `execute_astar(start_node, goal_node)` — Invokes `backend.algorithms.astar.astar`
  5. `execute_dstar(grid_size, start_x, start_y, goal_x, goal_y)` — Invokes `backend.algorithms.dstar.dstar_plan`
  6. `execute_hill_climbing(initial_x, function_type, max_iterations)` — Invokes `backend.algorithms.hill_climbing.hill_climbing`
  7. `execute_simulated_annealing(initial_x, initial_temp, cooling_rate, max_iterations)` — Invokes `backend.algorithms.simulated_annealing.simulated_annealing`
  8. `execute_eight_puzzle(heuristic)` — Invokes `backend.problems.eight_puzzle.solve_puzzle`
  9. `execute_towers_of_hanoi(num_disks)` — Invokes `backend.problems.towers_of_hanoi.hanoi`
  10. `execute_wumpus_world(action)` — Invokes `backend.problems.wumpus_world.WumpusWorld`
  11. `execute_bayesian_network(cloudy, rain, sprinkler)` — Invokes `backend.probabilistic.bayesian_network.compute_inference`
  12. `execute_expectation_maximization(n_samples, n_components, max_iterations)` — Invokes `backend.probabilistic.em_algorithm.run_em`
  13. `execute_hidden_markov_model(observations)` — Invokes `backend.probabilistic.hmm.run_hmm`

- **Zero-Fabrication Guarantee**: Gemini never fakes or hallucinates algorithm results. When requested, Gemini invokes the verified Python tool, inspects the returned mathematical output, explains the traversal steps to the user, and sends the structured data to the frontend for live Canvas rendering.
- **Dual-Engine Robust Fallback**:
  - **Online Mode (`llm_powered: true`)**: Gemini delivers contextual dialogue, multi-turn conversation memory, and automatic algorithm invocation. Chat bubbles display a cyan `✨ Gemini AI` badge.
  - **Offline Fallback Mode (`llm_powered: false`)**: If the API key is missing, network is disconnected, or Gemini is rate-limited, JARVIS automatically engages the local deterministic regex and pattern-matching intent engine. No crashes, no degraded core functionality.
- **Secure Key Management**:
  - API keys are stored server-side in `.env` (strictly Git-ignored).
  - API status endpoints (`GET /api/llm/status`) return masked keys (e.g., `AQ.Ab8...4CVw`) and never transmit the raw secret to browser JavaScript.
  - Users can configure their API key anytime via the in-app Glassmorphism modal or the Settings view, complete with a live "Test Connection" button.

### Local Intent Recognition & Slot Filling (Offline Fallback Engine)
When operating offline, the local intent engine in [`backend/core/intent_recognition.py`](file:///e:/mini_project/backend/core/intent_recognition.py) parses user queries into structured intents:
1. `GREETING` / `FAREWELL` — Conversational pleasantries.
2. `BFS_REQUEST`, `DFS_REQUEST`, `IDDFS_REQUEST` — Uninformed graph searches.
3. `ASTAR_REQUEST`, `DSTAR_REQUEST` — Heuristic and dynamic replanning requests.
4. `HILL_CLIMBING_REQUEST`, `SIMULATED_ANNEALING_REQUEST` — Continuous function optimization.
5. `PUZZLE_8_REQUEST`, `HANOI_REQUEST`, `WUMPUS_REQUEST` — Classic problem solving.
6. `BAYESIAN_REQUEST`, `EM_REQUEST`, `HMM_REQUEST` — Probabilistic reasoning.
7. `HELP` — System capability discovery.

**Entity Extraction**: Automatically extracts single-letter graph node names (`from A to G`), numeric parameters (`3 disks`, `10 iterations`), and target algorithm types from natural language input.

### Tool Dispatching & Execution Engine
Implemented in [`backend/services/assistant_service.py`](file:///e:/mini_project/backend/services/assistant_service.py), the assistant service coordinates:
- Intent parsing and entity extraction.
- Invocation of algorithm helpers.
- Formatting of rich technical explanations.
- UI View Dispatching: Returns a `navigate_to` parameter that instructs the frontend to switch to the relevant algorithm visualizer panel (e.g., navigating directly to the Wumpus cave or search tab).

### Voice Processing
- **Speech-to-Text (STT)**: Built using the browser's `webkitSpeechRecognition` / `SpeechRecognition` interface. Clicking the microphone icon initiates live audio capture, transcribing user speech directly into the chat prompt.
- **Text-to-Speech (TTS)**: Built using the browser's `window.speechSynthesis` interface. Responses from JARVIS are automatically voiced aloud using a professional, synthesized voice with markdown stripping. Voice output can be toggled on or off in the Settings panel.

---

## 9. Installation Instructions for Windows

### Prerequisites
1. **Windows 10 or Windows 11**.
2. **Python 3.9+** (Python 3.9, 3.10, 3.11, 3.12, 3.13, or 3.14).
   - Ensure the option **"Add Python to PATH"** was checked during Python installation.
3. **Modern Web Browser** (Google Chrome or Microsoft Edge recommended for native voice speech support).

### Step-by-Step Installation

1. **Open Command Prompt or PowerShell** and navigate to your project directory:
   ```cmd
   cd e:\mini_project
   ```

2. **Automated Setup (Recommended)**:
   Run the included setup script:
   ```cmd
   setup.bat
   ```
   This will verify Python, initialize a clean virtual environment, upgrade pip, install all dependencies from `requirements.txt`, and generate your `.env` configuration template.

3. **Configure Google Gemini API Key**:
   Open `.env` in any text editor and insert your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   GEMINI_MODEL=gemini-3.5-flash
   ```
   *(You can obtain a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey). If left unconfigured, JARVIS runs in local offline fallback mode).*

---

## 10. Dependencies & Requirements

All dependencies are defined in [`requirements.txt`](file:///e:/mini_project/requirements.txt):

| Package | Version Constraint | Role & Justification |
|---|---|---|
| `google-genai` | `>=3.0.0` | Official modern Google Gemini LLM SDK with function calling |
| `fastapi` | `>=0.104.1` | Asynchronous web framework hosting all 21+ REST endpoints |
| `uvicorn[standard]` | `>=0.24.0` | Production ASGI web server running the event loop |
| `pydantic` | `>=2.5.0` | Strict schema validation for all API inputs and outputs |
| `numpy` | `>=1.26.0` | Matrix mathematics for GMM, HMM, and function optimization |
| `scikit-learn` | `>=1.3.0` | Machine learning utilities and baseline evaluations |
| `networkx` | `>=3.2.0` | Graph structure verification and path analysis |
| `scipy` | `>=1.11.0` | Numerical calculations and probability densities |
| `python-multipart` | `>=0.0.6` | Form-data support for file and payload uploads |
| `python-dotenv` | `>=1.0.0` | Loading configuration variables from `.env` |
| `pytest` | `>=7.4.0` | Core automated testing framework |
| `pytest-asyncio` | `>=0.21.0` | Async test fixtures for testing asynchronous FastAPI endpoints |
| `httpx` | `>=0.25.0` | HTTP client for integration test requests |
| `aiofiles` | `>=23.2.0` | Asynchronous file I/O operations |

---

## 11. Exact Commands to Run the Application

### Method 1: One-Click Startup Script (Recommended)
Double-click [`start.bat`](file:///e:/mini_project/start.bat) in File Explorer, or run:
```cmd
cd e:\mini_project
start.bat
```
`start.bat` will verify Python, verify dependencies (including `google-genai`), activate the virtual environment, and launch the server.

### Method 2: Manual Terminal Execution
```cmd
cd e:\mini_project
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Once running, access the application at:
- **Application Dashboard:** `http://127.0.0.1:8000`
- **Interactive OpenAPI Documentation:** `http://127.0.0.1:8000/docs`
- **Health Check Endpoint:** `http://127.0.0.1:8000/api/health`
- **Gemini Status Endpoint:** `http://127.0.0.1:8000/api/llm/status`

---

## 12. Screenshots & UI Showcase

The application features a responsive Sci-Fi HUD design:

### 1. Main Dashboard
- High-level overview displaying JARVIS system telemetry, online status indicator, quick-action cards, algorithm shortcuts, and real-time activity history.

### 2. Conversational Assistant (`/section-chat`)
- Conversational chat interface with message bubbles, speech synthesis toggle, microphone voice input button, and prompt chips (*"Explain BFS"*, *"Solve the 8-puzzle"*, *"How does Wumpus World work?"*).
- **Gemini Status Pill**: Real-time indicator displaying active Gemini LLM status, model identifier, and one-click access to the API configuration modal.
- **LLM Badges**: Distinguishes between generative AI reasoning (`✨ Gemini AI`) and local rule responses (`⚙ Rule Engine`).
- Displays inline algorithm result cards directly within chat bubbles when algorithms are triggered.

### 3. Search Algorithms Laboratory (`/section-search`)
- Tab-based workspace for BFS, DFS, IDDFS, A\*, D\* Lite, Hill Climbing, and Simulated Annealing.
- Includes graph input controls, start/goal selectors, step-by-step tables, and real-time Canvas 2D graph visualizations.

### 4. Puzzle Solver Hub (`/section-puzzles`)
- **8-Puzzle**: Interactive 3×3 tile board with randomizer, heuristic selector (Manhattan vs. Misplaced), move-by-move animation playback, and state exploration metrics.
- **Towers of Hanoi**: Visual 3-peg disk stack display with speed-adjustable playback, recursive move sequence logs, and $2^n-1$ verification.

### 5. Wumpus World Cave Explorer (`/section-wumpus`)
- 4×4 hazardous cave map with fog-of-war cell discovery.
- Dedicated directional movement pad, arrow shooting mechanics, gold collection, and live indicator lights for *Stench*, *Breeze*, *Glitter*, and *Bump*.

### 6. Probabilistic AI Suite (`/section-probabilistic`)
- **Bayesian Network**: Interactive evidence selection checkboxes with animated posterior probability distribution bars.
- **Expectation-Maximization**: 2D scatter plot rendering cluster assignments and 2-sigma Gaussian contour ellipses alongside log-likelihood ascent curves.
- **Hidden Markov Model**: Interactive observation sequence builder (`Walk`, `Shop`, `Clean`) with Forward probability output and Viterbi state path breakdown.

---

## 13. Testing & Verification

The project includes an automated test suite located in `tests/`.

### Running All Tests
```cmd
cd e:\mini_project
python -m pytest tests/ -v
```

### Test Breakdown (68 Passed)
- **`tests/test_llm.py` (10 Tests)**:
  - LLM service initialization and model alias resolution (`gemini-flash-latest` → `gemini-3.5-flash`).
  - Secure API key masking (ensures raw keys never leak to frontend).
  - Conversation history pruning and role mapping (`user` / `model`).
  - Direct execution of algorithm tool dispatchers (BFS, 8-Puzzle, Hanoi, Bayesian Network).
  - LLM status and validation endpoints (`GET /api/llm/status`, `POST /api/llm/configure`).
  - Mocked connection testing (`POST /api/llm/test-connection`).
  - Graceful fallback to deterministic rule engine when Gemini is offline.
  - Successful LLM chat response and `llm_powered: true` attribution.
- **`tests/test_search.py` (19 Tests)**:
  - BFS path optimality and reachability.
  - DFS traversal order and cycle avoidance.
  - IDDFS depth-limited cutoff and goal discovery.
  - A\* optimal cost with admissible heuristics.
  - D\* Lite obstacle avoidance and replanning.
  - Hill Climbing local maxima detection.
  - Simulated Annealing temperature descent and convergence.
- **`tests/test_puzzles.py` (12 Tests)**:
  - 8-Puzzle solvability detection via inversion parity.
  - 8-Puzzle A\* solver path verification.
  - Towers of Hanoi $2^n-1$ mathematical invariant.
  - Wumpus World hazard placement, percept generation, and gold collection.
- **`tests/test_probabilistic.py` (10 Tests)**:
  - Bayesian Network exact probability axioms ($\sum P = 1.0$).
  - EM algorithm convergence and mixture weight normalization.
  - HMM Forward algorithm probability bounds ($0 < P \le 1$).
  - HMM Viterbi most-likely state sequence decoding.
- **`tests/test_api.py` (17 Tests)**:
  - HTTP status codes, JSON response formatting, and schema validation across all assistant, algorithm, puzzle, and probabilistic endpoints.
- **`tests/test_puzzles.py` (12 Tests)**:
  - 8-Puzzle solvability detection via inversion parity.
  - 8-Puzzle A\* solver path verification.
  - Towers of Hanoi $2^n-1$ mathematical invariant.
  - Wumpus World hazard placement, percept generation, and gold collection.
- **`tests/test_probabilistic.py` (10 Tests)**:
  - Bayesian Network exact probability axioms ($\sum P = 1.0$).
  - EM algorithm convergence and mixture weight normalization.
  - HMM Forward algorithm probability bounds ($0 < P \le 1$).
  - HMM Viterbi most-likely state sequence decoding.
- **`tests/test_api.py` (17 Tests)**:
  - HTTP status codes, JSON response formatting, and schema validation across all assistant, algorithm, puzzle, and probabilistic endpoints.

---

## 14. Future Enhancements

1. **Local LLM Integration**: Incorporating local quantized models (e.g., Llama 3 or Mistral via `llama.cpp` or `Ollama`) as an optional secondary conversational reasoning backend.
2. **Reinforcement Learning Arena**: Adding Q-Learning, SARSA, and Deep Q-Networks (DQN) for autonomous grid navigation and classic game benchmarks.
3. **Computer Vision Gestures**: Integrating MediaPipe camera tracking to manipulate holographic puzzles and graphs through hand gestures.
4. **Adversarial Game Search**: Expanding the game-playing module to include Minimax and Alpha-Beta Pruning for interactive Tic-Tac-Toe and Chess.

---

## License

This project is developed for educational and academic research purposes under the **MIT License**.
All algorithm implementations, user interface designs, and assistant integrations are original, modular, and fully functional.
