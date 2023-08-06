import matplotlib.pyplot as plt

import numpy as np
import jax.numpy as jnp
from jax import jit
# from tqdm import tqdm
#
# cbm = ticktack.load_presaved_model('Guttler14')
# cbm.compile()
# # cbm.define_growth_season(['january', 'february', 'march', 'september', 'october', 'november'])
# cbm.define_growth_season(['march', 'april', 'may'])
#
#

from ticktack import Box, Flow, CarbonBoxModel, save_model, load_presaved_model
#
m = load_presaved_model("Brehm21")
print([i.get_hemisphere() for i in m.get_nodes_objects()])

SS = Box("Sedimentary Sink", 378000)
Sw = Box("Surface Water", 900)
Sb = Box("Surface Biota", 3)
Idw = Box("Intermediate & Deep water", 37800)
Slb = Box("Short-lived biota", 110)
Llb = Box("Long-lived Biota", 450)
L = Box("Litter", 300)
S = Box("Soil", 1350)
P = Box("Peat", 500)
Sp = Box("Stratosphere", 88.5, production_coefficient=0.7)
Tp = Box("Troposphere", 501.5, production_coefficient=0.3)

f1 = Flow(SS, Tp, 0.7)
f2 = Flow(Sp, Tp, 45)
f3 = Flow(Tp, Sp, 45)
f4 = Flow(Tp, Sw, 60.5)
f5 = Flow(Sw, Tp, 61)
f6 = Flow(Sw, Sb, 40)
f7 = Flow(Sb, Sw, 36)
f8 = Flow(Sb, Idw, 4)
f9 = Flow(Idw, Sw, 42)
f10 = Flow(Sw, Idw, 38.2)
f11 = Flow(Sw, SS, 0.3)
f12 = Flow(Idw, SS, 0.2)
f13 = Flow(Tp, Slb, 115)
f14 = Flow(Slb, Tp, 60)
f15 = Flow(Slb, Llb, 15)
f16 = Flow(Llb, L, 15)
f17 = Flow(Slb, L, 40)
f18 = Flow(L, S, 3)
f19 = Flow(L, P, 1)
f20 = Flow(L, Sw, 1)
f21 = Flow(L, Tp, 50)
f22 = Flow(S, Tp, 3)
f23 = Flow(P, Tp, 0.8)
f24 = Flow(P, SS, 0.2)
CBM = CarbonBoxModel(production_rate_units='atoms/cm^2/s')
to_add = [Sp, Tp, Sw, Sb, Idw, Slb, Llb, L, S, P, SS]
CBM.add_nodes(to_add)
CBM.add_edges([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20,
               f21, f22, f23, f24])
CBM.compile()
save_model(CBM, 'data/Guttler14.hd5')

SSS = Box("Sedimentary Sink", 189000, hemisphere='south')
SwS = Box("Surface Water", 540, hemisphere='south')
SbS = Box("Surface Biota", 1.8, hemisphere='south')
IdwS = Box("Intermediate and Deep water South", 22680, hemisphere='south')
SlbS = Box("Short-lived biota", 33, hemisphere='south')
LlbS = Box("Long-lived Biota", 135, hemisphere='south')
LS = Box("Litter", 90, hemisphere='south')
SoS = Box("Soil", 405, hemisphere='south')
PS = Box("Peat", 150, hemisphere='south')
SpS = Box("Stratosphere", 44.5, production_coefficient=0.7 * 0.5, hemisphere='south')
TpS = Box("Troposphere", 250.5, production_coefficient=0.3 * 0.5, hemisphere='south')
SSN = Box("Sedimentary Sink", 189000, hemisphere='north')
SwN = Box("Surface Water", 360, hemisphere='north')
SbN = Box("Surface Biota", 1.2, hemisphere='north')
IdwN = Box("Intermediate & Deep water", 15120, hemisphere='north')
SlbN = Box("Short-lived biota", 77, hemisphere='north')
LlbN = Box("Long-lived Biota", 315, hemisphere='north')
LN = Box("Litter", 210, hemisphere='north')
SoN = Box("Soil", 945, hemisphere='north')
PN = Box("Peat", 350, hemisphere='north')
SpN = Box("Stratosphere", 44.5, production_coefficient=0.7 * 0.5, hemisphere='north')
TpN = Box("Troposphere", 250.5, production_coefficient=0.3 * 0.5, hemisphere='north')

