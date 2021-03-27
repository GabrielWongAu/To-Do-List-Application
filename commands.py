from main import db, bcrypt
from flask import Blueprint
from datetime import datetime

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def create_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_db():
    from models.List import List
    from models.Task import Task
    from models.User import User

    u1 = User()
    u1.username = "Gabe"
    u1.password = bcrypt.generate_password_hash("123456").decode("utf-8")
    db.session.add(u1)

    u2 = User()
    u2.username = "Sam"
    u2.password = bcrypt.generate_password_hash("123456").decode("utf-8")
    db.session.add(u2)

    db.session.commit()

    l1 = List()
    l1.name = "AWS Certified Solutions Architect Associate Certification"
    l1.description = "List of tasks to help prepare for my upcoming AWS Certified Solutions Architect exam"
    l1.user_id = 1
    db.session.add(l1)

    l2 = List()
    l2.name = "HashiCorp Cloud Engineer Certification Terraform Associate"
    l2.description = "List of tasks to help prepare for my upcoming Terraform Associate exam"
    l2.user_id = 1
    db.session.add(l2)

    l3 = List()
    l3.name = "CNCF Certified Kubernetes Administrator (CKA) Certification"
    l3.description = "List of tasks to help prepare for my Certified Kubernetes Administrator exam"
    l3.user_id = 2
    db.session.add(l3)

    db.session.commit()

    #Tasks for List1

    t1 = Task()
    t1.name = "Deep dive into Amazon VPC"
    t1.description = "Complete the ACG Hands-on Labs for VPCs"
    # t1.created = datetime.now()
    t1.list_id = 1
    db.session.add(t1)

    t2 = Task()
    t2.name = "Deep dive into Amazon Lambda and Serverless components"
    t2.description = "Take the ACG Intro to Lambda course but focus on limits/timeouts and events"
    # t1.created = datetime.now()
    t2.list_id = 1
    db.session.add(t2)

    t3 = Task()
    t3.name = "Learn the Test taking Strategies for This Exam"
    t3.description = "Find out the different exam strategies for this particular exam"
    # t1.created = datetime.now()
    t3.list_id = 1
    db.session.add(t3)

    #Tasks for List2

    t4 = Task()
    t4.name = "Understand Terraform Basics"
    t4.description = "For example, learn how to Handle Terraform and provider installation and versioning"
    # t4.created = datetime.now()
    t4.list_id = 2
    db.session.add(t4)

    t5 = Task()
    t5.name = "Use the Terraform CLI (outside of core workflow)"
    t5.description = "For example given a scenario choose when to use terraform fmt to format code"
    # t5.created = datetime.now()
    t5.list_id = 2
    db.session.add(t5)

    t6 = Task()
    t6.name = "Interact with Terraform modules"
    t6.description = "For example interact with module inputs and outputs	"
    # t6.created = datetime.now()
    t6.list_id = 2
    db.session.add(t6)


    #Tasks for List3

    t7 = Task()
    t7.name = "Setup a kubernetes cluster 10 times"
    t7.description = "Do this based on the Kubernetes the Hard Way course on Linux Academy"
    # t7.created = datetime.now()
    t7.list_id = 3
    db.session.add(t7)

    t8 = Task()
    t8.name = "Complete the Certified Kubernetes Administrator course on Linux Academy"
    t8.description = "This will start building the foundations required for the exam"
    # t5.created = datetime.now()
    t8.list_id = 3
    db.session.add(t8)

    t9 = Task()
    t9.name = "Read all blogs related to “How I passed CKA exam” that I have found on the internet"
    t9.description = "This will provide my good insight on how to best prepare for the exam"
    # t6.created = datetime.now()
    t9.list_id = 3
    db.session.add(t9)

    db.session.commit()
    print("Tables seeded")