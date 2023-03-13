import os
from supabase import create_client, Client

url: str = os.environ.get("https://nzfzusovrjcgmqdfhopn.supabase.co")
key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im56Znp1c292cmpjZ21xZGZob3BuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY3ODcyMzQ1OCwiZXhwIjoxOTk0Mjk5NDU4fQ.LbB07eekUE5xot9osHLW5GDLPb92389_ol8qEymuYO4")
supabase: Client = create_client(url, key)

def addUser(user, password)
    return
def deleteUser(user, password)
    return
def change_user_username(user, password, newUsername)
    return
def changeUserPassword(user, password, newPassword)
    return
