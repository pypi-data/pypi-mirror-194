#  """
#    Copyright (c) 2016- 2023, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """
import logging
import os.path
import PySimpleGUI as Sg
import datetime
import time
import pandas as pd
import threading

from wiliot.wiliot_core.utils import WiliotDir, check_user_config_is_ok
from wiliot.wiliot_cloud.manufacturing.manufacturing import ManufacturingClient
from wiliot.wiliot_testers.tester_utils import upload_to_cloud_api, SerializationWorker
from math import ceil
from queue import Queue

BATCH_SIZE = 50
MAX_NUM_TAGS = 6000
MAX_NUM_WORKERS = 50
MAX_RETRIALS = 10
MIN_DELAY_BETWEEN_BATCHES = 0
ENV = ''  # Leave empty for prod
OWNER = 'wiliot-ops'


def get_files_path():
    """
    opens GUI for selecting a file and returns it
    """
    # Define the window's contents
    layout = [[Sg.Text('Choose run data file that you want to upload:'), Sg.Input(key="run_data_file"),
               Sg.FileBrowse()],
              [Sg.Text('Choose packets data file that you want to upload:'), Sg.Input(key="tags_data_file"),
               Sg.FileBrowse()],
              [Sg.Checkbox(text='serialize only', key='serialize_only', enable_events=False)],
              [Sg.Text('environment:'),
               Sg.InputCombo(('prod', 'test'), default_value="prod", key='env')],
              [Sg.Text('Tester type:'),
               Sg.InputCombo(('offline-tester', 'sample-test'), default_value="offline-tester", key='tester_type')],
              [Sg.Button('Select')]]
    
    # Create the window
    window = Sg.Window('upload and serialize', layout)
    
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == 'Select' and (values['run_data_file'] != '' or values['tags_data_file'] != ''):
        window.close()
        return values
    else:
        window.close()
        return None


def create_summary_message(is_upload=True, is_serialization=True):
    """
    summary log
    :param is_upload:
    :type is_upload: bool or None
    :param is_serialization:
    :type is_serialization: bool or None
    :return:
    :rtype:
    """
    sum_msg_prefix = '\n\n\n***********************************************\n'
    sum_msg_suffix = '***********************************************\n'
    sum_msg_upload = '********* UPLOAD: files were uploaded *********\n'
    sum_msg_serial = '*** SERIALIZE: serialization was successful ***\n'
    sum_msg = sum_msg_prefix
    if is_upload is not None:
        sum_msg += sum_msg_upload
        if not is_upload:
            sum_msg = sum_msg.replace('were', 'were NOT')
    if is_serialization is not None:
        sum_msg += sum_msg_serial
        if not is_serialization:
            sum_msg = sum_msg.replace('successful', 'failed')
    sum_msg += sum_msg_suffix
    return sum_msg


