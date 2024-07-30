from utils import unique_logger
from transcriber import Transcriber
import time

logger = unique_logger()
transcriber = Transcriber(logger)

transcriber.start_listening()
time.sleep(30)
transcriber.stop_listening()


while not transcriber.audio_queue.empty():
    pass

print("-----------")
print(transcriber.transcribed_text)
print("-----------")

logger.debug("DONE")
