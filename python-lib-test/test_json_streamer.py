################################################################################
# Test of reading a large JSON file                                            #
# * Data: City Lots San Francisco(https://github.com/zemirco/sf-city-lots-json)#
# * Library: json-streamer                                                     #
################################################################################

import os, sys, traceback
import psutil
import time
from jsonstreamer import JSONStreamer, ObjectStreamer

################################################################################
# Functions                                                                    #
################################################################################

def print_memory_usage(message):
    print(f'*** MEMORY USAGE : {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2:.1f} MB ({message}) ***')

def _catch_all_json_streamer(event_name, *args):
    global lot_num_flag
    global lot_num_value
    global lot_num_count

    if lot_num_flag:
        lot_num_flag = False
        lot_num_value = args[0]
        lot_num_count += 1
    else:
        if event_name == 'key' and args[0] == 'LOT_NUM':
            lot_num_flag = True

def _catch_all_object_streamer(event_name, *args):
    if event_name == 'pair':
        #print(f'\t{event_name} : {args[0]}')
        print(f'\t{event_name}')
    elif event_name == 'element':
        #print(f'\t{event_name} : {args[0]}')
        print(f'\t{event_name}')

def test_json_streamer_initial_part(input_filepath):
    print('##### Test JSONStreamer.consume() : Get the initial LOT_NUM value #####')
    print_memory_usage('begin')
    start_time = time.time()

    streamer = JSONStreamer()
    streamer.add_catch_all_listener(_catch_all_json_streamer)

    with open(input_filepath, 'r') as f:
        while True:
            partial_data = f.read(10 * 1024)
            if not partial_data:
                break
            streamer.consume(partial_data)
            if lot_num_count > 0:
                break

    streamer.close()

    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f} seconds')

    print_memory_usage('processing done')

    print(f'lot_num_value: {lot_num_value}')
    print(f'lot_num_count: {lot_num_count}')

def test_json_streamer_last_part(input_filepath):
    print('##### Test JSONStreamer.consume() : Get the last LOT_NUM value #####')
    print_memory_usage('begin')
    start_time = time.time()

    streamer = JSONStreamer()
    streamer.add_catch_all_listener(_catch_all_json_streamer)

    with open(input_filepath, 'r') as f:
        while True:
            partial_data = f.read(10 * 1024)
            if not partial_data:
                break
            streamer.consume(partial_data)

    streamer.close()

    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f} seconds')

    print_memory_usage('processing done')

    print(f'lot_num_value: {lot_num_value}')
    print(f'lot_num_count: {lot_num_count}')

def test_object_streamer(input_filepath):
    print('##### Test ObjectStreamer.consume()')
    print_memory_usage('begin')

    start_time = time.time()

    streamer = ObjectStreamer()
    streamer.add_catch_all_listener(_catch_all_object_streamer)

    with open(input_filepath, 'r') as f:
        while True:
            partial_data = f.read(10 * 1024)
            if not partial_data:
                break
            streamer.consume(partial_data)

    streamer.close()

    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f} seconds')

    print_memory_usage('processing done')

################################################################################
# Main                                                                         #
################################################################################

lot_num_flag = False
lot_num_value = None
lot_num_count = 0

def main():
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <json-file>')
        return

    input_filepath = sys.argv[1]
   
    #test_json_streamer_initial_part(input_filepath)
    test_json_streamer_last_part(input_filepath)
    #test_object_streamer(input_filepath)

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc(file=sys.stdout)
