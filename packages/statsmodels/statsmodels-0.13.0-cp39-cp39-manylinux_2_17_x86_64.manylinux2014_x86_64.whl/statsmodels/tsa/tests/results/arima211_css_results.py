import numpy as np

from statsmodels.tools.tools import Bunch

llf = np.array([-240.29558272688])

nobs = np.array([202])

k = np.array([5])

k_exog = np.array([1])

sigma = np.array([.79494581155191])

chi2 = np.array([1213.6019521322])

df_model = np.array([3])

k_ar = np.array([2])

k_ma = np.array([1])

params = np.array([
    .72428568600554,
    1.1464248419014,
    -.17024528879204,
    -.87113675466923,
    .63193884330392])

cov_params = np.array([
    .31218565961764,
    -.01618380799341,
    .00226345462929,
    .01386291798401,
    -.0036338799176,
    -.01618380799341,
    .00705713030623,
    -.00395404914463,
    -.00685704952799,
    -.00018629958479,
    .00226345462929,
    -.00395404914463,
    .00255884492061,
    .00363586332269,
    .00039879711931,
    .01386291798401,
    -.00685704952799,
    .00363586332269,
    .00751765532203,
    .00008982556101,
    -.0036338799176,
    -.00018629958479,
    .00039879711931,
    .00008982556101,
    .00077550533053]).reshape(5, 5)

xb = np.array([
    .72428566217422,
    .72428566217422,
    .56208884716034,
    .53160965442657,
    .45030161738396,
    .45229381322861,
    .38432359695435,
    .40517011284828,
    .36063131690025,
    .30754271149635,
    .32044330239296,
    .29408219456673,
    .27966624498367,
    .29743707180023,
    .25011941790581,
    .27747189998627,
    .24822402000427,
    .23426930606365,
    .27233305573463,
    .23524768650532,
    .26427435874939,
    .21787133812904,
    .22461311519146,
    .22853142023087,
    .24335558712482,
    .22953669726849,
    .25524401664734,
    .22482520341873,
    .26450532674789,
    .31863233447075,
    .27352628111839,
    .33670437335968,
    .25623551011086,
    .28701293468475,
    .315819054842,
    .3238864839077,
    .35844340920448,
    .34399557113647,
    .40348997712135,
    .39373970031738,
    .4022718667984,
    .46476069092751,
    .45762005448341,
    .46842387318611,
    .50536489486694,
    .52051961421967,
    .47866532206535,
    .50378143787384,
    .50863671302795,
    .4302790760994,
    .49568024277687,
    .44652271270752,
    .43774726986885,
    .43010330200195,
    .42344436049461,
    .44517293572426,
    .47460499405861,
    .62086409330368,
    .52550911903381,
    .77532315254211,
    .78466820716858,
    .85438597202301,
    .87056696414948,
    1.0393311977386,
    .99110960960388,
    .85202795267105,
    .91560190916061,
    .89238166809082,
    .88917690515518,
    .72121334075928,
    .84221452474594,
    .8454754948616,
    .82078683376312,
    .95394861698151,
    .84718400239944,
    .839300096035,
    .91501939296722,
    .95743554830551,
    1.0874761343002,
    1.1326615810394,
    1.1169674396515,
    1.3300451040268,
    1.4790810346603,
    1.5027786493301,
    1.7226468324661,
    1.8395622968674,
    1.5940405130386,
    1.694568157196,
    1.8241587877274,
    1.7037791013718,
    1.838702917099,
    1.7334734201431,
    1.4791669845581,
    1.3007366657257,
    1.7364456653595,
    1.2694935798645,
    .96595168113708,
    1.1405370235443,
    1.1328836679459,
    1.1091921329498,
    1.171138882637,
    1.1465038061142,
    1.0319484472275,
    1.055313706398,
    .93150246143341,
    1.0844472646713,
    .93333613872528,
    .93137633800507,
    1.0778160095215,
    .38748729228973,
    .77933365106583,
    .75266307592392,
    .88410103321075,
    .94100385904312,
    .91849637031555,
    .96046274900436,
    .92494148015976,
    .98310285806656,
    1.0272513628006,
    1.0762135982513,
    1.0743116140366,
    1.254854798317,
    1.1723403930664,
    1.0479376316071,
    1.3550333976746,
    1.2255589962006,
    1.2870025634766,
    1.6643482446671,
    1.3312928676605,
    1.0657893419266,
    1.1804157495499,
    1.1335761547089,
    1.137326002121,
    1.1235628128052,
    1.1115798950195,
    1.1286649703979,
    1.0989991426468,
    1.0626485347748,
    .96542054414749,
    1.0419135093689,
    .93033194541931,
    .95628559589386,
    1.027433514595,
    .98328214883804,
    1.0063992738724,
    1.0645687580109,
    .94354963302612,
    .95077443122864,
    1.0226324796677,
    1.089217543602,
    .97552293539047,
    1.0441918373108,
    1.052937746048,
    .86785578727722,
    .82579529285431,
    .95432937145233,
    .79897737503052,
    .68320548534393,
    .85365778207779,
    .78336101770401,
    .80072748661041,
    .9089440703392,
    .82500487565994,
    .98515397310257,
    .96745657920837,
    1.0962044000626,
    1.195325255394,
    1.0824474096298,
    1.2239117622375,
    1.0142554044724,
    1.0399018526077,
    .80796521902084,
    .7145761847496,
    1.0631860494614,
    .86374056339264,
    .98086261749268,
    1.0528303384781,
    .86123734712601,
    .80300676822662,
    .96200370788574,
    1.0364016294479,
    .98456978797913,
    1.1556725502014,
    1.2025715112686,
    1.0507286787033,
    1.312912106514,
    1.0682457685471,
    2.0334177017212,
    1.0775905847549,
    1.2798084020615,
    1.461397767067,
    .72960823774338,
    1.2498733997345,
    1.466894865036,
    1.286082983017,
    1.3903408050537,
    1.8483582735062,
    1.4685434103012,
    2.3107523918152,
    .7711226940155,
    -.31598940491676,
    .68151205778122,
    1.0212944746017])

