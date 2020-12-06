# -*- coding:utf-8 -*-
import yaml
import os
import re
import copy


def dsw_information():
    with open('./DSW.yaml') as file:
        data = file.read()
    return yaml.safe_load(data)


def basic_info(manufacturer_info, slot_number):
    ports_pre_slot = []  # 每个板卡的所有端口
    all_port_name = []  # 所有的端口信息（包含所有信息）
    Tag1_port_name = []  # tag1的所有端口名
    Tag2_port_name = []  # tag2的所有端口名

    Tags = manufacturer_info.get('port_tag')
    try:
        del Tags['Console']
        del Tags['Mgmt']
    except Exception:
        pass
    for tag in Tags.keys():
        try:
            port_range = Tags[tag].get('port_range').split('-')
            port_range = range(int(port_range[0]), int(port_range[1]) + 1)
        except Exception:
            port_range = Tags[tag].get('port_range')

        # 获取所有端口信息，端口号前缀、后缀、端口类型，端口tag
        for port_suffix in Tags[tag].get('port_suffix'):
            for port in port_range:
                complete_port_name = '{}{}{}'.format(Tags[tag].get('port_prefix'), port_suffix, port)
                port_prefix = Tags[tag].get('port_prefix')
                split_suffix = Tags[tag].get('split_suffix')
                split_prefix = Tags[tag].get('split_prefix')
                all_port_name.append(
                    {'name': complete_port_name, 'port_prefix': port_prefix, 'port_suffix': port_suffix, 'tag': tag,
                     'port_type': Tags[tag].get('port_type'), 'split_prefix': split_prefix,
                     'split_suffix': split_suffix})
                # {'split_suffix': ':', 'port_prefix': 'HundredGigE', 'name': 'HundredGigE0/0/2', 'tag': 'Tag2', 'port_suffix': '0/0/', 'port_type': 'Hundred_Gigabit_port', 'split_prefix': 'Ten-GigabitEthernet'}

        for each_port_name in all_port_name:
            if each_port_name.get('port_suffix') in Tags[tag].get('port_suffix')[int(slot_number) - 1]:
                if each_port_name not in ports_pre_slot:
                    ports_pre_slot.append(each_port_name)
                if each_port_name.get('tag') == 'Tag1':
                    if each_port_name not in Tag1_port_name:
                        Tag1_port_name.append(each_port_name)
                else:
                    if each_port_name not in Tag2_port_name:
                        Tag2_port_name.append(each_port_name)

    ports_pre_slot = sorted(ports_pre_slot, key=lambda x: int(x.get('name').split('/')[-1]))
    return ports_pre_slot, all_port_name, Tag1_port_name, Tag2_port_name


