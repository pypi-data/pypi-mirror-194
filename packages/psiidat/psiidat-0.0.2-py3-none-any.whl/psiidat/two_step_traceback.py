# filename: two_step_ballistic_backmapping_method.py
# Aim:  给定起始点（卡林顿经纬度）和太阳风速度（km/s），沿着parker spiral 和 利用PFSS 输出磁力线在源表面上足点和光球层足点。
# Code by: Jiansen He and Chuanpeng Hou
# Last Change: 2022-03-15
import numpy as np
import julian
import datetime
import gzip
import sunpy.map
import astropy.constants as const
import astropy.units as u
from astropy.coordinates import SkyCoord
from sunpy.net import attrs as attrs
import sunpy.map
import sunpy.coordinates.frames as frames
import pfsspy
from pfsspy import tracing
import sunpy
import sunpy.map
import sunpy.data.sample
from sunpy.net import Fido
import warnings
import os
warnings.filterwarnings("ignore")

def parker_spiral_trace_back(r_vect_au, lat_beg_deg, lon_beg_deg, Vsw_r_vect_kmps):
    from_au_to_km = 1.49597871e8  # unit: km
    from_deg_to_rad = np.pi / 180.
    from_rs_to_km = 6.96e5
    from_au_to_rs = from_au_to_km / from_rs_to_km
    r_vect_km = r_vect_au * from_au_to_km
    num_steps = len(r_vect_km) - 1
    phi_r_vect = np.zeros(num_steps + 1)
    for i_step in range(0, num_steps):
        if (i_step == 0):
            phi_at_r_current = lon_beg_deg * from_deg_to_rad  # unit: rad
        else:
            phi_at_r_current = phi_at_r_next
        r_current = r_vect_km[i_step]
        r_next = r_vect_km[i_step + 1]
        r_mid = (r_current + r_next) / 2
        dr = r_current - r_next
        Vsw_at_r_current = Vsw_r_vect_kmps[i_step - 1]
        Vsw_at_r_next = Vsw_r_vect_kmps[i_step]
        Vsw_at_r_mid = (Vsw_at_r_current + Vsw_at_r_next) / 2
        k1 = dr * dphidr(r_current, phi_at_r_current, Vsw_at_r_current)
        k2 = dr * dphidr(r_current + 0.5 * dr, phi_at_r_current + 0.5 * k1, Vsw_at_r_mid)
        k3 = dr * dphidr(r_current + 0.5 * dr, phi_at_r_current + 0.5 * k2, Vsw_at_r_mid)
        k4 = dr * dphidr(r_current + 1.0 * dr, phi_at_r_current + 1.0 * k3, Vsw_at_r_next)
        phi_at_r_next = phi_at_r_current + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        phi_r_vect[i_step + 1] = phi_at_r_next
    lon_r_vect_deg = phi_r_vect / from_deg_to_rad  # from [rad] to [degree]
    lat_r_vect_deg = np.zeros(num_steps + 1) + lat_beg_deg  # unit: [degree]
    r_footpoint_on_SourceSurface_rs = r_vect_au[-1] * from_au_to_rs
    lon_footpoint_on_SourceSurface_deg = lon_r_vect_deg[-1]
    lat_footpoint_on_SourceSurface_deg = lat_r_vect_deg[-1]
    return r_footpoint_on_SourceSurface_rs, lon_footpoint_on_SourceSurface_deg, lat_footpoint_on_SourceSurface_deg

