import ddtank
from ddtank.status import Status

class DDTeam:
    status_list = []

    def __init__(self, team_name: str = None):
        if team_name:
            self.name = team_name
        else:
            self.name = '弹弹堂小队'

    def __add__(self, other: Status) -> bool:
        """
        添加一个角色到小队
        :param other: 被添加的角色
        :return: 返回布尔类型变量，代表操作是否成功
        """
        self.status_list += [other]
        return True

    def __sub__(self, other: Status) -> bool:
        """
        从小队删除一个角色
        :param other: 被删除的角色
        :return: 返回布尔类型变量，代表操作是否成功
        """
        if other in self.status_list:
            self.status_list.remove(other)
            return True
        return False

    def __repr__(self) -> str:
        team_info = f"""
        小队名称:{self.name}
        小队队长:{self.status_list[0]}
        """
        return team_info

    def perform(self):
        """
        执行小队的战斗任务
        :return: 无返回值
        """
        pass
