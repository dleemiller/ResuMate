test:
	python -m unittest discover -p "*_test.py"

dev-server:
	FLASK_APP=app.py flask run --port 8000