build:
		docker build -t currency_bot:v1  .
run:
		docker run -d --name cur_bot --env-file .env currency_bot:v1
