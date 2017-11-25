import cherrypy
import datetime
from webapp.libs.utils import DateUtils
from webapp.libs.models.event import Event
from webapp.libs.models.teacher import Teacher
from webapp.libs.models.schedule import Schedule
from sqlalchemy import desc


__all__ = ['InsideOutApp']


class InsideOutApp(object):
    @cherrypy.expose
    @cherrypy.tools.render(template='app/index.html')
    def index(self):
        session = cherrypy.request.db
        events = session.query(Event) \
            .filter(Event.enabled == True) \
            .order_by(desc(Event.date)) \
            .limit(3) \
            .all()
        return {
            'pageId': 'frontpage',
            'events': events
        }

    @cherrypy.expose
    @cherrypy.tools.render(template='app/schedule.html')
    def schedule(self, dt=None):

        def parse(content):
            r = []
            for line in content.split("\n"):
                if line:
                    tokens = line.split(" - ", 1)
                    if len(tokens) == 2:
                        r.append(tokens)
                    else:
                        r.append([tokens, "—"])
            return r

        session = cherrypy.request.db
        dt = datetime.datetime.strptime(dt, "%Y-%m-%d").date() if dt else datetime.date.today()

        # let's calc schedule
        # here we get 3 weeks to calculate prev and next week simultaneously
        prev_week_dt = DateUtils.get_prev_monday_sunday(dt)
        curr_week_dt = DateUtils.get_monday_sunday(dt)
        next_week_dt = DateUtils.get_next_monday_sunday(dt)

        data = session.query(Schedule) \
            .filter(Schedule.enabled == True, Schedule.date >= prev_week_dt[0], Schedule.date <= next_week_dt[1]) \
            .order_by(Schedule.date) \
            .limit(7*3) \
            .all()

        prev_link = None
        next_link = None
        schedule = [[], [], [], [], [], [], []]

        for rec in data:
            if prev_week_dt[0] <= rec.date <= prev_week_dt[1]:
                prev_link = prev_week_dt[0]
            elif next_week_dt[0] <= rec.date <= next_week_dt[1]:
                next_link = next_week_dt[0]
            elif curr_week_dt[0] <= rec.date <= curr_week_dt[1]:
                schedule[(rec.date-curr_week_dt[0]).days] = parse(rec.content)

        return {
            'pageId': 'schedule',
            'monday_f': DateUtils.format_dm(curr_week_dt[0]),
            'sunday_f': DateUtils.format_dm(curr_week_dt[1]),
            'prev_link': prev_link,
            'next_link': next_link,
            'schedule': schedule,
            "weekdays": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
            # if selected date in current week calc current weekday, else monday
            "today_weekday": datetime.date.today().weekday() if curr_week_dt[0] <= datetime.date.today() <= curr_week_dt[1] else 0
        }

    @cherrypy.expose
    @cherrypy.tools.render(template='app/teachers.html')
    def teachers(self):
        session = cherrypy.request.db
        teachers = session.query(Teacher).filter(Teacher.enabled == True).order_by(Teacher.sortkey).all()
        return {
            'pageId': 'teachers',
            "teachers": teachers
        }

    @cherrypy.expose
    @cherrypy.tools.render(template='app/psychotherapy.html')
    def psychotherapy(self):
        return {
            'pageId': 'psychotherapy'
        }

    @cherrypy.expose
    @cherrypy.tools.render(template='app/values.html')
    def values(self):
        return {
            'pageId': 'values'
        }

    @cherrypy.expose
    @cherrypy.tools.render(template='app/map.html')
    def map(self):
        return {
            'pageId': 'map'
        }

    @cherrypy.expose
    @cherrypy.tools.render(template='app/404.html')
    def default(self, arg1=None, arg2=None,):  # TODO: arrange this argsN
        return None


class InsideOutAppEvents(object):
    @cherrypy.expose
    @cherrypy.tools.render(template='app/events.html')
    def index(self, event_id=0):
        session = cherrypy.request.db
        if event_id and int(event_id):
            event = session.query(Event).filter(Event.event_id == event_id, Event.enabled == True).one()
            return {
                'pageId': 'eventsRecord',
                "event": event
            }
        else:
            return {
                'pageId': 'eventsIndex'
            }


class InsideOutAppMassage(object):
    @cherrypy.expose
    @cherrypy.tools.render(template='app/massage/index.html')
    def index(self):
        return {'pageId': 'massage_index'}

    @cherrypy.expose
    @cherrypy.tools.render(template='app/massage/classical.html')
    def classical(self):
        return {'pageId': 'massage_classical'}

    @cherrypy.expose
    @cherrypy.tools.render(template='app/massage/general.html')
    def general(self):
        return {'pageId': 'massage_general'}

    @cherrypy.expose
    @cherrypy.tools.render(template='app/massage/sports.html')
    def sports(self):
        return {'pageId': 'massage_sports'}

    @cherrypy.expose
    @cherrypy.tools.render(template='app/massage/lymphatic.html')
    def lymphatic(self):
        return {'pageId': 'massage_lymphatic'}

    @cherrypy.expose
    @cherrypy.tools.render(template='app/massage/modeling.html')
    def modeling(self):
        return {'pageId': 'massage_modeling'}

    @cherrypy.expose
    @cherrypy.tools.render(template='app/massage/aroma.html')
    def aroma(self):
        return {'pageId': 'massage_aroma'}

    @cherrypy.expose
    @cherrypy.tools.render(template='app/massage/creole.html')
    def creole(self):
        return {'pageId': 'massage_creole'}

    @cherrypy.expose
    @cherrypy.tools.render(template='app/massage/honey.html')
    def honey(self):
        return {'pageId': 'massage_honey'}
