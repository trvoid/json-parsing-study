################################################################################
# Test of reading a large JSON file                                            #
# * Data: City Lots San Francisco(https://github.com/zemirco/sf-city-lots-json)#
# * Library: ijson                                                             #
################################################################################

import os, sys, traceback
import psutil
import time
import ijson

################################################################################
# Functions                                                                    #
################################################################################

def print_memory_usage(message):
    print(f'*** MEMORY USAGE : {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2:.1f} MB ({message}) ***')

def test_ijson_items_initial_part(input_filepath):
    print('##### Test ijson.items() : Get the initial LOT_NUM value #####')
    print_memory_usage('begin')
    start_time = time.time()

    lot_num_value = None
    lot_num_count = 0

    with open(input_filepath, 'r') as f:
        feature_items = ijson.items(f, 'features.item')

        print_memory_usage('after ijson.items(f)')

        for feature_item in feature_items:
            lot_num_value = feature_item['properties']['LOT_NUM']
            lot_num_count += 1
            break

    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f} seconds')

    print_memory_usage('processing done')

    print(f'lot_num_value: {lot_num_value}')
    print(f'lot_num_count: {lot_num_count}')

def test_ijson_items_last_part(input_filepath):
    print('##### Test ijson.items() : Get the last LOT_NUM value #####')
    print_memory_usage('begin')
    start_time = time.time()

    lot_num_value = None
    lot_num_count = 0

    with open(input_filepath, 'r') as f:
        feature_items = ijson.items(f, 'features.item')

        print_memory_usage('after ijson.items(f)')

        for feature_item in feature_items:
            lot_num_value = feature_item['properties']['LOT_NUM']
            lot_num_count += 1

    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f} seconds')

    print_memory_usage('processing done')

    print(f'lot_num_value: {lot_num_value}')
    print(f'lot_num_count: {lot_num_count}')

def test_ijson_parse_initial_part(input_filepath):
    print('##### Test ijson.parse() : Get the initial LOT_NUM value #####')
    print_memory_usage('begin')
    start_time = time.time()

    lot_num_value = None
    lot_num_count = 0

    with open(input_filepath, 'r') as f:
        parser = ijson.parse(f)

        print_memory_usage('after ijson.parse(f)')

        for prefix, event, value in parser:
            if prefix == 'features.item.properties.LOT_NUM':
                lot_num_value = value
                lot_num_count += 1
                break

    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f} seconds')

    print_memory_usage('processing done')

    print(f'lot_num_value: {lot_num_value}')
    print(f'lot_num_count: {lot_num_count}')

def test_ijson_parse_last_part(input_filepath):
    print('##### Test ijson.parse() : Get the last LOT_NUM value #####')
    print_memory_usage('begin')
    start_time = time.time()

    lot_num_value = None
    lot_num_count = 0

    with open(input_filepath, 'r') as f:
        parser = ijson.parse(f)
        
        print_memory_usage('after ijson.parse(f)')

        for prefix, event, value in parser:
            if prefix == 'features.item.properties.LOT_NUM':
                lot_num_value = value
                lot_num_count += 1

    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f} seconds')

    print_memory_usage('processing done')

    print(f'lot_num_value: {lot_num_value}')
    print(f'lot_num_count: {lot_num_count}')

################################################################################
# Main                                                                         #
################################################################################

def main():
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <json-file>')
        return

    input_filepath = sys.argv[1]
   
    #test_ijson_items_initial_part(input_filepath)
    #test_ijson_items_last_part(input_filepath)

    #test_ijson_parse_initial_part(input_filepath)
    test_ijson_parse_last_part(input_filepath)

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc(file=sys.stdout)
