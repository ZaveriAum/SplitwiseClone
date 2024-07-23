import globals


class Groups:

    def __init__(self):
        pass

    def get_groups_involved(self):
        print("======Group List=====")
        for group_id, group_info in globals.GROUPS_LIST.items():
            print(f"Group_id: {group_id}, Group name: {group_info['group_name']}")

    def get_members_in_groups_involved(self, g_id):
        for group_id, group_info in globals.GROUPS_LIST.items():
            if group_id == g_id:
                print(f"Creator: {group_info['created_by']['full_name']}")
                for member_id, member_info in group_info['members'].items():
                    print(f"Member Name: {member_info['full_name']}")