y = np.array([
    np.nan,
    29.704284667969,
    29.712087631226,
    29.881610870361,
    29.820302963257,
    29.992294311523,
    29.934322357178,
    30.155170440674,
    30.200632095337,
    30.117542266846,
    30.24044418335,
    30.274082183838,
    30.319667816162,
    30.507436752319,
    30.470119476318,
    30.657470703125,
    30.68822479248,
    30.714269638062,
    30.962333679199,
    30.985248565674,
    31.204275131226,
    31.16787147522,
    31.244613647461,
    31.348531723022,
    31.523355484009,
    31.609535217285,
    31.835243225098,
    31.874824523926,
    32.144504547119,
    32.5986328125,
    32.723526000977,
    33.186702728271,
    33.156238555908,
    33.387012481689,
    33.7158203125,
    34.023887634277,
    34.458442687988,
    34.743995666504,
    35.303489685059,
    35.693740844727,
    36.102272033691,
    36.764759063721,
    37.257617950439,
    37.768424987793,
    38.405364990234,
    39.020519256592,
    39.378665924072,
    39.903781890869,
    40.408638000488,
    40.530277252197,
    41.095680236816,
    41.346523284912,
    41.637748718262,
    41.930103302002,
    42.223442077637,
    42.645172119141,
    43.174606323242,
    44.320865631104,
    44.725509643555,
    46.37532043457,
    47.584667205811,
    48.954383850098,
    50.170566558838,
    52.039329528809,
    53.291107177734,
    53.852027893066,
    54.915603637695,
    55.792385101318,
    56.6891746521,
    56.821212768555,
    57.842212677002,
    58.745475769043,
    59.5207862854,
    60.953948974609,
    61.6471824646,
    62.439296722412,
    63.615020751953,
    64.857437133789,
    66.587478637695,
    68.23265838623,
    69.616966247559,
    71.930046081543,
    74.479080200195,
    76.702774047852,
    79.722648620605,
    82.739562988281,
    84.194038391113,
    86.394561767578,
    89.024154663086,
    90.803779602051,
    93.33869934082,
    95.133476257324,
    95.879165649414,
    96.300735473633,
    99.236442565918,
    99.369491577148,
    98.865951538086,
    99.940536499023,
    100.93288421631,
    101.90919494629,
    103.27114105225,
    104.44651031494,
    105.13195037842,
    106.15531158447,
    106.63150024414,
    108.08444976807,
    108.63333129883,
    109.43137359619,
    110.9778137207,
    109.08748626709,
    110.27933502197,
    110.95265960693,
    112.28410339355,
    113.64099884033,
    114.71849822998,
    115.96046447754,
    116.9249420166,
    118.18309783936,
    119.52725219727,
    120.97621154785,
    122.27430725098,
    124.35485076904,
    125.67234039307,
    126.44793701172,
    128.85502624512,
    130.12554931641,
    131.78700256348,
    135.06434631348,
    136.03129577637,
    136.16580200195,
    137.38041687012,
    138.3335723877,
    139.43733215332,
    140.52355957031,
    141.61158752441,
    142.82865905762,
    143.8990020752,
    144.86265563965,
    145.46542358398,
    146.64192199707,
    147.2303314209,
    148.15628051758,
    149.42742919922,
    150.38327026367,
    151.50639343262,
    152.86457824707,
    153.54354858398,
    154.45077514648,
    155.72262573242,
    157.18922424316,
    157.97552490234,
    159.24418640137,
    160.45292663574,
    160.7678527832,
    161.22578430176,
    162.45433044434,
    162.79898071289,
    162.88320922852,
    164.05364990234,
    164.68334960938,
    165.50071716309,
    166.80894470215,
    167.52500915527,
    169.08515930176,
    170.26745605469,
    171.99620056152,
    173.89532470703,
    174.98243713379,
    176.82391357422,
    177.41424560547,
    178.43989562988,
    178.40797424316,
    178.41456604004,
    180.36318969727,
    180.86373901367,
    182.18086242676,
    183.65283203125,
    184.06123352051,
    184.50300598145,
    185.86199951172,
    187.33641052246,
    188.38456726074,
    190.25567626953,
    192.00257873535,
    192.85073852539,
    195.11291503906,
    195.76824951172,
    201.23341369629,
    200.47758483887,
    201.97981262207,
    204.16139221191,
    202.6296081543,
    204.82388305664,
    207.38688659668,
    208.62408447266,
    210.52333068848,
    214.34335327148,
    215.46553039551,
    220.92074584961,
    217.66012573242,
    211.85800170898,
    213.35252380371,
    215.49029541016])

