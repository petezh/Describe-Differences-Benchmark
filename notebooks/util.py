import json
import pickle as pkl
import numpy as np
import os
import random


def get_random_score_from_spec(spec):
    pos, neg = spec['pos'], spec['neg']
    return {
        'pos2score': {t: random.random() for t in pos},
        'neg2score': {t: random.random() for t in neg},
        'pos2highlight': [],
        'neg2highlight': []
    }


def load_jsonl(path):
    result = []
    with open(path, 'r') as in_file:
        for l in in_file:
            result.append(json.loads(l))
    return result


def write_job(spec):
    i = 0
    while os.path.exists('JOBS/%d/' % i):
        i += 1
    job_folder = os.path.join('JOBS/%d/' % i)
    os.mkdir(job_folder)
    spec_path = os.path.join(job_folder, 'spec.pkl')
    print('writing to folder %s' % job_folder)
    print('note: ', spec['note'])
    pkl.dump(spec, open(spec_path, 'wb'))
    
    get_extrem_result_path = os.path.join(job_folder, 'get_extreme_result.pkl')
    
    pkl.dump(get_random_score_from_spec(spec), open(get_extrem_result_path, 'wb'))


def parse_ai2_instruction(instruction):
    flattened_input = instruction.split('input: ')[-1].replace('output:', '').strip()
    return flattened_input


def get_all_fields(s):
    segs = s.split(':')
    last_words = {seg.split(' ')[-1].strip() for seg in segs[:-1]}
    last_words = {w for w in last_words if w != ''}
    return last_words


def parse_by_input_field(s, input_fields):
    if len(input_fields) != 0:
        d = {}
        f2starts = {f: s.index(f + ':') for f in input_fields}
        input_fields = sorted(f2starts, key=lambda f: f2starts[f])
        starts = [f2starts[f] for f in input_fields]
        
        
        for i, input_field in enumerate(input_fields):
            start = starts[i]
            end = len(s)
            if i != len(input_fields) - 1:
                end = starts[i + 1]
            d[input_field] = s[start:end].replace(input_field + ':', '').strip().rstrip(',')
        return d
    else:
        return {'whole': s}


def load_predictions_from_jsonl(path):
    raw_results = load_jsonl(path)
    raw_inputs = [parse_ai2_instruction(d['input']) for d in raw_results]
    input_fields = get_all_fields(raw_inputs[0])
    for raw_input in raw_inputs:
        input_fields &= get_all_fields(raw_input)
    
    for i in range(len(raw_results)):
        for k, v in parse_by_input_field(raw_inputs[i], input_fields).items():
            raw_results[i]['parsed_input-' + k] = v

    return raw_results
    

def write_gpt3_json(data_dicts, out_path):
    with open(out_path, 'w') as out_file:
        for d in data_dicts:
            out_file.write(json.dumps(d) + '\n')
            
def html_escape(text):
    import html
    return html.escape(text)

            
def distribute_t5(model):
    import torch
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device_count = torch.cuda.device_count()
    if device_count == 6:
        device_map = {
            0: [0, 1, 2],
            1: [3, 4, 5, 6],
            2: [7, 8, 9, 10, 11],
            3: [12, 13, 14, 15],
            4: [16, 17, 18, 19],
            5: [20, 21, 22, 23]
        }
        model.parallelize(device_map)

    elif device_count == 5:
        device_map = {
            0: [0, 1, 2],
            1: [3, 4, 5, 6, 7, 8],
            2: [9, 10, 11, 12, 13, 14],
            3: [15, 16, 17, 18, 19, 20],
            4: [21, 22, 23]
        }
        model.parallelize(device_map)
    elif device_count == 4:
        device_map = {
            0: [0, 1, 2],
            1: [3, 4, 5, 6, 7, 8, 9],
            2: [10, 11, 12, 13, 14, 15, 16],
            3: [17, 18, 19, 20, 21, 22, 23]
        }
        model.parallelize(device_map)
    elif device_count == 3:
        device_map = {
            0: [0, 1, 2, 3, 4, 5],
            1: [6, 7, 8, 9, 10, 11, 12, 13, 14],
            2: [15, 16, 17, 18, 19, 20, 21, 22, 23],
        }
        model.parallelize(device_map)
    elif device_count == 2:
        device_map = {
            0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            1: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        }
        model.parallelize(device_map)
    else:
        model.to(device)


def get_html_highlight(text, span2weights, max_alpha=None):
    result_str, cur_start = '', 0
    
    all_weights = np.array(sorted(list(span2weights.values())))
    if max_alpha is None:
        max_alpha = np.max(all_weights)
    
    def f(x):
        if x < np.percentile(all_weights, q=80):
            return 0
        return (x / max_alpha)
    
    end = 0
    for (start, end_), weight in span2weights.items():
        end = end_
        if start > cur_start:
            result_str += text[cur_start:start]
        word = text[start:end]
        cur_start = end
        result_str += '<span style="background-color:rgba(135,206,250,' + str(f(weight)) + ');">' + html_escape(word) + '</span>'
    if end != len(text):
        result_str += text[end:len(text)]
    return result_str


def parse_pred_file_name(f_name):
    n = f_name.split('.')[0]
    toks = n.split('_')
    task_number = int(toks[1].replace('task', ''))
    name = '_'.join(toks[2:-1])
    classification = toks[-1] == 'classification'
    return {
        'number': task_number,
        'name': name,
        'classification': classification,
        'f_name': f_name
    }
    
    

if __name__ == '__main__':
#     extreme_results = pkl.load(open('JOBS/47/get_extreme_result.pkl', 'rb'))
#     pos2highlight = extreme_results['pos2highlight']
    
#     for pos, span2weight in pos2highlight.items():
#         t = get_html_highlight(pos, span2weight)
#         print(t)
    
    exit(0)

