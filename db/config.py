import os
from supabase import create_client, Client


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


users_table: dict = {
    "uid" : str,
    "first_name" : str,
    "last_name" : str,
}





