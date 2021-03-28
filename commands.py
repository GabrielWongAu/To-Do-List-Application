import click
from flask.cli import with_appcontext
from main import db, bcrypt
from flask import Blueprint
from datetime import datetime

db_commands = Blueprint("db-custom", __name__)

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

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
    l1.name = "Prepare for AWS Certified Solutions Architect Associate Certification"
    l1.description = "Deep dive into Amazon VPC, deep dive into Amazon Lambda and Serverless components & learn the test taking strategies for This Exam"
    l1.user_id = 1
    db.session.add(l1)

    l2 = List()
    l2.name = "Prepare for HashiCorp Cloud Engineer Certification Terraform Associate"
    l2.description = "Study Terraform Basics, use the Terraform CLI (outside of core workflow) and interact with Terraform modules "
    l2.user_id = 1
    db.session.add(l2)

    l3 = List()
    l3.name = "Prepare for CNCF Certified Kubernetes Administrator (CKA) Certification"
    l3.description = "Setup a kubernetes cluster 10 times and complete the Certified Kubernetes Administrator course on Linux Academy"
    l3.user_id = 2
    db.session.add(l3)

    db.session.commit()

    print("Tables seeded")