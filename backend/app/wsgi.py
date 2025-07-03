
from app import create_app

# Use development config for now, can be changed to production
app = create_app()

if __name__ == "__main__":
    app.run()
