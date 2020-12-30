from EquationsSolver import *
import random
import time

show_steps = False
round_int = False


def test():
    gv.show_steps = show_steps
    gv.ROUND_INT = round_int
    if round_int:
        gv.MAX_DIGITS_IN_RATIONAL = gv.MAX_DIGITS_IN_FLOAT

    #test_general()
    #test_operator()
    #test_periodic()
    #test_fraction(20)
    test_random(30)
    #test_inf_and_no_solution()


def test_general():
    n = 73040216269692243
    n = 1000000000000002
    d = 3
    f = n/d
    r = Rational(f'{n}/{d}')

    an = 2028894896373277
    ad = 2028894896380340
    bn = 1697436535000049692318274597285957858394
    bd = 1
    a_mulb_n = 1721960161389570098983065643479711969108893924265868569
    a_mulb_d = 1014447448190170

    d = a_mulb_n * 2
    xn = div_large_number(d, an)
    y = xn - bn
    dif = a_mulb_n/a_mulb_d
    xrow = -5909125341137372427087358343 - dif
    xrow_n = -1721960161395564596106418318721920399967470985865956879
    xrow_d = 1014447448190170


    rx = [
        [1, '1/1269889185279', 1, 1],
        [0, '1/7503934365168430814652764318422482617976', '1/1697436535000049692318274597285957858394', 1],
        [0, 1, 0, 0],
    ]
    n = len(rx)
    for row in range(n):
        for col in range(n+1):
            rx[row][col] = Rational(rx[row][col])
    if not show_steps:
        print_matrix(rx)
    origin_m = copy_matrix(rx)
    tx = solve_matrix(rx)
#    print(get_solution_string(tx, spaces=2))
    result_r = check_result(origin_m, tx)
    if gv.err is not None:
        print_exception('while solving - ' + gv.err)
        gv.err = None
    dev_r = print_result(result_r)

