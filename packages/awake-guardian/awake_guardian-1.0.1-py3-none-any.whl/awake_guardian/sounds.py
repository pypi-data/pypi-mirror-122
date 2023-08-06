from .config import AUDIO_COIN, AUDIO_WILHELM, system

s = system()

if s == "Linux":
    from simpleaudio import WaveObject

    class Sound:
        @classmethod
        def remind(cls):
            cls.sound_remind = WaveObject.from_wave_file(AUDIO_COIN)
            cls.sound_remind.play()

        @classmethod
        def nag(cls):
            cls.sound_nag = WaveObject.from_wave_file(AUDIO_WILHELM)
            cls.sound_nag.play()


elif s == "Windows":
    from playsound import playsound

    class Sound:
        @classmethod
        def remind(cls):
            playsound(AUDIO_COIN)

        @classmethod
        def nag(cls):
            playsound(AUDIO_WILHELM)
