import core.common.tox_save as tox_save


class BaseGroupService(tox_save.ToxSave):

    def __init__(self, tox):
        super().__init__(tox)

    def accept_invite(self, friend_number, invite_data):
        pass

    def get_groups_names(self):
        return []

    def invite_friend(self, friend_number, group_order_number):
        pass

    def leave_group(self, group_order_number):
        pass

    def send_message(self, message, message_type, group_order_number):
        pass

    def get_group_number(self, group_order_number):
        pass

    def get_group_order_number(self, group_number):
        pass

    def get_group_peers_count(self, group_order_number):
        pass

    def get_groups_count(self):
        pass
