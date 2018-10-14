from enum import Enum


class PendingStatus(Enum):
    """交易状态"""
    Waiting = 1  # 等待
    Success = 2  # 成功
    Reject = 3  # 拒绝
    Redraw = 4  # 撤销
