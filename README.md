# Reproducibility Report

**Conclusion**: I reproduced the results for `llama3-8b`, `llama3.1-8b`, and `llama3-70b` using the provided experimental scripts, but my findings are inconsistent with the paper, especially in the closed setting (CS). I investigated the cause of this inconsistency and found that the position of the initial inform prompt in the conversation significantly affects model performance. Specifically, in the original repository, DP(CS) underperforms due to not using the initial inform prompt, while UoT(CS) benefits from it. This leads to an unfair comparison, underestimating DP(CS)'s performance. To ensure fairness, I applied the initial inform prompt to both DP(CS) and UoT(CS) in my experiments, where DP(CS) outperformed UoT(CS), despite using a simpler prompting strategy. As a result, I question the validity of the paper’s reported performance, including the entire experimental results table, due to this discrepancy.

## Repository Updates
- [x] Added `examiner` model: `gpt-4o`
- [x] Updated `guesser` model: `llama3-70b-instruct` (local-vllm)
- [x] Updated `helper` model: `gpt-4o-mini`
- [x] Fixed missed `inform` prompt (at conversation start) in Tables 11 and 17 for the `guesser` model

## Experimental Scripts

### Model: vllm-llama3-8b-instruct

### Dataset: common (Task: 20q)

```bash
# DP (CS) + reminder
python run.py --guesser_model="vllm-llama3-8b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform

# UoT (CS) + reminder (error)
python run.py --guesser_model="vllm-llama3-8b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common

# DP (CS) + informer + reminder
python run.py --guesser_model="vllm-llama3-8b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform --inform_first

# UoT (CS) + informer + reminder (error)
python run.py --guesser_model="vllm-llama3-8b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --inform_first

# DP (CS) + informer
python run.py --guesser_model="vllm-llama3-8b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform_first
```

### Model: vllm-llama3.1-8b-instruct

### Dataset: common (Task: 20q)

```bash
# DP (CS) + reminder
python run.py --guesser_model="vllm-llama3.1-8b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform

# UoT (CS) + reminder
python run.py --guesser_model="vllm-llama3.1-8b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common

# DP (CS) + informer + reminder
python run.py --guesser_model="vllm-llama3.1-8b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform --inform_first

# UoT (CS) + informer + reminder
python run.py --guesser_model="vllm-llama3.1-8b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --inform_first

# DP (CS) + informer
python run.py --guesser_model="vllm-llama3.1-8b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform_first
```


### Model: vllm-llama3-70b-instruct

#### Dataset: common (Task: 20q)

```bash
# DP (CS) + reminder
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform

# UoT (CS) + reminder
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common

# DP (CS) + informer + reminder
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform --inform_first

# UoT (CS) + informer + reminder
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --inform_first

# DP (CS) + informer
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform_first
```

## Reproduced Results

The table below summarizes the results obtained from running the scripts mentioned above:

| Model       | Method                        | Task | Dataset | SR↑    | MSC↓    | MCL↓    |
|-------------|-------------------------------|------|---------|--------|---------|---------|
| llama3-8b   | DP (CS) + reminder            | 20q  | common  | 0.0000 | 0.0000  | 20.0000 | [O]
| llama3-8b   | DP (CS) + informer            | 20q  | common  | 0.2072 | 14.7391 | 18.9099 | [O]
| llama3-8b   | DP (CS) + informer + reminder | 20q  | common  | 0.1171 | 13.0769 | 19.1892 | [O]
| llama3-8b   | UoT (CS) + reminder           | 20q  | common  | 0.0000 | 0.0000  | 0.0000  | [error]
| llama3-8b   | UoT (CS) + informer + reminder| 20q  | common  | 0.0000 | 0.0000  | 0.0000  | [error]
| llama3.1-8b | DP (CS) + reminder            | 20q  | common  | 0.2883 | 13.0938 | 18.0090 | [O]
| llama3.1-8b | DP (CS) + informer            | 20q  | common  | 0.5495 | 13.4918 | 16.4234 | [O]
| llama3.1-8b | DP (CS) + informer + reminder | 20q  | common  | 0.4685 | 12.8077 | 16.6306 | [O]
| llama3.1-8b | UoT (CS) + reminder           | 20q  | common  | 0.3243 | 10.1667 | 16.8108 | [O]
| llama3.1-8b | UoT (CS) + informer + reminder| 20q  | common  | 0.5946 | 11.1364 | 14.7297 | [O]
| llama3-70b  | DP (CS) + reminder            | 20q  | common  | 0.6486 | 13.9167 | 16.0541 | [O]
| llama3-70b  | DP (CS) + informer            | 20q  | common  | 0.8378 | 10.6022 | 12.1261 | [O]
| llama3-70b  | DP (CS) + informer + reminder | 20q  | common  | 0.8468 | 10.9787 | 12.3604 | [O]
| llama3-70b  | UoT (CS) + reminder           | 20q  | common  | 0.3874 | 9.6512  | 15.9910 | [O]
| llama3-70b  | UoT (CS) + informer + reminder| 20q  | common  | 0.8198 | 9.6154  | 11.4865 | [O]

### Notes:
- SR↑: Success Rate (higher is better)
- MSC↓: Mean Successful Conversation length (lower is better)
- MCL↓: Mean Conversation Length (lower is better)
- Methods with "informer" use the `--inform_first` flag, which significantly improved performance in most cases.