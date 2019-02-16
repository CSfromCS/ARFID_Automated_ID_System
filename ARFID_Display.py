import eel

eel.init('web')

web_app_options = {
	'mode': 'chrome-app',
	'port': 8080,
	'host': 'localhost',
	'chromeFlags': ["--browser-startup-dialog"]
}

eel.start('index.html', block=False, options=web_app_options, size=(600,500))

while True:
	eel.sleep(10)
