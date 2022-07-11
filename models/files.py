import struct
import numpy as np
from PyQt5.QtCore import qUncompress, QByteArray, QSettings


class dd_file:
    def __init__(self, filename):
        self.file = QSettings(filename, QSettings.IniFormat)
        self.sampling_frequency = float(self.file.value("Head/sampling_frequency"))
        self.number_of_samples = int(self.file.value("Head/number_of_samples"))

    def get_signal_time(self, channel):
        time = []
        for i in range(self.number_of_samples):
            time.append(i / self.sampling_frequency)
        return np.array(time)

    def get_signal(self, number_channel):
        channels = {
            1: "signalRight",
            2: "signalLeft"
        }
        signal_values = np.array(self.file.value(f"Data/{channels[number_channel]}"))
        return signal_values

    def get_count_channels(self):
        return 2

    def get_channel_name(self, channel):
        channels = {
            1: "signalRight",
            2: "signalLeft"
        }
        name_channel = channels[channel]
        return name_channel

    def get_sampling_frequency(self, channel):
        return self.sampling_frequency

    def get_number_of_samples(self, channel):
        return self.number_of_samples


class d2_file(dd_file):
    def __init__(self, filename):
        self.file = QSettings(filename, QSettings.IniFormat)
        count_samples_bytes = bytearray(qUncompress(QByteArray(self.file.value("Data/signalTime"))))[0:4]
        count_samples_bytes.reverse()
        self.number_of_samples = struct.unpack('i', count_samples_bytes)[0]
        self.sampling_frequency = int(self.file.value('Head/samplingFrequency'))

    def get_signal_time(self, channel):
        signal_time_bytes = bytearray(qUncompress(QByteArray(self.file.value("Data/signalTime"))))[4:]
        time_data_array = []
        for i in range(0, len(signal_time_bytes),
                       len(signal_time_bytes) // self.number_of_samples):
            signal_time_value_bytes = signal_time_bytes[i: i + len(signal_time_bytes) // self.number_of_samples]
            signal_time_value_bytes.reverse()
            signal_time_value = struct.unpack("d", signal_time_value_bytes)[0]
            time_data_array.append(signal_time_value)
        return np.array(time_data_array)

    def get_signal(self, number_channel):
        channels = {
            1: "signalRight",
            2: "signalLeft"
        }
        signal_bytes = bytearray(qUncompress(QByteArray(self.file.value(f"Data/{channels[number_channel]}"))))[4:]
        signal_data = []
        for i in range(0, len(signal_bytes),
                       len(signal_bytes) // self.number_of_samples):
            signal_right_value_bytes = signal_bytes[i: i + len(signal_bytes) // self.number_of_samples]
            signal_right_value_bytes.reverse()
            signal_value = struct.unpack("d", signal_right_value_bytes)[0]
            signal_data.append(signal_value)
        return np.array(signal_data)


class d3_file:
    def __init__(self, filename):
        self.file = QSettings(filename, QSettings.IniFormat)
        self.version_file0 = 1 if self.file.value(f"Head/point/1/name") is not None else 0
        self.version_file1 = 1 if self.file.value(f"Head/channel_0_point_name") is not None else 0


    def get_signal_time(self, channel):
        count_samples = self.get_number_of_samples(channel)
        sampling_rate = self.get_sampling_frequency(channel)

        if (count_samples == 0) or (sampling_rate == 0):
            return np.array([0])

        time = []
        for j in range(0, count_samples):
            time.append(j / sampling_rate)
        return np.array(time)

    def get_signal(self, channel):
        count_samples = self.get_number_of_samples(channel)

        if count_samples == 0:
            return np.array([0])

        try:
            signal_bytes = bytearray(qUncompress(QByteArray((self.file.value(f"Data/signal/{channel}/signal_data")))))
        except TypeError:
            signal_bytes = bytearray(qUncompress(QByteArray((self.file.value(f"Data/signal_channel_{channel}")))))
        signal_data = []
        for i in range(0, len(signal_bytes), len(signal_bytes) // count_samples):
            signal_value_bytes = signal_bytes[i: i + len(signal_bytes) // count_samples]
            signal_value_bytes.reverse()
            signal_value = struct.unpack("d", signal_value_bytes)[0]
            signal_data.append(signal_value)
        return np.array(signal_data)

    def get_count_channels(self):
        try:
            count_channels = int(self.file.value(f"Head/point/size"))
        except TypeError:
            count_channels = int(self.file.value(f"Head/points_count"))
        return count_channels

    def get_channel_name(self, channel):
        if self.version_file1:
            name_channel = self.file.value(f"Head/channel_{channel}_point_name")
        if self.version_file0:
            name_channel = self.file.value(f"Head/point/{channel}/name")
        return name_channel

    def get_number_of_samples(self, channel):
        try:
            count_samples = int(self.file.value(f"Head/point/{channel}/samples_count"))
        except TypeError:
            count_samples = int(self.file.value(f"Head/channel_{channel}_samples_count"))
        return count_samples

    def get_sampling_frequency(self, channel):
        try:
            sampling_rate = int(self.file.value(f"Head/point/{channel}/sampling_rate"))
        except TypeError:
            sampling_rate = int(self.file.value(f"Head/channel_{channel}_sampling_rate"))
        return sampling_rate


class udd_file:
    def __init__(self, filename):
        self.file = QSettings(filename, QSettings.IniFormat)

    def get_signal_time(self, channel):
        sampling_rate = int(self.file.value(f"Points/{channel}/sampling_rate"))
        count_samples = int(self.file.value(f"Points/{channel}/count"))
        time = []
        for j in range(0, count_samples):
            time.append(j / sampling_rate)
        return np.array(time)

    def get_signal(self, channel):
        count_samples = int(self.file.value(f"Points/{channel}/count"))
        signal_bytes = bytearray(qUncompress(QByteArray((self.file.value(f"Points/{channel}/data")))))
        signal_data = []
        for i in range(0, len(signal_bytes), len(signal_bytes) // count_samples):
            signal_value_bytes = signal_bytes[i: i + len(signal_bytes) // count_samples]
            signal_value_bytes.reverse()
            signal_value = struct.unpack("d", signal_value_bytes)[0]
            signal_data.append(signal_value)
        return np.array(signal_data)

    def get_count_channels(self):
        count_channels = int(self.file.value("Points/size"))
        return count_channels

    def get_channel_name(self, channel):
        channel_name = self.file.value(f"Points/{channel}/name")
        return channel_name

    def get_sampling_frequency(self, channel):
        sampling_rate = int(self.file.value(f"Points/{channel}/sampling_rate"))
        return sampling_rate

    def get_number_of_samples(self, channel):
        count_samples = int(self.file.value(f"Points/{channel}/count"))
        return count_samples