def test_fix_fraction():
    r2 = [
        [1, '1000/1001', '500/501', '1000/1003', '250/251', '200/201', '500/503', '1000/1007', '125/126', '1000/1009', '100/101', 50000000],
        [0, '1/1004005002', '1/503005503', '3/1008019012', '1/252507255', '1/202408206', '3/507027521', '1/145153008', '1/127261134', '9/1020109090', '1/102213111', '50000/1001'],
        [0, '1/503005503', '1/252005004', '1/168338505', '1/126505506', '1/101405907', '1/84673008', '7/509047563', '1/63757260', '1/56785511', '1/51208212', '10070000/501'],
        [0, '3/1008019012', '1/168338505', '9/1012045054', '3/253515271', '1/67738608', '9/509049581', '21/1020121210', '1/42589386', '27/1024171324', '3/102619939', '60330000/1003'],
        [0, '1/252507255', '1/126505506', '3/253515271', '1/63505008', '1/50905059', '3/127515530', '7/255537327', '1/32005512', '9/256551367', '1/25705914', '30170000/251'],
        [0, '1/202408206', '1/101405907', '1/67738608', '1/50905059', '1/40805010', '1/34071711', '7/204835884', '1/25655238', '1/22849814', '1/20605515', '40250000/201'],
        [0, '3/507027521', '1/84673008', '9/509049581', '3/127515530', '1/34071711', '9/256045108', '21/513105773', '1/21421764', '27/515139905', '3/51615848', '151050000/503'],
        [0, '1/145153008', '7/509047563', '21/1020121210', '7/255537327', '7/204835884', '21/513105773', '49/1028245686', '1/18397890', '63/1032320008', '7/103436019', '423290000/1007'],
        [0, '1/127261134', '1/63757260', '1/42589386', '1/32005512', '1/25655238', '1/21421764', '1/18397890', '1/16130016', '1/14366142', '1/12955068', '35305000/63'],
        [0, '9/1020109090', '1/56785511', '27/1024171324', '9/256551367', '1/22849814', '27/515139905', '63/1032320008', '1/14366142', '81/1036406458', '9/103845271', '726930000/1009'],
        [0, '1/102213111', '1/51208212', '3/102619939', '1/25705914', '1/20605515', '3/51615848', '7/103436019', '1/12955068', '9/103845271', '1/10405020', '90950000/101']
    ]
    r10 = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, '-2015498994722580378200/2225379264147034747271', -1059482316800582523596158310900000000],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, '201549899472258037820/22033458060861730171', 9628575295371910330687215723541800000],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, '-388703377553640501510/9349508910098597669', -38890501020614999595717449523453600000],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, '70313952322824311106555082750110316/627957818971399379338812755078689', 91629972194921550904051263087700800000],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, '-7219654789126920/36480336300421', -138784756948416185522842156160700000000],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '51774416814456/215859978109', 140136238783931822931758204687742000000],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, '-1502574285660/7443447521', -94332995758059604782638845061018400000],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, '6827943360/58609823', 40821317698248956647753312799260800000],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, '-22884120/518671', -10304406052959811256865182295914400000],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, '10090/1019', 1156038124376942867411031414233500000],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '1/103295242781510194071508514765363091168402885429180', '459499550000/318229234773025968859753']
    ]
    r9 = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, '3995042605991239600/4329156011275660409', '17977691726960578200/2183885440772359909', 7335683984561072035071676500000000],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, '-179776917269605782/21452705705033005', '-161239919577806430256/2183885440772359909', -59198969757978661239983792037600000],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, '205459334022406608/6074726565979643', '906974547625161170190/3092035822083638287', 209007501987149782290428641322400000],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, '-1435344648859128/18025894854539', '-416881140253899501786421890905356/616249086331108321235341270931', -421665135236603170520178619591200000],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, '8586308966256/71248596263', '36098273945634600/36265535497867', 531679210287780464395579145052000000],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, '-8552100564/70334251', '-34516277876304/35800133759', -429049890139011276480665695452000000],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, '170191056/2080895', '128792081628/211835111', 216392444598986187281031933050400000],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, '-507528/14351', '-1706985840/7304659', -62364079242581197092757272727200000],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, '1008/113', '2542680/57517', 7863233517696799332336868221600000],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, '1/9753631317146739901853053481889538990811351050', '1/985029763347128638254535331818180399567568555', '73374490000/619069309612419438487'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, '1/985029763347128638254535331818180399567568555', '1/99479124101839527940194705661482943955332380', '28227950000/24022739848495958999']
    ]
    r8 = [
        [1, 0, 0, 0, 0, 0, 0, 0, '-35670023267778925/38009452820063634', '-285360186142231400/38311115144032393', '-142680093071115700/4290541141006601', -43578323265920398490061670000000],
        [0, 1, 0, 0, 0, 0, 0, 0, '11414407445689256/1508311619843795', '11325945787985164266/191555575720161965', '1118611929677547088/4290541141006601', 307401492338205744258064565280000],
        [0, 0, 1, 0, 0, 0, 0, 0, '-5707203722844628/213764679521965', '-5547402018604978416/27148114299289555', '-544184728575096702114/613547383163943943', -929311270086996685445601028320000],
        [0, 0, 0, 1, 0, 0, 0, 0, '68349745183768/1269889185279', '21530169732886920/53758642176811', '10344733933563286800/6074726565979643', 1560775721099717235575841036000000],
        [0, 0, 0, 0, 1, 0, 0, 0, '-85181636570/1256072389', '-77276780696304/159521193403', '-36098273945634600/18025894854539', -1572778717999220949719658156000000],
        [0, 0, 0, 0, 0, 1, 0, 0, '271495256/4964713', '230906715228/630518551', '103548833628912/71248596263', 950916931784772578650949047200000],
        [0, 0, 0, 0, 0, 0, 1, 0, '-2026084/73515', '-510573168/3112135', '-42930693876/70334251', -319404934703562817021679326560000],
        [0, 0, 0, 0, 0, 0, 0, 1, '8056/1015', '652536/18415', '48771024/416179', 45979100833005292765693177440000],
        [0, 0, 0, 0, 0, 0, 0, 0, '1/750393436516843081465276431842248261797600', '1/84121486434923877188071663490252037284850', '1/16974365350000496923182745972859578583940', '15319000/1461902031540909'],
        [0, 0, 0, 0, 0, 0, 0, 0, '1/84121486434923877188071663490252037284850', '81/763852401687425789165404767944986999045450', '9/17125889099694501421397766431110461247415', '512749674000/5478489465596632199'],
        [0, 0, 0, 0, 0, 0, 0, 0, '1/16974365350000496923182745972859578583940', '9/17125889099694501421397766431110461247415', '1/383969199215069912267571553535314993980', '21918590000/47195952551072611']
    ]
    r8_4 = [
        [1, '68349745183768/1269889185279', '21530169732886920/53758642176811', '10344733933563286800/6074726565979643', 1560775721099717235575841036000000],
        [0, '1/750393436516843081465276431842248261797600', '1/84121486434923877188071663490252037284850', '1/16974365350000496923182745972859578583940', '15319000/1461902031540909'],
        [0, '1/84121486434923877188071663490252037284850', '81/763852401687425789165404767944986999045450', '9/17125889099694501421397766431110461247415', '512749674000/5478489465596632199'],
        [0, '1/16974365350000496923182745972859578583940', '9/17125889099694501421397766431110461247415', '1/383969199215069912267571553535314993980', '21918590000/47195952551072611']
    ]
    r8_4_1 = [
        [1, 0, '-1435344648859128/18025894854539', '-416881140253899501786421890905356/616249086331108321235341270931', -421665135236603170520178619591200000],
        [0, 1, '1008/113', '2542680/57517', 7863233517696799332336868221600000],
        [0, 0, '1/9753631317146739901853053481889538990811351050', '1/985029763347128638254535331818180399567568555', '73374490000/619069309612419438487'],
        [0, 0, '1/985029763347128638254535331818180399567568555', '1/99479124101839527940194705661482943955332380', '28227950000/24022739848495958999']
    ]
    r8_4_3 = [
        [1, '68349745183768/1269889185279', '101', '10344733933563286800/6074726565979643', 1000],
        [0, '1/750393436516843081465276431842248261797600', '102', '1/16974365350000496923182745972859578583940', 1000],
        [0, '101', '103', '9/17125889099694501421397766431110461247415', 1000],
        [0, '102', '104', '1/383969199215069912267571553535314993980', 1000]
    ]
    exp_10 = 10 ** 20
    r8_4_31 = [
        [1, '68349745183768/1269889185279', '10344733933563286800/6074726565979643', f'1/{exp_10}'],
        [0, '1/750393436516843081465276431842248261797600', '1/16974365350000496923182745972859578583940', f'1/{exp_10}'],
        [0, '101', '10', 1000],
    ]
    rx = r8_4_31
    n = len(rx)
    for row in range(n):
        for col in range(n+1):
            rx[row][col] = Rational(rx[row][col])
    if not show_steps:
        print_matrix(rx)
    origin_m = copy_matrix(rx)
    tx = solve_matrix(rx)
    print('reference:')
    print('x[1] = 134024509400515147106969351775700000000  x[2] = -1354719741049516958938024436151118200000  x[3] = 6162011262427009286855834658572216400000  x[4] = -1684909501239406368006319736354660281108268736890400000/101444744819017  x[5] = 29378943851943729109139207271397260000000  x[6] = -35633939629044715980399697715085690000000  x[7] = 30014031022356432534837118832028561600000  x[8] = -17334979785627126796748255661880099200000  x[9] = 6570327317661752381346315475815645600000  x[10] = -1475714132674030687659493269722796500000  x[11] = 149150713978550780525957926943373000000')
    print('\nresult:\n' + get_solution_string(tx, spaces=2))
    result_r = check_result(origin_m, tx)
    if gv.err is not None:
        print_exception('while solving - ' + gv.err)
        gv.err = None
    dev_r = print_result(result_r)


