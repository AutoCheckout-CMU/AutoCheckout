### About the Data

Videos are RTSP streams with no transcoding broken down into 10 minute segments.
For the RTSP video name of the file has the IP of the camera followed by the timestamp in UTC
that segment begins. There is an IP to camera ID mapping in the same dir as this file.

`sensor_data` and `depth_frame_data` are stored in a `bson` format. It is strongly recommended
that you use the [decode_file_iter](https://api.mongodb.com/python/3.4.0/api/bson/index.html#bson.decode_file_iter)
method to read the bson files otherwise you might fill up your computer's RAM.

When looking at a single document, the nested field `['document']['header']['t_issue']` is the
timestamp the sample was sent from the source.

The raw data is a base64 encoded byte string. Sensor data can be decoded like:

```
import numpy as np

decoded_bson # your decoded bson obj
array = np.frombuffer(base64.b64decode(decoded_bson['document']['plate_data']['values']['data']), dtype=np.float32)
array = array.reshape(res['document']['plate_data']['values']['shape'])
```

The array should have `NaN`s in the first column/row of every time slice.

The depth data can be decoded a similar way, but will have `uint16` values and requires `zstd` 
decompression after the base64 decoding.

Each of these types of underlying data type and any additional compression can be seen in the
`type` and `encoding` fields respectively. At the same level `shape` will show the overall shape
of the matrix. e.g. for sensors `python_obj['document']['plate_data']['values']['type']` will have
the data type of the byte array and for depth 
`python_obj['document']['frame_message']['frames'][0]['frame']['encoding']` would have the additional
encoding done to the depth frame (which should be `zstd`.

The location of the sensors are based on the camera calibration (in the same dir as this file),
and are hierarchical. Gondolas are relative to the world plane, shelves are relative to their
parent gondola, and plates are relative to their parent shelf. The translation and rotation for
each is represented as a Rodrigues vector.
