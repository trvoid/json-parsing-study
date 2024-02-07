################################################################################
# Test of reading a large JSON file                                            #
# * Library: ujson                                                             #
################################################################################

import os, sys, traceback
import psutil
import time
import ujson

################################################################################
# Functions                                                                    #
################################################################################

def print_memory_usage(message):
    print(f'*** MEMORY USAGE : {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2:.1f} MB ({message}) ***')

def extract_ujson_installedAppList(input_filepath):
    print('##### Get the "installedAppList" values #####')
    print_memory_usage('begin')
    start_time = time.time()

    user_data_arr = []

    with open(input_filepath, 'r', encoding='utf-8') as f:
        data = ujson.loads(f.read())
        
        print_memory_usage('after ujson.load(f)')

        for user_i in range(0, len(data)):
            user_data = {}
            user_data['id'] = data[user_i]['id']
            user_data['device_model'] = ''
            user_data['app_list'] = []

            payload_data_arr = data[user_i]['payload']['data']
            for payload_data_sub_arr in payload_data_arr:
                for payload_data_obj in payload_data_sub_arr:
                    if payload_data_obj['identifier']['scheme'] == 'UserInfo':
                        if 'deviceModel' in payload_data_obj.keys():
                            user_data['device_model'] = payload_data_obj['deviceModel']
                        if 'installedAppList' in payload_data_obj.keys():
                            app_list = payload_data_obj['installedAppList']
                            for app_obj in app_list:
                                user_data['app_list'].append(app_obj['name'])

            user_data_arr.append(user_data)

    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f} seconds')

    print_memory_usage('processing done')

    for user_data in user_data_arr:
        print(f'{user_data["id"]} {user_data["device_model"]:25} {user_data["app_list"]}')

################################################################################
# Main                                                                         #
################################################################################

def main():
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <json-file>')
        return

    input_filepath = sys.argv[1]
   
    extract_ujson_installedAppList(input_filepath)

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc(file=sys.stdout)
