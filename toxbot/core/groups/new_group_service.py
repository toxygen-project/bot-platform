from core.groups.base_group_service import BaseGroupService


class NewGroupService(BaseGroupService):

    def __init__(self, tox):
        super().__init__(tox)

    def accept_invite(self, friend_number, invite_data):
        nick = self._tox.self_get_name()
        status = self._tox.self_get_status()
        self._tox.group_invite_accept(invite_data, friend_number, nick, status)

    def get_groups_names(self):
        group_numbers = self._tox.groups_get_list()
        group_names = map(lambda n: self._tox.group_get_name(n), group_numbers)

        return list(group_names)

    def invite_friend(self, friend_number, group_order_number):
        group_number = self._get_group_number(group_order_number)
        self._tox.group_invite_friend(group_number, friend_number)

    def leave_group(self, group_order_number):
        group_number = self._get_group_number(group_order_number)
        self._tox.group_leave(group_number)

    def _get_group_number(self, group_order_number):
        group_numbers = self._tox.groups_get_list()

        return group_numbers[group_order_number - 1]
