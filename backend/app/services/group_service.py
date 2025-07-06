from app.extensions import db
from app.models.group import Group
from app.models.group_membership import GroupMembership
from app.models.user import User
from sqlalchemy.exc import IntegrityError


class GroupService:
    def create_group(self, name: str, description: str, creator_id: int, campus_id: int = None) -> dict:
        """
        Create a new group. The creator is automatically added as a member.
        """
        # Validate creator exists
        creator = User.query.get(creator_id)
        if not creator:
            raise ValueError("User not found.")

        # Create group
        group = Group(
            name=name,
            description=description,
            creator_id=creator_id,
            campus_id=campus_id
        )
        db.session.add(group)
        db.session.flush()  # Flush to get group.id before commit

        # Add creator as member (with role 'admin' or similar)
        membership = GroupMembership(
            user_id=creator_id,
            group_id=group.id,
            role='admin'  # Roles can be extended: admin, moderator, member
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

    def get_group_by_id(self, group_id: int) -> dict:
        """
        Get group details by ID.
        """
        group = Group.query.get(group_id)
        if not group:
            raise ValueError("Group not found.")

        return {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "creator_id": group.creator_id,
            "campus_id": group.campus_id
        }

    def list_groups(self, campus_id: int = None, limit: int = 50, offset: int = 0) -> list:
        """
        List groups, optionally filtered by campus.
        """
        query = Group.query
        if campus_id:
            query = query.filter_by(campus_id=campus_id)

        groups = query.order_by(Group.name.asc()).limit(limit).offset(offset).all()

        return [
            {
                "id": g.id,
                "name": g.name,
                "description": g.description,
                "creator_id": g.creator_id,
                "campus_id": g.campus_id
            }
            for g in groups
        ]

    def add_member(self, group_id: int, user_id: int, role: str = "member") -> dict:
        """
        Add a user to a group as a member.
        """
        group = Group.query.get(group_id)
        user = User.query.get(user_id)
        if not group or not user:
            raise ValueError("Group or User not found.")

        # Check if already member
        existing = GroupMembership.query.filter_by(group_id=group_id, user_id=user_id).first()
        if existing:
            raise ValueError("User is already a member of this group.")

        membership = GroupMembership(
            user_id=user_id,
            group_id=group_id,
            role=role
        )
        db.session.add(membership)
        db.session.commit()

        return {
            "message": "User added to group.",
            "group_id": group_id,
            "user_id": user_id
        }

    def remove_member(self, group_id: int, user_id: int) -> dict:
        """
        Remove a user from a group.
        """
        membership = GroupMembership.query.filter_by(group_id=group_id, user_id=user_id).first()
        if not membership:
            raise ValueError("Membership not found.")

        db.session.delete(membership)
        db.session.commit()

        return {
            "message": "User removed from group.",
            "group_id": group_id,
            "user_id": user_id
        }

    def list_members(self, group_id: int) -> list:
        """
        List members of a group.
        """
        memberships = GroupMembership.query.filter_by(group_id=group_id).all()
        return [
            {
                "user_id": m.user_id,
                "role": m.role
            }
            for m in memberships
        ]
