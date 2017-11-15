import cherrypy
import random
from sqlalchemy import desc
from webapp.libs.mediahelper import MediaHelper
from webapp.libs.models.teacher import Teacher
from webapp.libs.models.event import Event
from webapp.libs.models.schedule import Schedule


class InsideOutCms(object):
    @cherrypy.expose
    @cherrypy.tools.render(template="cms/index.html")
    def index(self, error="0", login=None, password=None):
        if cherrypy.request.method == "POST" and login and password:
            if not cherrypy.tools.auth.start_session(login, password):
                error = 2  # wrong credentials
        return {
            "error": error,
            "auth": cherrypy.tools.auth.check_session()
        }


class InsideOutCmsTeachers(object):
    @cherrypy.expose
    @cherrypy.tools.render(template="cms/teacher_list.html")
    @cherrypy.tools.auth()
    def index(self):
        session = cherrypy.request.db
        teachers = session.query(Teacher).order_by(Teacher.sortkey).all()
        return {"teachers": teachers}

    @cherrypy.expose
    @cherrypy.tools.render(on=False)
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def order(self, **kwargs):
        order = cherrypy.request.json
        if order:
            session = cherrypy.request.db
            teachers = session.query(Teacher).all()
            for teacher in teachers:
                teacher.sortkey = order.index(teacher.teacher_id) + 1
            session.commit()

    @cherrypy.expose
    @cherrypy.tools.render(template="cms/teacher_record.html")
    @cherrypy.tools.auth()
    def record(self, teacher_id=None, photo=None, name=None, col1=None, col2=None, enabled=False):
        session = cherrypy.request.db
        if cherrypy.request.method == "POST":
            # save model and redirect
            if teacher_id != "":
                teacher = session.query(Teacher).filter(Teacher.teacher_id == teacher_id).one()
                teacher.name = name
                teacher.col1 = col1
                teacher.col2 = col2
                teacher.enabled = enabled
            else:
                teacher = Teacher()
                teacher.name = name
                teacher.col1 = col1
                teacher.col2 = col2
                teacher.sortkey = 0
                teacher.enabled = enabled
                session.add(teacher)
            session.commit()

            if teacher.sortkey == 0:
                teacher.sortkey = teacher.teacher_id
                session.commit()

            if photo and photo.file:
                upload_file = MediaHelper.teacher_media_file(teacher.teacher_id)
                with open(upload_file, 'wb') as out:
                    while True:
                        upload_data = photo.file.read(8192)
                        if not upload_data:
                            break
                        out.write(upload_data)

            raise cherrypy.HTTPRedirect("/cms/teachers/record?teacher_id=%s" % teacher.teacher_id)
        else:
            # load and show model
            teacher = session.query(Teacher).filter(Teacher.teacher_id == teacher_id).one() if teacher_id else None
            return {"teacher": teacher}


class InsideOutCmsEvents(object):
    @cherrypy.expose
    @cherrypy.tools.render(template="cms/event_list.html")
    @cherrypy.tools.auth()
    def index(self):
        session = cherrypy.request.db
        events = session.query(Event).order_by(desc(Event.date)).all()
        return {"events": events}

    @cherrypy.expose
    @cherrypy.tools.render(template="cms/event_record.html")
    @cherrypy.tools.auth()
    def record(self, event_id=None, photo=None, title=None, text=None, date=None, enabled=False):
        session = cherrypy.request.db
        if cherrypy.request.method == "POST":
            # save model and redirect
            if event_id != "":
                event = session.query(Event).filter(Event.event_id == event_id).one()
                event.title = title
                event.text = text
                event.date = date
                event.enabled = enabled
            else:
                event = Event()
                event.title = title
                event.text = text
                event.date = date
                event.enabled = enabled
                session.add(event)
            session.commit()

            if photo and photo.file:
                upload_file = MediaHelper.event_media_file(event.event_id)
                with open(upload_file, 'wb') as out:
                    while True:
                        upload_data = photo.file.read(8192)
                        if not upload_data:
                            break
                        out.write(upload_data)

            raise cherrypy.HTTPRedirect("/cms/events/record?event_id=%s" % event.event_id)
        else:
            # load and show model
            event = session.query(Event).filter(Event.event_id == event_id).one() if event_id else None
            return {"event": event}


class InsideOutCmsSchedule(object):
    @cherrypy.expose
    @cherrypy.tools.render(template="cms/schedule_list.html")
    @cherrypy.tools.auth()
    def index(self):
        session = cherrypy.request.db
        schedule = session.query(Schedule).order_by(desc(Schedule.date)).all()
        return {"schedule": schedule}

    @cherrypy.expose
    @cherrypy.tools.render(template="cms/schedule_record.html")
    @cherrypy.tools.auth()
    def record(self, schedule_id=None, date=None, content=None, enabled=False):
        session = cherrypy.request.db
        if cherrypy.request.method == "POST":
            # save model and redirect
            if schedule_id != "":
                schedule = session.query(Schedule).filter(Schedule.schedule_id == schedule_id).one()
                schedule.date = date
                schedule.content = content
                schedule.enabled = enabled
            else:
                schedule = Schedule()
                schedule.date = date
                schedule.content = content
                schedule.enabled = enabled
                session.add(schedule)
            session.commit()
            raise cherrypy.HTTPRedirect("/cms/schedule/record?schedule_id=%s" % schedule.schedule_id)
        else:
            # load and show model
            schedule = session.query(Schedule).filter(Schedule.schedule_id == schedule_id).one() if schedule_id else None
            return {"schedule": schedule}
