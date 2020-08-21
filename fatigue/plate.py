import xlrd
from fatigue.utils import is_number


def static_pressure(draft, elevation, rho_s, g):
    """
    Generate static sea pressure on hull

    :param draft:
    :param elevation:
    :param rho_s:
    :param g:
    :return:
    """
    stat_pressure = (draft - elevation) * rho_s * g
    return (stat_pressure)


def get_panel_pressure(dict, lc, panel_location):
    """
    :param lc: str
        loading condition: 'Loaded', 'Part' or 'Ballast'
    :param panel_location: list
        List of location coordinates [m]
    :param panel_radius:

    :param fls_pressure: table in Excel with radius [m], elevation [m], directions [deg], pressure amplitudes [kPa],
        [  ]    [x-loc]     [z-loc]     [  ]    [weibull]   [period]    [pressure kN/m2]    [pressure N/m2]

    :param direction:

    Find the elevation value closest to the

    :return:
    """

    loc = ('C:\\Users\\oed\\PycharmProjects\\GeniEScript\\fls_pressures.xlsx')
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_name(lc)

    pressure_dict = {}

    for row_num in range(sheet.nrows):

        # Read row data from sheet.
        row_value = sheet.row_values(row_num)

        # If elevation is lower than panel elevation
        if is_number(row_value[1]) and row_value[1] == panel_location[0] and row_value[2] == panel_location[1]:
            pressure_dict = {
                "weibull": row_value[4],
                "period": row_value[5],
                "pressure": row_value[7]
            }
    return pressure_dict


def sn_curve_from_excel(sn_curve):
    """
    Fetch data on SN-curve from local Excel-file
    :param sn_curve:
    :return: sn_curve: dict
    {m1, log_a1, m2, log_a2, slope, k}

    """

    loc = ('C:\\Users\\oed\\PycharmProjects\\GeniEScript\\sn_curves.xlsx')
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    check = 0

    for row_num in range(sheet.nrows):
        row_value = sheet.row_values(row_num)
        if row_value[1] == sn_curve:
            sn_curve = dict(
                m1=row_value[2],
                log_a1=row_value[3],
                m2=row_value[4],
                log_a2=row_value[5],
                slope=row_value[6],
                k=row_value[7])
            check = 1
            return sn_curve

    if check == 0:
        print('SN-curve not recognized')



sn = sn_curve_from_excel('B1')
print(sn)