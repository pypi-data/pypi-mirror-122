# Python Text-to-speech Client

## Installation

### Ubuntu
- apt-get install python3.6
- apt-get install python3-pip

### Mac OSX
- `brew install python3`
- `brew install python3-pip`
___
### How to run Applicatiton
- update details in `user.config` file.
- `pip3 install requests`
- `pip3 install pytz`
- `Place the certificate in root directiory`

### Step 1: To Enroll your voice with VoiceBiometric server
- `python3 enroll.py` 

### Step 2: To Authenticate your voice with VoiceBiometric server
- `python3 authenticate.py` 

### Step 2: To disenroll your voice with VoiceBiometric server
- `python3 disenroll.py` 

### PyPi Package Link.
- For package link: [Package Link](https://pypi.org/project/gnani-voicebiometric-api/0.0.1/)

### Installation of package. 
- `pip install gnani-voicebiometric-api==0.0.1`

## Note:
- Please make sure you are running the python command from the directory which has certificate file and speaker audio file. 

### Import commands:
- give command `python or python3`

#### To test enroll API
- `from gnani_voicebiometric_api  import enroll`
- `enroll.start()`
- Enter the required inputs.

#### To test authenticate API
- `from gnani_voicebiometric_api  import authenticate`
- `authenticate.start()`
- Enter the required inputs.

#### To test enroll API
- `from gnani_voicebiometric_api  import disenroll`
- `disenroll.start()`
- Enter the required inputs.
  

