import os
from datetime import datetime
import discord
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からデータベースの資格情報を取得
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# SQLAlchemyのエンジンを作成
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
Base = declarative_base()


# メッセージを保存するためのテーブルを定義
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    username = Column(String)
    content = Column(String)
    created_at = Column(DateTime)


# テーブルを作成
Base.metadata.create_all(engine)

# セッションを作成
Session = sessionmaker(bind=engine)
session = Session()

# Discord botの設定
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# 環境変数からbotトークンとチャンネルIDを取得
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))


@client.event
async def on_message(message):
    if message.channel.id == DISCORD_CHANNEL_ID:
        # メッセージをデータベースに保存
        new_message = Message(
            user_id=str(message.author.id),
            username=message.author.name,
            content=message.content,
            created_at=message.created_at
        )
        session.add(new_message)
        session.commit()


# botを実行する
client.run(DISCORD_BOT_TOKEN)
