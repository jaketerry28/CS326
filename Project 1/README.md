# BFS, DFS, UCS Project 1

[Analysis Report](Analysis_Report.md)  
To run the program, use WSL.

# Commands

CD into src first. 

### Run Tests

Testing using pytest.

```
sudo apt install python3-pytest
python3 -m pytest
```

### Run main

Args can be included in command line or users will be prompted if left blank.

Algorithm args are: "bfs", "dfs", "ucs"

```
python3 main.py m n rs cs rg cg min_cost max_cost seed algorithm
```

Results will be stored in appended to results.json if ran individually.

### Run experiments

Generate 90 runs from the experiments_config.json file.

30 10x10 grid runs with seeds 1-10
30 25x25 grid runs with seeds 1-10
30 50x50 grid runs with seeds 1-10.

With each algorithm running 10 times per grid size.

```
python3 run_experiments.py
```

Results are stored in results.json.

```
python3 metrics/metrics_report.py
```

To run the metric report and generate 2 files, metric_report.csv and metrics_report.json. 
Calcultes means for various attributes.




# Experiment setup

[Node](src/node.py)  - establishes node attributes (self, state, parent, action, g)

[Grid](src/grid.py) - assigns random cost to grid and establishes legal moves.


# AI Disclosure

The code for the algorithm strictly follows the psuedo code provided in the powerpoint slides. AI was used in the design of test functions, analysis, and metric reporting.

Example prompts:

```
Given the [algorithm].py code, create test functions for:

- test_bfs_success_path_starts_and_ends
- test_bfs_success_moves_are_legal_and_match_actions
- test_bfs_returns_shortest_steps_on_uniform_grid
- test_bfs_failure_out_of_bounds_goal_returns_empty_and_failure
- test_bfs_start_is_goal
- test_bfs_path_has_no_repeated_states
```

```
Given the metrics_report.csv, generate an analysis report showing:

- Why BFS Usually Finds a Short Path in Steps but Uses a Lot of Memory
- Why DFS Is Unpredictable
- Why UCS Finds a Lower-Cost Path When Costs Vary (Even If It Uses More Steps)
- Summary Comparison
```

```
Create a experiment_config.json file that can be used to generate the following:

30 10x10 grid runs with seeds 1-10
30 25x25 grid runs with seeds 1-10
30 50x50 grid runs with seeds 1-10.

min_cost = 1
max_cost = 20

Start will always be (0,0)
Goal will be assigned inside the run_experiment.py code.

algorithms: bfs, dfs, ucs
```

Code was not copied and pasted mindlessly. I made sure to validate each line, ask questions if I did not understand, and often had to reprompt the AI to remove redundant or overly complex code. Verification occured through validating the analysis metrics matched the metric report csv.