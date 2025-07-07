from app.extensions import db
from app.models.group import Group
from app.models.group_membership import GroupMembership
from app.models.user import User
from sqlalchemy.exc import IntegrityError

def create_group(name: str, description: str, creator_id: int, campus_id: int = None) -> dict:
    # same code as your method but not inside a class
    creator = User.query.get(creator_id)
    if not creator:
        raise ValueError("User not found.")

    group = Group(
        name=name,
        description=description,
        creator_id=creator_id,
        campus_id=campus_id
    )
    db.session.add(group)
    db.session.flush()

    membership = GroupMembership(
        user_id=creator_id,
        group_id=group.id,
        role='admin'
    )
    db.session.add(membership)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Group with this name already exists.")

    return {
        "message": "Group created successfully.",
        "group_id": group.id
    }


