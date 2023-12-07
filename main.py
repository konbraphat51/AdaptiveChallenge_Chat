#
# logはclass ChatRoomが全て保存
#
#
from typing import List  # will deprecated


class User:
    """
    Userの情報をまとめるクラス
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other_user):
        return self.name == other_user.name

    def __str__(self):
        return f"{self.name}"


class Log:
    """
    Logの情報をまとめるクラス
    """

    def __init__(self, from_user: User, to_user: User, content: str):
        self.from_user = from_user
        self.to_user = to_user
        self.content: str = content


class ChatRoom:
    """
    Chatの機能と情報をまとめるクラス
    """

    def __init__(self):
        self.users: List[User] = []
        self.logs: List[Log] = []

    def add_user(self, user: User or str) -> None:
        if isinstance(user, str):
            user = User(user)
        for other_user in self.users:
            if other_user == user:
                print("ERROR: ID already used!")
                return
        self.users.append(user)
        print(f"{user} registered!")
        return

    def talk(self, from_user: str, to_user: str, contents: str):
        if not self.is_user_exists(from_user) or not self.is_user_exists(
            to_user
        ):
            print("Error: no user ID")
            return
        if from_user == to_user:
            print("Error: same user refered")
            return 
        from_user = User(from_user)
        to_user = User(to_user)
        self.logs.append(Log(from_user, to_user, contents))
        return

    def show_log(self, user_1: str, user_2: str):
        if not self.is_user_exists(user_1) or not self.is_user_exists(user_2):
            print("Error: no user ID")
            return
        if user_1 == user_2:
            print("Error: same user refered")
            return 
        user_1 = User(user_1)
        user_2 = User(user_2)
        for log in self.logs:
            if [log.from_user, log.to_user] == [user_1, user_2] or [
                log.from_user,
                log.to_user,
            ] == [user_2, user_1]:
                print(f"{log.from_user} -> {log.to_user}: {log.content}")

    def is_user_exists(self, user: User or str) -> bool:
        # ChatRoom内にいるかを検索する
        # 名前でもUserクラスでも使えるようにした
        if isinstance(user, str):
            user = User(user)

        for other_user in self.users:
            if other_user == user:
                return True
        return False

    def parse_chat(self, command_line: str):
        command_line = command_line.split(" ") #半角区切りにする
        if command_line[0] == "add_user":
            if len(command_line) != 2:
                print("Usage: add_user user_name")
                return 
            user = command_line[1]
            self.add_user(user)

        elif command_line[0] == "talk":
            print(command_line)
            if len(command_line) < 3:
                print("Usage: talk from_user_name to_user_name talk_content")
                return 
            from_user = command_line[1]
            to_user = command_line[2]
            content = " ".join(
                command_line[3:]
            )  # 文字列は4番目の要素以降, 英語の入力を仮定し, 半角スペースで結合する
            self.talk(from_user, to_user, content)

        elif command_line[0] == "show_log":
            if len(command_line) != 3:
                print("Usage: show_log user_name1 user_name2")
                return 
            from_user = command_line[1]
            to_user = command_line[2]
            self.show_log(from_user, to_user)

        elif command_line[0] == "quit":
            # 一応止めるコマンドを作る
            exit()


def main():
    chatroom = ChatRoom()
    while True:
        command_line = input(">> ")
        chatroom.parse_chat(command_line)


if __name__ == "__main__":
    main()