def test_periodic():
    min_n = 2
    max_n = 1000
    dif = max_n - min_n
    float_count = 0
    for i in range(min_n, max_n):
        f = 3/i
        r = Rational(f)
        if type(r.numerator) is float:
            float_count += 1
            print(f'1/{i}   {r}')
    print(f'\n{dif-float_count}/{dif} = {1-(float_count/(max_n-min_n))}')


def test_operator():
    print_each_result = False
    precision = 10 ** -9
    inf = float('inf')
    big_f = 10 ** (gv.MAX_DIGITS_IN_FLOAT + 10)
    big_i = 10 ** (gv.MAX_DIGITS_IN_RATIONAL + 10)
    gv.ROUND_INT = False
    s_fail = '\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n' \
             '                     fail     fail     fail     fail     fail    fail     fail\n' \
             'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    m_no_zero = [(inf, inf), (3, inf), (inf, 5), (1/53, 3/911), (big_f, 3), (3, big_f), (big_i, 7), (7, big_i)]
    m_with_zero = [(0, inf), (inf, 0), (0, 11), (11, 0)]
    for pair in m_no_zero:
        f1 = pair[0]
        f2 = pair[1]
        try:
            f1 = float(f1)
        except OverflowError:
            f1 = float('inf')
        try:
            f2 = float(f2)
        except OverflowError:
            f2 = float('inf')
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            test_all_operators(f1, f2, True, precision)
            print(s_fail)
            return
        f1 = -f1
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            test_all_operators(f1, f2, True, precision)
            print(s_fail)
            return
        f1 = -f1
        f2 = -f2
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            test_all_operators(f1, f2, True, precision)
            print(s_fail)
            return
        f1 = -f1
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            test_all_operators(f1, f2, True, precision)
            print(s_fail)
            return
    for pair in m_with_zero:
        f1 = pair[0]
        f2 = pair[1]
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            test_all_operators(f1, f2, True, precision)
            print(s_fail)
            return
        if f1 == 0:
            f2 = -f2
        else:
            f1 = -f1
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            print(s_fail)
            test_all_operators(f1, f2, True, precision)
            return
    f1 = 0
    f2 = 0
    success = test_all_operators(f1, f2, print_each_result, precision)
    if not success:
        print(s_fail)
        test_all_operators(f1, f2, True, precision)
        return
    print('\nSUCCESS')


