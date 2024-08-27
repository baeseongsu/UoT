# Reproducibility Report

## Repository Updates
- [x] Added `examiner` model: `gpt-4o`
- [x] Updated `guesser` model: `llama3-70b-instruct` (local-vllm)
- [x] Updated `helper` model: `gpt-4o-mini`
- [x] Fixed missed `inform` prompt (at conversation start) in Tables 11 and 17 for the `guesser` model

## Experimental Scripts

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
| llama3-70b  | DP (CS) + reminder            | 20q  | common  | 0.6486 | 13.9167 | 16.0541 |
| llama3-70b  | UoT (CS) + reminder           | 20q  | common  | 0.3874 | 9.6512  | 15.9910 |
| llama3-70b  | DP (CS) + informer + reminder | 20q  | common  | 0.8468 | 10.9787 | 12.3604 |
| llama3-70b  | UoT (CS) + informer + reminder| 20q  | common  | 0.8198 | 9.6154  | 11.4865 |
| llama3-70b  | DP (CS) + informer            | 20q  | common  | 0.8378 | 10.6022 | 12.1261 |

### Notes:
- SR↑: Success Rate (higher is better)
- MSC↓: Mean Successful Conversation length (lower is better)
- MCL↓: Mean Conversation Length (lower is better)
- Methods with "informer" use the `--inform_first` flag, which significantly improved performance in most cases.