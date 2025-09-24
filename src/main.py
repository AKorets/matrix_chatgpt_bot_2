import asyncio
import json
import os
from pathlib import Path
import signal
import sys

from bot import Bot
from log import getlogger

logger = getlogger()


async def main():
    need_import_keys = False
    config_path = Path(os.path.dirname(__file__)).parent / "config.json"
    help_message_path = (
        Path(os.path.dirname(__file__)).parent / "custom_help_message.txt"
    )

    if os.path.isfile(help_message_path):
        try:
            f = open(help_message_path, encoding="utf8")
            custom_help_message = ""
            for line in f.readlines():
                custom_help_message += line
        except Exception as e:
            logger.error(e)
            sys.exit(1)
    else:
        custom_help_message = None

    # Load .env if present
    from dotenv import load_dotenv
    dotenv_path = Path(os.path.dirname(__file__)).parent / ".env"
    if os.path.isfile(dotenv_path):
        load_dotenv(dotenv_path)

    if os.path.isfile(config_path):
        try:
            fp = open(config_path, encoding="utf8")
            config = json.load(fp)
        except Exception:
            logger.error("config.json load error, please check the file")
            sys.exit(1)

        # Get the actual values being used
        homeserver = config.get("homeserver") or os.environ.get("HOMESERVER")
        user_id = config.get("user_id") or os.environ.get("USER_ID")
        password = config.get("password") or os.environ.get("PASSWORD")
        device_id = config.get("device_id") or os.environ.get("DEVICE_ID")
        openai_api_key = config.get("openai_api_key") or os.environ.get("OPENAI_API_KEY")
        
        # Log the Matrix connection parameters
        logger.info("=== Matrix Bot Configuration ===")
        logger.info(f"Homeserver: {homeserver}")
        logger.info(f"User ID: {user_id}")
        logger.info(f"Device ID: {device_id}")
        logger.info(f"Password: {'***' if password else 'None'}")
        logger.info(f"OpenAI API Key: {'***' if openai_api_key else 'None'}")
        logger.info("================================")
        
        matrix_bot = Bot(
            homeserver=homeserver,
            user_id=user_id,
            password=password,
            access_token=config.get("access_token") or os.environ.get("ACCESS_TOKEN"),
            device_id=device_id,
            whitelist_room_id=config.get("room_id") or os.environ.get("ROOM_ID"),
            import_keys_path=config.get("import_keys_path") or os.environ.get("IMPORT_KEYS_PATH"),
            import_keys_password=config.get("import_keys_password") or os.environ.get("IMPORT_KEYS_PASSWORD"),
            openai_api_key=openai_api_key,
            gpt_api_endpoint=config.get("gpt_api_endpoint") or os.environ.get("GPT_API_ENDPOINT"),
            gpt_model=config.get("gpt_model") or os.environ.get("GPT_MODEL"),
            max_tokens=config.get("max_tokens") or int(os.environ.get("MAX_TOKENS", 4000)),
            top_p=config.get("top_p") or float(os.environ.get("TOP_P", 1.0)),
            presence_penalty=config.get("presence_penalty") or float(os.environ.get("PRESENCE_PENALTY", 0.0)),
            frequency_penalty=config.get("frequency_penalty") or float(os.environ.get("FREQUENCY_PENALTY", 0.0)),
            reply_count=config.get("reply_count") or int(os.environ.get("REPLY_COUNT", 1)),
            system_prompt=config.get("system_prompt") or os.environ.get("SYSTEM_PROMPT"),
            temperature=config.get("temperature") or float(os.environ.get("TEMPERATURE", 0.8)),
            lc_admin=config.get("lc_admin") or os.environ.get("LC_ADMIN"),
            image_generation_endpoint=config.get("image_generation_endpoint") or os.environ.get("IMAGE_GENERATION_ENDPOINT"),
            image_generation_backend=config.get("image_generation_backend") or os.environ.get("IMAGE_GENERATION_BACKEND"),
            image_generation_size=config.get("image_generation_size") or os.environ.get("IMAGE_GENERATION_SIZE"),
            sdwui_steps=config.get("sdwui_steps") or int(os.environ.get("SDWUI_STEPS", 20)),
            sdwui_sampler_name=config.get("sdwui_sampler_name") or os.environ.get("SDWUI_SAMPLER_NAME"),
            sdwui_cfg_scale=config.get("sdwui_cfg_scale") or float(os.environ.get("SDWUI_CFG_SCALE", 7)),
            image_format=config.get("image_format") or os.environ.get("IMAGE_FORMAT"),
            gpt_vision_model=config.get("gpt_vision_model") or os.environ.get("GPT_VISION_MODEL"),
            gpt_vision_api_endpoint=config.get("gpt_vision_api_endpoint") or os.environ.get("GPT_VISION_API_ENDPOINT"),
            timeout=config.get("timeout") or float(os.environ.get("TIMEOUT", 120.0)),
            custom_help_message=custom_help_message,
        )
        if (
            (config.get("import_keys_path") or os.environ.get("IMPORT_KEYS_PATH"))
            and (config.get("import_keys_password") or os.environ.get("IMPORT_KEYS_PASSWORD")) is not None
        ):
            need_import_keys = True

    else:
        matrix_bot = Bot(
            homeserver=os.environ.get("HOMESERVER"),
            user_id=os.environ.get("USER_ID"),
            password=os.environ.get("PASSWORD"),
            access_token=os.environ.get("ACCESS_TOKEN"),
            device_id=os.environ.get("DEVICE_ID"),
            whitelist_room_id=os.environ.get("ROOM_ID"),
            import_keys_path=os.environ.get("IMPORT_KEYS_PATH"),
            import_keys_password=os.environ.get("IMPORT_KEYS_PASSWORD"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            gpt_api_endpoint=os.environ.get("GPT_API_ENDPOINT"),
            gpt_model=os.environ.get("GPT_MODEL"),
            max_tokens=int(os.environ.get("MAX_TOKENS", 4000)),
            top_p=float(os.environ.get("TOP_P", 1.0)),
            presence_penalty=float(os.environ.get("PRESENCE_PENALTY", 0.0)),
            frequency_penalty=float(os.environ.get("FREQUENCY_PENALTY", 0.0)),
            reply_count=int(os.environ.get("REPLY_COUNT", 1)),
            system_prompt=os.environ.get("SYSTEM_PROMPT"),
            temperature=float(os.environ.get("TEMPERATURE", 0.8)),
            lc_admin=os.environ.get("LC_ADMIN"),
            image_generation_endpoint=os.environ.get("IMAGE_GENERATION_ENDPOINT"),
            image_generation_backend=os.environ.get("IMAGE_GENERATION_BACKEND"),
            image_generation_size=os.environ.get("IMAGE_GENERATION_SIZE"),
            sdwui_steps=int(os.environ.get("SDWUI_STEPS", 20)),
            sdwui_sampler_name=os.environ.get("SDWUI_SAMPLER_NAME"),
            sdwui_cfg_scale=float(os.environ.get("SDWUI_CFG_SCALE", 7)),
            image_format=os.environ.get("IMAGE_FORMAT"),
            gpt_vision_model=os.environ.get("GPT_VISION_MODEL"),
            gpt_vision_api_endpoint=os.environ.get("GPT_VISION_API_ENDPOINT"),
            timeout=float(os.environ.get("TIMEOUT", 120.0)),
            custom_help_message=custom_help_message,
        )
        if (
            os.environ.get("IMPORT_KEYS_PATH")
            and os.environ.get("IMPORT_KEYS_PASSWORD") is not None
        ):
            need_import_keys = True

    await matrix_bot.login()
    if need_import_keys:
        logger.info("start import_keys process, this may take a while...")
        await matrix_bot.import_keys()
    else:
        logger.info("no import_keys process")

    sync_task = asyncio.create_task(
        matrix_bot.sync_forever(timeout=30000, full_state=True)
    )

    # handle signal interrupt
    loop = asyncio.get_running_loop()
    for signame in ("SIGINT", "SIGTERM"):
        loop.add_signal_handler(
            getattr(signal, signame),
            lambda: asyncio.create_task(matrix_bot.close(sync_task)),
        )

    if matrix_bot.client.should_upload_keys:
        await matrix_bot.client.keys_upload()

    await sync_task


if __name__ == "__main__":
    logger.info("matrix chatgpt bot start.....")
    asyncio.run(main())
