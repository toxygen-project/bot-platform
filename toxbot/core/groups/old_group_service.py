from core.groups.base_group_service import BaseGroupService


class OldGroupService(BaseGroupService):

    def __init__(self, tox):
        super().__init__(tox)
        self._groups = []

    # -----------------------------------------------------------------------------------------------------------------
    # Public methods
    # -----------------------------------------------------------------------------------------------------------------

    def accept_invite(self, friend_number, invite_data):
        group_number = self._tox.conference_join(friend_number, invite_data)
        self._groups.append(group_number)

    def get_groups_names(self):
        group_names = map(lambda n: self._tox.conference_get_title(n), self._groups)

        return list(group_names)

    def invite_friend(self, friend_number, group_order_number):
        group_number = self._get_group_number(group_order_number)
        self._tox.conference_invite(friend_number, group_number)

    def leave_group(self, group_order_number):
        group_number = self._get_group_number(group_order_number)
        self._tox.conference_delete(group_number)
        self._groups.remove(group_number)

    def send_message(self, message, message_type, group_order_number):
        if group_order_number is None:
            group_numbers = self._groups
        else:
            group_numbers = [self._get_group_number(group_order_number)]
        for group_number in group_numbers:
            self._tox.conference_send_message(group_number, message, message_type)

    # -----------------------------------------------------------------------------------------------------------------
    # Public methods
    # -----------------------------------------------------------------------------------------------------------------

    def _get_group_number(self, group_order_number):
        return self._groups[group_order_number - 1]