def PFSS_trace_back(dir_data_PFSS, time_beg_str_FidoQuery, time_end_str_FidoQuery, rss, lon_seed, lat_seed):
    data_dir = dir_data_PFSS
    query = (attrs.Time(time_beg_str_FidoQuery, time_end_str_FidoQuery),
             ## (a.Time('2018/11/04 03:00:00', '2018/11/04 04:00:00'),
             attrs.Instrument('GONG'),
             attrs.Physobs.los_magnetic_field)
    try:
        result = Fido.search(*query)
        print(result)
    except:
        field_line = []
        input_v2 = []
        output = []
        filename = []
        return field_line, input_v2, output, filename

    downloaded_file = Fido.fetch(result, path=data_dir + '{file}', overwrite=False)
    # print(downloaded_file)
    if downloaded_file == []:
        field_line = []
        input_v2 = []
        output = []
        filename = []
        return field_line, input_v2, output, filename
    else:
        # The PFSS solution is calculated on a regular 3D grid in (phi, s, rho), where rho = ln(r), and r is the standard spherical radial coordinate. We need to define the number of rho grid points, and the source surface radius.
        filename = downloaded_file[0]
        print('filename: ', filename)
        import gzip


        filename_out = filename.rstrip('.gz')
        uncompress_file(filename, filename_out)
        filename = filename_out
        print('filename_out: ', filename_out)

        gong_map = sunpy.map.Map(filename)
        nrho = 35
        rss = rss  # 2.5 or 2.0 or 1.2

        # From the boundary condition, number of radial grid points, and source surface, we now construct an Input object that stores this information
        input_v2 = pfsspy.Input(gong_map, nrho, rss)

        # Now calculate the PFSS solution
        output = pfsspy.pfss(input_v2)

        # get the position/coordinate of the seed
        tracer = tracing.PythonTracer()
        r = ((rss - 1) * 0.99 + 1) * const.R_sun
        r_seed = r
        lat = lat_seed * np.pi / 180 * u.rad
        lon = lon_seed * np.pi / 180 * u.rad
        seeds = SkyCoord(lon, lat, r, frame=output.coordinate_frame)

        # get the field line information using 'tracer' procedure
        field_line = tracer.trace(seeds, output)

        '''
        # the coords of field_line can be used to 
        for field_line in field_lines:
            color = {0: 'black', -1: 'tab:blue', 1: 'tab:red'}.get(field_line.polarity)
            coords = field_line.coords
            coords.representation_type = 'cartesian'
            ax.plot(coords.x / const.R_sun,
                    coords.y / const.R_sun,
                    coords.z / const.R_sun,
                    color=color, linewidth=1)
        '''
        from_rad_to_deg = 180 / np.pi
        MFL_photosphere_lon_deg = field_line[0].solar_footpoint.data.lon.value * from_rad_to_deg
        MFL_photosphere_lat_deg = field_line[0].solar_footpoint.data.lat.value * from_rad_to_deg
        return MFL_photosphere_lon_deg, MFL_photosphere_lat_deg

def get_Vsw_r_vect(r_vect_au, Vsw_r_beg_kmps):
    num_steps = len(r_vect_au)
    Vsw_r_vect_kmps = np.zeros(num_steps) + Vsw_r_beg_kmps
    return Vsw_r_vect_kmps

def dphidr(r, phi_at_r, Vsw_at_r):
    period_sunrot = 27. * (24. * 60. * 60)  # unit: s
    omega_sunrot = 2 * np.pi / period_sunrot
    result = omega_sunrot / Vsw_at_r  # unit: rad/km
    return result

def uncompress_file(fn_in, fn_out):
    f_in = gzip.open(fn_in, 'rb')
    f_out = open(fn_out, 'wb')
    file_content = f_in.read()
    f_out.write(file_content)
    f_out.close()
    f_in.close()

def Carrington_To_Helioprojective(carr_lon, carr_lat, obstime):
    # 将卡林顿坐标转换到天空平面，比如转到AIA图中x,y,单位角秒。
    Carrington_lon_lat = SkyCoord(lon=carr_lon * u.deg, lat=carr_lat * u.deg, \
                                  frame=frames.HeliographicCarrington, obstime=obstime, observer="earth")
    helioprojective = Carrington_lon_lat.transform_to(frames.Helioprojective)
    x_arcsec = helioprojective.Tx.value
    y_arcsec = helioprojective.Ty.value
    return x_arcsec, y_arcsec