def test_all_operators(f1, f2, show_result=False, precision=0):
    r1 = Rational(f1)
    r2 = Rational(f2)
    gt = r1 > r2
    ge = r1 >= r2
    lt = r1 < r2
    le = r1 <= r2
    eq = r1 == r2
    f_plus = f1+f2
    r_plus = r1+r2
    f_minus = f1-f2
    r_minus = r1-r2
    f_mul = f1*f2
    r_mul = r1*r2
    try:
        f_div = f1/f2
    except ZeroDivisionError:
        f_div = float('nan')
    r_div = r1/r2
    t_plus = f_plus == float(r_plus) or (str(f_plus).lower() == 'nan' and not r_plus.is_valid()) or abs(f_plus - float(r_plus)) < precision
    t_minus = f_minus == float(r_minus) or (str(f_minus).lower() == 'nan' and not r_minus.is_valid()) or abs(f_minus - float(r_minus)) < precision
    t_mul = f_mul == float(r_mul) or (str(f_mul).lower() == 'nan' and not r_mul.is_valid()) or abs(f_mul - float(r_mul)) < precision
    t_div = (f_div == float(r_div)) or (str(f_div).lower() == 'nan' and not r_div.is_valid()) or abs(f_div - float(r_div)) < precision
    t_eq = eq == (f1 == f2)
    t_gt = gt == (f1 > f2)
    t_ge = ge == (f1 >= f2)
    t_lt = lt == (f1 < f2)
    t_le = le == (f1 <= f2)
    if show_result:
        print('')
        print(f'r1: {r1}   r2: {r2}')
        print(f'+   float: {f_plus}   rational: {r_plus}   | {t_plus}')
        print(f'-   float: {f_minus}   rational: {r_minus}   | {t_minus}')
        print(f'*   float: {f_mul}   rational: {r_mul}   | {t_mul}')
        print(f'/   float: {f_div}   rational: {r_div}   | {t_div}')
        print(f'r1 == r2: {eq}   | {t_eq}')
        print(f'r1 > r2: {gt}   | {t_gt}')
        print(f'r1 >= r2: {ge}   | {t_ge}')
        print(f'r1 < r2: {lt}   | {t_lt}')
        print(f'r1 <= r2: {le}   | {t_le}')
        if gv.err is not None:
            print(f'{r1}   {r2}   err: {gv.err}')
            gv.err = None
    if gv.numerator_converted_to_float:
        print(f'{r1}   {r2}   rational_converted_to_float')
        gv.numerator_converted_to_float = False

    return t_plus and t_minus and t_mul and t_div and t_eq and t_gt and t_ge and t_lt and t_le


