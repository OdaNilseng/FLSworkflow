# from collections import OrderedDict
# from sqlalchemy import Column, Integer, Float, ForeignKey, String, text
# from sqlalchemy.dialects.postgresql import ARRAY, UUID
# from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy.orm import relationship
# from .base import Base

import scipy.special as sc
from scipy import stats
import math
import xlrd


class Fls:
    """
    FLS calculations side shell

    Parameters
    --------------------------------------------------------
    HULL
    project_id          -   int
    project             -   str
    description         -   str
    hull_radius         -   float   [m]
    no_outer_tanks      -   int                 -   Number of outer tanks
    design_life         -   int     [years]

    PLATES
    location            -   str                 -   'side shell', 'bilge box top', 'bottom' etc
    panel_elevation     -   float   [m]         -   Elevation above BL
    stiffener_spacing   -   float   [m]
    thickness           -   float   [mm]
    panel_id            -   int
    is_curved           -   bool
    global_stress       -   float   [kPa]

    TANKS
    a_vertical          -   float   [m/s2]      -   Vertical acceleration tanks
    tank_density        -   float   [ton/m3]     -   Density of tank content
    filling_height_tank -   float   [m]         -   Filling height from EL0

    CONDITIONS
    ext_pressure        -   float   [kPa]       -   External wave pressure, probability 10^4
    period              -   float   [s]         -   Wave period
    draft               -   float   [m]


    FATIGUE PARAMETERS
    sn_curve            -   str
    m1                  -   float               -   negative inverse slope of the SN-curve for n <= 10^7 cycles
    m2                  -   float               -   negative inverse slope of the SN-curve for n > 10^7 cycles
    log_a1              -   float               -   intercept of the design SN curve with the log N axis
    log_a2              -   float               -   intercept of the design SN curve with the log N axis
    slope               -   float               -
    DFF                 -   int                 -   Design fatigue factor
    combination         -   list                -   [Fully loaded, Partly loaded, Ballast]
    """

    # __table_args__ = {"schema": "concept_data"}
    #
    # id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"), )
    # project_id = Column('project_id', UUID(as_uuid=True), ForeignKey('project_data.project.id'), nullable=False)
    # project = relationship('Project', back_populates='fls_test')
    # description = Column('description', String(250), nullable=False)
    # hull_radius = Column('hull_id', Float, nullable=False)
    # no_outer_tanks = Column('no_outer_tanks', Integer, nullable=False)
    # design_life = Column('design_life', Integer, nullable=False)
    #
    # panel_location = Column('panel_location', String(250), nullable=False)
    # panel_elevation = Column('panel_elevation', Float, nullable=False)
    # stiffener_spacing = Column('stiffener_spacing', Float, nullable=False)
    # thickness = Column('panel_thickness', Float, nullable=False)
    # # panel_id = Column('panel_id', UUID(as_uuid=True), )
    # is_curved = Column('is_curved', Bool, nullable=True)
    #
    # a_vertical = Column('a_vertical', Float, nullable=False)
    # tank_density = Column('tank_density', Float, nullable=False)
    # filling_height = Column('filling_height', Float, nullable=False)
    # ext_pressure = Column('ext_pressure', Float, nullable=False)
    # period = Column('period', Float, nullable=False)
    # draft = Column('period', Float, nullable=False)
    #
    # sn_curve = Column('sn_curve', String(250), nullable=False)
    # m1 = Column('m1', Float, nullable=False)
    # m2 = Column('m2', Float, nullable=False)
    # log_a1 = Column('log_a1', Float, nullable=False)
    # log_a2 = Column('log_a2', Float, nullable=False)
    # slope = Column('slope', Float, nullable=False)
    # DFF = Column('DFF', Integer, nullable=False)
    # combination = Column('combination', Float, nullable=False)

    def __init__(self, project_id: int, description: str, hull_radius: float, no_outer_tanks: int, design_life: int,
                 panel_location: str, panel_elevation: float, stiffener_spacing: float, thickness: float,
                 is_curved: bool, a_vertical: float, tank_density: float, filling_height: float, ext_pressure: float,
                 period: float, draft: float, sn_curve: str):
        self.project_id = project_id
        self.description = description
        self.hull_radius = hull_radius
        self.no_outer_tanks = no_outer_tanks
        self.design_life = design_life

        self.panel_location = panel_location
        self.panel_elevation = panel_elevation
        self.stiffener_spacing = stiffener_spacing
        self.thickness = thickness
        self.is_curved = is_curved

        self.a_vertical = a_vertical
        self.tank_density = tank_density
        self.filling_height = filling_height
        self.ext_pressure = ext_pressure
        self.period = period
        self.draft = draft

        self.sn_curve = sn_curve
        # self.m1 = m1
        # self.m2 = m2

    tank_density = 1.025
    a_vertical = [0.82, 0.91, 1.03]
    filling_height = [0.0, 5.0, 17.0]
    draft = [27.0, 22.0, 17.0]
    cycles = 10000
    # design_life[1] = 25
    # panel_elevation[1] = 7.5,
    # stiffener_spacing[1] = 0.659
    design_life = 25

    panel_elevation = 7.5,
    stiffener_spacing = 0.659
    plate_thickness = 20.5

    ext_pressure = [71.70, 74.93, 79.12]
    global_stress = [18.3, 17.1, 16.7]
    weibull_shape = [0.950, 0.965, 1.008]
    period = [9.29, 9.27, 8.75]
    correlation = 0.5
    splash_zone = [1.0, 1.0, 0.976]

    def __repr__(self):
        return f"<Fls #{self.id}>"

    def to_dict(self):
        """OrderedDict: Dictionary representation of model data."""
        data = dict(
            id=self.id,
            project_id=self.project_id,
            project_name=self.project.name,
            project_number=self.project.number,
            project_location=self.project.location,
            project_client=self.project.client.name,
            project_description=self.project.description,
            description=self.description,
            panel_elevation=self.panel_elevation,
            stiffener_spacing=self.stiffener_spacing,
            thickness=self.thickness,
            sn_curve=self.sn_curve
        )

        return data

    # GET PLATE PRESSURES AS FUNCTION OF ELEVATION?

    def get_panel_pressure(self, panel_elevation, panel_radius, orientation):
        """
        :param panel_loc
        :param fls_pressure: table in Excel with radius [m], elevation [m], directions [deg], pressure amplitudes [kPa],
        :param direction:

        Find the elevation value closest to the

        :return:
        """

        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        loc = ('C:\\Users\\oed\\PycharmProjects\\GeniEScript\\fls_pressures.xlsx')
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)

        # absolute_difference_function = lambda list_value: abs(list_value - panel_elevation)
        # lower_elevation = min(fls_pressure[2], key=absolute_difference_function)

        low_index = 0
        column = 0
        panel_loc = 0

        # if orientation == 'horizontal':
        #     column = 1
        #     panel_loc = panel_radius
        # elif orientation == 'vertical':
        #     column = 2
        #     panel_loc = panel_elevation

        column = 2

        for row_num in range(sheet.nrows):

            # Read row data from sheet.
            row_value = sheet.row_values(row_num)

            # If elevation is lower than panel elevation
            if is_number(row_value[column]) and row_value[column] <= panel_loc:
                low_index = row_num

        panel_low = sheet.row_values(low_index)
        high_index = low_index + 1
        panel_high = sheet.row_values(high_index)

        # print(panel_low, panel_high)
        # interpolate to find values at correct elevation
        panel_pressure = panel_low[6] + (panel_loc - panel_low[column]) / (panel_high[column] - panel_low[column]) * (
                panel_high[6] - panel_low[6])
        panel_weibull = panel_low[4] + (panel_loc - panel_low[column]) / (panel_high[column] - panel_low[column]) * (
                panel_high[4] - panel_low[4])
        panel_period = panel_low[5] + abs(
            (panel_loc - panel_low[column]) / (panel_high[column] - panel_low[column])) * (panel_high[5] - panel_low[5])

        # difference_function = lambda list_value: (list_value - panel_elevation)
        # lower_elevation = min(fls_pressure[2], key=difference_function)

        return panel_pressure, panel_weibull, panel_period

    # add if statement to check direction of plate
    # x1, x3, y1, y3, z1, z3 = 1, 2, 3, 4, 5, 6
    # if (x1, y1) == (x3, y3) and z1 is not z3:
    #     orientation = 'vertical'
    # elif z1 == z3 and (x1, y1) is not (x3, y3):
    #     orientation = 'horizontal'
    # else:
    #     orientation = 'inclined'

    def calc_stress_fraction(self, tank_density, a_vertical, filling_height_tank, panel_elevation, ext_pressure,
                             global_stress,
                             cycles, weibull_shape, correlation, stiffener_spacing, plate_thickness, splash_zone):
        # INTERNAL STRESS   [MPa]
        int_pressure = max(tank_density * a_vertical * (filling_height_tank - panel_elevation), 0)
        int_stress = 0.5 / 1000 * int_pressure * (stiffener_spacing / (plate_thickness / 1000)) ** 2
        # EXTERNAL STRESS   [MPa]
        ext_stress = -0.5 / 1000 * ext_pressure * (stiffener_spacing / (plate_thickness / 1000)) ** 2 * splash_zone
        # LOCAL STRESS
        local_stress = 2 * math.sqrt(ext_stress ** 2 + int_stress ** 2 + 2 * correlation * ext_stress * int_stress)

        # COMBINED STRESS
        combined_stress = max(global_stress + 0.6 * local_stress, 0.6 * global_stress + local_stress)

        # STRESS FRACTION
        stress_fraction = combined_stress / (math.log(cycles) ** (1 / weibull_shape))

        return stress_fraction

    def sn_curve_from_excel(self, sn_curve):
        """
        Fetch data on SN-curve from local Excel-file
        :param sn_curve:
        :return: m1, log_a1, m2, log_a2, slope, k
        """

        loc = ('C:\\Users\\oed\\PycharmProjects\\GeniEScript\\sn_curves.xlsx')
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        check = 0

        for row_num in range(sheet.nrows):
            row_value = sheet.row_values(row_num)
            if row_value[1] == sn_curve:
                m1 = row_value[2]
                log_a1 = row_value[3]
                m2 = row_value[4]
                log_a2 = row_value[5]
                slope = row_value[6]
                k = row_value[7]
                check = 1

        if check == 0:
            print('SN-curve not recognized')

        return m1, log_a1, m2, log_a2, slope, k

    # sF = calc_stress_fraction(tank_density, a_vertical[2], filling_height[2], panel_elevation, ext_pressure[2],
    #                           global_stress[2], cycles, weibull_shape[2], correlation, stiffener_spacing,
    #                           plate_thickness, splash_zone[2])

    def slope_change(self, platethickness, m1, log_a1, slope, k_thickness):
        thickness_effect = math.log10(max(1, platethickness / 25)) * k_thickness
        slope_change = math.exp(math.log(10 ** (log_a1 - m1 * thickness_effect) / slope) / m1)

        return thickness_effect, slope_change

    def damage_plate(self, designlife, waveperiod, stress_fraction, weibullshape):
        m1, log_a1, m2, log_a2, slope, k = sn_curve_from_excel('Ec')

        thickness_effect, slopech = slope_change(plate_thickness, m1, log_a1, slope, k)

        designlife_seconds = designlife * 365 * 24 * 3600

        # sc.gammaincc(a,x) - regularized upper incomplete gamma function
        damage1 = designlife_seconds / waveperiod / (10 ** (log_a1 - m1 * thickness_effect)) * (stress_fraction ** m1) * \
                  sc.gamma(1 + m1 / weibullshape) * sc.gammaincc((1 + m1 / weibullshape),
                                                                 (slopech / stress_fraction) ** weibullshape)
        # sc.gammainc(a,x) - regularized lower incomplete gamma function
        damage2 = designlife_seconds / waveperiod / (10 ** (log_a2 - m2 * thickness_effect)) * (stress_fraction ** m2) * \
                  sc.gamma(1 + m2 / weibullshape) * sc.gammainc((1 + m2 / weibullshape),
                                                                ((slopech / stress_fraction) ** weibullshape))

        total_damage = damage1 + damage2
        return total_damage

    # damage = damage_plate(design_life, period[2], sF, weibull_shape[2])
    # print('Total damage: ', damage)

    def damage_load_combination(self, designlife, waveperiod, stress_fraction, weibullshape, combination):
        return damage_combination

    # hull_circum = hull_radius*2*math.pi
    # deg_tanks = 360/no_outer_tanks
    # tank_girder_distance = hull_circum/no_outer_tanks

    # __table_args__ = {"schema": "concept_data"}
    #
    # id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"), )
    # project_id = Column('project_id', UUID(as_uuid=True), ForeignKey('project_data.project.id'), nullable=False)
    # project = relationship('Project', back_populates='fls_test')
    # description = Column('description', String(250), nullable=False)
    # panel_elevation = Column('panel_elevation', Float, nullable=False)
    # stiffener_spacing = Column('stiffener_spacing', Float, nullable=False)
    # thickness = Column('panel_thickness', Float, nullable=False)
    # sn_curve = Column('sn_curve', String(250), nullable=False)
    #
    # def __init__(self, project_id: int, description: str, panel_elevation: float, stiffener_spacing: float, thickness: float, sn_curve: str):
    #     self.project_id = project_id
    #     self.description = description
    #     self.panel_elevation = panel_elevation
    #     self.stiffener_spacing = stiffener_spacing
    #     self.thickness = thickness
    #     self.sn_curve = sn_curve
    #
    # def __repr__(self):
    #     return f"<Flstest #{self.id}>"
    #
    # def to_dict(self):
    #     """OrderedDict: Dictionary representation of model data."""
    #     data = dict(
    #         id=self.id,
    #         project_id=self.project_id,
    #         project_name=self.project.name,
    #         project_number=self.project.number,
    #         project_location=self.project.location,
    #         project_client=self.project.client.name,
    #         project_description=self.project.description,
    #         description=self.description,
    #         panel_elevation=self.panel_elevation,
    #         stiffener_spacing=self.stiffener_spacing,
    #         thickness=self.thickness,
    #         sn_curve=self.sn_curve
    #     )
    #
    #
    #
    #     return data


plate1 = Fls(1, 'test', 82, 12, 25, 'side', 7.5, 0.7, 15, False, 1.2, 1.025, 5, 70, 10, 17.5, 'Ec')
print(plate1.get_panel_pressure(6.5, 42, 'vertical'))
print(plate1.calc_stress_fraction(tank_density, a_vertical[2], filling_height[2], panel_elevation, ext_pressure[2],
                                  global_stress[2], cycles, weibull_shape[2], correlation, stiffener_spacing,
                                  plate_thickness, splash_zone[2]))
print(plate1)
