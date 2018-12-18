import re
from datetime import datetime
import operator

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        entries = f.read().strip().split('\n')

    entries = map(lambda s: re.findall(r'(\d+|wakes|asleep)', s), entries)
    entry_list = []
    for (yr, mo, day, hr, min, state) in entries:
        entry_dict = {'date': datetime.strptime(yr+mo+day+hr+min, '%Y%m%d%H%M')}
        if re.match(r'\d+', state):
            entry_dict['id'] = state
            entry_dict['state'] = 'start'
        else:
            entry_dict['state'] = state
        entry_list.append(entry_dict)

    entry_list.sort(key=operator.itemgetter('date'))
    guard_times = {}
    who_is_sleeping = {}
    on_duty = -1
    time_asleep = None
    for entry in entry_list:
        if 'id' in entry:
            on_duty = entry['id']
            if entry['id'] not in guard_times:
                guard_times[on_duty] = {}
                guard_times[on_duty]['total'] = 0
                guard_times[on_duty]['times'] = {}
        elif entry['state'] == 'asleep':
            time_asleep = entry['date']
        elif entry['state'] == 'wakes':
            old_time = guard_times[on_duty]['total']
            minutes_asleep = ((entry['date'] - time_asleep).seconds % 3600) // 60
            guard_times[on_duty]['total'] += minutes_asleep
            for min in range(minutes_asleep):
                which_minute = (time_asleep.minute + min) % 60
                if which_minute not in guard_times[on_duty]['times']:
                    guard_times[on_duty]['times'][which_minute] = 1
                else:
                    guard_times[on_duty]['times'][which_minute] += 1

                if which_minute not in who_is_sleeping:
                    who_is_sleeping[which_minute] = {}
                if on_duty not in who_is_sleeping[which_minute]:
                    who_is_sleeping[which_minute][on_duty] = 1
                else:
                    who_is_sleeping[which_minute][on_duty] += 1
            time_asleep = None

    # TODO: VALUABLE
    max_guard = max(guard_times, key=lambda key: guard_times[key]['total'])
    times = guard_times[max_guard]['times']

    # TODO: VALUABLE
    min_most_asleep = max(times, key=times.get)

    print('a:', max_guard, 'x', min_most_asleep, '=', int(max_guard) * int(min_most_asleep))

    max = 0
    max_min = -1
    max_guard = -1
    for min in who_is_sleeping:
        for guard in who_is_sleeping[min]:
            if who_is_sleeping[min][guard] >= max:
                max = who_is_sleeping[min][guard]
                max_min = min
                max_guard = guard

    print('b:', max_min, 'x', max_guard, '=', int(max_min) * int(max_guard))




