from users.models import User


def reset_shared_with(note):
    """Reset shared with users."""
    note.shared_with.clear()
    return note

def assign_shared_with(users, note):
    """Assign shared with users."""
    reset_shared_with(note)
    for user_dict in users:
        username = user_dict.get('username')
        user = User.objects.get(username=username)
        note.shared_with.add(user)
    return note
