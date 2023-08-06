from configparser import ConfigParser
from gnani_voicebiometric_api.log_config.logger import get_logger
from gnani_voicebiometric_api.utils import voicebiometric_service

import os

current_dir = os.getcwd()

logger = get_logger(__name__)

# Reading from config file
parser = ConfigParser()
parser.read('user.config')

authenticate_api_url = "https://armour365.gnani.ai/api/verification"

def start():
    """ Set all below parameters in the config file. """
    token = input("Enter Token: ")
    accesskey = input("Enter AccessKey: ")
    userid = input("Enter Email ID: ")

    audio_name = input("Enter the full name of the audiofile with extention: ")
    audio_file = current_dir + "/" + audio_name

    speaker = input("Enter Speaker's name: ")
    try:
        logger.info("Authenticate Method ! - Start")

        # construct request headers
        headers = {
            "product": "voice-biometric",
            "token": token,
            "accesskey": accesskey,
            "userid": userid
        }

        # construct request payload
        payload = {'speaker': speaker}

        files = {'audio_file': open(audio_file, 'rb')}
        """
            Request Gnani VoiceBiometric Service to enroll your voice
        """
        response = voicebiometric_service(authenticate_api_url, headers, payload, files)
        logger.info("Response from VoiceBiometric server : {}".format(response))
        logger.info("Authenticate Method ! - End")
    except BaseException as e:
        logger.exception(e)
        logger.info("Exception in main method !")


if __name__ == '__main__':
    start()