f1 = Flow(SpS, TpS, 22.5)
f2 = Flow(TpS, SpS, 22.5)
f3 = Flow(TpS, SlbS, 34.5)
f4 = Flow(SlbS, TpS, 18)
f5 = Flow(TpS, SwS, 36.6)
f6 = Flow(SwS, TpS, 36.6)
f7 = Flow(SlbS, LlbS, 4.5)
f8 = Flow(LlbS, LS, 4.5)
f9 = Flow(SlbS, LS, 12)
f10 = Flow(LS, TpS, 15)
f11 = Flow(LS, SwS, 0.3)
f12 = Flow(LS, PS, 0.3)
f13 = Flow(LS, SoS, 0.9)
f14 = Flow(PS, TpS, 0.24)
f15 = Flow(PS, SSS, 0.06)
f16 = Flow(SoS, TpS, 0.9)
f17 = Flow(SwS, SSS, 0.18)
f18 = Flow(IdwS, SSS, 0.12)
f19 = Flow(SwS, SbS, 22.6)
f20 = Flow(SwS, IdwS, 37.92)
f21 = Flow(SwS, SwN, 13)
f22 = Flow(SbS, SwS, 20.2)
f23 = Flow(SbS, IdwS, 2.4)
f24 = Flow(IdwS, SwS, 43.2)
f25 = Flow(IdwS, IdwN, 15.12)
f26 = Flow(SSS, TpS, 0.36)
f27 = Flow(SpS, SpN, 44.1)
f28 = Flow(TpS, TpN, 71)
f29 = Flow(SpN, SpS, 44.1)
f30 = Flow(TpN, TpS, 71)
f31 = Flow(SpN, TpN, 22.5)
f32 = Flow(TpN, SpN, 22.5)
f33 = Flow(TpN, SwN, 24.4)
f34 = Flow(TpN, SlbN, 80.5)
f35 = Flow(SwN, TpN, 24.89)
f36 = Flow(SwN, SwS, 10)
f37 = Flow(SwN, SbN, 16)
f38 = Flow(SwN, IdwN, 28.29)
f39 = Flow(SlbN, TpN, 42)
f40 = Flow(SlbN, LlbN, 10.5)
f41 = Flow(SlbN, LN, 28)
f42 = Flow(LlbN, LN, 10.5)
f43 = Flow(SbN, SwN, 14.4)
f44 = Flow(SbN, IdwN, 1.6)
f45 = Flow(SwN, SSN, 0.12)
f46 = Flow(IdwN, SwN, 26.8)
f47 = Flow(IdwN, SSN, 0.09)
f48 = Flow(IdwN, IdwS, 18.12)
f49 = Flow(LN, SwN, 0.7)
f50 = Flow(LN, SoN, 2.1)
f51 = Flow(LN, TpN, 35)
f52 = Flow(LN, PN, 0.7)
f53 = Flow(SoN, TpN, 2.1)
f54 = Flow(PN, TpN, 0.56)
f55 = Flow(PN, SSN, 0.14)
f56 = Flow(SSN, TpN, 0.35)
cbm = CarbonBoxModel()
to_add = [SpS, TpS, SwS, SbS, IdwS, SlbS, LlbS, LS, SoS,
          PS, SSS, SpN, TpN, SwN, SbN, IdwN, SlbN, LlbN, LN, SoN, PN, SSN]
cbm.add_nodes(to_add)
cbm.add_edges([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20,
               f21, f22, f23, f24, f25, f26, f27, f28, f29, f30, f31, f32, f33, f34, f35, f36, f37, f38, f39, f40,
               f41, f42, f43, f44, f45, f46, f47, f48, f49, f50, f51, f52, f53, f54, f55, f56])