def upload_and_serialize_data_from_file(values=None, logger=None, log_path=None, client=None, is_packet_data=False):
    if values is None:
        values = get_files_path()
    if values is None:
        print('user exited the program')
        return False
    
    if log_path is None:
        if os.path.isfile(values['run_data_file']):
            files_dir = os.path.dirname(values['run_data_file'])
        elif os.path.isfile(values['tags_data_file']):
            files_dir = os.path.dirname(values['run_data_file'])
        else:
            env_dir = WiliotDir()
            files_dir = os.path.join(env_dir.get_tester_dir("serialization"), "logs")
            if not os.path.isdir(files_dir):
                env_dir.create_dir(files_dir)
        log_path = os.path.join(files_dir,
                                datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + 'serialization_log.log')
    
    if logger is None:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S'))
        file_handler.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S'))
        stream_handler.setLevel(logging.DEBUG)
        logger = logging.getLogger('Manual Upload')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    
    else:
        logger = logging.getLogger(logger)

    tags_or_packets = values['tags_data_file'].split('@')[-1]
    if 'packets_data' in tags_or_packets:
        is_packet_data = True
    if values['run_data_file'] != '' and not values['run_data_file'].endswith('.csv'):
        logger.warning('SERIALIZATION: run_data file format is not csv, please insert a csv file')
        logger.info(create_summary_message(False, False))
        return False
    if values['tags_data_file'] != '' and not values['tags_data_file'].endswith('.csv'):
        logger.warning('SERIALIZATION: tags_data file format is not csv, please insert a csv file')
        logger.info(create_summary_message(False, False))
        return False
    
    batch_name, run_data_csv_name, tags_data_csv_name = None, None, None
    
    if values['run_data_file'] != '':
        batch_name = values['run_data_file'][:(len(values['run_data_file']) -
                                               len(values['run_data_file'].split("/")[-1]))]
        run_data_csv_name = values['run_data_file'].split('/')[-1]
    if values['tags_data_file'] != '':
        if batch_name is None:
            batch_name = values['tags_data_file'][:(len(values['tags_data_file']) -
                                                    len(values['tags_data_file'].split("/")[-1]))]
        tags_data_csv_name = values['tags_data_file'].split('/')[-1]
    if batch_name is None:
        logger.warning('SERIALIZATION: no files were selected, will exit the program')
        logger.info(create_summary_message(False, False))
        return False
    
    upload_success = None
    serialization_success = None
    if not values['serialize_only']:
        if is_packet_data and values['tester_type'] == 'offline-tester':
            values['tester_type'] = 'offline-test'
        upload_success = upload_to_cloud_api(batch_name=batch_name, tester_type=values['tester_type'],
                                             run_data_csv_name=run_data_csv_name, tags_data_csv_name=tags_data_csv_name,
                                             to_logging=True, env=values['env'], is_batch_name_inside_logs_folder=False,
                                             logger_=logger.name, packets_instead_tags=is_packet_data)
    
    else:
        try:
            tags_df = pd.read_csv(values['tags_data_file'], )
            if is_packet_data:
                all_adv = tags_df['adv_address'].unique()
                dict_for_serialization = {'advAddress': [], 'status': [], 'externalId': [], 'raw_packet': []}
                for adv in all_adv:
                    if pd.isnull(adv):
                        continue
                    adv_df = tags_df.loc[(tags_df['adv_address'] == adv) & (tags_df['selected_tag'] == adv)]
                    if len(adv_df):
                        adv_df_first = adv_df.iloc[0]
                        dict_for_serialization['advAddress'].append(adv_df_first['adv_address'])
                        dict_for_serialization['status'].append(adv_df_first['status_offline'])
                        dict_for_serialization['externalId'].append(adv_df_first['external_id'])
                        dict_for_serialization['raw_packet'].append(adv_df_first['raw_packet'])
                tags_df = dict_for_serialization

        except Exception as e:
            logger.warning('SERIALIZATION: unable to get data from csv: {}'.format(e))
            logger.info(create_summary_message(is_upload=upload_success, is_serialization=False))
            return False

        if client is None:
            file_path, api_key, is_successful = check_user_config_is_ok(env=ENV)
            client = ManufacturingClient(api_key=api_key, env=ENV, logger_=logger.name)
        else:
            client = client

        batch_num_queued = 0
        num_workers = 0
        num_tags = 0
        adv_address = []
        packet = []
        serialization_threads_working = []
        next_batch_to_serialization = {'response': '', 'upload_data': []}
        failed_tags_counter = 0
        failed_tags_list = []

        pre_ser_batch_q = Queue()
        post_ser_batch_q = Queue()
        failed_tags_q = Queue()

        try:
            num_tags = len(tags_df['advAddress'])
            if MAX_NUM_TAGS != 0 and num_tags > MAX_NUM_TAGS:
                num_tags = MAX_NUM_TAGS
            
            num_batches = ceil(num_tags / BATCH_SIZE)
            
            num_workers = min(MAX_NUM_WORKERS, ceil(num_batches / 5))
            for i in range(num_workers):
                serialization_threads_working.append(
                    SerializationWorker(client=client, input_q=pre_ser_batch_q, output_q=post_ser_batch_q,
                                        failed_tags_q=failed_tags_q, max_retrials=MAX_RETRIALS))
                serialization_threads_working[-1].start()

            # serialization part
            for tag in range(num_tags):
                if tags_df['status'][tag] == 'Failed' or tags_df['status'][tag] == 0 or tags_df['status'][tag] == '0':
                    failed_tags_list.append(tags_df['externalId'][tag])
                    failed_tags_counter += 1
                    continue
                elif tags_df['status'][tag] == '':
                    continue
                external_id_tmp = None
                packet_tmp = None
                try:
                    external_id_tmp = tags_df['externalId'][tag]
                    if pd.isnull(external_id_tmp):
                        print('row #{} has no external id. continue to the next row'.format(tag))
                        continue
                    if 'rawData' in tags_df:
                        packet_tmp = tags_df['rawData'][tag].split('"')[5]
                    elif 'raw_packet' in tags_df:
                        packet_tmp = tags_df['raw_packet'][tag]
                    else:
                        raise Exception('no packet data available for serialization')
                except Exception as e:
                    if (external_id_tmp is None or pd.isnull(external_id_tmp)) and \
                            (packet_tmp is None or pd.isnull(packet_tmp)):
                        print('row #{} has none data. continue to the next row'.format(tag))
                        continue
                    else:
                        raise Exception('error to extract data from row #{} with the following exception:{}'.
                                        format(tag, e))
                adv_address.append(external_id_tmp)
                packet.append(packet_tmp)
                
                if len(next_batch_to_serialization['upload_data']) == 0:
                    next_batch_to_serialization = {'response': '',
                                                   'upload_data': [{"payload": packet_tmp[16:74],
                                                                    "tagId": external_id_tmp}],
                                                   'writing_lock': threading.Lock()}
                else:
                    next_batch_to_serialization['upload_data'].append({"payload": packet_tmp[16:74],
                                                                       "tagId": external_id_tmp})
                
                # tag_idx = tag + 1
                if len(next_batch_to_serialization['upload_data']) == BATCH_SIZE:
                    logger.info("SERIALIZATION: Batch {} has Added {} tags for serialization, upload data {}".format(
                        str(batch_num_queued + 1), len(next_batch_to_serialization['upload_data']),
                        next_batch_to_serialization['upload_data']))
                    pre_ser_batch_q.put(next_batch_to_serialization)
                    batch_num_queued += 1
                    next_batch_to_serialization = {'response': '', 'upload_data': []}
            
            # add the last group to serialization:
            if len(next_batch_to_serialization['upload_data']) > 0:
                logger.info("SERIALIZATION: Batch {} has Added {} tags for serialization, upload data {}".format(
                    str(batch_num_queued + 1), len(next_batch_to_serialization['upload_data']),
                    next_batch_to_serialization['upload_data']))
                pre_ser_batch_q.put(next_batch_to_serialization)
                batch_num_queued += 1
            
            # Status prints:
            max_iterations = 10 * num_tags / (BATCH_SIZE * num_workers)
            idle_time = 10
            iter_num = 0
            while post_ser_batch_q.qsize() < batch_num_queued and iter_num < max_iterations:
                time.sleep(10)
                logger.info(
                    "SERIALIZATION: After {} seconds: "
                    "finished {} batches out of {} ({}%)".format(iter_num * idle_time, post_ser_batch_q.qsize(),
                                                                 batch_num_queued,
                                                                 100 * post_ser_batch_q.qsize() / batch_num_queued))
                iter_num += 1
        
        except Exception as e:
            raise ValueError("Failed serialization with exception {}".format(str(e)))
        
        finally:
            for i in range(num_workers):
                serialization_threads_working[i].stop()
            # wait for the thread to really stop- sample the event every sample_timeout_dt seconds
            # TODO: change to Q event
            time.sleep(serialization_threads_working[-1].sample_timeout_dt)
            
            num_ser_batches = 0
            num_ser_tags = 0
            while not post_ser_batch_q.empty():
                curr_batch = post_ser_batch_q.get(timeout=10)  # Should happen...
                num_ser_batches += 1
                num_ser_tags += len(curr_batch["upload_data"])

            expected_ser_tags = num_tags - failed_tags_counter
            # pre_ser_batch_q.join() #Wait for all to finish..
            logger.info(
                "SERIALIZATION: Finish serializing {} tags out of {} expected tags "
                "(skipped serialization of {} bad tags)\n  "
                "Num batches: {} batches (expected {} batches)".format(
                    num_ser_tags, expected_ser_tags, failed_tags_counter, num_ser_batches, batch_num_queued))
            logger.info('SERIALIZATION: Bad tags:')
            logger.info(failed_tags_list)
            serialization_success = False
            if num_ser_tags == expected_ser_tags and num_ser_batches == batch_num_queued and failed_tags_q.empty():
                serialization_success = True
            
            else:
                if not failed_tags_q.empty():
                    logger.info(
                        "SERIALIZATION:  The following {} tags failed serialization process at the cloud:".format(
                            failed_tags_q.qsize()))
                    while not failed_tags_q.empty():
                        failed_tag = failed_tags_q.get()
                        logger.info(failed_tag)
                if num_ser_tags != expected_ser_tags:
                    logger.warning(
                        "SERIALIZATION: Error: serialization succeed on all batches, "
                        "but only {} tags were serialized out of expected {}!!".format(
                            num_ser_tags, expected_ser_tags))
                if num_ser_batches != batch_num_queued:
                    logger.warning("SERIALIZATION: Some batches failed to be processed by the cloud:")
                    while not pre_ser_batch_q.empty():
                        curr_batch = pre_ser_batch_q.get()
                        logger.warning(
                            "SERIALIZATION: Failed to serialize after {} retrials. Error: {}  Upload data:\n {}".format(
                                curr_batch['retrials'], curr_batch['response'], curr_batch['upload_data']))
            if not serialization_success:
                logger.warning("SERIALIZATION: Serialization Failed!! See above errors!!")
            else:
                logger.info("SERIALIZATION: \n\nSerialization of {} tags succeed!!!".format(num_ser_tags))

    logger.info(create_summary_message(is_upload=upload_success, is_serialization=serialization_success))
    success = upload_success if upload_success is not None else serialization_success
    return success


if __name__ == '__main__':
    upload_and_serialize_data_from_file()
    print("upload_and_serialize_csv_manually is done\n")