resid = np.array([
    np.nan,
    -.55428558588028,
    -.36208805441856,
    -.5116091966629,
    -.28030154109001,
    -.4422954916954,
    -.18432281911373,
    -.31516996026039,
    -.39063200354576,
    -.19754208624363,
    -.26044383645058,
    -.23408082127571,
    -.10966806858778,
    -.2874368429184,
    -.09011957794428,
    -.21747054159641,
    -.20822501182556,
    -.02426831051707,
    -.21233357489109,
    -.0452471524477,
    -.25427412986755,
    -.14787164330482,
    -.12461274117231,
    -.06853157281876,
    -.14335711300373,
    -.02953593060374,
    -.18524432182312,
    .00517434487119,
    .13549427688122,
    -.14863033592701,
    .12647144496441,
    -.28670132160187,
    -.05623856931925,
    .01299012638628,
    -.01581981778145,
    .07611121237278,
    -.05844036862254,
    .15600442886353,
    -.00349225639366,
    .0062618162483,
    .19772660732269,
    .03523930162191,
    .04237993061543,
    .13157841563225,
    .09463357180357,
    -.12051809579134,
    .021334676072,
    -.00378143391572,
    -.30863979458809,
    .06972090899944,
    -.19567719101906,
    -.14652347564697,
    -.13774801790714,
    -.13010406494141,
    -.02344283089042,
    .05482704937458,
    .52539497613907,
    -.12086410820484,
    .87448859214783,
    .42467761039734,
    .51533102989197,
    .34561482071877,
    .82943379878998,
    .2606680393219,
    -.29110881686211,
    .14797207713127,
    -.01560037955642,
    .00761602073908,
    -.58917766809464,
    .17878817021847,
    .05778701230884,
    -.04547626897693,
    .47921240329742,
    -.15394935011864,
    -.0471847653389,
    .26070219278336,
    .28498136997223,
    .64256292581558,
    .51252233982086,
    .2673399746418,
    .9830310344696,
    1.0699564218521,
    .72091597318649,
    1.2972244024277,
    1.1773546934128,
    -.13956540822983,
    .50595796108246,
    .80543184280396,
    .07584273815155,
    .6962223649025,
    .06129856407642,
    -.73347336053848,
    -.87916851043701,
    1.1992633342743,
    -1.1364471912384,
    -1.4694905281067,
    -.0659501478076,
    -.14053705334663,
    -.13288362324238,
    .19080325961113,
    .02886573970318,
    -.34650835394859,
    -.03194846212864,
    -.45531520247459,
    .36850056052208,
    -.38445034623146,
    -.13333308696747,
    .46862518787384,
    -2.2778205871582,
    .41251575946808,
    -.07933671027422,
    .4473415017128,
    .4158943593502,
    .1590022444725,
    .28150060772896,
    .03953726217151,
    .27505549788475,
    .31690016388893,
    .37275013327599,
    .22378182411194,
    .82568991184235,
    .14514668285847,
    -.27233889698982,
    1.052060842514,
    .04496052488685,
    .37444713711739,
    1.6129913330078,
    -.36434525251389,
    -.93128365278244,
    .03420155867934,
    -.1804157346487,
    -.03357006236911,
    -.03733511269093,
    -.02355666831136,
    .08841699361801,
    -.02865886501968,
    -.09899909794331,
    -.36265158653259,
    .13458555936813,
    -.34191656112671,
    -.03033804148436,
    .24371138215065,
    -.02743346057832,
    .1167239844799,
    .29360374808311,
    -.26456567645073,
    -.04355576634407,
    .24922250211239,
    .37737664580345,
    -.18922370672226,
    .22447402775288,
    .15580512583256,
    -.55293774604797,
    -.36785578727722,
    .27421084046364,
    -.45432937145233,
    -.59898042678833,
    .31679451465607,
    -.1536608338356,
    .01664204336703,
    .39926943182945,
    -.10894102603197,
    .57500427961349,
    .21484296023846,
    .63253426551819,
    .7037987112999,
    .00467173522338,
    .61756485700607,
    -.4239239692688,
    -.014255377464,
    -.83988964557648,
    -.70797437429428,
    .88542991876602,
    -.36318910121918,
    .33625638484955,
    .41914650797844,
    -.4528394639492,
    -.36123737692833,
    .39699018001556,
    .43800541758537,
    .06358920782804,
    .71544241905212,
    .54432433843613,
    -.20257151126862,
    .94927132129669,
    -.41291815042496,
    3.4317541122437,
    -1.8334206342697,
    .22241242229939,
    .72019159793854,
    -2.2614006996155,
    .94440299272537,
    1.0961196422577,
    -.04889564588666,
    .50891524553299,
    1.971658706665,
    -.34635934233665,
    3.1444630622864,
    -4.0317454338074,
    -5.4861345291138,
    .81299871206284,
    1.1164767742157,
    .89470589160919])

