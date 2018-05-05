import tornado.ioloop
import tornado.web
import os.path
from PIL import Image
import io
import base64
class MainHandler(tornado.web.RequestHandler):
    # renders main home page
    def get(self):
       self.render("index.html")
class DemoHandler(tornado.web.RequestHandler):
    #render demo page
    def get(self):
       self.render("demo.html")
class ImagesHandler(tornado.web.RequestHandler):
    # handles images request via get request 
    def get(self,zoom,xcooridinate,ycoordinate):
        outputImg=io.BytesIO()
        self.getImage(int(zoom),int(xcooridinate),int(ycoordinate))# get image passing this parameters
        self.img.save(outputImg,"JPEG")# self.write expects an byte type output therefore we convert image into byteIO steam
        self.set_header("Connection","keep-alive")
        self.set_header("Content-Type", "image/jpeg")
        self.write(outputImg.getvalue())#we get actual data write it to front end
    def getImage(self,param1,param2,param3):
        #dummy image generation
        self.img = Image.new('RGB', (256, 256), ((param1)*18%256,(param2)*126%256,(param3)*150%256))
    def convertZXYtoreuqired(self,z,x,y):
        #TODO given zoom level x y tile in required parameter of the fpa circuit

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/home", MainHandler),
        (r"/demo", DemoHandler),
        (r"/images/(?P<param1>[^\/]+)/?(?P<param2>[^\/]+)?/?(?P<param3>[^\/]+)?",ImagesHandler)
    ],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"))
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