def test_fraction(n=11):
    gv.MATRIX_SIZE = n
    rx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n):
            r = Rational(f'1/{row+1000+col}')
            #r = Rational(f'{row}/{(col + 1) ** 2}') ** 7 - (row * col - 11) ** 6
            #r = Rational((row + col) ** 15 - (row - col - 11) ** 6)
            cr.append(r)
        #r = Rational(row+1)
        r = Rational((row ** 2 - row + 5) * 10000)
        cr.append(r)
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    #test_n_vs_n_minus_one_steps(rx)
    test_double_vs_random_matrix(rx)


def test_random(n=10):
    gv.MATRIX_SIZE = n
    rx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n+1):
            rnd = random.randint(0, 10000)
            cr.append(Rational(rnd))
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_random_matrix(rx)


def test_inf_and_no_solution():
    n = 2
    gv.MATRIX_SIZE = n
    print('\nTest - no solution')
    rx = [
        [1, 1, 1],
        [1, 1, 2]
    ]
    convert_matrix_to_rational(rx)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_random_matrix(rx)
    print('\nTest - infinite solution')
    rx = [
        [1, 1, 1],
        [0, 0, 0]
    ]
    convert_matrix_to_rational(rx)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_random_matrix(rx)


def test_n_vs_n_minus_one_steps(rx):
    gv.MATRIX_SIZE = len(rx)
    r1 = copy_matrix(rx)
    for row in range(len(rx)):
        r1[row][-2] = rx[row][-1]
        r1[row].pop(-1)
    r1.pop(-1)
    gv.MATRIX_SIZE -= 1
    r1 = solve_matrix(r1, True)
    r1_steps = gv.step_by_step_matrix
    gv.step_by_step_matrix = []
    gv.MATRIX_SIZE += 1
    rx = solve_matrix(rx, True)
    rx_steps = gv.step_by_step_matrix
    for i in range(len(r1_steps)):
        m1 = r1_steps[i]
        m2 = rx_steps[i]
        print(f'{i}:')
        print_matrix(m1)
        print_matrix(m2)
        if not is_step_matrices_equal(m1, m2):
            print('fail')
    print('success')