for manufacturer_info in dsw_information():

    for network_type in ['10GE', '40GE']:
        # print manufacturer_info.get('port_tag').get('Console').get('port_prefix')
        Summary = []
        # file_name = "{}_{}_{}#lsw-{}.yaml".format(manufacturer_info.get('role'),
        #                                           manufacturer_info.get('manufacturer'),
        #                                           manufacturer_info.get('model'),
        #                                           network_type)

        """Console端口"""

        # name = '{}{}'.format(manufacturer_info.get('port_tag').get('Console').get('port_prefix'),
        #                      manufacturer_info.get('port_tag').get('Console').get('port_suffix'))
        #
        # slotnumbers = manufacturer_info.get('port_tag').get('Console').get('slotnumbers')
        # devicetype = manufacturer_info.get('port_tag').get('Console').get('connect_role')

        devicetype = manufacturer_info.get('port_tag').get('Console')
        if not devicetype:
            devicetype = {}


        console = {'remoteconnections': [{'deviceindex': 1, 'devicetype': devicetype.get('connect_role')}],
                   'name': '{}{}'.format(devicetype.get('port_prefix'),
                                         devicetype.get('port_suffix')), 'slotnumbers': devicetype.get('slotnumbers')}
        print console

        Summary.append(console)

        # """Mgmt端口"""
        # suffix = manufacturer_info.get('port_tag').get('Mgmt').get('port_suffix')
        #
        # for mgmt_port_suffix in suffix:
        #     name ='{}{}'.format(manufacturer_info.get('port_tag').get('Mgmt').get('port_prefix'),
        #                         mgmt_port_suffix)
        #     devicetype = manufacturer_info.get('port_tag').get('Mgmt').get('connect_role')
        #     slotnumbers = manufacturer_info.get('port_tag').get('Mgmt').get('slotnumbers')
        #     speed = manufacturer_info.get('port_tag').get('Mgmt').get('speed')
        #
        #     if mgmt_port_suffix == suffix[0]:
        #         mgmt = {'name': name, 'remoteconnections': [{'deviceindex': 1, 'devicetype': devicetype}],
        #                 'slotnumbers': [2,4], 'speed': speed}
        #         Summary.append(mgmt)
        #     else:
        #         mgmt = {'name': name, 'remoteconnections': [{'deviceindex': 1, 'devicetype': devicetype}],
        #                 'slotnumbers': [2,4], 'speed': speed, 'standby': True}
        #         Summary.append(mgmt)

        """ 第一组板卡 """


        def first_group(slotnumber):
            ports_pre_slot, all_port_name, Tag1_port_name, Tag2_port_name = basic_info(manufacturer_info, slotnumber)
            #  生成ASW.GE部分 第一块板卡的第一个口，这个没法做循环
            asw_ge_role = copy.deepcopy(ports_pre_slot[0])
            if slotnumber == 1:
                for port in range(1, 5):
                    splitfrom = asw_ge_role.get('name')
                    port_suffix_with_number = '{}{}'.format(asw_ge_role.get('port_suffix'),
                                                            asw_ge_role.get('name').split(
                                                                asw_ge_role.get('port_suffix'))[-1])
                    split_prefix = asw_ge_role.get('split_prefix')
                    split_suffix = asw_ge_role.get('split_suffix')
                    name = '{}{}{}{}'.format(split_prefix, port_suffix_with_number, split_suffix, port)
                    asw_ge_yaml_format = {'remoteconnections': [{'deviceindex': 1, 'devicetype': 'ASW.GE'}],
                                          'splitfrom': splitfrom, 'speed': 10000,
                                          'name': name, 'slotnumbers': [2, 4]}
                    Summary.append(asw_ge_yaml_format)

            # 生成ISW部分 第一块板卡的第二个口
            isw_role = ports_pre_slot[1]
            for port in range(1, 5):
                splitfrom = isw_role.get('name')
                port_suffix_with_number = '{}{}'.format(isw_role.get('port_suffix'),
                                                        isw_role.get('name').split(
                                                            isw_role.get('port_suffix'))[-1])
                split_prefix = isw_role.get('split_prefix')
                split_suffix = isw_role.get('split_suffix')
                name = '{}{}{}{}'.format(split_prefix, port_suffix_with_number, split_suffix, port)
                deviceindex = 1 if slotnumber == 1 else 2

                isw_yaml_format = {'remoteconnections': [{'deviceindex': deviceindex, 'devicetype': 'ISW'},
                                                         {'deviceindex': deviceindex, 'devicetype': 'CSR'}],
                                   'splitfrom': splitfrom, 'speed': 10000,
                                   'name': name, 'slotnumbers': [2, 4]}
                # print yaml.safe_dump(isw_yaml_format)
                Summary.append(isw_yaml_format)

            # 生成LSW部分  第三到第八个端口
            if network_type == '40GE':
                for port in range(3, 9):
                    ports_pre_slot, all_port_name, Tag1_port_name, Tag2_port_name = basic_info(manufacturer_info,
                                                                                               slotnumber)
                    name = ports_pre_slot[port - 1].get('name')
                    deviceindex = 1 if port % 2 == 1 else 2
                    lsw_yaml_format = {'remoteconnections': [{'deviceindex': deviceindex, 'devicetype': 'LSW'}],
                                       'speed': 40000,
                                       'name': name, 'slotnumbers': [2, 4]}
                    Summary.append(lsw_yaml_format)
            else:
                for port in range(3, 5):
                    ports_pre_slot, all_port_name, Tag1_port_name, Tag2_port_name = basic_info(manufacturer_info,
                                                                                               slotnumber)
                    name = ports_pre_slot[port - 1].get('name')
                    deviceindex = 1 if port == 3 else 2
                    lsw_yaml_format = {'remoteconnections': [{'deviceindex': deviceindex, 'devicetype': 'LSW'}],
                                       'speed': 40000,
                                       'name': name, 'slotnumbers': [2, 4]}
                    Summary.append(lsw_yaml_format)

            if network_type == '40GE':
                # 生成MSW部分 第九个端口
                msw_role = ports_pre_slot[8]
                for port in range(1, 5):
                    splitfrom = msw_role.get('name')
                    port_suffix_with_number = '{}{}'.format(msw_role.get('port_suffix'),
                                                            msw_role.get('name').split(
                                                                msw_role.get('port_suffix'))[-1])
                    split_prefix = msw_role.get('split_prefix')
                    split_suffix = msw_role.get('split_suffix')
                    name = '{}{}{}{}'.format(split_prefix, port_suffix_with_number, split_suffix, port)
                    deviceindex = 1 if slotnumber == 1 else 2
                    msw_yaml_format = {'remoteconnections': [{'deviceindex': deviceindex, 'devicetype': 'MSW'}],
                                       'splitfrom': splitfrom, 'speed': 10000,
                                       'name': name, 'slotnumbers': [2, 4]}

                    Summary.append(msw_yaml_format)
            else:
                for port in range(1, 5):
                    splitfrom = ports_pre_slot[4].get('name')
                    port_suffix_with_number = '{}{}'.format(ports_pre_slot[4].get('port_suffix'),
                                                            ports_pre_slot[4].get('name').split(
                                                                ports_pre_slot[4].get('port_suffix'))[-1])
                    split_prefix = ports_pre_slot[4].get('split_prefix')
                    split_suffix = ports_pre_slot[4].get('split_suffix')
                    name = '{}{}{}{}'.format(split_prefix, port_suffix_with_number, split_suffix, port)
                    deviceindex = 1 if slotnumber == 1 else 2
                    msw_yaml_format = {'remoteconnections': [{'deviceindex': deviceindex, 'devicetype': 'MSW'}],
                                       'splitfrom': splitfrom, 'speed': 10000,
                                       'name': name, 'slotnumbers': [2, 4]}
                    Summary.append(msw_yaml_format)

            """100GE及40GE端口"""
            filter_tag2_port_name = copy.deepcopy(Tag2_port_name)
            ignore_Tag1_port_name = copy.deepcopy(Tag1_port_name)
            ignore_Tag2_port_name = copy.deepcopy(Tag2_port_name)
            first_slot_last_eight_port_name = copy.deepcopy(ports_pre_slot[-8:])
            to_use_ignore_port = copy.deepcopy(ports_pre_slot)
            middle_port_name = copy.deepcopy(ports_pre_slot)

            # 移除tag1和tag2需要忽略的端口
            if network_type == '40GE':
                ignore_ports = to_use_ignore_port[:10] + to_use_ignore_port[-8:]
                for port_name in ignore_ports:
                    if port_name in ignore_Tag1_port_name:
                        ignore_Tag1_port_name.remove(port_name)
                    else:
                        ignore_Tag2_port_name.remove(port_name)
                filter_tag_info = ignore_Tag1_port_name + ignore_Tag2_port_name  # 获取过滤后的所有端口，包含tag1和tag2的端口信息
                filter_all_port_name = []  # 过滤所有端口的name字段
                for name in filter_tag_info:
                    filter_all_port_name.append(name.get('name'))

                # 通用连接ASW10GE及HSW10GE的端口的deviceindex的列表,不包含前六个及后八个端口的
                public_index = []
                deviceindex = 0
                for name in filter_all_port_name:
                    if name in filter_all_port_name[::2]:
                        deviceindex = deviceindex + 1
                    public_index.append({'indexASW10GE': deviceindex, 'indexHSW10GE': deviceindex, 'name': name})
                # print public_index
                # 过滤后的端口名,只包含tag2的端口(除去前十个，包含后八个)
                filter_index25ge_port_name = []
                for name in filter_tag2_port_name:
                    if name not in to_use_ignore_port[:10]:
                        filter_index25ge_port_name.append(name.get('name'))
                # 每四个一对
                filter_index25ge_port_name = filter_index25ge_port_name[:len(filter_index25ge_port_name) // 4 * 4]
                asw25ge_index = []  # 连接ASW25GE的index的列表
                deviceindex = 0
                for name in filter_index25ge_port_name:
                    if name in filter_index25ge_port_name[::4]:
                        deviceindex = deviceindex + 1
                    asw25ge_index.append({'indexASW25GE': deviceindex, 'name': name})

                # 获取移除后前十个及后八个的端口信息,中间剩余端口
                for port in ignore_ports:
                    middle_port_name.remove(port)
                # 遍历过滤后的端口信息（不包含前十个及后八个）
                for every_port in middle_port_name:
                    # 判断每个端口的deviceindex
                    for index in public_index:
                        if index.get('name') == every_port.get('name'):
                            indexHSW10GE = index.get('indexHSW10GE')
                            indexASW10GE = index.get('indexASW10GE')
                    for index in asw25ge_index:
                        if index.get('name') == every_port.get('name'):
                            indexASW25GE = index.get('indexASW25GE')
                    # 如果是tag2则套用下列格式，否则套用tag1格式
                    if every_port.get('tag') == 'Tag2':
                        if manufacturer_info.get('manufacturer') == 'Huawei':
                            overwritedname = '{}{}{}'.format('100GE', every_port.get('port_suffix'),
                                                             every_port.get('name').split(
                                                                 every_port.get('port_suffix'))[-1])
                            every = {'remoteconnections': [{'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                           {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'},
                                                           {'deviceindex': indexASW25GE, 'devicetype': 'ASW.25GE',
                                                            'overwritedname': overwritedname}],
                                     'name': every_port.get('name'), 'speeds': [40000, 100000], 'slotnumbers': [2, 4]}
                            # print every
                            Summary.append(every)
                        else:
                            every = {'remoteconnections': [{'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                           {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'},
                                                           {'deviceindex': indexASW25GE, 'devicetype': 'ASW.25GE'}],
                                     'name': every_port.get('name'), 'speeds': [40000, 100000], 'slotnumbers': [2, 4]}
                            Summary.append(every)
                    else:
                        every = {'remoteconnections': [{'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                       {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'}],
                                 'speed': 40000, 'name': every_port.get('name'), 'slotnumbers': [2, 4]}
                        # print every
                        Summary.append(every)

            else:
                # 移除需要忽略的端口
                ignore_ports = to_use_ignore_port[:6] + to_use_ignore_port[-8:]
                for port_name in ignore_ports:
                    if port_name in ignore_Tag1_port_name:
                        ignore_Tag1_port_name.remove(port_name)
                    else:
                        ignore_Tag2_port_name.remove(port_name)
                filter_tag_info = ignore_Tag1_port_name + ignore_Tag2_port_name  # 获取过滤后的所有端口，包含tag1和tag2的端口信息
                filter_all_port_name = []
                for name in filter_tag_info:
                    filter_all_port_name.append(name.get('name'))

                # 通用连接ASW10GE及HSW10GE的端口的deviceindex的列表,不包含前六个及后八个端口的
                public_index = []
                deviceindex = 0
                for name in filter_all_port_name:
                    if name in filter_all_port_name[::2]:
                        deviceindex = deviceindex + 1
                    public_index.append({'indexASW10GE': deviceindex, 'indexHSW10GE': deviceindex, 'name': name})

                # 过滤后的端口名,只包含tag2的端口(除去前六个，包含后八个)
                filter_index25ge_port_name = []
                for name in filter_tag2_port_name:
                    if name not in ports_pre_slot[:6]:
                        filter_index25ge_port_name.append(name.get('name'))
                # 每四个一对
                filter_index25ge_port_name = filter_index25ge_port_name[:len(filter_index25ge_port_name) // 4 * 4]
                asw25ge_index = []  # 连接ASW25GE的index的列表
                deviceindex = 0
                for name in filter_index25ge_port_name:
                    if name in filter_index25ge_port_name[::4]:
                        deviceindex = deviceindex + 1
                    asw25ge_index.append({'indexASW25GE': deviceindex, 'name': name})
                # 获取移除后前六个及后八个的端口信息
                for port in ignore_ports:
                    ports_pre_slot.remove(port)
                # 遍历过滤后的端口信息（不包含前六个及后八个）
                for every_port in ports_pre_slot:
                    # 判断每个端口的deviceindex
                    for index in public_index:
                        if index.get('name') == every_port.get('name'):
                            indexHSW10GE = index.get('indexHSW10GE')
                            indexASW10GE = index.get('indexASW10GE')
                    for index in asw25ge_index:
                        if index.get('name') == every_port.get('name'):
                            indexASW25GE = index.get('indexASW25GE')
                    # 如果是tag2则套用下列格式，否则套用tag1格式
                    if every_port.get('tag') == 'Tag2':
                        if manufacturer_info.get('manufacturer') == 'Huawei':
                            overwritedname = '{}{}{}'.format('100GE', every_port.get('port_suffix'),
                                                             every_port.get('name').split(
                                                                 every_port.get('port_suffix'))[-1])
                            every = {'remoteconnections': [{'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                           {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'},
                                                           {'deviceindex': indexASW25GE, 'devicetype': 'ASW.25GE',
                                                            'overwritedname': overwritedname}],
                                     'name': every_port.get('name'), 'speeds': [40000, 100000], 'slotnumbers': [2, 4]}
                            # print every
                            Summary.append(every)
                            pass
                        else:
                            every = {'remoteconnections': [{'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                           {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'},
                                                           {'deviceindex': indexASW25GE, 'devicetype': 'ASW.25GE'}],
                                     'name': every_port.get('name'), 'speeds': [40000, 100000], 'slotnumbers': [2, 4]}
                            Summary.append(every)
                    else:
                        every = {'remoteconnections': [{'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                       {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'}],
                                 'speed': 40000, 'name': every_port.get('name'), 'slotnumbers': [2, 4]}
                        Summary.append(every)

            """千兆万兆混布"""
            # 千兆万兆混布连接ASW10GE及HSW10GE的端口的deviceindex的列表，(后八个端口)
            hybrid_index = []
            deviceindex = 999
            for name in first_slot_last_eight_port_name:
                if name in first_slot_last_eight_port_name[::2]:
                    deviceindex = deviceindex + 1
                hybrid_index.append(
                    {'indexASW10GE': deviceindex, 'indexHSW10GE': deviceindex, 'name': name.get('name')})

            for port_last_eight in first_slot_last_eight_port_name:
                if port_last_eight.get('tag') == 'Tag1':
                    for index in hybrid_index:
                        if index.get('name') == port_last_eight.get('name'):
                            indexHSW10GE = index.get('indexHSW10GE')
                            indexASW10GE = index.get('indexASW10GE')
                            hybrid_port = {
                                'remoteconnections': [{'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                      {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'}],
                                'speed': 40000, 'name': port_last_eight.get('name'), 'slotnumbers': [2, 4]}
                            # print hybrid_port
                            Summary.append(hybrid_port)
                else:
                    if port_last_eight.get('name') in filter_index25ge_port_name:

                        for index25ge in asw25ge_index:
                            if port_last_eight.get('name') in index25ge.values():
                                indexASW25GE = index25ge.get('indexASW25GE')
                                for index in hybrid_index:
                                    if index.get('name') == port_last_eight.get('name'):
                                        indexASW10GE = index.get('indexASW10GE')
                                        indexHSW10GE = index.get('indexHSW10GE')
                                        if manufacturer_info.get('manufacturer') == 'Huawei':
                                            # print port_last_eight
                                            overwritedname = '{}{}{}'.format('100GE',
                                                                             port_last_eight.get('port_suffix'),
                                                                             port_last_eight.get('name').split(
                                                                                 port_last_eight.get('port_suffix'))[
                                                                                 -1])
                                            hybrid_port = {'remoteconnections': [
                                                {'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'},
                                                {'deviceindex': indexASW25GE, 'devicetype': 'ASW.25GE',
                                                 'overwritedname': overwritedname}],
                                                           'speeds': [40000, 100000],
                                                           'name': port_last_eight.get('name'), 'slotnumbers': [2, 4]}
                                            # print hybrid_port
                                            Summary.append(hybrid_port)
                                        else:
                                            hybrid_port = {'remoteconnections': [
                                                {'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'},
                                                {'deviceindex': indexASW25GE, 'devicetype': 'ASW.25GE'}],
                                                'speeds': [40000, 100000], 'name': port_last_eight.get('name'),
                                                'slotnumbers': [2, 4]}
                                            # print hybrid_port
                                            Summary.append(hybrid_port)
                    else:
                        for index in hybrid_index:
                            if index.get('name') == port_last_eight.get('name'):
                                indexASW10GE = index.get('indexASW10GE')
                                indexHSW10GE = index.get('indexHSW10GE')
                                hybrid_port = {
                                    'remoteconnections': [{'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                          {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'}],
                                    'speed': 40000, 'name': port_last_eight.get('name'), 'slotnumbers': [2, 4]}
                                # print hybrid_port
                                Summary.append(hybrid_port)


        for number in range(1, 3):
            first_group(number)

        # 千兆万兆混布一分四

        first_ports_pre_slot, first_all_port_name, first_Tag1_port_name, first_Tag2_port_name = basic_info(
            manufacturer_info, 1)
        second_ports_pre_slot, second_all_port_name, second_Tag1_port_name, second_Tag2_port_name = basic_info(
            manufacturer_info, 2)
        # 第一块板卡和第二块板卡的后八个端口
        hybrid_split = first_ports_pre_slot[-8:] + second_ports_pre_slot[-8:]
        deviceindex = 1
        for port_name in hybrid_split:
            deviceindex = deviceindex + 1
            # 一分四端口
            for port in range(1, 5):
                splitfrom = port_name.get('name')
                port_suffix_with_number = '{}{}'.format(port_name.get('port_suffix'),
                                                        port_name.get('name').split(
                                                            port_name.get('port_suffix'))[-1])
                split_prefix = port_name.get('split_prefix')
                split_suffix = port_name.get('split_suffix')
                name = '{}{}{}{}'.format(split_prefix, port_suffix_with_number, split_suffix, port)

                hybrid_split_name = {'remoteconnections': [{'deviceindex': deviceindex, 'devicetype': 'ASW.GE'}],
                                     'splitfrom': splitfrom,
                                     'speed': 10000, 'name': name, 'slotnumbers': [2, 4]}
                # print yaml.safe_dump(hybrid_split_name)
                # print hybrid_split_name
                Summary.append(hybrid_split_name)

        """第三,四块板卡端口"""


        def second_group(slotnumber):
            third_slot_ports_pre_slot, third_slot_all_port_name, third_slot_Tag1_port_name, third_slot_Tag2_port_name = basic_info(
                manufacturer_info, slotnumber)

            # 连接ASW10GE及HSW10GE的deviceindex  ,deviceindex 从 100开始
            third_slot_all_tag = third_slot_Tag1_port_name + third_slot_Tag2_port_name
            second_group_ASW10GE_HSW10GE_index = []
            deviceindex = 99
            for name in third_slot_all_tag:
                if name in third_slot_all_tag[::2]:
                    deviceindex = deviceindex + 1
                second_group_ASW10GE_HSW10GE_index.append(
                    {'indexASW10GE': deviceindex, 'indexHSW10GE': deviceindex, 'name': name.get('name')})
            # print second_group_ASW10GE_HSW10GE_index
            # 连接ASW25GE的deviceindex,deviceindex 从 101开始
            second_group_ASW25GE_index = []
            second_group_ASW25GE_port = []

            for name in third_slot_Tag2_port_name:
                second_group_ASW25GE_port.append(name.get('name'))
            second_group_has_ASW25GE_port = second_group_ASW25GE_port[:len(second_group_ASW25GE_port) // 4 * 4]
            deviceindex = 100
            for name in second_group_has_ASW25GE_port:
                if name in second_group_has_ASW25GE_port[::4]:
                    deviceindex = deviceindex + 1
                second_group_ASW25GE_index.append({'indexASW25GE': deviceindex, 'name': name})
            # print second_group_ASW25GE_index

            for third_slot_port in third_slot_ports_pre_slot:
                if third_slot_port.get('tag') == 'Tag1':
                    # print third_slot_port
                    for index in second_group_ASW10GE_HSW10GE_index:
                        if index.get('name') == third_slot_port.get('name'):
                            indexHSW10GE = index.get('indexHSW10GE')
                            indexASW10GE = index.get('indexASW10GE')
                            hybrid_port = {
                                'remoteconnections': [{'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                      {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'}],
                                'speed': 40000, 'name': third_slot_port.get('name'), 'slotnumbers': [4]}
                            # print hybrid_port
                            Summary.append(hybrid_port)
                else:
                    if third_slot_port.get('name') in second_group_has_ASW25GE_port:
                        for index25ge in second_group_ASW25GE_index:
                            if third_slot_port.get('name') in index25ge.values():
                                indexASW25GE = index25ge.get('indexASW25GE')
                                for index in second_group_ASW10GE_HSW10GE_index:
                                    if index.get('name') == third_slot_port.get('name'):
                                        indexASW10GE = index.get('indexASW10GE')
                                        indexHSW10GE = index.get('indexHSW10GE')
                                        if manufacturer_info.get('manufacturer') == 'Huawei':
                                            overwritedname = '{}{}{}'.format('100GE',
                                                                             third_slot_port.get('port_suffix'),
                                                                             third_slot_port.get('name').split(
                                                                                 third_slot_port.get('port_suffix'))[
                                                                                 -1])
                                            hybrid_port = {'remoteconnections': [
                                                {'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'},
                                                {'deviceindex': indexASW25GE, 'devicetype': 'ASW.25GE',
                                                 'overwritedname': overwritedname}],
                                                'speeds': [40000, 100000], 'name': third_slot_port.get('name'),
                                                'slotnumbers': [4]}
                                            # print hybrid_port
                                            Summary.append(hybrid_port)
                                        else:

                                            hybrid_port = {'remoteconnections': [
                                                {'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'},
                                                {'deviceindex': indexASW25GE, 'devicetype': 'ASW.25GE', }],
                                                           'speeds': [40000, 100000],
                                                           'name': third_slot_port.get('name'), 'slotnumbers': [4]}
                                            # print hybrid_port
                                            Summary.append(hybrid_port)
                    else:

                        for index in second_group_ASW10GE_HSW10GE_index:
                            if index.get('name') == third_slot_port.get('name'):
                                indexASW10GE = index.get('indexASW10GE')
                                indexHSW10GE = index.get('indexHSW10GE')
                                hybrid_port = {
                                    'remoteconnections': [{'deviceindex': indexASW10GE, 'devicetype': 'ASW.10GE'},
                                                          {'deviceindex': indexHSW10GE, 'devicetype': 'HSW.10GE'}],
                                    'speed': 40000, 'name': third_slot_port.get('name'), 'slotnumbers': [4]}
                                # print hybrid_port
                                Summary.append(hybrid_port)


        for number in range(3, 5):
            second_group(number)

        with open("{}_{}_{}#lsw-{}.yaml".format(
                manufacturer_info.get('role'),
                manufacturer_info.get('manufacturer'),
                manufacturer_info.get('model'),
                network_type), 'wb') as file:
            file.write(yaml.safe_dump(Summary))
    # break
