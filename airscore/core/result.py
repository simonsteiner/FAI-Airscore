"""
JSON Results Creation

contains
    Task_result class
    Comp_result class

Methods:
    Contains the list of fields that should be used during JSON file creation
    Creating the result JSON files, functions get field list from this classes.
    JSON will also reflect field order inside lists.

    create_json_file:   function to create task and comp results file.
                        It also insert the entry in database.

- AirScore -
Stuart Mackintosh - Antonio Golfari
2019
"""

from myconn import Database


class Task_result:
    """
        Task result fields lists
    """

    info_list = ['comp_name',
                 'comp_site',
                 'comp_class',
                 'date',
                 'task_name',
                 'time_offset',
                 'comment',
                 'window_open_time',
                 'task_deadline',
                 'window_close_time',
                 'check_launch',
                 'start_time',
                 'start_close_time',
                 'SS_interval',
                 'start_iteration',
                 'last_start_time',
                 'task_type',
                 'distance',
                 'opt_dist',
                 'SS_distance',
                 'stopped_time',
                 'goal_altitude']

    route_list = ['name',
                  'description',
                  'how',
                  'radius',
                  'shape',
                  'type',
                  'lat',
                  'lon',
                  'altitude']

    formula_list = ['formula_name',
                    'formula_type',
                    'formula_version',
                    'formula_distance',  # 'on', 'difficulty', 'off'
                    'formula_arrival',  # 'position', 'time', 'off'
                    'formula_departure',  # 'on', 'leadout', 'off'
                    'lead_factor',  # float
                    'formula_time',  # 'on', 'off'
                    'arr_alt_bonus',  # float
                    'arr_min_height',  # int
                    'arr_max_height',  # int
                    'validity_min_time',  # seconds
                    'score_back_time',  # seconds
                    'max_JTG',
                    'JTG_penalty_per_sec',
                    'nominal_goal',  # percentage / 100
                    'nominal_dist',  # meters
                    'nominal_time',  # seconds
                    'nominal_launch',  # percentage / 100
                    'min_dist',  # meters
                    'score_back_time',  # seconds
                    'no_goal_penalty',
                    'glide_bonus',
                    'tolerance',  # percentage / 100
                    'scoring_altitude',  # 'GPS', 'QNH'
                    ]

    stats_list = ['pilots_launched',
                  'pilots_present',
                  'pilots_ess',
                  'pilots_landed',
                  'pilots_goal',
                  'fastest',
                  'fastest_in_goal',
                  'min_dept_time',
                  'min_ess_time',
                  'max_distance',
                  'tot_distance_flown',
                  'tot_dist_over_min',
                  'day_quality',
                  'dist_validity',
                  'time_validity',
                  'launch_validity',
                  'stop_validity',
                  'arr_weight',
                  'dep_weight',
                  'time_weight',
                  'dist_weight',
                  'avail_dist_points',
                  'avail_dep_points',
                  'avail_time_points',
                  'avail_arr_points',
                  'max_score',
                  'min_lead_coeff',
                  'tot_flight_time']

    results_list = ['track_id',
                    'par_id',
                    'ID',
                    'civl_id',
                    'fai_id',
                    'name',
                    'sponsor',
                    'nat',
                    'sex',
                    'glider',
                    'glider_cert',
                    'team',
                    'nat_team',
                    'distance_flown',
                    'distance',
                    'speed',
                    'real_start_time',
                    'goal_time',
                    'result_type',
                    'SSS_time',
                    'ESS_time',
                    'ESS_rank',
                    'turnpoints_made',
                    'distance_score',
                    'time_score',
                    'departure_score',
                    'arrival_score',
                    'score',
                    'penalty',
                    'comment',
                    'lead_coeff',
                    'ESS_altitude',
                    'goal_altitude',
                    'last_altitude',
                    'max_altitude',
                    'first_time',
                    'last_time',
                    'landing_altitude',
                    'landing_time',
                    'flight_time',
                    'track_file',
                    'pil_id']


class Comp_result(object):
    """
        Comp result fields lists
    """

    info_list = ['id',
                 'comp_name',
                 'comp_class',
                 'type',
                 'comp_site',
                 'date_from',
                 'date_to',
                 'sanction',
                 'MD_name',
                 'contact',
                 'comp_code',
                 'restricted',
                 'time_offset',
                 'website']

    formula_list = ['formula_name',
                    'formula_type',
                    'formula_version',
                    'comp_class',  # 'HG', 'PG'
                    'overall_validity',  # 'ftv', 'all',
                    'validity_param',
                    'formula_distance',  # 'on', 'difficulty', 'off'
                    'formula_arrival',  # 'position', 'time', 'off'
                    'formula_departure',  # 'on', 'leadout', 'off'
                    'lead_factor',  # float
                    'formula_time',  # 'on', 'off'
                    'arr_alt_bonus',  # float
                    'arr_min_height',  # int
                    'arr_max_height',  # int
                    'validity_min_time',  # seconds
                    'score_back_time',  # seconds
                    'max_JTG',      # seconds
                    'JTG_penalty_per_sec',
                    'nominal_goal',  # percentage / 100
                    'nominal_dist',  # meters
                    'nominal_time',  # seconds
                    'nominal_launch',  # percentage / 100
                    'min_dist',  # meters
                    'score_back_time',  # seconds
                    'no_goal_penalty',  # percentage / 100
                    'glide_bonus',
                    'tolerance',  # percentage / 100
                    'scoring_altitude',  # 'GPS', 'QNH'
                    ]

    tasks_list = ['task_name',
                  'date',
                  'comment',
                  'opt_dist',
                  'pilots_goal',
                  'day_quality',
                  'max_score',
                  'task_type']

    ''' result_list comes from Participant obj, and RegisteredPilotView
        available fields are: (`par_id`, `comp_id`, `civl_id`, `fai_id`, `pil_id`, `ID`, `name`, `sex`, `nat`,
                            `glider`, `class`, `sponsor`, `team`, `nat_team`, 'results')'''
    result_list = ['ID',
                   'par_id',
                   'civl_id',
                   'fai_id',
                   'name',
                   'sex',
                   'nat',
                   'glider',
                   'glider_cert',
                   'sponsor',
                   'team',
                   'nat_team',
                   'status',
                   'pil_id',
                   'score',
                   'results']


def create_json_file(comp_id, code, elements, task_id=None, status=None):
    """
    creates the JSON file of results
    """
    import os
    import json
    from time import time
    from datetime import datetime
    import Defines as d
    from db_tables import tblResultFile as R
    from calcUtils import CJsonEncoder
    import jsonpickle

    timestamp = int(time())  # timestamp of generation
    dt = datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M%S')
    filename = '_'.join([code, dt]) + '.json'

    '''adding data section to the elements, with:
        timestamp, status'''
    result = {'file_stats': {'timestamp': timestamp, 'status': status}}
    result.update(elements)

    '''creating json formatting'''
    content = json.dumps(result, cls=CJsonEncoder)
    # content = jsonpickle.encode(result)

    '''creating file'''
    with open(d.RESULTDIR + filename, 'w') as f:
        f.write(content)
    os.chown(d.RESULTDIR + filename, 1000, 1000)

    '''create database entry'''
    with Database() as db:
        result = R(comPk=comp_id, tasPk=task_id, refTimestamp=timestamp, refJSON=filename, refStatus=status)
        db.session.add(result)
        db.session.commit()
        ref_id = result.refPk
    return ref_id