def two_step_backmapping(datetime_trace, r_beg_au, lat_beg_deg, lon_beg_deg, Vsw_r, r_source_surfae_rs, dir_data_PFSS=os.getcwd()+'/'):
    # frame: HeliographicCarrington
    # datetime_trace = datetime.datetime(2020, 1, 24, 0, 0, 0)
    num_steps = 1000
    from_au_to_km = 1.49597871e8  # unit: km
    from_Rs_to_km = 6.96e5
    from_rs_to_au = from_Rs_to_km / from_au_to_km # unit: au
    from_au_to_Rs = 214.9394693836
    #step1: 按帕克螺旋回溯到源表面
    r_source_surfae_rs_au = r_source_surfae_rs * from_rs_to_au
    r_vect_au = np.linspace(r_beg_au, r_source_surfae_rs_au, num=num_steps)
    Vsw_r_vect_kmps = get_Vsw_r_vect(r_vect_au, Vsw_r)
    r_footpoint_on_SourceSurface_rs, \
    lon_footpoint_on_SourceSurface_deg, \
    lat_footpoint_on_SourceSurface_deg = parker_spiral_trace_back(r_vect_au, lat_beg_deg, lon_beg_deg, Vsw_r_vect_kmps)

    # step2: 从源表面回溯到光球层（太阳表面）
    JulDay_trace = julian.to_jd(datetime_trace)
    JulDay_start = JulDay_trace - 1.0 / 24.
    JulDay_end   = JulDay_trace + 1.0 / 24.
    transit_time_unit_day = (r_beg_au * from_au_to_Rs - 1) * from_Rs_to_km / Vsw_r / 86400
    time_beg_str_FidoQuery = julian.from_jd(JulDay_start - transit_time_unit_day)
    time_end_str_FidoQuery = julian.from_jd(JulDay_end - transit_time_unit_day)
    MFL_photosphere_lon_deg, MFL_photosphere_lat_deg = PFSS_trace_back(dir_data_PFSS, time_beg_str_FidoQuery,
                                                                         time_end_str_FidoQuery, r_source_surfae_rs,
                                                             lon_footpoint_on_SourceSurface_deg,
                                                                         lat_footpoint_on_SourceSurface_deg)
    return r_footpoint_on_SourceSurface_rs, \
           lon_footpoint_on_SourceSurface_deg, \
           lat_footpoint_on_SourceSurface_deg,\
           MFL_photosphere_lon_deg, MFL_photosphere_lat_deg

def example():
    # 设置时间和起始点，frame: Carrington
    # 验证：目前这组参数的输出结果 和 http://connect-tool.irap.omp.eu/ 的结果符合。
    datetime_trace = datetime.datetime(2022, 3, 15, 0, 6, 0)
    r_beg_au = 0.99433529  # au
    lon_beg_deg = 257.79047678  # deg frame: Carrington
    lat_beg_deg = -7.17059345  # deg frame: Carrington
    Vsw_r = 389.2 # km/s
    r_source_surface_rs = 2.5 # Rs
    dir_data_PFSS = os.getcwd()+'/' #'/Users/hcp/research/MFL/data/PFSS_data/' # 存放Gong的磁图
    # 两步回溯
    r_footpoint_on_SourceSurface_rs, lon_footpoint_on_SourceSurface_deg, lat_footpoint_on_SourceSurface_deg, \
    MFL_photosphere_lon_deg, MFL_photosphere_lat_deg\
        =two_step_backmapping(datetime_trace, r_beg_au, lat_beg_deg, lon_beg_deg, Vsw_r, r_source_surface_rs, dir_data_PFSS)
    print('--------------------you can try----------------------------')
    print('type: psiidat.two_step_backtrace.two_step_backmapping(datetime.dateime(2022,3,15,0,06,0), r_beg_au, lat_beg_deg, lon_beg_deg, Vsw_r, r_source_surfae_rs, dir_data_PFSS))')
    
    print('------------------input------------------------------')
    print('datetime_trace: 2022-03-15 00:06:00')
    print('initial position (r[au], Carri_lon[deg], Carri_lat[deg]): ', r_beg_au, lon_beg_deg, lat_beg_deg)
    print('Vsw_r[km/s]: ', Vsw_r)
    print('source_surface[Rs]: ', r_source_surface_rs)
    # 输出结果
    print('--------------------output----------------------------')
    print('frame: Carrington')
    print('SS [Rs] lon_on_SS [deg] lat_on_SS [deg] lon_on_photosphere [deg] lat_on_photosphere [deg]')
    print(r_footpoint_on_SourceSurface_rs, \
           lon_footpoint_on_SourceSurface_deg, \
           lat_footpoint_on_SourceSurface_deg,\
           MFL_photosphere_lon_deg, MFL_photosphere_lat_deg)
    print('------------------------------------------------')
