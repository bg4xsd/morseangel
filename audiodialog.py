from PyQt5 import QtCore, QtWidgets, QtMultimedia

class AudioDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(AudioDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Audio Devices")
        self.device_index = -1
        self.device_rate_index = -1
        self.device_rates = []

        self.deviceCombo = QtWidgets.QComboBox(self)
        self.deviceCombo.currentIndexChanged.connect(self.device_selected)

        self.sampleRateCombo = QtWidgets.QComboBox(self)
        self.sampleRateCombo.currentIndexChanged.connect(self.rate_selected)

        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.deviceCombo)
        self.layout.addWidget(self.sampleRateCombo)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def set_audio_devices(self, audio_devices):
        self.audio_devices = audio_devices
        device_names = [device.deviceName() for device in audio_devices]
        self.deviceCombo.blockSignals(True)
        self.deviceCombo.addItems(device_names)
        self.deviceCombo.blockSignals(False)
        default_device = QtMultimedia.QAudioDeviceInfo.defaultInputDevice()
        # Modified to running on windows 11
        # self.default_device_index = audio_devices.index(default_device)
        # self.deviceCombo.setCurrentIndex(self.default_device_index)
        import platform
        plat = platform.system().lower()
        if plat == 'windows': # choose first device as default for windows
            self.default_device_index = 0
        else : # OK for linux
            self.default_device_index = audio_devices.index(default_device)

        self.deviceCombo.setCurrentIndex(self.default_device_index)
        # It seems lost default sample rate
        # add the sample rate for default device
        self.device_rates = self.audio_devices[self.device_index].supportedSampleRates()
        self.sampleRateCombo.blockSignals(True)
        self.sampleRateCombo.clear()
        self.sampleRateCombo.addItems([str(x) for x in self.device_rates])
        self.sampleRateCombo.blockSignals(False)
        self.sampleRateCombo.setCurrentIndex(0) # choose Min

    def device_selected(self):
        self.device_index = self.deviceCombo.currentIndex()
        self.device_rates = self.audio_devices[self.device_index].supportedSampleRates()
        self.sampleRateCombo.blockSignals(True)
        self.sampleRateCombo.clear()
        self.sampleRateCombo.addItems([str(x) for x in self.device_rates])
        self.sampleRateCombo.blockSignals(False)
        self.sampleRateCombo.setCurrentIndex(len(self.device_rates)-1)

    def rate_selected(self):
        self.device_rate_index = self.sampleRateCombo.currentIndex()


