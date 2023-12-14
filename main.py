#
# logはclass ChatRoomが全て保存
#
#
from typing import List, Dict  # will deprecated

# NG Wordsリストのファイル名
NG_WORDS_FILE = "ngwords.txt"

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

    def __repr__(self):
        return f"{self.name}"

    def __hash__(self) -> int:  # 辞書型を使うのでhashableに
        return hash(self.name)


class Log:
    """
    Logの情報をまとめるクラス
    """

    def __init__(
        self, from_user: User, to_user: User, content: str, time: int
    ):
        self.from_user = from_user
        self.to_user = to_user
        self.content: str = content
        self.time = time

    def __repr__(self) -> str:
        return f"{self.from_user} -> {self.to_user}: {self.content}"

    def __str__(self) -> str:
        return f"{self.from_user} -> {self.to_user}: {self.content}"

class ChatRoom:
    def __init__(self, room_name: str):
        self.room_name = room_name
        self.logs: List[Log] = []
        self.users: List[User] = []
    
    def add_user(self, user: User or str) -> None:
        if isinstance(user, str):
            user = User(user)

        self.users.append(user)
        return
    
    def is_user_exists(self, user: User or str) -> bool:
        # RoomManager内にいるかを検索する
        # 名前でもUserクラスでも使えるようにした
        if isinstance(user, str):
            user = User(user)

        if user in self.users:
            return True
        return False


    
    def get_all_logs(self) -> List[Log]:
        return self.logs

class RoomManager:
    """
    Chatの機能と情報をまとめるクラス
    """

    def __init__(self):
        self.users: List[User] = []
        self.logs: Dict[Dict[List[Log]]] = {}
        """
        {adam: User: {eve: User: [Log], ..., }} のような構造にする
        """
        self.time = 0
        self.rooms: Dict[ChatRoom] = {}

        # NG Wordsリストを作る
        f = open(NG_WORDS_FILE, 'r')
        self.ng_words = f.readlines()
        self.ng_words = [word.rstrip('\n') for word in self.ng_words]
        f.close()

    def add_user(self, user: User or str) -> None:
        if isinstance(user, str):
            user = User(user)

        if self.is_user_exists(user):
            print("ERROR: ID already used!")
            return

        self.users.append(user)
        print(f"{user} registered!")

        self.logs[user] = {}
        return
    
    def check_DM(self, from_user: str, room_name: str) -> str:
        if not self.is_user_exists(room_name):
            print("Error: room not exists")
            return            
        DM1_name = f"DM_{from_user}_{room_name}"
        DM2_name = f"DM_{room_name}_{from_user}"
        if DM1_name in self.rooms:
            room_name = DM1_name
        elif DM2_name in self.rooms:
            room_name = DM2_name
        else:
            self.create_room(DM1_name, [from_user, room_name])
            room_name = DM1_name
        return room_name

    def talk(self, from_user: str, room_name: str, contents: str):
        if not self.is_user_exists(from_user):
                print("Error: no user ID")
                return
        
        if room_name not in self.rooms:
            room_name = self.check_DM(from_user, room_name)
        
        room = self.rooms[room_name]
        if not room.is_user_exists(from_user):
            print("Error: not in room")
            return

        room.logs.append(Log(from_user, room_name, contents, self.time))

    def show_log(self, room_name: str):
        room = self.rooms[room_name]
        contents = room.get_all_logs()

        for content in contents:
            # NGワードのマクス
            for word in self.ng_words:
                content = str(content).replace(word, "*")
            print(content)
    
    def create_room(self, room_name: str, users: List[str]):
        # ルームを作る
        if self.is_user_exists(room_name):
            print("Error: room already exists")
            return
        room = ChatRoom(room_name)
        for user in users:
            if not self.is_user_exists(user):
                print("Error: no user ID")
                return
            room.add_user(user)
        self.rooms[room_name] = room

    def is_user_exists(self, user: User or str) -> bool:
        # RoomManager内にいるかを検索する
        # 名前でもUserクラスでも使えるようにした
        if isinstance(user, str):
            user = User(user)

        if user in self.users:
            return True
        return False

    def parse_chat(self, command_line: str):
        command_line = command_line.split(" ")  # 半角区切りにする
        if command_line[0] == "add_user":
            if len(command_line) != 2:
                print("Usage: add_user user_name")
                return
            user = command_line[1]
            self.add_user(user)

        elif command_line[0] == "create_room":
            if len(command_line) < 4:
                print("Usage: create_room room_name user_name1 user_name2 ...")
                return
            room_name = command_line[1]
            users = command_line[2:]
            self.create_room(room_name, users)

        elif command_line[0] == "talk":
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
            room_name = command_line[1]

            if len(command_line) == 3:
                user_1 = command_line[1]
                user_2 = command_line[2]
                room_name = self.check_DM(user_1, user_2)
            elif len(command_line) != 2:
                print("Usage: show_log room_name")
                return
            
            if not room_name in self.rooms:
                print("Error: room not exists")
                return

            self.show_log(room_name)
        
        elif command_line[0] == "show_rooms":
            print(self.rooms.keys())
        
        elif command_line[0] == "show_users":
            if len(command_line) == 1:
                print(self.users)
            elif len(command_line) == 2:
                room_name = command_line[1]
                if not room_name in self.rooms:
                    print("Error: room not exists")
                    return
                print(self.rooms[room_name].users)

        elif command_line[0] == "quit":
            # 一応止めるコマンドを作る
            exit()


def main():
    manager = RoomManager()
    while True:
        try:
            command_line = input(">> ")
            manager.parse_chat(command_line)
        except EOFError:
            # Ctrl + D で終了
            break


if __name__ == "__main__":
    main()
