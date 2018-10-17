from flask_login import current_user

from app.libs.enum import PendingStatus


class DriftCollection():
    def __init__(self, drifts):
        self.data = []
        self._parse(drifts)

    def _parse(self, drifts):
        for drift in drifts:
            temp = DriftViewModel(drift)
            self.data.append(temp.data)

class DriftViewModel():
    def __init__(self, drift):
        self.data = {}
        self.data = self._parse(drift)

    @staticmethod
    def requester_or_gifter(drift):
        if drift.requester_id == current_user.id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are

    def _parse(self, drift):
        you_are = self.requester_or_gifter(drift)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_image': drift.book_image,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'operator': drift.requester_nickname if you_are != 'requester' else drift.gifter_nickname,
            'message': drift.message,
            'address': drift.address,
            'status_str': pending_status,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending
        }
        return r
