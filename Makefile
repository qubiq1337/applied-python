fmt:
	black .


dev:
	poetry install --only=main,dev


lock:
	poetry lock