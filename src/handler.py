'''
IMPORTANT: This file is only used for testing purposes.
'''

import os
import time
import argparse


import runpod


# ----------------------------- Standard Handler ----------------------------- #
def handler(job):
    '''
    The handler function that will be called by the serverless.
    '''
    job_input = _side_effects(job['input'])

    # Prepare the job output
    job_output = job_input.get('mock_return', 'Hello World!')

    # Mock enabled refresh_worker
    if job_input.get('mock_refresh', False):
        job_output = {
            'refresh_worker': True,
            'mock_return': job_output
        }

    # Mock the job returning a value
    return job_output


# ----------------------------- Generator handler ---------------------------- #
def generator_handler(job):
    '''
    Generator type handler.
    '''
    job_input = _side_effects(job['input'])

    # Prepare the job output
    job_output = job_input.get('mock_return', ['Hello World!'])

    for output in job_output:
        yield output


# ------------------------------- Side Effects ------------------------------- #
def _side_effects(job_input):
    '''
    Modify the behavior of the handler based on the job input.
    '''
    # Mock the duration of the job
    time.sleep(job_input.get('mock_delay', 0))

    # Mock the job crashing the worker
    if job_input.get('mock_crash', False):
        os._exit(1)

    # Mock the job throwing an exception
    if job_input.get('mock_error', False):
        raise Exception('Mock error')  # pylint: disable=broad-exception-raised

    return job_input


# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--generator', action='store_true',
                        help='Starts serverless with the generator_handler')
    args = parser.parse_args()

    # Start the serverless worker
    if args.generator:
        runpod.serverless.start({"handler": generator_handler})

    runpod.serverless.start({"handler": handler})
