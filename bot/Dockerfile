FROM python:3.11-slim
WORKDIR /app
# O bot do telegram usa a lib pyTelegramBotAPI, precisamos instalá-la
RUN pip install pyTelegramBotAPI
COPY . .
CMD ["python", "telegram_bot.py"]