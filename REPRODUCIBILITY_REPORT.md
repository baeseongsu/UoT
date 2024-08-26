# Reproducibility Report

This document details the steps taken to reproduce the results from the UoT paper, using the updated experimental setup and models.

## Updates from the Original UoT GitHub Repository
- [x] Added `examiner` model for `gpt-4o`.
- [x] Updated `guesser` model to `llama3-70b-instruct` (local-vllm).
- [x] Updated `helper` model to `gpt-4o-mini`.
- [x] Fixed missed `inform` prompt (at the beginning of conversation) in Tables 11 and 17 for the `guesser` model.

## Experimental Scripts

### vllm-llama3-70b-instruct

```bash
# DP (CS)
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform

# UoT (CS)
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common

# DP (CS) with the first informer prompt
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform --inform_first

# UoT (CS) with the first informer prompt
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --inform_first
```

## Reproduced Results

The table below summarizes the results obtained from running the scripts mentioned above:

<!-- 
# DP (CS)
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform
Dialogue Count: 111
Success Rate: 0.6486486486486487
Mean Conversation Length in Successful Cases: 13.916666666666666
Mean Conversation Length: 16.054054054054053 
-->

<!-- 
# DP (CS) with the first informer prompt
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --naive_run --inform --inform_first
Success Rate: 0.8468468468468469
Mean Conversation Length in Successful Cases: 10.97872340425532
Mean Conversation Length: 12.36036036036036 
-->

<!-- 
# UoT (CS)
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common
Dialogue Count: 111
Success Rate: 0.36036036036036034
Mean Conversation Length in Successful Cases: 9.775
Mean Conversation Length: 16.315315315315317 
-->

<!-- 
# UoT (CS) with the first informer prompt
python run.py --guesser_model="vllm-llama3-70b-instruct" --examiner_model="gpt-4o" --task=20q --dataset=common --inform_first
Dialogue Count: 111
Success Rate: 0.8288288288288288
Mean Conversation Length in Successful Cases: 10.706521739130435
Mean Conversation Length: 12.297297297297296 
-->


| Model     | Method            | Task | Dataset | SR↑        | MSC↓                  | MCL↓                  |
|-----------|-------------------|------|---------|------------|-----------------------|-----------------------|
| llama3-70b | DP (CS)           | 20q  | common  | 0.6486     | 13.9167               | 16.0541               |
| llama3-70b | UoT (CS)          | 20q  | common  | 0.3604     | **9.7750**                | 16.3153               |
| llama3-70b | DP (CS), fixed    | 20q  | common  | **0.8468** | 10.9787           | 12.3604           |
| llama3-70b | UoT (CS), fixed   | 20q  | common  | 0.8288     | 10.7065               | **12.2973**               |

Notes:
- SR↑: Success Rate (higher is better)
- MSC↓: Mean Successful Conversation length (lower is better)
- MCL↓: Mean Conversation Length (lower is better)
- The best results in each column are highlighted in bold.

The "fixed" methods refer to the experiments run with the `--inform_first` flag, which seems to have significantly improved performance in most cases.