import base64
import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any

from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from dotenv import load_dotenv


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


BASE_DIR = Path(__file__).resolve().parent

# Загружаем .env из корня проекта и (на всякий случай) из .venv/.env.
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / ".venv" / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
KB_PATH = BASE_DIR / "knowledge_base.json"


if not OPENAI_API_KEY:
    raise RuntimeError("Не найден OPENAI_API_KEY в переменных окружения.")
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Не найден TELEGRAM_BOT_TOKEN в переменных окружения.")


client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """
Ты ассистент интернет-магазина. Отвечай кратко и по-деловому (до 5 предложений).
Используй только подтвержденные факты из базы знаний и из входных данных пользователя.
Нельзя придумывать характеристики и цены.
Если данных недостаточно, ответь ровно так:
"Недостаточно данных в базе знаний для точного ответа."
В конце дай короткую практическую рекомендацию по выбору.
""".strip()


def load_kb() -> dict[str, Any]:
    if not KB_PATH.exists():
        return {"products": []}
    try:
        return json.loads(KB_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logger.warning("knowledge_base.json невалидный JSON, использую пустую базу.")
        return {"products": []}


def kb_as_text(kb_data: dict[str, Any]) -> str:
    return json.dumps(kb_data, ensure_ascii=False, indent=2)


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я бот-консультант магазина.\n"
        "Можно прислать:\n"
        "- текстовый вопрос\n"
        "- голосовое сообщение\n"
        "- фото товара с подписью-вопросом\n\n"
        "Также доступна команда:\n"
        "/image <описание> - сгенерировать изображение товара."
    )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = (update.message.text or "").strip()
    if not user_text:
        return
    await process_question(update, context, question_text=user_text, image_path=None)


async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    voice = update.message.voice
    if not voice:
        return

    with tempfile.TemporaryDirectory() as tmp:
        audio_path = Path(tmp) / "voice.ogg"
        tg_file = await context.bot.get_file(voice.file_id)
        await tg_file.download_to_drive(custom_path=str(audio_path))

        with audio_path.open("rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file,
            )

        question_text = transcript.text.strip()
        if not question_text:
            await update.message.reply_text("Не удалось распознать голосовое сообщение.")
            return

    await process_question(update, context, question_text=question_text, image_path=None)


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photos = update.message.photo
    if not photos:
        return

    caption = (update.message.caption or "").strip()
    question_text = caption if caption else "Проанализируй фото товара и дай краткую рекомендацию."

    with tempfile.TemporaryDirectory() as tmp:
        photo_path = Path(tmp) / "photo.jpg"
        largest = photos[-1]
        tg_file = await context.bot.get_file(largest.file_id)
        await tg_file.download_to_drive(custom_path=str(photo_path))
        await process_question(update, context, question_text=question_text, image_path=photo_path)


def ask_llm(question_text: str, kb_text: str, image_path: Path | None) -> str:
    user_content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": (
                f"Вопрос пользователя:\n{question_text}\n\n"
                f"База знаний JSON:\n{kb_text}\n\n"
                "Ответ верни кратко: 1) вывод, 2) 2-4 факта, 3) рекомендация."
            ),
        }
    ]

    if image_path is not None and image_path.exists():
        image_b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
        user_content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
            }
        )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def make_tts_mp3(text: str, output_path: Path) -> None:
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    )
    speech.stream_to_file(output_path)


async def process_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    question_text: str,
    image_path: Path | None,
) -> None:
    kb_data = load_kb()
    kb_text = kb_as_text(kb_data)

    answer_text = ask_llm(question_text=question_text, kb_text=kb_text, image_path=image_path)
    await update.message.reply_text(answer_text)

    with tempfile.TemporaryDirectory() as tmp:
        mp3_path = Path(tmp) / "answer.mp3"
        make_tts_mp3(answer_text, mp3_path)
        with mp3_path.open("rb") as audio_file:
            await update.message.reply_audio(audio=audio_file, title="Голосовой ответ")


async def image_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = " ".join(context.args).strip()
    if not prompt:
        await update.message.reply_text("Использование: /image <описание изображения>")
        return

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    with tempfile.TemporaryDirectory() as tmp:
        image_path = Path(tmp) / "generated.png"
        image_path.write_bytes(image_bytes)
        with image_path.open("rb") as img:
            await update.message.reply_photo(photo=img, caption="Сгенерированное изображение")


def main() -> None:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("image", image_cmd))
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.run_polling()


if __name__ == "__main__":
    main()
