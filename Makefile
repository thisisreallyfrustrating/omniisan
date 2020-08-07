all: run

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

venv:
	virtualenv --python=python3 venv && venv/bin/python setup.py develop

run: venv
	FLASK_DEBUG=1 FLASK_APP=omniisan OMNIISAN_SETTINGS=../settings.cfg venv/bin/flask run

run-worker: venv
	OMNIISAN_SETTINGS=../settings.cfg venv/bin/python omniisan/worker.py

cp-systemd:
	sudo cp systemd/omniisan.service /etc/systemd/system/omniisan.service
	sudo cp systemd/omniisan-workers\@.service /etc/systemd/system/omniisan-workers\@.service
	sudo daemon-reload

sdist:
	venv/bin/python setup.py sdist
