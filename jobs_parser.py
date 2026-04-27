from flask_restful import reqparse


job_parser = reqparse.RequestParser()
job_parser.add_argument('job', required=True)
job_parser.add_argument('team_leader', required=True, type=int)
job_parser.add_argument('work_size', required=True, type=int)
job_parser.add_argument('collaborators', required=True)
job_parser.add_argument('is_finished', required=True, type=bool)