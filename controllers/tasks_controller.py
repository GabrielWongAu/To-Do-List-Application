from models.Task import Task
from main import db

from flask import Blueprint, request, jsonify

tasks = Blueprint('tasks',__name__, url_prefix="/tasks")