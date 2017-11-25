import os.path

import cherrypy

from webapp.libs.tools.satool import SATool
from webapp.libs.tools.makotool import MakoTool
from webapp.libs.plugins.saplugin import SAEnginePlugin
from webapp.libs.plugins.makoplugin import MakoTemplatePlugin
from webapp.libs.tools.authtool import AuthTool

cur_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(cur_dir, 'templates')
template_cache_dir = os.path.join(cur_dir, 'templates', '.cache')
conf_dir = os.path.join(cur_dir, 'conf')
conf_path = os.path.join(cur_dir, 'conf', 'server.conf')

cherrypy.tools.db = SATool()
cherrypy.tools.render = MakoTool()
cherrypy.tools.auth = AuthTool()

from webapp.app import InsideOutApp, InsideOutAppEvents, InsideOutAppMassage
app = InsideOutApp()
app.events = InsideOutAppEvents()
app.massage = InsideOutAppMassage()

from webapp.cms import InsideOutCms, InsideOutCmsTeachers, InsideOutCmsEvents, InsideOutCmsSchedule
app.cms = InsideOutCms()
app.cms.teachers = InsideOutCmsTeachers()
app.cms.events = InsideOutCmsEvents()
app.cms.schedule = InsideOutCmsSchedule()

cherrypy.tree.mount(app, '/', conf_path)

MakoTemplatePlugin(cherrypy.engine, template_dir, template_cache_dir).subscribe()

cherrypy.engine.db = SAEnginePlugin(cherrypy.engine, "mysql://%s:%s@%s:%s/%s?charset=utf8" % (
    os.environ['INSIDEOUT_SQL_USER'],
    os.environ['INSIDEOUT_SQL_PASSWORD'],
    os.environ['INSIDEOUT_SQL_ADDRESS'],
    os.environ['INSIDEOUT_SQL_PORT'],
    os.environ['INSIDEOUT_SQL_DATABASE']
))

cherrypy.engine.db.subscribe()

if os.environ['INSIDEOUT_DEBUG'] == '1':
    cherrypy.engine.start()
