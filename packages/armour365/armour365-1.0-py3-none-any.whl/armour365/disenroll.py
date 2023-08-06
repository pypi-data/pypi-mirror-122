from configparser import ConfigParser
from armour365.log_config.logger import get_logger
from armour365.utils import voicebiometric_service

import os

current_dir = os.getcwd()

logger = get_logger(__name__)

# Reading from config file
parser = ConfigParser()
parser.read('user.config')

disenroll_api_url = "https://armour365.gnani.ai/api/delete_enrollment"


def start():
    """ Set all below parameters in the config file. """
    token = input("Enter Token: ")
    accesskey = input("Enter AccessKey: ")
    userid = input("Enter Email ID: ")
    speaker = input("Enter Speaker's name: ")
    try:
        logger.info("DisEnrollment Method ! - Start")

        # construct request headers
        headers = {
            "product": "voice-biometric",
            "token": token,
            "accesskey": accesskey,
            "userid": userid
        }

        # construct request payload
        payload = {'speaker': speaker}
        """
            Request Gnani VoiceBiometric Service to enroll your voice
        """
        response = voicebiometric_service(disenroll_api_url, headers, payload)
        logger.info("Response from VoiceBiometric server : {}".format(response))
        logger.info("DisEnrollment Method ! - End")
    except BaseException as e:
        logger.exception(e)
        logger.info("Exception in main method !")


if __name__ == '__main__':
    start()
