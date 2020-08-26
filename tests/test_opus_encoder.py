import pytest
import pyogg

# Function to create an encoder and encode a sample of silence
def init_encoder(samples_per_second=48000,
                 application="audio",
                 channels=1,
                 set_sampling_frequency=True,
                 set_application=True,
                 set_channels=True):
    encoder = pyogg.OpusEncoder()
    if set_application:
        encoder.set_application(application)
    if set_sampling_frequency:
        encoder.set_sampling_frequency(samples_per_second)
    if set_channels:
        encoder.set_channels(channels)

    # Create a sample of silence
    bytes_per_sample = 2
    duration_ms = 60
    buf = (
        b"\x00"
        * bytes_per_sample
        * channels
        * (samples_per_second // 1000)
        * duration_ms
    )

    # Encode the sample
    encoder.encode(buf)

    return encoder

# Most of the useful functionality is already well tested thanks to
# OggOpusWriter.

def test_application_voip():
    encoder = init_encoder(application="voip")
    
def test_application_restricted_lowdelay():
    encoder = init_encoder(application="restricted_lowdelay")

# We now focus on testing the error conditions.

def test_invalid_number_of_channels():
    encoder = pyogg.OpusEncoder()
    with pytest.raises(pyogg.PyOggError):
        encoder.set_channels(3)

    
def test_cannot_change_channels():
    encoder = init_encoder()
    # Test that we cannot change the number of channels
    with pytest.raises(pyogg.PyOggError):
        encoder.set_channels(2)

        
def test_invalid_sampling_frequency():
    with pytest.raises(pyogg.PyOggError):
        encoder = init_encoder(44100)
    
        
def test_cannot_change_sampling_frequency():
    encoder = init_encoder()
    # Test that we cannot change the sampling frequency
    with pytest.raises(pyogg.PyOggError):
        encoder.set_sampling_frequency(24000)

        
def test_invalid_application():
    with pytest.raises(pyogg.PyOggError):
        encoder = init_encoder(application="invalid")


def test_cannot_change_application():
    encoder = init_encoder()
    # Test that we cannot change the application
    with pytest.raises(pyogg.PyOggError):
        encoder.set_application("audio")


def test_invalid_frame_size():
    encoder = init_encoder()
    # Test that we cannot change the application
    with pytest.raises(pyogg.PyOggError):
        encoder.encode(b"\x00")

        
def test_application_not_set():
    with pytest.raises(pyogg.PyOggError):
        encoder = init_encoder(set_application=False)
    

def test_sampling_frequency_not_set():
    with pytest.raises(pyogg.PyOggError):
        encoder = init_encoder(set_sampling_frequency=False)


def test_channels_not_set():
    with pytest.raises(pyogg.PyOggError):
        encoder = init_encoder(set_channels=False)
