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


class udb_file:

    """
    Бинарный файл со следующей структурой:

    1-4 байты - версия файла
    5-16 байты - дата и время создания файла
    17-21 байты - количество каналов

    Уникальные данные каждого канала (начало и конец включительно):
    1-4 байты - кол-во отсчетов
    5-8 байты - номер канала
    9-16 байты - имя канала и сокращенное имя
    17-24 байты - чувствительность канала
    25-32 байты - частота дискретизации
    33-40 байты - размер сжатых с помощью qCompress данных
    41-... байты - сжатые данные сигнала

    Данные о каждом канале расположены последовательно

    """

    def __init__(self, filename):
        with open(filename, mode='rb') as f:
            self.file = bytearray(f.read())
            f.close()

        # в массив channels_pos сохраняются начальные позиции каждого канала
        # начальная позиция канала - место, откуда начинаются его уникальные данные
        # в случае с udb файлом, уникальные данные начинаются с количества отсчетов канала
        self.channels_pos = []
        self.count_channels = struct.unpack(">i", self.file[17:21])[0]
        start_pos = 21  # начальная позиция 0 канала

        # добавление начальных позиций каналов в массив
        for i in range(self.count_channels):
            self.channels_pos.append(start_pos)
            pos_data = start_pos + 32  # начало байтов размера сжатых данных
            size_data = struct.unpack(">i", self.file[pos_data:pos_data + 4])[0]  # размер сжатых данных - 4 байтовое число
            start_pos = pos_data + size_data + 4  # получение нач. позиции следующего канала с учетом размера сжатых данных и размера переменной size_data

    def get_signal_time(self, channel):
        """ Возвращает массив с временем, в которое брались отсчеты """
        number_samples = self.get_number_of_samples(channel)
        sampling_frequency = self.get_sampling_frequency(channel)
        sampling_step = 1 / sampling_frequency
        time = []
        for j in range(0, number_samples):
            time.append(j * sampling_step)
        return np.array(time)

    def get_signal(self, channel):
        channel_pos = self.channels_pos[channel]  # начальная позиция канала

        # получение размера сжатых данных
        # с 32 по 36 байты от начальной позиции расположен рзамер сжатых данных
        channel_data_size = struct.unpack(">i", self.file[channel_pos + 32: channel_pos + 36])[0]
        count_samples = self.get_number_of_samples(channel)

        # сжатые данные расположение с 36 по 36+размер сжатых данных байты от нач. позиции
        data_start, data_stop = channel_pos + 36, channel_pos + channel_data_size + 36

        # распаковка с помощью qUncompress
        channel_data_bytes = bytearray(qUncompress((self.file[data_start:data_stop])))

        # размер в байтах одного числа отсчета
        step = len(channel_data_bytes) // count_samples
        data_array = []

        # цикл, в котором каждые step байт распакованных данных преобразуются в double и добавляются в массив
        for i in range(0, len(channel_data_bytes), step):
            signal_value_bytes = channel_data_bytes[i: i + step]
            signal_value = struct.unpack(">d", signal_value_bytes)[0]
            data_array.append(signal_value)
        return np.array(data_array)

    def get_count_channels(self):
        """ Возвращает число каналов в файле """
        return self.count_channels

    def get_channel_name(self, channel):
        """ Получение имени канала """
        return f"{channel}"

    def get_sampling_frequency(self, channel):
        """ Получение частоты дискретизации указанного канала """
        channel_pos = self.channels_pos[channel]  # начальная позиция для канала channel

        # с 24 по 32 байты от начальной позиции находится частота дискретизации
        dt_pos_start, dt_pos_stop = channel_pos + 24, channel_pos + 32

        # преобразование из байт в double с порядком big-endian
        sampling_frequency = struct.unpack(">d", self.file[dt_pos_start:dt_pos_stop])[0]
        return sampling_frequency

    def get_number_of_samples(self, channel):
        """ Получение числа отсчетов указанного канала """
        channel_pos = self.channels_pos[channel]  # начальная позиция канала
        dt_pos_start, dt_pos_stop = channel_pos, channel_pos + 4  # первые 4 байта от начала - число отсчетов

        # преобразование из байт в int с порядком big-endian
        number_samples = struct.unpack(">i", self.file[dt_pos_start:dt_pos_stop])[0]
        return number_samples
