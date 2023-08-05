# encoding: utf-8
"""
@project: djangoModel->enroll_statistics
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 报名统计服务
@created_time: 2023/2/22 14:31
"""


class EnrollStatistics(object):
    """报名主项统计服务(发布人统计)"""

    @staticmethod
    def every_one_total(params=None):
        """
        每个人汇总统计，可以根据事件和状态码筛选。
        :param params:
        :return: [{
        "count":"发布次数",
        "amount_total":"总收合计"，
        "paid_amount_total":"为首合计",
        "paid_amount_total":"以收合计",
        "average_price":"平均价格",
        "commision_total":"总佣金",
        "counts_total":"份数总计"
        }]，err_msg
        """
        if params is None:
            params = {}
        return None, None

    @staticmethod
    def every_day_total(params=None):
        """
        每个人汇总统计，可以根据事件和状态码筛选。
        :param params:
        :return: [{
        "count":"发布次数",
        "amount_total":"总收合计"，
        "paid_amount_total":"为首合计",
        "paid_amount_total":"以收合计",
        "average_price":"平均价格",
        "commision_total":"总佣金",
        "counts_total":"份数总计"
        }]，err_msg
        """

        return {}, None


class EnrollRecordStatistics(object):
    """报名记录统计（报名人统计）"""
    pass


class EnrollSubitemRecordStatistics(object):
    """报名分你想记录统计（任务统计）"""
    pass
