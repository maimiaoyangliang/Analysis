#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zhoujiebin
@contact: zhoujiebing@maimiaotech.com
@date: 2012-10-31 13:25
@version: 0.0.0
@license: zhoujiebing@maimiaotech.com
@copyright: zhoujiebing@maimiaotech.com

"""
from CommonTools.report_tools import Report

class Statistics():
    """
    Statistics some import report data
    """
    def __init__(self):
        self.count = 0
        self.low_roi_count = 0
        self.unnormal_count = 0
        self.sum_roi = 0.0
        self.sum_cost = 0.0
        self.sum_pay = 0.0

        self.sum_multi_cost = 0.0
        self.sum_multi_roi = 0.0
        self.sum_multi_pay = 0.0
        self.sum_click = 0
        self.sum_day_cost = 0.0
        self.sum_day_pay = 0.0
        
    def statistics(self, _report):
        """
        statistics
        """
        if _report['multi_cost'] <= 0:
            self.unnormal_count += 1
        else:
            self.count += 1
            self.sum_roi += _report['roi']
            self.sum_cost += _report['cost']
            self.sum_pay += _report['pay']

            self.sum_multi_cost += _report['multi_cost']
            self.sum_multi_roi += _report['multi_roi']
            self.sum_multi_pay += _report['multi_pay']

            self.sum_day_cost += _report['multi_cost'] / _report['count_days']
            self.sum_day_pay += _report['multi_pay'] / _report['count_days']
            self.sum_click += _report['click']
            if _report['roi'] <= 0:
                self.low_roi_count += 1

def analysis_campaign_simple(file_name):
    """
    get simple report
    """
    soft_list = ['省油宝长尾计划', '省油宝加力计划', '广撒网计划', '喜宝计划', '极品飞车', '懒人开车', '疯狂车手', '大麦']
    soft_statistics_dict = {}
    for key in soft_list:
        soft_statistics_dict[key] = Statistics()

    for line in file(file_name):
        report = Report.parser_report(line)
        if not report:
            continue
        for campaign_name in soft_list:
            if report['campaign'].find(campaign_name) != -1:
                soft_statistics_dict[campaign_name].statistics(report)
        
    content = ''
    for key in soft_list:
        result = soft_statistics_dict[key]
        content += key + '\n'
        content += '有效数(多天花费不为0)：%d, 多天花费为0数：%d\n' % (result.count, result.unnormal_count)
        content += '昨天 有效用户的平均花费：%.1f, 平均成交额：%.1f, 平均ROI：%.1f, 平均CPC：%.1f\n' % \
                (result.sum_cost / result.count, result.sum_pay / result.count, \
                result.sum_pay / result.sum_cost, result.sum_cost / result.sum_click)
        content += '昨天 有效用户中ROI为0数：%d,   占比：%.2f\n' % (result.low_roi_count, \
                result.low_roi_count / (result.count + 0.001))
        content += '多天 有效用户的平均花费：%.1f, 平均成交额：%.1f\n' % \
                (result.sum_multi_cost / result.count, result.sum_multi_pay / result.count)
        content += '多天 有效用户的日均花费：%.1f, 日均成交额：%.1f, 日均ROI：%.1f\n\n' % \
                (result.sum_day_cost / result.count, result.sum_day_pay / result.count, \
                result.sum_day_pay / result.sum_day_cost)
    
    return content


if __name__ == '__main__':
    import os
    import sys
    if len(sys.argv) < 2:
        print 'input arg'
        exit(0) 

    FILE_NAME = str(sys.argv[1])
    if os.path.exists(FILE_NAME):
        SIMPLE_REPORT = analysis_campaign_simple(FILE_NAME)    
        print SIMPLE_REPORT
