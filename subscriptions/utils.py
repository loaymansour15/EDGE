import uuid

def generate_reference(user_id: int) -> str:
    return f"EGX-{user_id}-{uuid.uuid4().hex[:6].upper()}"