yr = np.array([
    np.nan,
    -.55428558588028,
    -.36208805441856,
    -.5116091966629,
    -.28030154109001,
    -.4422954916954,
    -.18432281911373,
    -.31516996026039,
    -.39063200354576,
    -.19754208624363,
    -.26044383645058,
    -.23408082127571,
    -.10966806858778,
    -.2874368429184,
    -.09011957794428,
    -.21747054159641,
    -.20822501182556,
    -.02426831051707,
    -.21233357489109,
    -.0452471524477,
    -.25427412986755,
    -.14787164330482,
    -.12461274117231,
    -.06853157281876,
    -.14335711300373,
    -.02953593060374,
    -.18524432182312,
    .00517434487119,
    .13549427688122,
    -.14863033592701,
    .12647144496441,
    -.28670132160187,
    -.05623856931925,
    .01299012638628,
    -.01581981778145,
    .07611121237278,
    -.05844036862254,
    .15600442886353,
    -.00349225639366,
    .0062618162483,
    .19772660732269,
    .03523930162191,
    .04237993061543,
    .13157841563225,
    .09463357180357,
    -.12051809579134,
    .021334676072,
    -.00378143391572,
    -.30863979458809,
    .06972090899944,
    -.19567719101906,
    -.14652347564697,
    -.13774801790714,
    -.13010406494141,
    -.02344283089042,
    .05482704937458,
    .52539497613907,
    -.12086410820484,
    .87448859214783,
    .42467761039734,
    .51533102989197,
    .34561482071877,
    .82943379878998,
    .2606680393219,
    -.29110881686211,
    .14797207713127,
    -.01560037955642,
    .00761602073908,
    -.58917766809464,
    .17878817021847,
    .05778701230884,
    -.04547626897693,
    .47921240329742,
    -.15394935011864,
    -.0471847653389,
    .26070219278336,
    .28498136997223,
    .64256292581558,
    .51252233982086,
    .2673399746418,
    .9830310344696,
    1.0699564218521,
    .72091597318649,
    1.2972244024277,
    1.1773546934128,
    -.13956540822983,
    .50595796108246,
    .80543184280396,
    .07584273815155,
    .6962223649025,
    .06129856407642,
    -.73347336053848,
    -.87916851043701,
    1.1992633342743,
    -1.1364471912384,
    -1.4694905281067,
    -.0659501478076,
    -.14053705334663,
    -.13288362324238,
    .19080325961113,
    .02886573970318,
    -.34650835394859,
    -.03194846212864,
    -.45531520247459,
    .36850056052208,
    -.38445034623146,
    -.13333308696747,
    .46862518787384,
    -2.2778205871582,
    .41251575946808,
    -.07933671027422,
    .4473415017128,
    .4158943593502,
    .1590022444725,
    .28150060772896,
    .03953726217151,
    .27505549788475,
    .31690016388893,
    .37275013327599,
    .22378182411194,
    .82568991184235,
    .14514668285847,
    -.27233889698982,
    1.052060842514,
    .04496052488685,
    .37444713711739,
    1.6129913330078,
    -.36434525251389,
    -.93128365278244,
    .03420155867934,
    -.1804157346487,
    -.03357006236911,
    -.03733511269093,
    -.02355666831136,
    .08841699361801,
    -.02865886501968,
    -.09899909794331,
    -.36265158653259,
    .13458555936813,
    -.34191656112671,
    -.03033804148436,
    .24371138215065,
    -.02743346057832,
    .1167239844799,
    .29360374808311,
    -.26456567645073,
    -.04355576634407,
    .24922250211239,
    .37737664580345,
    -.18922370672226,
    .22447402775288,
    .15580512583256,
    -.55293774604797,
    -.36785578727722,
    .27421084046364,
    -.45432937145233,
    -.59898042678833,
    .31679451465607,
    -.1536608338356,
    .01664204336703,
    .39926943182945,
    -.10894102603197,
    .57500427961349,
    .21484296023846,
    .63253426551819,
    .7037987112999,
    .00467173522338,
    .61756485700607,
    -.4239239692688,
    -.014255377464,
    -.83988964557648,
    -.70797437429428,
    .88542991876602,
    -.36318910121918,
    .33625638484955,
    .41914650797844,
    -.4528394639492,
    -.36123737692833,
    .39699018001556,
    .43800541758537,
    .06358920782804,
    .71544241905212,
    .54432433843613,
    -.20257151126862,
    .94927132129669,
    -.41291815042496,
    3.4317541122437,
    -1.8334206342697,
    .22241242229939,
    .72019159793854,
    -2.2614006996155,
    .94440299272537,
    1.0961196422577,
    -.04889564588666,
    .50891524553299,
    1.971658706665,
    -.34635934233665,
    3.1444630622864,
    -4.0317454338074,
    -5.4861345291138,
    .81299871206284,
    1.1164767742157,
    .89470589160919])

