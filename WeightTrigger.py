import numpy as np
from cpsdriver.codec import DocObjectCodec
from datetime import datetime

class PickUpEvent():
    triggerBegin: datetime
    triggerEnd: datetime
    nBegin: int
    nEnd: int
    deltaWeight: np.float
    gondolaID: int
    shelfID: int
    plateIDs: list
    def __init__(self, triggerBegin, triggerEnd, nBegin, nEnd, deltaWeight, gondolaID, shelfID, plateIDs):
        self.triggerBegin = triggerBegin
        self.triggerEnd = triggerEnd
        self.nBegin = nBegin
        self.nEnd = nEnd
        self.deltaWeight = deltaWeight
        self.gondolaID = gondolaID
        self.shelfID = shelfID
        self.plateIDs = plateIDs

    def __str__(self):
        return "deltaWeight: {}, position: {}, {}, {}".format(self.deltaWeight, self.gondolaID, self.shelfID, self.plateIDs)

class WeightTrigger:

    # full event trigger: to get all event triggers from the current database
    # results: a list of events including their information of:
    # event start and end time,
    # event start and end index,
    # weight changes in gram,
    # gondola where event happens,
    # shelf where event happens,
    # a list plates where event happens.


    def __init__(self, BK):
        self.db = BK.db
        self.plate_data = BK.plateDB
        self.agg_plate_data, self.agg_shelf_data, self.timestamps = self.get_agg_weight()


    def init_1D_array(self, dim):
        array = np.array([None for i in range(dim)],
                         dtype=object)
        for i in range(dim):
            array[i] = []
        return array

    # [gondola, shelf, ts]
    def init_2D_array(self, dim1, dim2):
        array = np.array([[None for j in range(dim2)] for i in range(dim1)],
                         dtype=object)
        for i in range(dim1):
            for j in range(dim2):
                array[i][j] = []
        return array

    # [gondola, shelf, plate_id, ts]
    def init_3D_array(self, dim1, dim2, dim3):
        array = np.array([[[None for k in range(dim3)] for j in range(dim2)] for i in range(dim1)],
                         dtype=object)
        for i in range(dim1):
            for j in range(dim2):
                for k in range(dim3):
                    array[i][j][k] = []
        return array

    # sliding window detect events
    # concentacate the data set , and use sliding window (60 data points per window)
    # moving average weight, can remove noise and reduce the false trigger caused by shake or unstable during an event

    def get_agg_weight(self, number_gondolas=5):
        plate_data = self.db['plate_data']
        agg_plate_data = [None] * number_gondolas
        agg_shelf_data = [None] * number_gondolas
        timestamps = self.init_1D_array(number_gondolas)
        date_times = self.init_1D_array(number_gondolas)

        for item in plate_data.find():
            gondola_id = item['gondola_id']
            plate_data_item = DocObjectCodec.decode(doc=item, collection='plate_data')
            
            timestamp = plate_data_item.timestamp  # seconds since epoch
        
            np_plate = plate_data_item.data  # [time,shelf,plate]
            np_plate = np.nan_to_num(np_plate, copy=True, nan=0) # replace all NaN elements to 0
            np_plate = np_plate[:, 1:13, 1:13]  # remove first line, which is always NaN elements
            np_shelf = np_plate.sum(axis=2)  # [time,shelf]
            np_shelf = np_shelf.transpose()  # [shelf, time]
            np_plate = np_plate.transpose(1, 2, 0)  # [shelf,plate,time]
            if agg_plate_data[gondola_id - 1] is not None:
                agg_plate_data[gondola_id - 1] = np.append(agg_plate_data[gondola_id - 1], np_plate, axis=2)
                agg_shelf_data[gondola_id - 1] = np.append(agg_shelf_data[gondola_id - 1], np_shelf, axis=1)
            else:
                agg_plate_data[gondola_id - 1] = np_plate
                agg_shelf_data[gondola_id - 1] = np_shelf

            timestamps[gondola_id - 1].append(timestamp)

        return agg_plate_data, agg_shelf_data, timestamps

    def rolling_window(self, a, window):
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

    def get_agg_timestamps(self, number_gondolas=5):
        agg_timestamps = self.init_1D_array(number_gondolas)
        for gondola_id in range(number_gondolas):
            for i, date_time in enumerate(self.timestamps[gondola_id]):
                if i < len(self.timestamps[gondola_id]) - 1:
                    next_date_time = self.timestamps[gondola_id][i + 1]
                    time_delta = (next_date_time - date_time) / 12
                    agg_timestamps[gondola_id] += [date_time + time_delta * j for j in range(0, 12)]
                else:
                    time_delta = 1/60
                    agg_timestamps[gondola_id] += [date_time + time_delta * j for j in range(0, 12)]
        return agg_timestamps

    def get_moving_weight(self, num_gondola=5, window_size=60):
        moving_weight_plate_mean = []
        moving_weight_plate_std = []
        moving_weight_shelf_mean = []
        moving_weight_shelf_std = []
        for gondola_id in range(num_gondola):
            if (self.agg_shelf_data[gondola_id] is None):
                continue
            moving_weight_shelf_mean.append(np.mean(self.rolling_window(self.agg_shelf_data[gondola_id], window_size), -1))
            moving_weight_shelf_std.append(np.std(self.rolling_window(self.agg_shelf_data[gondola_id], window_size), -1))
            moving_weight_plate_mean.append(np.mean(self.rolling_window(self.agg_plate_data[gondola_id], window_size), -1))
            moving_weight_plate_std.append(np.std(self.rolling_window(self.agg_plate_data[gondola_id], window_size), -1))
        return moving_weight_shelf_mean, moving_weight_shelf_std, moving_weight_plate_mean, moving_weight_plate_std


    # detect events from weight trigger

    # return a list of events in the whole database, including the details of the events:
    # trigger_begin, trigger_end, n_begin, n_end, delta_weight, gondola, shelf, plates

    # active state: use variance, i.e. when variance is larger than the given threshold
    # valid active interval: based on how long the active state is, i.e. n(>threshold which is 1) continuous active time spots
    # event trigger based on valid active interval: find start index and end index (currently use 2 time spots for both thresholds)
    # of the n continuous active time spots, then find delta mean weight.
    # Trigger an event if the difference is large than a threshold

    def detect_weight_events(self,
                             weight_shelf_mean,
                             weight_shelf_std, # TODO: matlab used var
                             weight_plate_mean,
                             weight_plate_std,
                             timestamps,
                             num_plate=12,
                             thresholds={'std_shelf': 22, 'mean_shelf': 10, 'mean_plate': 5, 'N_high': 30, 'N_low': 30}):
        # the lightest product is: {'_id': ObjectId('5e30c1c0e3a947a97b665757'), 'product_id': {'barcode_type': 'UPC', 'id': '041420027161'}, 'metadata': {'name': 'TROLLI SBC ALL STAR MIX', 'thumbnail': 'https://cdn.shopify.com/s/files/1/0083/0704/8545/products/41420027161_cce873d6-f143-408c-864e-eb351a730114.jpg?v=1565210393', 'price': 1, 'weight': 24}}

        events = []
        num_gondola = len(weight_shelf_mean)
        num_times = len(timestamps[0])
        for gondola_idx in range(num_gondola):
            num_shelf = weight_shelf_mean[gondola_idx].shape[0]
            for shelf_idx in range(num_shelf):
                var_is_active = np.array(weight_shelf_std[gondola_idx][shelf_idx]) > thresholds.get('std_shelf')

                state_changes = np.diff(var_is_active)
                state_change_inds = [i for i, v in enumerate(state_changes) if v > 0]
                state_lengths = np.diff([0] + state_change_inds + [len(var_is_active) - 1])
                active_inds = [i for i in range(1, len(state_lengths), 2)]
                stable_inds = [i for i in range(2, len(state_lengths), 2)]
                valid_active_intervals = [i for i, ind in enumerate(active_inds) if
                                          state_lengths[ind] > thresholds.get('N_high')]
                valid_stable_intervals = [i for i, ind in enumerate(stable_inds) if
                                          state_lengths[ind] > thresholds.get('N_low')]

                min_next_active_interval = -1
                for active_idx in valid_active_intervals:
                    if active_idx <= min_next_active_interval:
                        continue

                    stable_idx = -1
                    for i in valid_stable_intervals:
                        if i >= active_idx:
                            stable_idx = i
                            break
                    if stable_idx == -1:
                        break

                    n_begin = state_change_inds[active_inds[active_idx] - 1] - thresholds.get('N_low')
                    n_end = state_change_inds[stable_inds[stable_idx] - 1] + 1 + thresholds.get('N_low')
                    w_begin = weight_shelf_mean[gondola_idx][shelf_idx][n_begin]
                    w_end = weight_shelf_mean[gondola_idx][shelf_idx][n_end]
                    delta_w = w_end - w_begin

                    if abs(delta_w) > thresholds.get('mean_shelf'):
                        trigger_begin = timestamps[gondola_idx][n_begin]
                        trigger_end = timestamps[gondola_idx][n_end]

                        plates = [0] * num_plate
                        for plate_id in range(num_plate):
                            # plates[plate_id] = int(abs(weight_plate_mean[gondola_idx][shelf_idx][plate_id][n_end]
                            #                            - weight_plate_mean[gondola_idx][shelf_idx][plate_id][n_begin])
                            #                        > thresholds.get('mean_plate'))
                            plates[plate_id] = weight_plate_mean[gondola_idx][shelf_idx][plate_id][n_end] \
                                               - weight_plate_mean[gondola_idx][shelf_idx][plate_id][n_begin]

                        event = PickUpEvent(
                            trigger_begin, 
                            trigger_end,
                            n_begin,
                            n_end,
                            delta_w,
                            gondola_idx+1,
                            shelf_idx+1,
                            plates
                        )

                        events.append(event)
                    min_next_active_interval = stable_idx
        return events