from core.groups.base_group_service import BaseGroupService


class NewGroupService(BaseGroupService):

    def __init__(self, tox):
        super().__init__(tox)

    # -----------------------------------------------------------------------------------------------------------------
    # Public methods
    # -----------------------------------------------------------------------------------------------------------------

    def accept_invite(self, friend_number, invite_data):
        nick = self._tox.self_get_name()
        status = self._tox.self_get_status()
        self._tox.group_invite_accept(invite_data, friend_number, nick, status)

    def get_groups_names(self):
        group_numbers = self._tox.groups_get_list()
        group_names = map(lambda n: self._tox.group_get_name(n), group_numbers)

        return list(group_names)

    def invite_friend(self, friend_number, group_order_number):
        group_number = self.get_group_number(group_order_number)
        self._tox.group_invite_friend(group_number, friend_number)

    def leave_group(self, group_order_number):
        group_number = self.get_group_number(group_order_number)
        self._tox.group_leave(group_number)

    def send_message(self, message, message_type, group_order_number):
        if group_order_number is None:
            group_numbers = self._get_groups_list()
        else:
            group_numbers = [self.get_group_number(group_order_number)]
        for group_number in group_numbers:
            self._tox.group_send_message(group_number, message_type, message)

    def get_group_number(self, group_order_number):
        group_numbers = self._get_groups_list()

        return group_numbers[group_order_number - 1]

    def get_group_order_number(self, group_number):
        group_numbers = self._get_groups_list()

        return group_numbers.index(group_number)

    def get_group_peers_count(self, group_order_number):
        return 0  # TODO: implement

    def get_groups_count(self):
        return self._tox.group_get_number_groups()

    # -----------------------------------------------------------------------------------------------------------------
    # Private methods
    # -----------------------------------------------------------------------------------------------------------------

    def _get_groups_list(self):
        return self._tox.groups_get_list()
