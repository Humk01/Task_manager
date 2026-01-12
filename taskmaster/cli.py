import argparse
from taskmaster.database import add_task, all_tasks, get_task_by_id
from taskmaster.database import db
import json

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="adds something")
    sub.add_parser("list", help="list something")
    get_id = sub.add_parser("get", help="helps get task id")
    

    # params data for add_task
    add.add_argument("title", help="add a title")
    add.add_argument("--description", help="add a description", default="")
    add.add_argument("--status", help='add a status to the project', default='todo')
    add.add_argument("--priority", help="add a prioriy", default="")
    add.add_argument("--due_date", help="add a due date")
    add.add_argument("--tags", help="add a tag or tags")

    # params data for get_id
    get_id.add_argument("id", help="task id required",type=int)

    


    args = parser.parse_args()

    


    if args.command =="add":
        tags_list = args.tags.split(',') if args.tags else []
        tags_json = json.dumps(tags_list)
        task=add_task(db,
                      title=args.title,
                 description=args.description,
                 status=args.status,
                 priority=args.priority,
                 due_date=args.due_date,
                 tags=tags_json)
        print("task added successfully")
    
    elif args.command == "list":
        tasks = all_tasks(db)
        print("All the items in the database")
        print("="*100)
        for task in tasks:
            print(task)

    elif args.command == "get":
        item_id = get_task_by_id(db, id=args.id)
        print(item_id)
        

    def add_command():
        pass

if __name__ == "__main__":
    main()


