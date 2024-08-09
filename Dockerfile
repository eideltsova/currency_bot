FROM python:3.10.2

RUN mkdir -p /app/telegram_bot/
RUN python -m venv /app/telegram_bot/venv

ENV PATH="/app/telegram_bot/venv/bin:$PATH"

COPY . /app/telegram_bot/
WORKDIR /app/telegram_bot/

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "main.py"]
