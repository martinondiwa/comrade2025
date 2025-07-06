from app.models.post import Post

def get_all_posts():
    return Post.query.order_by(Post.created_at.desc()).all()

def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
