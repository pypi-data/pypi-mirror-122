from sys import argv
from os import mkdir, getcwd

mkdir('a')

args = argv
#print(args)
cwd = getcwd()
mainpy = """from webhost.api import init, server
from views import *
from settings import settings

app = init()
app.config(settings)

views(app)

server.run(app)
"""

viewspy = """
def views(app):
	def home(request, response):
		response.text = app.usetemplate("index.html")

	app.url('/', home)

	@app.route('/about')
	def about(request, response):
		response.text = "This is the about page!"
"""

settings = """settings = {

	'Http404': '404, Page not found!'

}
"""


if args[1] == '-n':

	if args[2] == '-project':

		if args[3] == '-demo':

			folder = args[4]
			mkdir(folder)

			mainfile = f'{cwd}\\{folder}\\main.py'
			mainfile = mainfile.replace('\\', "/")	
			x = open(mainfile, 'x').write(mainpy)

			viewsfile = f'{cwd}\\{folder}\\views.py'
			viewsfile = viewsfile.replace('\\', "/")
			x = open(viewsfile, 'x').write(viewspy)

			settfile = f'{cwd}\\{folder}\\settings.py'
			settfile = settfile.replace('\\', "/")
			x = open(settfile, 'x').write(settings)

			mkdir(f'{args[4]}\\templates')
			mkdir(f'{args[4]}\\static')			

			index = f'{cwd}\\{folder}\\templates\\index.html'
			index = index.replace('\\', "/")
			x = open(index, 'x').write("""<!DOCTYPE html>
<html>
<header>
    <title>Demo App</title>

    <link href="/main.css" type="text/css" rel="stylesheet">
</header>

<body>
    <h1>Hello, the name of the framework is WebHost</h1>
</body>

</html>""")

			css = f'{cwd}\\{folder}\\static\\main.css'
			css = css.replace('\\', "/")
			x = open(css, 'x').write("""body {
    background-color: grey;
    text-align: center;
}""")

		else:
			folder = args[3]
			mkdir(folder)

			mainfile = f'{cwd}\\{folder}\\main.py'
			mainfile = mainfile.replace('\\', "/")	
			x = open(mainfile, 'x').write("""from webhost.api import init, server""")

			viewsfile = f'{cwd}\\{folder}\\views.py'
			viewsfile = viewsfile.replace('\\', "/")
			x = open(viewsfile, 'x')

			mkdir(f'{cwd}\\{folder}\\templates')
			mkdir(f'{cwd}\\{folder}\\static')

			css = f'{cwd}\\{folder}\\static\\main.css'
			css = css.replace('\\', "/")
			x = open(css, 'x').write("""body {
    background-color: white;
    text-decoration: none;
    font-family: sans-serif;    
}""")			

	else:
		print("Unidentified command!")
		exit()


else:
	print("Unidentified command!")
	exit()		