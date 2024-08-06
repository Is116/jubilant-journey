from pyfingerprint.pyfingerprint import PyFingerprint

def get_fingerprint():
    try:
        # Initialize the fingerprint sensor
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')

        print('Fingerprint sensor initialized successfully.')

        print('Waiting for finger...')

        # Wait for the user to place their finger
        while not f.readImage():
            pass

        print('Finger detected.')

        # Convert the image to characteristics and store in charbuffer 1
        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]

        if positionNumber >= 0:
            raise Exception('Template already exists at position #' + str(positionNumber))

        print('Creating template...')
        # Create a template
        f.createTemplate()
        characteristics = f.downloadCharacteristics(0x01)
        print('Fingerprint characteristics:', characteristics)
        return characteristics

    except Exception as e:
        print('Operation failed!')
        print('Exception message:', str(e))
        return None
