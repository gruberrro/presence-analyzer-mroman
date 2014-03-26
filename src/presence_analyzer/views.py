# -*- coding: utf-8 -*-
"""
Defines views.
"""
import logging

import calendar
from collections import OrderedDict
from flask import redirect, render_template, redirect, url_for

from presence_analyzer.main import app
from presence_analyzer.utils import jsonify
from presence_analyzer import utils

log = logging.getLogger(__name__)  # pylint: disable-msg=C0103


@app.route('/')
def mainpage():
    """
    Redirects to front page.
    """
    return render_template('presence_weekday.html')


@app.route('/presence-weekday')
def presence_weekday():
    """
    Redirects to presence weekday page.
    """
    return render_template('presence_weekday.html')


@app.route('/mean-time-weekday')
def mean_time_weekday():
    """
    Redirects to mean time weekday page.
    """
    return render_template('mean_time_weekday.html')


@app.route('/presence-start-end')
def presence_start_end():
    """
    Redirects to presence start end page.
    """
    return render_template('presence_start_end.html')


@app.route('/api/v1/users', methods=['GET'])
@jsonify
def users_view():
    """
    Users listing for dropdown.
    """
    data = utils.get_data()

    return [{'user_id': user, 'name': u'User {0}'.format(user)}
            for user in data]


@app.route('/api/v1/mean_time_weekday/<int:user_id>', methods=['GET'])
@jsonify
def mean_time_weekday_view(user_id):
    """
    Returns mean presence time of given user grouped by weekday.
    """
    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return []

    weekdays = utils.group_by_weekday(data[user_id])
    result = [
        (
            calendar.day_abbr[weekday], utils.mean(intervals)
        )
        for weekday, intervals in weekdays.items()
    ]

    return result


@app.route('/api/v1/presence_weekday/<int:user_id>', methods=['GET'])
@jsonify
def presence_weekday_view(user_id):
    """
    Returns total presence time of given user grouped by weekday.
    """
    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return []

    weekdays = utils.group_by_weekday(data[user_id])
    result = [
        (
            calendar.day_abbr[weekday], sum(intervals)
        )
        for weekday, intervals in weekdays.items()
    ]

    result.insert(0, ('Weekday', 'Presence (s)'))
    return result


@app.route('/api/v1/presence_start_end/<int:user_id>', methods=['GET'])
@jsonify
def presence_start_end_view(user_id):
    """
    Returns time of given user grouped by mean start and end job.
    """
    data = utils.get_data()

    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return []

    weekdays = utils.group_times_by_weekday(data[user_id])
    result = [
        (
            calendar.day_abbr[weekday],
            utils.mean(times['start']),
            utils.mean(times['end']),
        )
        for weekday, times in weekdays.items()
    ]
    return result


@app.route('/api/v2/users', methods=['GET'])
@jsonify
def users_view_names():
    """
    Users listing for dropdown.
    """
    data_xml = utils.get_data_from_xml()


#na poczatku bylo to:
    # {'141': {'avatar': 'https://intranet.stxnext.pl/api/images/users/141',
    #         'name': 'Adam P.'},
    # '142': {'avatar': 'https://intranet.stxnext.pl/api/images/users/142',
    #         'name': u'Micha\u0142 K.'},
    # '144': {'avatar': 'https://intranet.stxnext.pl/api/images/users/144',
    #         'name': 'Neysa K.'},
    # '146': {'avatar': 'https://intranet.stxnext.pl/api/images/users/146',
    #         'name': 'Waldemar S.'},
    # '147': {'avatar': 'https://intranet.stxnext.pl/api/images/users/147',
    #         'name': 'Malwina N.'}}
 

#wczesniej bylo to:
    # [
    #  ('141', {'avatar': 'https://intranet.stxnext.pl/api/images/users/141',
    #    'name': 'Adam P.'}
    # ),
    #  ('176',
    #   {'avatar': 'https://intranet.stxnext.pl/api/images/users/176',
    #    'name': 'Adrian K.'}
    # ),
    #  ('170',
    #   {'avatar': 'https://intranet.stxnext.pl/api/images/users/170',
    #    'name': 'Agata J.'}),
    #  ('26',
    #   {'avatar': 'https://intranet.stxnext.pl/api/images/users/26',
    #    'name': 'Andrzej S.'}),
    #  ('165',
    #   {'avatar': 'https://intranet.stxnext.pl/api/images/users/165',
    #    'name': 'Anna D.'}),
    #  ('19',
    #   {'avatar': 'https://intranet.stxnext.pl/api/images/users/19',
    #    'name': 'Anna K.'})]
     

#bylo to:
 #    [
 #     {"141": {"name": "Adam P.", 
 #        "avatar": "https://intranet.stxnext.pl/api/images/users/141"}, 
    
 #     "176": {"name": "Adrian K.", 
 #        "avatar": "https://intranet.stxnext.pl/api/images/users/176"}, 

 #     "170": {"name": "Agata J.", 
 #        "avatar": "https://intranet.stxnext.pl/api/images/users/170"}, 

 #     "26": {"name": "Andrzej S.", 
 #        "avatar": "https://intranet.stxnext.pl/api/images/users/26"}, 

 # # jest:        
 #     [
 #     {"user_id": "141", "name": "Adam P.", 
 #        "avatar": "https://intranet.stxnext.pl/api/images/users/141"}, 
 #     "user_id": "176", "name": "Adrian K.", 
 #        "avatar": "https://intranet.stxnext.pl/api/images/users/176"}, 
 #     "user_id":"170", "name": "Agata J.", 
 #        "avatar": "https://intranet.stxnext.pl/api/images/users/170"}, 
 #     ]

    data_xml = sorted(data_xml.items(), key=lambda x: x[1]['name'])
    next_data_xml = [
            {'user_id' : user[0],
            'name': user[1]['name'],
            'avatar': user[1]['avatar']
            }
        for user in data_xml]
    
    # for user in data_xml:
    #     next_data_xml.append(
    #         {'user_id' : user[0],
    #         'name': user[1]['name'],
    #         'avatar': user[1]['avatar']
    #         })
            
    
    return next_data_xml
    # return data_xml