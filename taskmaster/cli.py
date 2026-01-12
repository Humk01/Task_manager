import argparse
from taskmaster.database import add_task
from taskmaster.database import db

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="adds something")
    sub.add_parser("list", help="list something")
    

    # params data for add_task
    add.add_argument("title", help="add a title")
    add.add_argument("--description", help="add a description", default="")
    add.add_argument("--status", help='add a status to the project', default='todo')
    add.add_argument("--priority", help="add a prioriy", default="")
    add.add_argument("--due_date", help="add a due date")

    args = parser.parse_args()

    if args.command =="add":
        task=add_task(db,
                      title=args.title,
                 description=args.description,
                 status=args.status,
                 priority=args.priority,
                 due_date=args.due_date)
        print(task)
    elif args.command == "list":
        print("called list")

    def add_command():
        pass

if __name__ == "__main__":
    main()


