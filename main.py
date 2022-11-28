import os
from urllib import request


def load_time_correction_data(standard: str = 'UT1') -> (list[int], list[float], list[float]):
    """
    Load tabular time correction data from the US Naval Observatory for different time standards
    Attempts to locate the file '{standard}.txt', if not found, web is accessed to retrieve the
    latest data (which is subsequently stored in a file of the same name)
    :param standard: time standard to retrieve correction data for ('UT1' or 'GPS')
    :return: list, list, list: Julian dates (+fractions), time correction data (in seconds)
    """
    # Raise error for unsupported time standards
    if standard not in ('UT1', 'GPS'):
        raise ValueError(f"Time standard '{standard}' not supported (UT1 or GPS).")

    # Check if a file for the standard already exists, load it if so
    if os.path.isfile(f'{standard}.dat'):
        data = []
        with open(f'{standard}.dat', 'r') as file:
            for line in file:
                data.append(line.strip())

    # Otherwise, retrieve the data from the web and store the result in a file
    else:

        # Get the correct url to retrieve the data from
        urls = {'UT1': 'https://maia.usno.navy.mil/ser7/finals.daily',
                'GPS': 'https://maia.usno.navy.mil/ser7/tai-utc.dat'}
        url = urls[standard]

        # Load data from url
        raw_data = request.urlopen(url).read()
        data = str(raw_data)[2:-3].split('\\n')

        # Save result to file
        with open(f'{standard}.dat', 'w') as file:
            for line in data:
                file.write(line + '\n')

    # Initialise lists for return values (Julian dates (+fractional), correction data)
    jds: list[int] = []
    frs: list[float] = []
    corrections: list[float] = []

    # Parse UT1 time standard data
    if standard == 'UT1':
        for row in data:
            date = row[7:15].split('.')
            jds.append(int(date[0]) + 2400000)
            frs.append(float('0.' + date[1]) + 0.5)
            corrections.append(float(row[58:68]))

    # Parse GPS time standard data
    if standard == 'GPS':
        for row in data:
            date = row[16:27].split('.')
            jds.append(int(date[0]))
            frs.append(float('0.' + date[1]))
            part1 = float(row[36:48].strip())
            part2 = float(row[59:64])
            part3 = float(row[70:78])
            mjd = int(date[0]) - 2400000.5
            diff_tai_gps = 19
            correction = part1 + (mjd - part2) * part3 - diff_tai_gps
            corrections.append(correction)

    return jds, frs, corrections


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # Use the function to retrieve time correction data (choose a time standard)
    corr_jds, corr_frs, corr_data = load_time_correction_data(standard='GPS')  # alternatively: GPS

    # Plot the data against the provided Julian date
    fig, ax = plt.subplots()
    ax.plot(corr_jds, corr_data)
    plt.show()
