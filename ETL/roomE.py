import json
from dao.DaoRoom import DaoRooms

roomdao = DaoRooms()
with open('files/rooms.json') as f:
    rooms = json.load(f)

for building, roomlist in rooms.items():
    for room in roomlist:
        roomid = room["id"]
        room_num= room["number"]
        capacity = room["capacity"]

        roomdata = (roomid,building, room_num, capacity)

        success = roomdao.InsertRoom(roomdata)

roomdao.closeConnection()











