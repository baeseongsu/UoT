import os
import json
import argparse
import pickle

from tqdm import tqdm

from uot.tasks import get_task
from uot.method import converse, naive_converse
from uot.eval import evaluate_performance


def run(args):
    task = get_task(args)

    args.task_start_index = max(args.task_start_index, 0)
    if args.task_end_index < 0:
        args.task_end_index = len(task.data)
    else:
        args.task_end_index = min(args.task_end_index, len(task.data))

    if args.naive_run:
        log_file = (f'./logs/{args.task}/{args.guesser_model}_as_guesser/{args.dataset}_{args.temperature}'
                    f'_naive_{"" if args.inform else "un"}inform_EXAMINER{args.examiner_model}'
                    f'_{args.task_start_index}-{args.task_end_index}.json')
    else:
        log_file = (f'./logs/{args.task}/{args.guesser_model}_as_guesser/'
                    f'{f"OS_init{args.open_set_size}_renew{args.size_to_renew}_" if args.open_set_size > 0 else ""}'
                    f'{f"pre{args.n_pre_ask}_" if args.n_pre_ask > 0 else ""}'
                    f'{args.dataset}_{args.temperature}_lambda{args.reward_lambda}_acc{not args.none_acc_reward}'
                    f'_exp{args.expected_reward_method}_L{args.n_extend_layers}_K{args.n_potential_actions}'
                    f'_PRUN{args.n_pruned_nodes}_EXAMINER{args.examiner_model}'
                    f'_{args.task_start_index}-{args.task_end_index}.json')
        root_file = (f'./roots/{args.task}/{args.guesser_model}'
                     f'{f"OS_init{args.open_set_size}_" if args.open_set_size > 0 else ""}'
                     f'_{args.dataset}_{args.temperature}_root.pickle')
        if os.path.exists(root_file):
            r = open(root_file, 'rb')
            root = pickle.load(r)
            task.create_root(root)
        else:
            os.makedirs(os.path.dirname(root_file), exist_ok=True)
            task.create_root()
            pickle.dump(task.root, open(root_file, 'wb'))
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.loads(f.readline())
        args.task_start_index = len(logs)

    for i in tqdm(range(args.task_start_index, args.task_end_index)):
        if args.naive_run:
            log = naive_converse(task, i)
        else:
            log = converse(task, i)
            pickle.dump(task.root, open(root_file, 'wb'))
        logs.append(log)
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(logs) + '\n')

    evaluate_performance(log_file, task)


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--guesser_model', type=str, default='gpt-3.5-turbo',
                      choices=['gpt-4', 'gpt-3.5-turbo',
                               '_claude-2', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229',
                               'palm-2', 'cohere', 'llama-2-70b-chat',
                               'mistral-small-latest', 'mistral-medium-latest', 'mistral-large-latest',
                               'gemma', 'gemini-1.0-pro', 'vllm-llama3-70b-instruct'])
    args.add_argument('--temperature', type=float, default=0)
    args.add_argument('--examiner_model', type=str, default='gpt-4', choices=['gpt-4', 'gpt-4o'])

    args.add_argument('--task', type=str, default='20q',
                      choices=['20q', 'md', 'tb'])
    args.add_argument('--dataset', type=str, default='common',
                      choices=['bigbench', 'common', 'thing', 'DX', 'MedDG', 'FloDial'])
    args.add_argument('--task_start_index', type=int, default=-1)
    args.add_argument('--task_end_index', type=int, default=-1)
    args.add_argument('--open_set_size', type=int, default=-1)
    args.add_argument('--size_to_renew', type=int, default=-1)  # only used when open_set_size > 0
    args.add_argument('--n_pre_ask', type=int, default=0)  # only used when open_set_size > 0 and data doesn't contain self-repo

    args.add_argument('--naive_run', action='store_true', default=False)
    args.add_argument('--inform', action='store_true', default=False)  # only used when naive_run

    args.add_argument('--reward_lambda', type=float, default=0.4)
    args.add_argument('--n_extend_layers', type=int, default=3)
    args.add_argument('--n_potential_actions', type=int, default=3)
    args.add_argument('--n_pruned_nodes', type=float, default=0)
    # not prun when = 0
    # exact number when > 0 (e.g. 10: Each layer has a maximum of 10 nodes, M or U, remaining)
    # percentage when < 0 (e.g. -0.5: The remaining 50% of nodes in each layer)

    args.add_argument('--expected_action_tokens', type=int, default=50)
    args.add_argument('--expected_target_tokens', type=int, default=10)

    args.add_argument('--none_acc_reward', action='store_true', default=False)
    args.add_argument('--expected_reward_method', type=str, default='avg', choices=['avg', 'max'])

    args = args.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    run(args)
