from service.tca_service import TCAService


def run(seed, maps, rates, schedule = {}):

    # Make different simulations
    for map in maps:
        for rate in rates:

            print('Evaluating map {} - rate {}'.format(map, rate))

            # Object
            service = TCAService(map, rate)

            # Set schedule
            # service.set_traffic_lights(schedule)

            # Start running fixed time
            # service.fixed_time_start(1000, True)
            service.random_dynamic_time_start(1000, 10, 0.5, True)
            # service.random_fixed_time_start(1000, True)


if __name__ == '__main__':

    seeds = [4731, 3891, 3678, 5671, 9188, 7495, 4431, 5587, 9433, 6743, 8504, 3548, 5536, 8525, 2344, 5288, 8816, 4170, 6943, 8449, 4229, 7639, 4669, 2326, 4560, 8893, 1458, 3437, 1990, 6973, 6782, 1510, 8566, 6415, 2364, 1670, 5904, 6755, 9784, 6561, 3138, 3432, 2471, 7124, 6289, 6825, 2416, 5420, 8788, 9089, 9845, 5625, 2006, 4522, 9268, 9292, 8350, 8889, 7884, 1058, 7622, 9279, 8345, 3534, 8899, 6803, 1483, 9376, 1943, 1998, 8143, 4774, 3033, 3335, 4652, 9199, 1264, 5430, 4638, 5422, 2991, 6541, 1477, 1191, 8172, 3684, 8849, 9564, 8538, 9841, 4448, 7285, 1109, 4432, 5614, 2650, 8444, 2543, 1275, 9478, 4237, 4536, 9831, 9086, 1163, 2450, 4236, 1438, 1913, 6870, 9208, 8604, 8130, 2267, 6908, 9513, 3110, 8764, 3954, 3202, 8359, 8080, 9897, 2964, 6068, 5448, 6516, 7083, 6792, 1159, 3810, 9909, 3944, 3627, 9844, 6049, 8260, 3091, 7285, 9396, 2488, 2601, 8373, 5421, 4312, 6882, 5587, 4439, 1821, 8122, 8179, 1593, 8948, 8189, 7012, 2873, 5585, 5912, 1078, 1312, 7394, 2728, 2064, 9878, 1908, 6314, 3782, 4766, 8716, 9045, 3386, 7584, 6439, 3794, 5563, 2720, 3591, 3019, 6738, 5813, 7755, 2558, 1032, 6934, 6164, 9949, 8651, 4264, 2953, 1602, 3968, 6651, 6669, 8193, 1314, 3135, 5380, 1360, 3193, 4523, 3133, 7949, 9611, 1086, 5039, 4915, 1473, 9997, 5253, 4548, 1740, 7896, 3421, 4659, 3794, 2761, 8834, 9408, 9803, 6883, 8255, 6166, 2647, 4266, 4703, 7335, 7502, 3177, 2285, 8003, 8266, 7519, 6781, 4685, 5023, 5877, 5027, 6945, 4149, 9227, 8534, 6062, 8824, 1913, 1879, 1002, 7658, 5080, 6411, 1888, 8390, 4871, 7494, 5602, 7602, 5728, 7107, 5861, 6239, 1271, 7398, 3985, 2456, 2091, 8711, 3730, 3410, 8926, 9075, 7302, 8850, 6863, 2564, 7564, 6668, 1356, 6752, 3524, 4473, 4753, 6238, 6675, 3245, 3622, 7061, 3184, 1738, 1563, 8721, 2960, 9280, 7993, 1742, 4478, 2956, 3692, 2672, 6892, 9175, 7167]

    maps = [1, 2, 3]

    rates = [0.2, 0.4, 0.6, 0.8, 1]

    schedule_1 = [{'id': 0, 'schedule': {0: 0, 2: 1, 3: 0, 6: 1, 7: 0, 11: 1, 12: 0}}, {'id': 1, 'schedule': {0: 2, 2: 3, 3: 2, 6: 3, 7: 2, 11: 3, 12: 2}}, {'id': 2, 'schedule': {0: 4, 2: 5, 3: 4, 6: 5, 7: 4, 11: 5, 12: 4}}, {'id': 3, 'schedule': {0: 6, 2: 7, 3: 6, 6: 7, 7: 6, 11: 7, 12: 6}}]

    schedule_2 = [{'schedule': {0: 1, 4: 0, 7: 1, 8: 0, 9: 1, 14: 0},  'id': 0}, {'schedule': {0: 3, 4: 2, 7: 3, 8: 2, 9: 3, 14: 2}, 'id': 1}, {'schedule': {0: 5, 4: 4, 7: 5, 8: 4, 9: 5, 14: 4}, 'id': 2}, {'schedule': {0: 7, 4: 6, 7: 7, 8: 6, 9: 7, 14: 6}, 'id': 3}, {'schedule': {0: 9, 4: 8, 7: 9, 8: 8, 9: 9, 14: 8}, 'id': 4}, {'schedule': {0: 11, 4: 10, 7: 11, 8: 10, 9: 11, 14: 10}, 'id': 5}, {'schedule': {0: 13, 4: 12, 7: 13, 8: 12, 9: 13, 14: 12}, 'id': 6}, {'schedule': {0: 15, 4: 14, 7: 15, 8: 14, 9: 15, 14: 14}, 'id': 7}]

    schedule_3 = [{'id': 0, 'schedule': {0: 1, 1: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1, 11: 0}}, {'id': 1, 'schedule': {0: 3, 1: 2, 4: 3, 5: 2, 6: 3, 7: 2, 8: 3, 11: 2}}, {'id': 2, 'schedule': {0: 5, 1: 4, 4: 5, 5: 4, 6: 5, 7: 4, 8: 5, 11: 4}}, {'id': 3, 'schedule': {0: 7, 1: 6, 4: 7, 5: 6, 6: 7, 7: 6, 8: 7, 11: 6}}, {'id': 4, 'schedule': {0: 9, 1: 8, 4: 9, 5: 8, 6: 9, 7: 8, 8: 9, 11: 8}}, {'id': 5, 'schedule': {0: 11, 1: 10, 4: 11, 5: 10, 6: 11, 7: 10, 8: 11, 11: 10}}, {'id': 6, 'schedule': {0: 13, 1: 12, 4: 13, 5: 12, 6: 13, 7: 12, 8: 13, 11: 12}}, {'id': 7, 'schedule': {0: 15, 1: 14, 4: 15, 5: 14, 6: 15, 7: 14, 8: 15, 11: 14}}, {'id': 8, 'schedule': {0: 17, 1: 16, 4: 17, 5: 16, 6: 17, 7: 16, 8: 17, 11: 16}}, {'id': 9, 'schedule': {0: 19, 1: 18, 4: 19, 5: 18, 6: 19, 7: 18, 8: 19, 11: 18}}, {'id': 10, 'schedule': {0: 21, 1: 20, 4: 21, 5: 20, 6: 21, 7: 20, 8: 21, 11: 20}}, {'id': 11, 'schedule': {0: 23, 1: 22, 4: 23, 5: 22, 6: 23, 7: 22, 8: 23, 11: 22}}, {'id': 12, 'schedule': {0: 25, 1: 24, 4: 25, 5: 24, 6: 25, 7: 24, 8: 25, 11: 24}}, {'id': 13, 'schedule': {0: 27, 1: 26, 4: 27, 5: 26, 6: 27, 7: 26, 8: 27, 11: 26}}, {'id': 14, 'schedule': {0: 29, 1: 28, 4: 29, 5: 28, 6: 29, 7: 28, 8: 29, 11: 28}}, {'id': 15, 'schedule': {0: 31, 1: 30, 4: 31, 5: 30, 6: 31, 7: 30, 8: 31, 11: 30}}]

    run(seeds, maps, rates)