def test_double_vs_random_matrix(rx):
    dx = copy_matrix(rx)
    convert_matrix_to_float(dx)
    td = copy_matrix(dx)
    tr = copy_matrix(rx)
    if gv.err is not None:
        if gv.ROUND_INT:
            gv.err += ' -> change ROUND_INT to False'
        print_exception(gv.err, gv.exception_type_notice)
        gv.err = None
        return
    if gv.numerator_converted_to_float:
        print_exception('before solving - rational converted to float', gv.exception_type_notice)
        gv.is_rational_converted_to_float = False
    start_time = time.perf_counter()
    td = solve_matrix(td)
    end_time = time.perf_counter()
    time_d = end_time - start_time
    print('double:\n' + get_solution_string(td, spaces=2))
    result_d = check_result(dx, td)
    dev_d = print_result(result_d)
    print(f'time: {time_d} sec')
    print('\nfraction:')
    start_time = time.perf_counter()
    tr = solve_matrix(tr, False)
    end_time = time.perf_counter()
    time_r = end_time - start_time
    if gv.err is not None:
        print_exception(gv.err)
        gv.err = None
    max_digits = gv.rational_largest_digits
    if gv.numerator_converted_to_float:
        print_exception('while solving - rational converted to float', gv.exception_type_notice)
        gv.is_rational_converted_to_float = False
    print(get_solution_string(tr, spaces=2))
    result_r = check_result(rx, tr)
    if gv.err is not None:
        print_exception('while solving - ' + gv.err)
        gv.err = None
    dev_r = print_result(result_r)
    print(f'time: {time_r} sec')
    r_d_dev = 'inf'
    if dev_r == 0:
        if dev_d == 0:
            r_d_dev = '0'
        else:
            r_d_dev = 'inf'
    elif dev_d is not gv.no_solution and dev_d != 0:
        r_d_dev = float(dev_r / dev_d)
    print(f'\nr_deviation / d_deviation: {r_d_dev}')
    print(f'r_time / d_time: {time_r / time_d}')
    print(f'max rational digits: {max_digits}\n')


def print_exception(msg=gv.unknown_exception, ex_type=gv.exception_type_warning):
    line = 'oooooooooooooooooooooooooooooooooo'
    if ex_type == gv.exception_type_warning:
        print('\n')
        line = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    elif ex_type == gv.exception_type_notice:
        line = '---------------------------------------------'
    print(line)
    print(msg)
    print(line)
    if ex_type == gv.exception_type_warning:
        print('\n')


def check_result(x, r):
    n = len(r)
    result = []
    max_digits = 0
    if r[0][0] == Rational(gv.invalid_rational):
        return [gv.no_solution]
    for row in range(n):
        if r[row][row] == Rational(gv.inf_rational):
            r[row][row] = 0

    for row in range(0, n):
        result_row = x[row][0] * r[0][0]
        for col in range(1, n):
            f1 = x[row][col]
            f2 = r[col][col]
            add = f1 * f2
            result_row += add
        result_row -= x[row][-1]
        result.append(abs(result_row))
    result.append(max_digits)
    return result


def print_result(r):
    dev = r[0]
    if dev is gv.no_solution:
        return dev
    dev_vector = f'{r[0]}   '
    for i in range(1, len(r) - 1):
        dev += r[i]
        dev_vector += f'{r[i]}   '
    print('row deviation: ' + dev_vector)
    dev /= len(r)
    print(f'average deviation: {float(dev)}')
    return dev


def convert_matrix_to_float(x):
    n = len(x)
    for row in range(n):
        for col in range(n+1):
            if x[row][col].denominator != 0:
                x[row][col] = x[row][col].numerator / x[row][col].denominator


def convert_matrix_to_rational(x):
    n = len(x)
    for row in range(n):
        for col in range(n+1):
            x[row][col] = Rational(x[row][col])


def get_none_matrix(n):
    m = []
    row_m = []
    for col in range(n + 1):
        row_m.append(None)
    for row in range(n):
        m.append(row_m)
    return m


def is_step_matrices_equal(m1, m2):
    n = len(m1)
    for row in range(n):
        for col in range(n):
            if m1[row][col] != m2[row][col]:
                return False
        if m1[row][-1] != m2[row][-1]:
            return False
    return True

