from configparser import ConfigParser
from armour365.log_config.logger import get_logger
from armour365.utils import voicebiometric_service

import os

current_dir = os.getcwd()

logger = get_logger(__name__)

# Reading from config file
parser = ConfigParser()
parser.read('user.config')

enroll_api_url = "https://armour365.gnani.ai/api/enrollment"

def start():
    """ Set all below parameters in the config file. """
    # certificate = input("Enter the name of the certificate with extention: ")
    # cert = current_dir + "/" + certificate
    token = input("Enter Token: ")
    accesskey = input("Enter AccessKey: ")
    audio_name = input("Enter the full name of the audiofile with extention: ")
    audio_file = current_dir + "/" + audio_name

    speaker = input("Enter Speaker's name: ")
    userid = input("Enter Email ID: ")
    try:
        logger.info("Enrollment Method ! - Start")

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
        response = voicebiometric_service(enroll_api_url, headers, payload, files)
        logger.info("Response from VoiceBiometric server : {}".format(response))
        logger.info("Enrollment Method ! - End")

    except BaseException as e:
        logger.exception(e)
        logger.info("Exception in main method !")


if __name__ == '__main__':
    start()