cbm.compile()
save_model(cbm, 'data/Brehm21.hd5')

SSS = Box("Sedimentary Sink", 189000, hemisphere='south')
SwS = Box("Surface Water", 540, hemisphere='south')
SbS = Box("Surface Biota", 1.8, hemisphere='south')
IdwS = Box("Intermediate and Deep water", 22680, hemisphere='south')
SlbS = Box("Short-lived biota", 33, hemisphere='south')
LlbS = Box("Long-lived Biota", 135, hemisphere='south')
LS = Box("Litter", 90, hemisphere='south')
SoS = Box("Soil", 405, hemisphere='south')
PS = Box("Peat", 150, hemisphere='south')
SpS = Box("Stratosphere", 44.5, production_coefficient=0.7 * 0.5, hemisphere='south')
TpS = Box("Troposphere", 250.5, production_coefficient=0.3 * 0.5, hemisphere='south')
SSN = Box("Sedimentary Sink", 189000, hemisphere='north')
SwN = Box("Surface Water", 360, hemisphere='north')
SbN = Box("Surface Biota", 1.2, hemisphere='north')
IdwN = Box("Intermediate & Deep water", 15120, hemisphere='north')
SlbN = Box("Short-lived biota", 77, hemisphere='north')
LlbN = Box("Long-lived Biota", 315, hemisphere='north')
LN = Box("Litter", 210, hemisphere='north')
SoN = Box("Soil", 945, hemisphere='north')
PN = Box("Peat", 350, hemisphere='north')
SpN = Box("Stratosphere", 44.5, production_coefficient=0.7 * 0.5, hemisphere='north')
TpN = Box("Troposphere", 250.5, production_coefficient=0.3 * 0.5, hemisphere='north')

f1 = Flow(SpS, TpS, 23.8)
f2 = Flow(TpS, SpS, 23.8)
f3 = Flow(TpS, SlbS, 35.36)
f4 = Flow(SlbS, TpS, 18.86)
f5 = Flow(TpS, SwS, 38.25)
f6 = Flow(SwS, TpS, 38.25)
f7 = Flow(SlbS, LlbS, 4.5)
f8 = Flow(LlbS, LS, 4.5)
f9 = Flow(SlbS, LS, 12)
f10 = Flow(LS, TpS, 15)
f11 = Flow(LS, SwS, 0.3)
f12 = Flow(LS, PS, 0.3)
f13 = Flow(LS, SoS, 0.9)
f14 = Flow(PS, TpS, 0.24)
f15 = Flow(PS, SSS, 0.06)
f16 = Flow(SoS, TpS, 0.9)
f17 = Flow(SwS, SSS, 0.18)
f18 = Flow(IdwS, SSS, 0.12)
f19 = Flow(SwS, SbS, 22.6)
f20 = Flow(SwS, IdwS, 8.52)
f21 = Flow(SwS, SwN, 28.8)
f22 = Flow(SbS, SwS, 20.2)
f23 = Flow(SbS, IdwS, 2.4)
f24 = Flow(IdwS, SwS, 39.6)
f25 = Flow(IdwS, IdwN, 0.72)
f26 = Flow(SSS, TpS, 0.36)
f27 = Flow(SpS, SpN, 22.25)
f28 = Flow(TpS, TpN, 71.6)
f29 = Flow(SpN, SpS, 22.25)
f30 = Flow(TpN, TpS, 71.6)
f31 = Flow(SpN, TpN, 23.8)
f32 = Flow(TpN, SpN, 23.8)
f33 = Flow(TpN, SwN, 29.16)
f34 = Flow(TpN, SlbN, 80.51)
f35 = Flow(SwN, TpN, 29.65)
f36 = Flow(SwN, SwS, 0)
f37 = Flow(SwN, SbN, 16)
f38 = Flow(SwN, IdwN, 49.69)
f39 = Flow(SlbN, TpN, 42.01)
f40 = Flow(SlbN, LlbN, 10.5)
f41 = Flow(SlbN, LN, 28)
f42 = Flow(LlbN, LN, 10.5)
f43 = Flow(SbN, SwN, 14.4)
f44 = Flow(SbN, IdwN, 1.6)
f45 = Flow(SwN, SSN, 0.12)
f46 = Flow(IdwN, SwN, 22.4)
f47 = Flow(IdwN, SSN, 0.09)
f48 = Flow(IdwN, IdwS, 29.52)
f49 = Flow(LN, SwN, 0.7)
f50 = Flow(LN, SoN, 2.1)
f51 = Flow(LN, TpN, 35)
f52 = Flow(LN, PN, 0.7)
f53 = Flow(SoN, TpN, 2.1)
f54 = Flow(PN, TpN, 0.56)
f55 = Flow(PN, SSN, 0.14)
f56 = Flow(SSN, TpN, 0.35)
CBM = CarbonBoxModel()
to_add = [SpS, TpS, SwS, SbS, IdwS, SlbS, LlbS, LS, SoS,
          PS, SSS, SpN, TpN, SwN, SbN, IdwN, SlbN, LlbN, LN, SoN, PN, SSN]
