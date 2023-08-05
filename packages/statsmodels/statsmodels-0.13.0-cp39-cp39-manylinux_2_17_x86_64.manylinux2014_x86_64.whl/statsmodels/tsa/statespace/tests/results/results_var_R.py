"""
Results for VARMAX tests

Results from R using script `test_var.R`.
See also the packages "vars" and "MTS"

Data from:

https://www.stata-press.com/data/r14/lutkepohl2.dta

Author: Chad Fulton
License: Simplified-BSD
"""

res_basic = {
    'llf': 596.164145004717,
    'params': [-0.29883655890699, 0.0628044611244012, 0.659886869389918,
               -0.148082523252922, 0.0344024216201084, 0.626435414218001,
               0.0243232147401712, -0.0743006500599362, 0.572632299564782,
               0.0382739144340661, 0.0947818948355414, 0.280177703027101,
               -0.0184971989547667, 0.289109890254681, -0.0310399835571299,
               0.0242429009692667, 0.416904807490799, 0.215822310109252,
               0.0441917021237108, 0.000878653005437675, 0.0121587857077158,
               0.00204049993421116, 0.0060703628735368, 0.00748745583771755]
}

res_c = {
    'llf': 606.307040676657,
    'params': [-0.016722145613102, 0.0157671932107926, 0.0129257858993457,
               -0.319631834481441, 0.145985129742841, 0.961228756482211,
               -0.160550841116343, 0.114600859415788, 0.934400111915348,
               0.0439309334767638, -0.152731116093091, 0.288499158625839,
               0.0500302034483248, 0.0191633532210331, -0.0102000393418508,
               -0.0024229889812185, 0.224813385583416, -0.263969465525517,
               0.0338805880793048, 0.35491349008493, -0.0222264331018897,
               0.0438795670052806, 0.00147561682483683, 0.0110449368419315,
               0.00253927594913203, 0.00469160198527878, 0.00722432245241668]
}

res_ct = {
    'llf': 607.438331754865,
    'params': [
        -0.0091687448890928, -0.000202696805258128, 0.0164700664012876,
        -0.0000188617227419232, 0.0116594765736253, 0.0000339816281660043,
        -0.33053195210291, 0.0991441034301294, 1.02497527768337,
        -0.168768113189076, 0.052065599978203, 1.01832964242176,
        0.0429166353176552, -0.157089854999372, 0.294431019303797,
        0.0492655544577624, 0.0133442051412007, -0.00239007148243754,
        -0.00059561067840422, 0.232666170125558, -0.274656415315255,
        0.0352581938277472, 0.365397374775498, -0.0362970154881497,
        0.043680752565187, 0.00144524803260901, 0.0110421281684084,
        0.00261764677471134, 0.00471411575165134, 0.00714742282804776]
}

res_ct_as_exog0 = {
    'llf': 607.438331754865,
    'params': [
        -0.33053195210291, 0.0991441034301291, 1.02497527768337,
        -0.168768113189076, 0.0520655999782025, 1.01832964242176,
        0.0429166353176552, -0.157089854999372, 0.294431019303796,
        0.0492655544577624, 0.0133442051412007, -0.00239007148243758,
        -0.000595610678404244, 0.232666170125558, -0.274656415315255,
        0.0352581938277472, 0.365397374775498, -0.0362970154881497,
        -0.00937144169435092, -0.000202696805258128, 0.0164512046785456,
        -0.0000188617227419232, 0.0116934582017913, 0.0000339816281660044,
        0.043680752565187, 0.00144524803260901, 0.0110421281684084,
        0.00261764677471134, 0.00471411575165134, 0.00714742282804776]

}

res_ctt_as_exog1 = {
    'llf': 609.490393107865,
    'params': [
        -0.337732421246314, 0.131516202959048, 1.02963148737009,
        -0.17420176313584, 0.0790611026384549, 1.0252507470967,
        0.0465815476938576, -0.173566685306448, 0.29206109032178,
        0.0520311868827124, -0.000396031756002358, -0.00591279224896053,
        0.00084626300027174, 0.226183748313225, -0.275588808199104,
        0.0363462669353941, 0.359991601352511, -0.0376829472183479,
        0.00135916831998363, -0.00105584065752325, 0.0000109426769125814,
        0.0111115434152017, 0.00041537351951475, -0.00000556963042921238,
        0.00955129158661523, 0.000204821283222681, -0.00000219124025119403,
        0.0434681194741622, 0.00166930018759676, 0.0107902800396133,
        0.00271581816352387, 0.00457956681075423, 0.00714628937734587]
}

res_ct_exog = {
    'llf': 608.068437908288,
    'params': [
        -0.00891774296871338, -0.000177588386858893, 0.0197390895235663,
        0.000308147728766951, 0.0126534322433763, 0.000133409771140667,
        -0.330531447689365, 0.0984883875114303, 1.02556206489488,
        -0.168762569285516, 0.0515915213025295, 1.01893167456814,
        0.0429232047476493, -0.165629831492911, 0.302073275424366,
        0.0493377576859194, 0.00716985336647014, 0.00545073309741857,
        -0.000593613224747432, 0.230069566266306, -0.272332765858951,
        0.035280147422236, 0.363520045761914, -0.0339129968146675,
        -0.00000107342140085188, -0.0000139801296102807,
        -0.00000425069770699759, 0.0436806162945145, 0.00144170298545239,
        0.0109507769345455, 0.00261657568854817, 0.0046983621886579,
        0.00714512825214436]
}

res_c_2exog = {
    'llf': 609.051601848607,
    'params': [
        -0.0183154996756286, 0.0153812380370316, 0.0103369264061738,
        -0.337960592073415, 0.0503833175581312, 0.869221695835652,
        -0.177121478778926, -0.00828627855953333, 0.833693547676962,
        0.0408338136200346, -0.168937622492442, 0.271586426539891,
        0.0472115548647617, -0.00167581111974649, -0.0288652616238083,
        -0.00180977814169972, 0.226832537597882, -0.291808329427557,
        0.0340137235903244, 0.357345372917494, -0.0561689416451492,
        -0.0000711052323565154, 0.000226083635596117, -0.0000123876692635146,
        0.0000396928767974614, -0.00000605563782898125, 0.0000261698003981677,
        0.0430020095866888, 0.00119895869898935, 0.0109748059062083,
        0.00248803192377248, 0.00471772840157074, 0.00714511199868448]
}
