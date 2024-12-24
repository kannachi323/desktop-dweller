from db.config import supabase, users_table

def add_user(user_data: dict):
    response = (
        supabase.table("users")
        .insert("first_name", user_data["first_name"])
        .insert("last_name", user_data["last_name"])
    )

    return response