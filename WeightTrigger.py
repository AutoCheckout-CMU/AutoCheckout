import numpy as np
import base64
from cpsdriver.codec import DocObjectCodec
# import matplotlib.pyplot as plt
# import matplotlib.dates as md
import datetime as dt

class WeightTrigger:

    def __init__(self, db):
        self.db = db
        self.plate_data = db['plate_data']
    
    # aggregate weight per shelf
    # compute moving mean and variance

    def init_1D_array(self, dim):
        array = np.array( [None for i in range(dim) ],
                        dtype=object)
        for i in range(dim):
            array[i] = []
        return array

    # [gondola, shelf, ts]
    def init_2D_array(self, dim1, dim2):
        array = np.array( [ [None for j in range(dim2)] for i in range(dim1) ],
                        dtype=object)
        for i in range(dim1):
            for j in range(dim2):
                array[i][j] = []
        return array

    # [gondola, shelf, plate_id, ts]
    def init_3D_array(self, dim1, dim2, dim3):
        array = np.array( [ [ [None for k in range(dim3)] for j in range(dim2)] for i in range(dim1) ],
                        dtype=object)
        for i in range(dim1):
            for j in range(dim2):
                for k in range(dim3):
                    array[i][j][k] = []
        return array

    def get_weights(self, number_gondolas=5, number_shelves=6, number_plates=12,window_moving_avg=1):
        weight_plate_mean = self.init_3D_array(number_gondolas, number_shelves, number_plates)
        weight_plate_std = self.init_3D_array(number_gondolas, number_shelves, number_plates)
        weight_shelf_mean = self.init_2D_array(number_gondolas, number_shelves)
        weight_shelf_std = self.init_2D_array(number_gondolas, number_shelves)
        timestamps = self.init_1D_array(number_gondolas)
        date_times = self.init_1D_array(number_gondolas)
        plate_data = self.db['plate_data']
        
        for item in plate_data.find():
            gondola_id = item['gondola_id']
            plate_data_item = DocObjectCodec.decode(doc=item, collection='plate_data')
            date_time = item['date_time']
            timestamp = plate_data_item.timestamp # seconds since epoch
            np_plate = plate_data_item.data # [time,shelf,plate]
            np_plate = np_plate[:,1:13,1:13] # remove NaN elements
            
            # sum plates per shelf
            np_shelf = np_plate.sum(axis=2)      # [time,shelf]
            np_shelf = np_shelf.transpose()      # [shelf, time]
            np_plate = np_plate.transpose(1,2,0) # [shelf,plate,time]
            
            # get mean/std for weights per 12 data points (0.2 seconds)
            mean_plate = np.mean(np_plate, axis=2) # [shelf, plate]
            std_plate = np.std(np_plate, axis=2)   # [shelf, plate]
            mean_shelf = np.mean(np_shelf, axis=1) # [shelf]
            std_shelf = np.std(np_shelf, axis=1)   # [shelf]
            
            timestamps[gondola_id - 1].append(timestamp)
            date_times[gondola_id - 1].append(date_time)
            number_shelves = len(mean_shelf)
            for shelf_index in range(number_shelves):
                weight_shelf_mean[gondola_id - 1][shelf_index].append(mean_shelf[shelf_index])
                weight_shelf_std[gondola_id - 1][shelf_index].append(std_shelf[shelf_index])
                for plate_index in range(number_plates):
                    weight_plate_mean[gondola_id - 1][shelf_index][plate_index].append(mean_plate[shelf_index][plate_index])
                    weight_plate_std[gondola_id - 1][shelf_index][plate_index].append(std_plate[shelf_index][plate_index])
                    
        return weight_plate_mean,weight_plate_std,weight_shelf_mean,weight_shelf_std,timestamps,date_times
    

    def detect_weight_events(self, 
                         weight_shelf_mean, 
                         weight_shelf_std, 
                         weight_plate_mean, 
                         weight_plate_std, 
                         date_times, 
                         number_plates=12, 
                         thresholds={'std_shelf': 40, 'mean_shelf': 10}):
        events = []
        num_gondola, num_shelf = weight_shelf_mean.shape
        num_times = len(date_times[0])
        for gondola_id in range(num_gondola):
            for shelf_id in range(num_shelf):
                var_is_active = np.array(weight_shelf_std[gondola_id][shelf_id]) > thresholds.get('std_shelf', 40)
                state_changes = np.diff(var_is_active)
                state_change_inds = [i for i, v in enumerate(state_changes) if v > 0]
                state_lengths = np.diff([0] + state_change_inds + [len(var_is_active) - 1])
                active_inds = [i for i in range(1, len(state_lengths), 2)]
                stable_inds = [i for i in range(2, len(state_lengths), 2)]
                valid_active_intervals = [i for i, ind in enumerate(active_inds) if state_lengths[ind] > thresholds.get('N_high', 1)]
                valid_stable_intervals = [i for i, ind in enumerate(stable_inds) if state_lengths[ind] > thresholds.get('N_low', 5)]
                min_next_active_interval = 0
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
                    
                    n_begin = state_change_inds[active_inds[active_idx] - 1] - thresholds.get('N_low', 5)
                    n_end = state_change_inds[stable_inds[stable_idx] - 1] + 1 + thresholds.get('N_low', 5)
                    w_begin = weight_shelf_mean[gondola_id][shelf_id][n_begin]
                    w_end = weight_shelf_mean[gondola_id][shelf_id][n_end]
                    delta_w = w_end - w_begin
                    
                    if abs(delta_w) > thresholds.get('mean_shelf', 10):
                        trigger_begin = date_times[gondola_id][n_begin]
                        trigger_end = date_times[gondola_id][n_end]
                        
                        plates = [0] * number_plates
                        for plate_id in range(number_plates):
                            
                            plates[plate_id] = int(abs(weight_plate_mean[gondola_id][shelf_id][plate_id][n_end] 
                                                    - weight_plate_mean[gondola_id][shelf_id][plate_id][n_begin]) 
                                                > thresholds.get('mean_plate', 5))
                        
                        
                        event = {'trigger_begin': trigger_begin,
                                'trigger_end': trigger_end,
                                'n_begin': n_begin,
                                'n_end': n_end,
                                'delta_weight': delta_w,
                                'gondola': gondola_id + 1,
                                'shelf': shelf_id + 1,
                                'plates': plates, 
                                }
                        events.append(event)
                    min_next_active_interval = stable_idx
        return events 