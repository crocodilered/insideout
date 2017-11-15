import os
import os.path
import cherrypy


class MediaHelper(object):
    """
    Temporary solution to manage files dirs and uris logic in project
    """
    @staticmethod
    def teacher_media_dir():
        return os.path.join(MediaHelper.media_root(), "teachers")

    @staticmethod
    def teacher_media_uri(teacher_id):
        return \
            "/media/teachers/%02i.png" % teacher_id if MediaHelper.teacher_media_file(teacher_id, True) \
            else None

    @staticmethod
    def teacher_media_file(teacher_id, check_existence=False):
        fname = os.path.join(MediaHelper.teacher_media_dir(), "%02i.png" % teacher_id)
        if check_existence:
            return fname if os.path.isfile(fname) else None
        else:
            return fname

    @staticmethod
    def event_uri(event_id):
        return \
            "/events/?event_id=%s" % event_id if event_id \
            else None

    @staticmethod
    def event_media_dir():
        return os.path.join(MediaHelper.media_root(), "events")

    @staticmethod
    def event_media_uri(event_id):
        return \
            "/media/events/%04i.jpg" % event_id if MediaHelper.event_media_file(event_id, True) \
            else None

    @staticmethod
    def event_media_file(event_id, check_existence=False):
        fname = os.path.join(MediaHelper.event_media_dir(), "%04i.jpg" % event_id)
        if check_existence:
            return fname if os.path.isfile(fname) else None
        else:
            return fname

    @staticmethod
    def media_root():
        return cherrypy.request.app.config['/media']['tools.staticdir.dir']
