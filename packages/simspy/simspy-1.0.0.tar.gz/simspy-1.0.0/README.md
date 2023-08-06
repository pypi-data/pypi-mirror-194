# simspy
This package is specifically designed for solving *single-machine scheduling problems*. It comprises a total of 8 functions, including 7 heuristic functions and 1 metaheuristic function.

### Heuristic Method
 - Earliest Due Date (EDD) Rule
 - Shortest Processing Time (SPT) Rule
 - Largest Penalty per Unit Length (LPUL) Rule
 - Shortest Processing Time and LPUL Rule
 - Shortest Weighted Processing Time (SWPT) Rule
 - Largest Weight (WT) and LPUL Rule
 - Critical Ratio (CR) Rule
 
### Metaheuristic Method
 - Genetic Algorithm (GA)

## Data Input
This package requires 3 essential data inputs: **Processing Time**, **Due Date**, and **Penalty**.

| Function | Description |
| -------- | ----------- |
| `fc_edd` | The Earliest Due Date Rule is utilized to solve single-machine scheduling problems. |
| `fc_spt` | The Shortest Processing Time Rule is utilized to solve single-machine scheduling problems. |
| `fc_lpul` | The Largest Penalty per Unit Length Rule is utilized to solve single-machine scheduling problems. |
| `fc_spt_lpul` | The Shortest Processing Time and LPUL Rule is utilized to solve single-machine scheduling problems. |
| `fc_swpt` | The Shortest Weighted Processing Time Rule is utilized to solve single-machine scheduling problems. |
| `fc_wt_lpul` | The Largest Weight and LPUL Rule is utilized to solve single-machine scheduling problems. |
| `fc_cr` | The Critical Ratio Rule is utilized to solve single-machine scheduling problems. |
| `fc_ga` | The Genetic Algorithm is utilized to solve single-machine scheduling problems. |
