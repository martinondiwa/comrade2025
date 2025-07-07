from app.extensions import db
from app.models.group import Group
from app.models.group_membership import GroupMembership
from app.models.user import User
from sqlalchemy.exc import IntegrityError

class GroupService:

    @staticmethod
    def create_group(name, description, creator_id, campus_id=None):
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

        return group

    @staticmethod
    def get_all_groups():
        return Group.query.all()

    @staticmethod
    def get_group_by_id(group_id):
        return Group.query.get(group_id)

    @staticmethod
    def get_user_groups(user_id):
        memberships = GroupMembership.query.filter_by(user_id=user_id).all()
        group_ids = [m.group_id for m in memberships]
        return Group.query.filter(Group.id.in_(group_ids)).all()

    @staticmethod
    def update_group(group_id, name=None, description=None):
        group = Group.query.get(group_id)
        if not group:
            raise ValueError("Group not found.")
        if name:
            group.name = name
        if description:
            group.description = description
        db.session.commit()
        return group

    @staticmethod
    def delete_group(group_id):
        group = Group.query.get(group_id)
        if not group:
            raise ValueError("Group not found.")
        db.session.delete(group)
        db.session.commit()

    @staticmethod
    def join_group(group_id, user_id):
        if GroupMembership.query.filter_by(group_id=group_id, user_id=user_id).first():
            return False
        membership = GroupMembership(user_id=user_id, group_id=group_id, role='member')
        db.session.add(membership)
        db.session.commit()
        return True

    @staticmethod
    def leave_group(group_id, user_id):
        membership = GroupMembership.query.filter_by(group_id=group_id, user_id=user_id).first()
        if not membership:
            return False
        db.session.delete(membership)
        db.session.commit()
        return True
