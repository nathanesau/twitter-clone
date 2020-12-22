from flask import current_app
from app import create_app

app = create_app()


@app.before_first_request
def populate_elasticsearch():
    if not current_app.elasticsearch:
        return
    from app.models import Post
    from app.search import add_to_index
    if not current_app.elasticsearch.indices.exists(index='post'):
        for post in Post.query.all():
            add_to_index('post', post)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
