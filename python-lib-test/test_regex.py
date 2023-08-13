################################################################################
# Test of reading a large JSON file                                            #
# * Data: City Lots San Francisco(https://github.com/zemirco/sf-city-lots-json)#
# * Library: re                                                                #
################################################################################

import os, sys, traceback
import psutil
import time
import re

################################################################################
# Functions                                                                    #
################################################################################
def print_memory_usage(message):
    print(f'*** MEMORY USAGE : {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2:.1f} MB ({message}) ***')

def test_regex_initial_part(input_filepath):
    print('##### Test re.finditer() : Get the initial LOT_NUM value #####')
    print_memory_usage('begin')
    start_time = time.time()

    lot_num_value = None
    lot_num_count = 0

    read_size = READ_BLOCK_SIZE
    margin_start = read_size - READ_MARGIN_SIZE
    margin_str = ''

    with open(input_filepath, 'r') as f:
        while True:
            data = f.read(read_size)
            if not data:
                break
            data = margin_str + data
            
            last_match_end = 0
            m = re.search(r'"LOT_NUM"\s*:\s*"(\w+)"', data)
            if m != None:
                last_match_end = m.span()[1]
                lot_num_value = m.group(1)
                lot_num_count += 1
                break
            
            if last_match_end < margin_start:
                last_match_end = margin_start

            margin_str = data[last_match_end:] if last_match_end < len(data) else ''

    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f} seconds')

    print_memory_usage('processing done')

    print(f'lot_num_value: {lot_num_value}')
    print(f'lot_num_count: {lot_num_count}')

def test_regex_last_part(input_filepath):
    print('##### Test re.finditer() : Get the last LOT_NUM value #####')
    print_memory_usage('begin')
    start_time = time.time()

    lot_num_value = None
    lot_num_count = 0

    read_size = READ_BLOCK_SIZE
    margin_start = read_size - READ_MARGIN_SIZE
    margin_str = ''
    
    with open(input_filepath, 'r') as f:
        while True:
            data = f.read(read_size)
            if not data:
                break
            data = margin_str + data
            
            last_match_end = 0
            for m in re.finditer(r'"LOT_NUM"\s*:\s*"(\w+)"', data):
                last_match_end = m.span()[1]
                lot_num_value = m.group(1)
                lot_num_count += 1
            
            if last_match_end < margin_start:
                last_match_end = margin_start

            margin_str = data[last_match_end:] if last_match_end < len(data) else ''
    
    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f} seconds')

    print_memory_usage('processing done')

    print(f'lot_num_value: {lot_num_value}')
    print(f'lot_num_count: {lot_num_count}')

################################################################################
# Configuration                                                                #
################################################################################

READ_BLOCK_SIZE = 1 * 1024
READ_MARGIN_SIZE = 20

################################################################################
# Main                                                                         #
################################################################################

def main():
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <json-file>')
        return

    input_filepath = sys.argv[1]
    
    test_regex_initial_part(input_filepath)
    #test_regex_last_part(input_filepath)

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc(file=sys.stdout)