mse = np.array([
    1.1115040779114,
    .69814515113831,
    .63478744029999,
    .63409090042114,
    .63356643915176,
    .63317084312439,
    .63287192583084,
    .63264590501785,
    .63247483968735,
    .63234525918961,
    .63224703073502,
    .63217264413834,
    .63211619853973,
    .63207340240479,
    .63204091787338,
    .63201630115509,
    .63199764490128,
    .63198345899582,
    .63197267055511,
    .63196450471878,
    .63195830583572,
    .63195365667343,
    .63195008039474,
    .63194733858109,
    .63194531202316,
    .6319437623024,
    .6319425702095,
    .63194167613983,
    .63194096088409,
    .63194048404694,
    .63194006681442,
    .6319397687912,
    .63193953037262,
    .63193941116333,
    .6319392323494,
    .63193917274475,
    .63193905353546,
    .63193899393082,
    .63193899393082,
    .63193893432617,
    .63193893432617,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193887472153,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688,
    .63193881511688])

stdp = np.array([
    .72428566217422,
    .72428566217422,
    .56208884716034,
    .53160965442657,
    .45030161738396,
    .45229381322861,
    .38432359695435,
    .40517011284828,
    .36063131690025,
    .30754271149635,
    .32044330239296,
    .29408219456673,
    .27966624498367,
    .29743707180023,
    .25011941790581,
    .27747189998627,
    .24822402000427,
    .23426930606365,
    .27233305573463,
    .23524768650532,
    .26427435874939,
    .21787133812904,
    .22461311519146,
    .22853142023087,
    .24335558712482,
    .22953669726849,
    .25524401664734,
    .22482520341873,
    .26450532674789,
    .31863233447075,
    .27352628111839,
    .33670437335968,
    .25623551011086,
    .28701293468475,
    .315819054842,
    .3238864839077,
    .35844340920448,
    .34399557113647,
    .40348997712135,
    .39373970031738,
    .4022718667984,
    .46476069092751,
    .45762005448341,
    .46842387318611,
    .50536489486694,
    .52051961421967,
    .47866532206535,
    .50378143787384,
    .50863671302795,
    .4302790760994,
    .49568024277687,
    .44652271270752,
    .43774726986885,
    .43010330200195,
    .42344436049461,
    .44517293572426,
    .47460499405861,
    .62086409330368,
    .52550911903381,
    .77532315254211,
    .78466820716858,
    .85438597202301,
    .87056696414948,
    1.0393311977386,
    .99110960960388,
    .85202795267105,
    .91560190916061,
    .89238166809082,
    .88917690515518,
    .72121334075928,
    .84221452474594,
    .8454754948616,
    .82078683376312,
    .95394861698151,
    .84718400239944,
    .839300096035,
    .91501939296722,
    .95743554830551,
    1.0874761343002,
    1.1326615810394,
    1.1169674396515,
    1.3300451040268,
    1.4790810346603,
    1.5027786493301,
    1.7226468324661,
    1.8395622968674,
    1.5940405130386,
    1.694568157196,
    1.8241587877274,
    1.7037791013718,
    1.838702917099,
    1.7334734201431,
    1.4791669845581,
    1.3007366657257,
    1.7364456653595,
    1.2694935798645,
    .96595168113708,
    1.1405370235443,
    1.1328836679459,
    1.1091921329498,
    1.171138882637,
    1.1465038061142,
    1.0319484472275,
    1.055313706398,
    .93150246143341,
    1.0844472646713,
    .93333613872528,
    .93137633800507,
    1.0778160095215,
    .38748729228973,
    .77933365106583,
    .75266307592392,
    .88410103321075,
    .94100385904312,
    .91849637031555,
    .96046274900436,
    .92494148015976,
    .98310285806656,
    1.0272513628006,
    1.0762135982513,
    1.0743116140366,
    1.254854798317,
    1.1723403930664,
    1.0479376316071,
    1.3550333976746,
    1.2255589962006,
    1.2870025634766,
    1.6643482446671,
    1.3312928676605,
    1.0657893419266,
    1.1804157495499,
    1.1335761547089,
    1.137326002121,
    1.1235628128052,
    1.1115798950195,
    1.1286649703979,
    1.0989991426468,
    1.0626485347748,
    .96542054414749,
    1.0419135093689,
    .93033194541931,
    .95628559589386,
    1.027433514595,
    .98328214883804,
    1.0063992738724,
    1.0645687580109,
    .94354963302612,
    .95077443122864,
    1.0226324796677,
    1.089217543602,
    .97552293539047,
    1.0441918373108,
    1.052937746048,
    .86785578727722,
    .82579529285431,
    .95432937145233,
    .79897737503052,
    .68320548534393,
    .85365778207779,
    .78336101770401,
    .80072748661041,
    .9089440703392,
    .82500487565994,
    .98515397310257,
    .96745657920837,
    1.0962044000626,
    1.195325255394,
    1.0824474096298,
    1.2239117622375,
    1.0142554044724,
    1.0399018526077,
    .80796521902084,
    .7145761847496,
    1.0631860494614,
    .86374056339264,
    .98086261749268,
    1.0528303384781,
    .86123734712601,
    .80300676822662,
    .96200370788574,
    1.0364016294479,
    .98456978797913,
    1.1556725502014,
    1.2025715112686,
    1.0507286787033,
    1.312912106514,
    1.0682457685471,
    2.0334177017212,
    1.0775905847549,
    1.2798084020615,
    1.461397767067,
    .72960823774338,
    1.2498733997345,
    1.466894865036,
    1.286082983017,
    1.3903408050537,
    1.8483582735062,
    1.4685434103012,
    2.3107523918152,
    .7711226940155,
    -.31598940491676,
    .68151205778122,
    1.0212944746017])

icstats = np.array([
    202,
    np.nan,
    -240.29558272688,
    5,
    490.59116545376,
    507.13250394077])


results = Bunch(
    llf=llf,
    nobs=nobs,
    k=k,
    k_exog=k_exog,
    sigma=sigma,
    chi2=chi2,
    df_model=df_model,
    k_ar=k_ar,
    k_ma=k_ma,
    params=params,
    cov_params=cov_params,
    xb=xb,
    y=y,
    resid=resid,
    yr=yr,
    mse=mse,
    stdp=stdp,
    icstats=icstats
)
