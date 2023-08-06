import json
import os
import sys
import time
from pandas import DataFrame

sys.path.append(os.getcwd())

from prompt import PromptSet, PromptLoader
from api import APIWrapper

def querylm(dataset_infer, prompt_schema_infer,
            backend, engine_name, keys,
            dataset_demo = None, prompt_schema_demo = None,
            context_schema = None,
            batch_size = 1, num_workers = 1,
            request_per_minute=1, use_cache=True):

    prompt_infer = PromptSet(dataset_infer, prompt_schema=prompt_schema_infer)

    prompt_demo = None
    if dataset_demo != None and prompt_schema_demo != None:
        prompt_demo = PromptSet(dataset_demo, prompt_schema=prompt_schema_demo)

    prompt_loader = PromptLoader(prompt_infer=prompt_infer, prompt_demo=prompt_demo,
                                 context_schema=context_schema,
                                 batch_size=batch_size, num_workers=num_workers)

    api = APIWrapper(backend=backend, engine_name=engine_name, keys=keys,
                     request_per_minute=request_per_minute)

    outputs = []
    for input_batch in prompt_loader:
        output = inference(input_batch, api, use_cache=use_cache)
        outputs.append(output)
    return outputs

def inference(prompt_batch, api, use_cache):
    response = api.infer(prompt_batch)
    return response


def test():
    dataset = {'text': ['This is a test: ', 'This is a test: ']}
    dataset_df = DataFrame(dataset)
    prompt_schema = ''

    backend = 'openai'
    engine = 'text-davinci-003'
    keys = [{'key': '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'}] # json list

    result = querylm(dataset_df, prompt_schema, backend, engine, keys)
    print (result)



if __name__ == '__main__':
    test()