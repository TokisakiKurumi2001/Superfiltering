import json
import numpy as np
import argparse
from tqdm import tqdm
import math
from loguru import logger

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_data_path", type=str, default='alpaca_data_gpt2_data.json')
    parser.add_argument("--json_save_path", type=str, default='alpaca_data_gpt2_data_10per.json')
    parser.add_argument("--sample_rate", type=float, default=None)
    parser.add_argument("--sample_num", type=int, default=None)
    parser.add_argument("--filter_threash", type=float, default=1)
    parser.add_argument("--key_name", type=str, default='ifd_ppl',help='ifd_ppl')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    print(args)

    json_data = []
    with open(args.json_data_path) as fin:
        for line in fin:
            d = json.loads(line)
            json_data.append(d)
    if args.sample_num is None and args.sample_rate is None:
        assert "sample_num and sample_rate cannot be stimutaneously None"
    elif args.sample_rate is None:
        sample_num = args.sample_num
    else:
        sample_num = int(len(json_data) * args.sample_rate)

    def sort_key(x):
        # Check if the value is nan
        if math.isnan(x[args.key_name]):
            return (0, 0) 
        return (1, x[args.key_name]) 

    filtered_data = [x for x in json_data if (isinstance(x[args.key_name], (int, float)) and x[args.key_name] < args.filter_threash)]
    new_data = sorted(filtered_data, key=sort_key, reverse=True)

    new_data = new_data[:sample_num]
    
    with open(args.json_save_path, 'w+') as fout:
        for d in new_data:
            fout.write(json.dumps(d) + "\n")
    
    logger.success(f'Done! Data Selection has sample {len(new_data)}')

if __name__ == '__main__':
    main()