CBM.add_nodes(to_add)
CBM.add_edges([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20,
               f21, f22, f23, f24, f25, f26, f27, f28, f29, f30, f31, f32, f33, f34, f35, f36, f37, f38, f39, f40,
               f41, f42, f43, f44, f45, f46, f47, f48, f49, f50, f51, f52, f53, f54, f55, f56])
CBM.compile()
save_model(CBM, 'data/Buntgen18.hd5')

strat = Box('Stratosphere', 112.5, 0.7)
trop = Box('Troposphere', 637.5, 0.3)
MS = Box("Marine surface", 900)
Bio = Box("Biosphere", 1600)
f1 = Flow(strat, trop, 1 / 2)
f2 = Flow(trop, MS, 1 / 11)
f3 = Flow(trop, Bio, 1 / 23)
CBM = CarbonBoxModel(flow_rate_units='1/yr')
CBM.add_nodes([strat, trop, MS, Bio])
CBM.add_edges([f1, f2, f3])
CBM.compile()
save_model(CBM, 'data/Miyake17.hd5')

# start = 760
# resolution = 1000
# burn_in_time = np.linspace(760 - 1000, 760, resolution)
# steady_state_burn_in = cbm.equilibrate(target_C_14=707)
# burn_in_solutions = cbm.equilibrate(production_rate=steady_state_burn_in)
# d_14_time_series_fine = np.linspace(760, 900, 3000)
# d_14_time_series_coarse = np.arange(760, 788)
#
#
# # @jit
# # def miyake_event(t, start_time, duration, phase, area):
# #     height = sg(t, start_time, duration, area)
# #     prod = steady_state_burn_in + 0.18 * steady_state_burn_in * jnp.sin(2 * np.pi / 11 * t + phase) + height
# #     return prod
#
#
#
# # burn_in, _ = cbm.run(burn_in_time, production=(lambda x: jnp.sin(x) + steady_state_burn_in),
# #                      y0=burn_in_solutions)
# # #
# # prod = (lambda x: jnp.sin(x) + steady_state_burn_in)(d_14_time_series_fine)
# # #
# # event, _ = cbm.run(d_14_time_series_fine, production=(lambda x: jnp.sin(x) + steady_state_burn_in),
# #                    y0=burn_in[-1, :])
# #
# # burn_in, _ = cbm.run(burn_in_time, production=(lambda x: jnp.interp(x, d_14_time_series_fine, steady_state_burn_in *
# #                                                                     jnp.ones_like(d_14_time_series_fine))), y0=burn_in_solutions)
# # prod = gauss(d_14_time_series_fine)
# # #
# # event, _ = cbm.run(d_14_time_series_fine, production=gauss, y0=burn_in[-1, :])
#
#
# # data = [0., 0.02703184, 0.05466421, 0.08266299, 0.11080523, 0.13887943,
# #         0.16668472, 0.19403065, 0.22073735, 0.24663486, 0.2715631, 0.29537192,
# #         0.31792056, 0.3390777, 0.35872152, 0.37673911, 0.39302671, 0.40748962,
# #         0.42004178, 0.43060585, 0.43911329, 0.44550386, 0.4497257, 0.45173534,
# #         0.45149734, 0.44898432, 0.44417682, 0.43706305, 0.42763894, 0.41590783,
# #         0.40188034, 0.38557431, 0.36701454, 0.3462326, 0.3232667, 0.29816149,
# #         0.27096781, 0.24174255, 0.21054838, 0.17745352, 0.14253159, 0.10586123,
# #         0.06752599, 0.02761401, -0.01378227, -0.05656629, -0.10063769, -0.14589266,
# #         -0.19222406, -0.23952186, -0.28767336, -0.33656346, -0.38607503, -0.43608921,
# #         -0.48648555, -0.53714254, -0.58793788, -0.63874852, -0.6894513, -0.73992313,
# #         -0.79004118, -0.83968337, -0.88872854, -0.93705672, -0.98454958, -1.03109057,
# #         -1.07656515, -1.12086129, -1.16386959, -1.20548339, -1.24559937, -1.28411755,
# #         -1.32094151, -1.35597884, -1.38914111, -1.42034417, -1.44950846, -1.47655903,
# #         -1.50142572, -1.52404354, -1.5443526, -1.56229824, -1.57783138, -1.59090843,
# #         -1.60149142, -1.60954824, -1.61505251, -1.61798374, -1.61832745, -1.61607507,
# #         -1.61122401, -1.60377776, -1.59374572, -1.58114327, -1.5659918, -1.54831852,
# #         -1.52815649, -1.50554454, -1.48052715, -1.45315437, -1.42348171, -1.39156998,
# #         -1.35748521, -1.32129844, -1.2830856, -1.24292731, -1.20090872, -1.15711928,
# #         -1.11165258, -1.06460609, -1.01608098, -0.96618189, -0.9150166, -0.86269594,
# #         -0.80933341, -0.75504492, -0.69994863, -0.64416463, -0.58781458, -0.53102156,
# #         -0.47390972, -0.41660396, -0.3592298, -0.3019129, -0.24477884, -0.18795296,
# #         -0.13155988, -0.07572326, -0.02056569, 0.0337918, 0.08722998, 0.13963155,
# #         0.1908816, 0.24086778, 0.28948045, 0.33661319, 0.38216283, 0.42602967,
# #         0.46811793, 0.50833579, 0.54659553, 0.58281395, 0.61691245, 0.64881711,
# #         0.67845909, 0.70577458, 0.73070499, 0.75319722, 0.7732036, 0.79068205,
# #         0.80559632, 0.81791589, 0.82761604, 0.83467811, 0.83908932, 0.8408429
# #     , 0.83993813, 0.83638028, 0.83018062, 0.82135643, 0.8099309, 0.79593312,
# #         0.77939803, 0.76036628, 0.73888419, 0.71500363, 0.68878189, 0.66028158,
# #         0.62957045, 0.59672127, 0.56181165, 0.52492385, 0.48614461, 0.44556497,
# #         0.40328, 0.35938869, 0.31399361, 0.26720073, 0.21911919, 0.16986107,
# #         4.26516881, 8.12505955, 8.48855954, 8.81671607, 9.11198556, 9.37666688,
# #         9.61291263, 9.822739161, 0.008037291, 0.17057886, 10.3120274, 10.43394556,
# #         10.53779625, 10.624957381, 0.696725191, 0.75431408, 10.7988669, 10.83146047,
# #         10.85310516, 10.864750841, 0.867293061, 0.86157281, 10.84838028, 10.82845945,
# #         10.80250862, 10.771184061, 0.73510261, 0.69484191, 10.65094437, 10.60391873,
# #         10.55424002, 10.502352731, 0.448672711, 0.39358692, 10.33745557, 10.28061374,
# #         10.2233716, 10.16601619, 10.10881242, 10.05200322, 9.9958115, 9.94044065,
# #         9.88607468, 9.8328799, 9.78100552, 9.73058382, 9.68173127, 9.63454923,
# #         9.5891242, 9.54552888, 9.50382256, 9.46405148, 9.42624985, 9.39044013,
# #         9.35663338, 9.32483018, 9.29502096, 9.26718636, 9.24129795, 9.21731862,
# #         9.195203, 9.17489806, 9.15634349, 9.13947212, 9.12421055, 9.11047937,
# #         9.09819376, 9.08726392, 9.07759541, 9.06908967, 9.06164444, 9.05515407,
# #         9.0495101, 9.04460156, 9.04031536, 9.0365368, 9.03314984, 9.03003746,
# #         9.02708227, 9.02416663, 9.02117302, 9.01798462, 9.01448546, 9.01056076,
# #         9.00609742, 9.00098414, 8.99511186, 8.98837408, 8.980667, 8.97188992,
# #         8.9619456, 8.95074028, 8.93818402, 8.92419111, 8.90868003, 8.89157378,
# #         8.87280016, 8.85229171, 8.82998614, 8.80582638, 8.7797606, 8.75174254,
# #         8.72173156, 8.6896926, 8.65559642, 8.61941967, 8.58114482, 8.54076032,
# #         8.49826056, 8.45364587, 8.40692259, 8.358103, 8.30720521, 8.2542533
# #     , 8.19927709, 8.1423121, 8.08339954, 8.02258611, 7.95992393, 7.89547043,
# #         7.82928815, 7.76144464, 7.69201228, 7.62106806, 7.5486935, 7.47497433,
# #         7.40000033, 7.32386518, 7.24666613, 7.16850378, 7.08948196, 7.0097073
# #     , 6.9292891, 6.84833905, 6.7669709, 6.68530025, 6.6034443, 6.52152147,
# #         6.43965114, 6.35795353, 6.27654917, 6.19555875, 6.11510285, 6.03530153,
# #         5.9562742, 5.87813927, 5.80101375, 5.72501317, 5.65025128, 5.57683954,
# #         5.50488713, 5.43450065, 5.36578369, 5.29883673, 5.23375694, 5.17063775]
#
# data = [0] * len(d_14_time_series_fine)
#
# @jit
# def gauss(t, a):
#     return steady_state_burn_in + a * steady_state_burn_in * jnp.exp(-1 / 2 * ((t - 762) / 10) ** 2.)
#
#
# d_14_c = cbm.run_D_14_C_values(d_14_time_series_coarse, 20, production=gauss, y0=burn_in_solutions,
#                                steady_state_solutions=burn_in_solutions, args=(0.2,), hemisphere='north')
#
#
# d_14_c_2 = cbm.run_D_14_C_values(d_14_time_series_coarse, 20, production=gauss, y0=burn_in_solutions,
#                                steady_state_solutions=burn_in_solutions, args=(0.2,), hemisphere='south')
#
# plt.plot(d_14_time_series_coarse[1:], d_14_c)
# plt.plot(d_14_time_series_coarse[1:], d_14_c_2)
# plt.legend(['north', 'south'])
# # d_14_c = cbm.run_D_14_C_values(d_14_time_series_coarse, 36, production=miyake_event,
# #                                args=(775, 1 / 12, np.pi / 2, 81 / 12),
# #                                y0=burn_in[-1, :], steady_state_solutions=burn_in_solutions)
#
# # d_14_c = cbm.run_D_14_C_values(d_14_time_series_coarse, 100, production=miyake_event,
# #                                args=(775, 1 / 12, np.pi / 2, 81 / 12),
# #                                y0=burn_in[-1, :], steady_state_solutions=burn_in_solutions)
#
#
# # time = [760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781,
# #         782, 783, 784, 785, 786,
# #         787]
# # data = [1.06410298, 1.5367276, 1.51169672, 0.9969651, 0.15607606, -0.74379975, -1.41675028, -1.64896262, -1.36665597,
# #         -0.65952345, 0.24776537, 1.06694693, 1.53775122, 1.51059531, 0.99410909, 13.04279632, 15.60237974, 15.31378764,
# #         14.39241923, 13.61596338, 13.20866813, 13.07626751, 12.97493428, 12.65005045, 11.94170986, 10.84298464,
# #         9.50193803]
#
#
#
# # prdo = cbm.production_rate_finder(np.array(event[:, 1]), np.array(d_14_time_series_fine), i =10)
# # event3, _ = cbm.run(d_14_time_series_fine, production=(lambda x: jnp.interp(x, d_14_time_series_fine[1:], prdo[:])), target_C_14=707)
# # prdo2 = cbm.production_rate_finder(np.array(event[:, 1]), np.array(d_14_time_series_fine), i=30)
# # event2, _ = cbm.run(d_14_time_series_fine, production=(lambda x: jnp.interp(x, d_14_time_series_fine[1:], prdo2[:])), target_C_14=707)
#
# # prdo = cbm.production_rate_finder(np.array(event[:, 1]), np.array(d_14_time_series_fine), i =10)
# # event3, _ = cbm.run(d_14_time_series_fine, production=(lambda x: jnp.interp(x, d_14_time_series_fine[1:], prdo[:])), target_C_14=707)
# # prdo2 = cbm.production_rate_finder(np.array(event[:, 1]), np.array(d_14_time_series_fine), i=30)
# # event2, _ = cbm.run(d_14_time_series_fine, production=(lambda x: jnp.interp(x, d_14_time_series_fine[1:], prdo2[:])), target_C_14=707)
# # prdo3 = cbm.production_rate_finder(np.array(event[:, 1]), np.array(d_14_time_series_fine), i=0)
# # event1, _ = cbm.run(d_14_time_series_fine, production=(lambda x: jnp.interp(x, d_14_time_series_fine[1:], prdo3[:])), target_C_14=707)
# # prdo4 = cbm.production_rate_finder(np.array(event[:, 1]), np.array(d_14_time_series_fine), i=1)
# # event0, _ = cbm.run(d_14_time_series_fine, production=(lambda x: jnp.interp(x, d_14_time_series_fine[1:], prdo4[:])), target_C_14=707)
#
# # print(prdo)
# #
# # rec_amp = []
# # burn_in, _ = cbm.run(burn_in_time, production=(lambda x: jnp.interp(x, d_14_time_series_fine, steady_state_burn_in *
# #                                                                     jnp.ones_like(d_14_time_series_fine))),
# #                      y0=burn_in_solutions)
# # # event, _ = cbm.run(d_14_time_series_fine, production=gauss, y0=burn_in[-1, :])
# # fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(16.0, 6.0))
# # steady_state_production = cbm.equilibrate(target_C_14=707)
# # actual_amp = []
# # rec_max = []
# # rec_min = []
# # nodes = cbm.get_nodes_objects()
#
# # for i in range(1, 10):
# #     amp = i * 0.2
# #     actual_amp.append(amp)
# #     print('amplitude = ' + str(amp))
# #     prod = gauss(d_14_time_series_fine, amp)
# #     event, _ = cbm.run(d_14_time_series_fine, production=gauss, y0=burn_in[-1, :], args=(amp,))
# #     # box1, rec_prod = cbm.production_rate_finder(jnp.array(event[:, 1]), jnp.array(d_14_time_series_fine),
# #     #                                       steady_state_production,nodes[0].get_reservoir_content(), nodes[1].get_reservoir_content(),i=0, idx=0, prod=0.7)
# #     box2, rec_prod_2 = cbm.production_rate_finder(jnp.array(event[:, 1]), jnp.array(d_14_time_series_fine),steady_state_production,
# #                                             nodes[0].get_reservoir_content(), nodes[1].get_reservoir_content(), i=0, idx=0, prod=0.7)
# #     rec_amp.append(np.max(rec_prod_2) - np.min(rec_prod_2))
# #     ax1.plot(prod[1:], rec_prod_2[:])
# #     ax3.plot(d_14_time_series_fine[1:], rec_prod_2, 'b')
# #     ax3.plot(d_14_time_series_fine, prod, 'r')
# #     ax3.legend(['simulated', 'actual'])
#
#     # # ax4.plot(d_14_time_series_fine[1:], rec_prod, 'b')
#     # ax4.plot(d_14_time_series_fine[1:], rec_prod_2, 'r')
#     # ax4.plot(d_14_time_series_fine, prod, 'g')
#     # ax4.legend(['0 iterations', '10 iterations', 'actual'])
#     # rows = 4
#     # columns = 3
#     # grid = plt.GridSpec(rows, columns, wspace=0.5, hspace=0.5)
#     # for j in range(rows * columns - 1):
#     #     exec(f"plt.subplot(grid{[j]})")
#     #     plt.plot(d_14_time_series_fine, box1[:, j],d_14_time_series_fine, event[:, j], d_14_time_series_fine, box2[:, j])
#     #     plt.legend(['simulated 0 iterations', 'actual', 'simulated 10 iterations'])
#     #     plt.ticklabel_format(useOffset=False)
#     #     plt.title(nodes[j].get_name())
#     # exec(f"plt.subplot(grid{[11]})")
#     # plt.plot(d_14_time_series_fine, event[:, 1])
#     # plt.title('actual Troposphere content')
#
# # ax1.legend(['amp=' + str(amp)])
#
# # ax2.plot(actual_amp, rec_amp, '.')
# # ax2.plot(actual_amp, actual_amp, '-')
# # print(np.array(actual_amp) / np.array(rec_amp))
# # ax2.plot(rec_amp, rec_amp, '-')
#
# # ax1.plot(d_14_time_series_fine[1:], prdo[:], 'b')
# # ax1.plot(d_14_time_series_fine[1:], prdo2, 'r')
# # ax1.plot(d_14_time_series_fine, prod, 'g')
# # ax1.plot(d_14_time_series_fine[1:], prdo3[:], 'm')
# # ax1.plot(d_14_time_series_fine[1:], prdo4, 'c')
# #
# # ax2.plot(d_14_time_series_fine, event3[:, 1], 'b')
# # ax2.plot(d_14_time_series_fine, event2[:, 1], 'r')
# # ax2.plot(d_14_time_series_fine, event[:, 1], 'g')
# # ax2.plot(d_14_time_series_fine, event1[:, 1], 'm')
# # ax2.plot(d_14_time_series_fine, event0[:, 1], 'c')
# # ax1.legend(['10 iterations', '30 iterations', 'actual', '1 iteration', '2 iterations'])
# # ax2.legend(['10 iterations', '30 iterations', 'actual', '1 iteration', '2 iterations'])
#
# # ax1.plot(d_14_time_series_fine, prod, 'r')
# # ax1.plot(d_14_time_series_fine, event[:, 1])
# # ax1.plot(d_14_time_series_fine[:20], event_2[:20, 1]-event[0, 1], 'g')
#
# # produc = miyake_event(burn_in_time, 775, 1 / 12, np.pi / 2, 81 / 12)
# # produc = miyake_event(burn_in_time, 775, 1/12, np.pi/2, 8/12)
#
# # ax1.plot(d_14_time_series_coarse[0:-1], d_14_c[0:], 'o')
# # ax1.plot(d_14_time_series_coarse[0:-1], d_14_c_2[0:], 'go')
# # ax1.plot(d_14_time_series_coarse[0:-1], d_14_c, 'o')
# # ax1.plot(d_14_time_series_coarse[0:-1], d_14_c, 'o')
#
# # ax2.plot(d_14_time_series_fine,prod)
# # ax2.set_xlim(774,776)
# # plt.axvline(775)
# # plt.axvline(775+ 1 / 12)
# # ax2.set_ylim(0,5)
#
# # ax1.ticklabel_format(useOffset=False)
# # ax2.ticklabel_format(useOffset=False)
#
# plt.show()
#
#
#
#
