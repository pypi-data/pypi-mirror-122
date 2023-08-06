from sdsRayanArvin.Dataset import DeviceData


class LastData:
    LastDataDevice = {}

    def setLastData(self, LastDataDevice):
        index = str(LastDataDevice['topic']) + str(LastDataDevice['type']) + str(LastDataDevice['pan']) + str(LastDataDevice['add'])
        print(index)
        LastDataDevice['ID_device_data'] = 0
        LastDataDevice['data'] = str(LastDataDevice['data'])
        LastData.LastDataDevice[index] = DeviceData(LastDataDevice)
        self.getLastData(index)

    def getLastData(self, index):
        print(LastData.LastDataDevice)
        return LastData.LastDataDevice[index]
