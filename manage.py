from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from app import create_app
from app.commands import InitDemoDbCommand

app = create_app()
manager = Manager(app)
manager.add_command("db", MigrateCommand)
manager.add_command("build_demo_data", InitDemoDbCommand)
manager.add_command("runserver", Server())

if __name__ == "__main__":
    manager.run()
