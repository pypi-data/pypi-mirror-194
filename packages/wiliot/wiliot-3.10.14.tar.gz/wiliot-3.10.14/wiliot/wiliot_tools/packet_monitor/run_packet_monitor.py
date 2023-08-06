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

import datetime

from wiliot.wiliot_tools.packet_monitor.packet_monitor import PacketMonitor
from wiliot.wiliot_core.utils import WiliotDir, check_user_config_is_ok

from bokeh.plotting import curdoc
from bokeh.models.widgets import Button, Div, DataTable, TableColumn, TextInput, CheckboxGroup
from bokeh.layouts import column, row
from bokeh.models import Column, ColumnDataSource
import sys
import logging
import os
import pandas as pd


class PlotPacketMonitor(object):
    def __init__(self):
        print("Please run using CLI (command line interface) with the following line at the code location:"
              "bokeh serve --show run_packet_monitor.py")
        # user_name = input('Please Enter user name:\n')
        # user_pass = getpass('Please Enter Password:\n')
        owner_id = input('Please Enter owner id:\n')
        config_file, api_key, is_success = check_user_config_is_ok(env='prod', owner_id=owner_id)
        if is_success:
            print('credentials saved/upload from {}'.format(config_file))
        else:
            raise Exception('invalid credentials - please try again to login')

        self.user_configs = {'api_key': api_key, 'owner_id': owner_id, 'env': ''}
        self.logger = logging.getLogger('WiliotMonitor')
        self.logger_path = None
        self.set_logger()
        # init monitor
        self.monitor = None
        self.init_monitor()
        # init graph
        self.bokeh_doc = None
        self.unique_tags_title_div = None
        self.stop_button = None
        self.table_title_div = None
        self.table_col = None
        self.data_table = None
        self.is_tag_only = None
        self.num_of_physical_tags = None
        self.filter_tags = None
        self.filter_tags_title = None
        self.output_path = None
        self.file_path = None
        self.log_div = None
        self.save_button = None
        self.clear_button = None
        self.create_packet_data = None
        self.init_graph()
    
    def set_logger(self):
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        wiliot_dir = WiliotDir()
        logger_path = os.path.join(wiliot_dir.get_wiliot_root_app_dir(), 'wiliot_monitor')
        if not os.path.isdir(logger_path):
            os.mkdir(logger_path)
        logger_name = 'monitor_log_{}.log'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        self.logger_path = os.path.join(logger_path, logger_name)
        file_handler = logging.FileHandler(self.logger_path, mode='a')
        file_formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.INFO)
    
    def init_monitor(self):
        try:
            self.monitor = PacketMonitor(user_configs=self.user_configs, logger_name=self.logger.name)
        except Exception as e:
            self.logger.log(logging.WARNING, e)
            sys.exit()
    
    def log_results(self):
        if not os.path.isdir(self.output_path.value):
            wiliot_dir = WiliotDir()
            self.output_path.value = os.path.join(wiliot_dir.get_wiliot_root_app_dir(), 'wiliot_monitor')
            if not os.path.isdir(self.output_path.value):
                os.makedirs(self.output_path.value)
        if self.num_of_physical_tags.value == '':
            self.num_of_physical_tags.value = 'X'
        
        table_to_log = self.filter_table()
        self.file_path = os.path.join(self.output_path.value, 'wiliot_monitor_{}.csv'.format(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
        df_title = pd.DataFrame({'summary': ['Received {} unique tags '
                                             'out of {} tags'.format(len(table_to_log['tag_id']),
                                                                     self.num_of_physical_tags.value)]})
        df_title.to_csv(self.file_path, index=False)
        df_tags = pd.DataFrame(table_to_log)
        df_tags.to_csv(self.file_path, mode='a', index=False)
        if not self.create_packet_data.active[0]:
            packet_data = self.create_packet_data_file()
            df_packets = pd.DataFrame(packet_data)
            df_packets.to_csv(self.file_path.replace('wiliot_monitor_', 'packet_data_'), mode='a', index=False)
        self.log_div.text = 'data was saved at {}'.format(self.output_path.value)
    
    def init_graph(self):
        # init the graph:
        self.bokeh_doc = curdoc()
        
        # unique tag log:
        self.unique_tags_title_div = Div(text='', width=300, height=30,
                                         style={'font-size': '150%', 'color': 'blue', 'font-weight': 'bold'})
        self.unique_tags_title_div.text = 'Number of Unique Tags:'
        
        # Button to stop the server
        self.stop_button = Button(label="Stop", button_type="danger")
        self.stop_button.on_click(self.monitor.stop_monitor)
        # save to csv
        self.num_of_physical_tags = TextInput(value="", title="number of physical tags")
        self.output_path = TextInput(value="", title="folder directory")
        self.log_div = Div(text='', width=300, height=800, style={'font-size': '100%', 'color': 'black',
                                                                  'font-weight': 'bold'})
        self.save_button = Button(label="Save", button_type="success")
        self.save_button.on_click(self.log_results)
        # check for listen to tag only:
        self.is_tag_only = CheckboxGroup(labels=['listen to tag only'], active=[1])
        self.is_tag_only.on_click(self.listen_to_tag_only)
        # clear button:
        self.clear_button = Button(label="Clear", button_type="primary", width=100)
        self.clear_button.on_click(self.clear_table)
        # filter input:
        self.filter_tags_title = Div(text='filter tag id:')
        self.filter_tags = TextInput(value="", title="", width=100)
        # create packet_data:
        self.create_packet_data = CheckboxGroup(labels=['create packet data'], active=[0])
        # Summary table:
        self.table_title_div = Div(text='Summary:', width=300, height=30,
                                   style={'font-size': '200%', 'color': 'black', 'font-weight': 'bold'})
        cols_names = self.monitor.get_tags_data()
        self.table_col = [TableColumn(field=k, title=k) for k in cols_names.keys()]
        self.data_table = DataTable(columns=self.table_col, source=ColumnDataSource(self.monitor.get_tags_data()))
        
        # log the results:
        self.logger.log(logging.INFO,
                        'You can type "http://localhost:5006/packet_monitor" in your browser to see the results')
    
    def run_graph(self):
        # run continuously
        self.bokeh_doc.title = "Wiliot Monitor"
        self.bokeh_doc.add_root(row([column([self.unique_tags_title_div, self.table_title_div, self.data_table,
                                             row([self.is_tag_only, self.filter_tags_title,
                                                  self.filter_tags, self.clear_button]),
                                             Column(self.stop_button, align="center")]),
                                     column([self.num_of_physical_tags, self.output_path, self.create_packet_data,
                                             self.save_button, self.log_div])]))
        self.bokeh_doc.add_periodic_callback(self.plot_callback, 50)
    
    def filter_table(self):
        full_table = self.monitor.get_tags_data()
        table_to_present = {}
        if self.filter_tags.value != '':
            index_to_present = [i for i, t_id in enumerate(full_table['tag_id_suffix'])
                                if self.filter_tags.value in t_id]
            for k in full_table.keys():
                table_to_present[k] = [full_table[k][i] for i in index_to_present]
        else:
            table_to_present = full_table
        return table_to_present
    
    def update_table(self):
        try:
            self.data_table.source.data = self.filter_table()
        except Exception as e:
            self.logger.log(logging.WARNING, 'skip table updating due to {}'.format(e))
    
    def update_unique_tags(self):
        table_to_present = self.filter_table()
        self.unique_tags_title_div.text = 'Number of Unique Tags: {}'.format(len(table_to_present['tag_id']))
    
    def plot_callback(self):
        self.update_table()
        self.update_unique_tags()
        if self.monitor.is_stop:
            self.logger.log(logging.INFO, 'done')
            sys.exit(0)
    
    def listen_to_tag_only(self, checkbox_stat):
        if self.monitor.GwObj.connected:
            self.monitor.GwObj.write('!listen_to_tag_only {}'.format(int(not checkbox_stat[0])), with_ack=True)
        self.logger.log(logging.INFO, 'set gw to listen to tag only: {}'.format(int(not checkbox_stat[0])))
    
    def clear_table(self):
        self.monitor.clear_tags()
    
    def create_packet_data_file(self):
        if self.logger_path is None:
            self.logger.log(logging.WARNING, 'no log path was found. Export csv failed')
            return
        try:
            packet_data = {'encrypted_packet': [], 'time_from_start': [], 'timestamp': []}
            if os.path.isfile(self.logger_path):
                f = open(self.logger_path, 'r')
                lines = f.readlines()
                for line in lines:
                    # a data line
                    if 'process_packet("' in line:
                        try:
                            encrypted_packet = line.split('process_packet("')[1].split('")')[0]
                            time_from_start = float(line.split(', time:')[1])
                            timestamp = line.split(' WiliotMonitor')[0]
                            packet_data['encrypted_packet'].append(encrypted_packet)
                            packet_data['time_from_start'].append(time_from_start)
                            packet_data['timestamp'].append(timestamp)
                        except Exception as e:
                            self.logger.log(logging.WARNING, 'line:[{}] was not saved due to: {}'.format(line, e))
                            pass
                
                f.close()
            return packet_data
        except Exception as e:
            self.logger.log(logging.WARNING, 'export packets from log was failed: {}'.format(e))
            return None


# run graph:
p = PlotPacketMonitor()
p.run_graph()
