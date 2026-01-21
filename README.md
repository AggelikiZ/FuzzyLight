# FuzzyLight – Modifications and Experimental Setup

This repository contains a **modified version of the FuzzyLight traffic
signal control framework**, developed as part of an academic project.
The goal of this work is to align the implementation more closely with
the conceptual design described in the original paper and to explore
improvements in robustness, fairness, and interpretability.

The original README describing the baseline FuzzyLight implementation is
preserved separately for reference.

---

## 1. Overview

The original FuzzyLight framework proposes a **two-stage traffic signal
control strategy**:

1. **Deterministic phase selection** using fuzzy logic and compressed sensing  
2. **Reinforcement learning–based phase duration control**

While the paper clearly separates these two stages conceptually, this
separation is not always explicit in the released reference
implementation. This project introduces targeted modifications to
re-establish this separation and extend the system with explicit
starvation-aware fuzzy phase selection.

---

## 2. Summary of Modifications

The main modifications introduced in this work are:

- Hierarchical action representation  
- Explicit fuzzy phase selection  
- Starvation-aware phase prioritization  
- Unchanged reward function for fair comparison  
- Additional evaluation metrics (starvation analysis)

Each modification is described in detail below.

---

## 3. Action Redefinition (Hierarchical Control)

### Original behavior

In the reference implementation, reinforcement learning operates over a
flat discrete action space, where each action implicitly encodes both:

- the selected traffic signal phase, and  
- the corresponding green time duration  

This allows the learning agent to indirectly influence phase selection.

### Modified behavior

We reformulate the control process as a **two-stage hierarchical
decision mechanism**:

1. **Stage 1 – Phase selection (deterministic)**  
   Phase selection is performed independently of reinforcement learning
   using a rule-based or fuzzy policy.

2. **Stage 2 – Phase duration control (reinforcement learning)**  
   Reinforcement learning is restricted to selecting the green time
   duration for the already selected phase.

This change enforces the safety-critical nature of phase selection while
preserving adaptability in duration control.

**Relevant files:**
```text
models/network_agent.py
models/fuzzy_light.py
```

## 4. Fuzzy Phase Selection with Starvation Awareness

### Original behavior

In the reference implementation, phase selection is based on a
pressure-like heuristic that considers only instantaneous traffic
demand, computed from aggregated lane queue lengths.

While effective in many cases, this approach does not explicitly
consider **phase starvation**, potentially leading to unfair serving of
low-demand phases under sustained congestion.

### Modified behavior

This work introduces an **explicit fuzzy phase selection mechanism**
that jointly considers:

- **Traffic demand**, computed as the aggregated queue length per phase
- **Phase starvation**, defined as the number of consecutive decision
  steps during which a phase has not been selected

Both variables are mapped to fuzzy linguistic variables using
trapezoidal membership functions. A deterministic fuzzy scoring rule is
then applied to compute a priority score for each phase, and the phase
with the highest score is selected.

This modification improves fairness by reducing prolonged starvation,
while preserving deterministic and safety-critical operation.

**Relevant files:**
```text
models/fuzzy_light.py
```

## 5. Reward Function

The **original reward function is intentionally preserved** and is not
modified in this work. This decision was made to ensure a fair and
direct comparison with the reference implementation provided by the
authors.

The reward is based on congestion-related quantities such as:

- traffic pressure
- lane queue length

No starvation-related terms are included in the reward signal.

Starvation is instead treated as an **evaluation metric**, not as a
learning objective. This separation allows us to study fairness effects
without altering the optimization target of the reinforcement learning
agent.

---

## 6. Additional Evaluation Metrics

In addition to the metrics reported in the original FuzzyLight paper
(Average Travel Time and Throughput), we introduce an explicit metric to
quantify **phase starvation**.

### Starvation Metric

We use the following starvation-related metrics extracted from the
simulation logs:

- `starved_120`: number of starvation events exceeding 120 seconds

To enable fair comparison across different traffic volumes, normalized
variants are also computed:

- `starved_120 / vehicle_in`
- `starved_120 / vehicle_out`

These metrics are **not used during training** and are computed
offline for evaluation purposes only.

---

## 7. Experimental Setup

### 7.1 Traffic Simulator

All experiments are conducted using the **CityFlow traffic simulator**,
which is built and installed from source, using Docker,  following the official
documentation:

https://cityflow.readthedocs.io/en/latest/install.html

CityFlow provides a realistic, step-based traffic simulation environment
and supports large-scale urban road networks.

---

### 7.2 Execution Environment

To ensure reproducibility and consistent dependency management, all
experiments are executed inside a **Docker container**.

The container environment includes:

- Python 3.10
- TensorFlow 2.13.1
- CityFlow 
- All required system dependencies

Due to limited computational resources (in particular, the absence of a
high-end GPU), experiments are conducted with:

- reduced traffic demand
- fewer simulated vehicles compared to the original paper

All algorithm variants are evaluated under **identical conditions**,
ensuring that relative comparisons remain meaningful.

---

## 8. Running the Experiments

> **Important**  
> The different algorithm variants (**Baseline**, **Stage 2**, and
> **Stage 1 + Stage 2**) are **not selected via command-line flags**.

Instead, variants are enabled by **manually commenting and uncommenting
specific code blocks** in the source files. This design choice allows
precise experimental control and avoids unintended interactions between
variants.

---

### 8.1 Main Execution Script

All experiments are launched using the provided shell script:

```bash
run.sh
```
### 8.1 Main Εvaluation Script

The evaluation of the experiments is executed using the file:

```bash
summary.py
```
This has been slightly modified also to utilize the new metrics mentioned above.



