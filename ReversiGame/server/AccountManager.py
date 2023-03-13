import os
from supabase import create_client, Client

url: str = os.environ.get("db.nzfzusovrjcgmqdfhopn.supabase.co")
key: str = os.environ.get("diZWo38Md4CLtftc")
supabase: Client = create_client(url, key)

def addUser(user, password)
    return
def deleteUser(user, password)
    return
def change_user_username(user, password, newUsername)
    return
def changeUserPassword(user, password, newPassword)
    return
