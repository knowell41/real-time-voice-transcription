from utils import unique_logger
from transcriber import Transcriber
import time

logger = unique_logger()
transcriber = Transcriber(logger)

transcriber.start_listening()
try:
    logger.debug("press ctrl+c to exit")
    while True:
        pass
except KeyboardInterrupt:
    logger.debug("Terminating transcriber process...")
    transcriber.stop_listening()

print("========Transcribed text in this session=========")
print(transcriber.transcribed_text)
print("=================================================")
logger.debug("DONE")
