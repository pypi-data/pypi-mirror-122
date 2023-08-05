from .bonds import get_qlfixedratebond
import QuantLib as ql 
from .ql_enums import *
from .pymodels import *
from .ql_utils import *
from .ql_conventions import *
from .termstructure import *
from . import pymodels


def flat_forward():
    thedict = {"date": '2021-02-28',
                "rate": 5.00,
                "day_count": DayCount.act_act_act365,
                "frequency": Frequency.semi_annual,
                "compounding": Compounding.compounded }
    ffwd = FlatForwardCurve(**thedict)
    return ffwd


def sample_piecewise(value_date):
    rates, depo_setting, parrates, par_setting = sample_curveinfo()

    return curve_piecewise(value_date, 
                            depo_setting, 
                            rates, 
                            par_setting, 
                            parrates)


def sample_curveinfo():
    depo_rates = [
        {"tenor": "1M", "rate": 2.00},
        {"tenor": "2M", "rate": 2.05}, 
        {"tenor": "3M", "rate": 2.10},
        {"tenor": "6M", "rate": 2.20}
    ]

    rates = []
    for depo_rate in depo_rates:
        rate = Rate(**depo_rate)
        rates.append(rate)

    depo_sett = {
        "start_basis": StartBasis.today, 
        "business_day": BusinessDay.mod_following,
        "day_count": DayCount.act_act_act365,
        "eom": False
        }
    depo_setting = DepoSetting(**depo_sett)

    par_rates = [
        {"tenor": "1Y", "rate": 2.30},
        {"tenor": "2Y", "rate": 2.40}, 
        {"tenor": "3Y", "rate": 2.50},
        {"tenor": "5Y", "rate": 2.70},
        {"tenor": "7Y", "rate": 2.80},
        {"tenor": "10Y", "rate": 2.90},
        {"tenor": "20Y", "rate": 3.00},
        {"tenor": "30Y", "rate": 3.10}
    ]

    parrates = []
    for par_rate in par_rates:
        rate = Rate(**par_rate)
        parrates.append(rate)

    par_sett = {
        "frequency": "Semi-Annual",
        "start_basis": 2,
        "day_count": "Actual/Actual (ISMA)",
        "business_day": "Modified Following",
        "terminate_business_day": "Modified Following",
        "date_gen": "Backward from maturity date",
        "is_eom":  False
    }
    par_setting = BondSetting(**par_sett)

    return rates, depo_setting, parrates, par_setting


def sample_spreadinfo():
    spread_rates = [
        {"tenor": "1M", "rate": 0.4},
        {"tenor": "2M", "rate": 0.45}, 
        {"tenor": "3M", "rate": 0.5},
        {"tenor": "6M", "rate": 0.55},
        {"tenor": "1Y", "rate": 0.6},
        {"tenor": "2Y", "rate": 0.65}, 
        {"tenor": "3Y", "rate": 0.75},
        {"tenor": "5Y", "rate": 0.85},
        {"tenor": "7Y", "rate": 0.95},
        {"tenor": "10Y", "rate": 1.1},
        {"tenor": "20Y", "rate": 1.3},
        {"tenor": "30Y", "rate": 1.5}
    ]
    rates = []
    for depo_rate in spread_rates:
        rate = Rate(**depo_rate)
        rates.append(rate)
    return rates


#NOTE: changing business_day to no_adjustment will not give
#      clean price of 100 even on issue date.
def sample_bondinfo():
    bondsetting = {
        "frequency":Frequency.semi_annual,
        "start_basis": StartBasis.today,
        "day_count": DayCount.act_act_isma,
        "business_day": BusinessDay.no_adjustment,
        "terminate_business_day": BusinessDay.no_adjustment,
        "date_gen": DateGeneration.backward,
        "is_eom":  True
        }

    setting = BondSetting(**bondsetting)

    bonddata = {"issue_date": "2021-08-18", 
                "maturity": "2025-08-18", 
                "settings": setting, 
                "coupon": 5.00,
                "face_value": 10_000_000
                }
    thebond = FixedRateBond(**bonddata)

    return thebond, setting


def sample_convertiblebondinfo():
    bondsetting = {
        "frequency":Frequency.semi_annual,
        "start_basis": StartBasis.today,
        "day_count": DayCount.act_act_isma,
        "business_day": BusinessDay.no_adjustment,
        "terminate_business_day": BusinessDay.no_adjustment,
        "date_gen": DateGeneration.backward,
        "is_eom":  True
        }

    setting = BondSetting(**bondsetting)

    bonddata = {"issue_date": "2021-08-18", 
                "maturity": "2031-08-18", 
                "settings": setting, 
                "coupon": 5.75,
                "face_value": 100
                }
    thebond = FixedRateBond(**bonddata)

    return thebond

# NOTE: it is possible but yet to be tested to have multiple coupons
# for a fixed rate bond since the argument accepts list of coupons
def sample_fixedratebond():
    thebond, setting = sample_bondinfo()
    ql_period = ql.Period(ql_freq_tenor[setting.frequency])
    #print(ql_period)
    #1. Create Schedule
    schedule = ql.Schedule(datestr_to_qldate(thebond.issue_date), 
                        datestr_to_qldate(thebond.maturity), 
                        ql_period, 
                        ql.WeekendsOnly(), 
                        ql_business_day[setting.business_day],
                        ql_business_day[setting.terminate_business_day],
                        ql_date_generation[setting.date_gen],
                        setting.is_eom)
    fixbond = ql.FixedRateBond(setting.start_basis, 
                thebond.face_value, 
                schedule, 
                [thebond.coupon/100], 
                ql_day_count[setting.day_count])
    return fixbond


def sample_index(setting: BondSetting):
    # Create and index for Floating Rate
    ff = ql.FlatForward(setting.start_basis, 
                        ql.WeekendsOnly(), 
                        0.05,
                        ql_day_count[setting.day_count],
                        ql.Simple, 
                        ql_frequency[setting.frequency])
    
    #yts = ql.RelinkableYieldTermStructureHandle() 
    #yts.linkTo(ff)
    ff_handle = ql.YieldTermStructureHandle(ff)
    frb_engine = ql.DiscountingBondEngine(ff_handle)

    myr_br_index = ql.IborIndex('MYR-BR', 
                        ql.Period('6M'), 
                        0, 
                        ql.MYRCurrency(), 
                        ql.WeekendsOnly(), 
                        ql.ModifiedFollowing, 
                        True, 
                        ql.ActualActual(ql.ActualActual.Actual365),
                        ff_handle)
    #historical fixing is required for the active coupon period
    myr_br_index.addFixing(ql.Date(5,1,2021),0.05)

    return myr_br_index, frb_engine


def sample_FRB():
    thebond, setting = sample_bondinfo()
    ql_period = ql.Period(ql_freq_tenor[setting.frequency])
    schedule = ql.Schedule(datestr_to_qldate(thebond.issue_date), 
                        datestr_to_qldate(thebond.maturity), 
                        ql_period, 
                        ql.WeekendsOnly(), 
                        ql_business_day[setting.business_day],
                        ql_business_day[setting.terminate_business_day],
                        ql_date_generation[setting.date_gen],
                        setting.is_eom)

    index, engine = sample_index(setting)
    frb = ql.FloatingRateBond(setting.start_basis, 
                            thebond.face_value, 
                            schedule, 
                            index, 
                            ql.ActualActual(ql.ActualActual.Actual365), 
                            spreads=[0.005])
    # Note changing the engine doesnt seem to have an effect
    # presumably bcoz index is set in ql.FloatingRateBond
    frb.setPricingEngine(engine)

    return frb


# NOTE: it is possible but yet to be tested to have multiple coupons
# and face value for a  bond since the argument accepts list of coupons
# and face values. However, the face value can only be amortising which is 
# equivalent to using ql.AmortizingFixedRateBond
def sample_qlbond():
    thebond, setting = sample_bondinfo()
    abond = get_qlfixedratebond(thebond, setting,ql.WeekendsOnly())
    ql_period = ql.Period(ql_freq_tenor[setting.frequency])
    #print(ql_period)
    #1. Create Schedule
    schedule = ql.Schedule(datestr_to_qldate(thebond.issue_date), 
                        datestr_to_qldate(thebond.maturity), 
                        ql_period, 
                        ql.WeekendsOnly(), 
                        ql_business_day[setting.business_day],
                        ql_business_day[setting.terminate_business_day],
                        ql_date_generation[setting.date_gen],
                        setting.is_eom)
    interest = ql.FixedRateLeg(schedule, 
                                ql_day_count[setting.day_count], 
                                [thebond.face_value], 
                                [thebond.coupon/100])

    bond = ql.Bond(0, ql.WeekendsOnly(), 
                    datestr_to_qldate(thebond.issue_date),
                    interest)
    return bond


def sample_bondrisk(thebond, ql_irate):

    clean_price = ql.BondFunctions.cleanPrice(thebond, ql_irate)
    accrued = ql.BondFunctions.accruedAmount(thebond)
    bps = ql.BondFunctions.bps(thebond, ql_irate)
    duration = ql.BondFunctions.duration(thebond, ql_irate, ql.Duration.Macaulay)
    modified_duration = ql.BondFunctions.duration(thebond, ql_irate, ql.Duration.Modified)
    convexity = ql.BondFunctions.convexity(thebond, ql_irate)
    basis_point_value = ql.BondFunctions.basisPointValue(thebond, ql_irate)
    yield_value_basis_point = ql.BondFunctions.yieldValueBasisPoint(thebond, ql_irate)
    stats = {"accrued":  accrued,
            "clean_price": clean_price,
            "bps": bps,
            "duration": duration,
            "modified_duration": modified_duration,
            "convexity": convexity,
            "basis_point_value": basis_point_value,
            "yield_value_basis_point": yield_value_basis_point}
    bondrisk = BondRisk(**stats)
    return bondrisk


def sample_structuredloaninfo():
    loan_setting = {
        "frequency":Frequency.monthly,
        "start_basis": StartBasis.today,
        "day_count": DayCount.act_act_act365,
        "business_day": BusinessDay.mod_following,
        "terminate_business_day": BusinessDay.mod_following,
        "date_gen": DateGeneration.forward,
        "is_eom":  True
    }

    setting = BondSetting(**loan_setting)
    
    loan_data = {"issue_date": "2021-01-05", 
                "maturity": "2024-01-05", 
                "settings": setting, 
                }
    theloan = StructuredBond(**loan_data)

    return theloan, setting


def sample_fixrate_structuredloan():
    theloan, setting  = sample_structuredloaninfo()
    ql_period = ql.Period(ql_freq_tenor[setting.frequency])
    schedule = ql.Schedule(datestr_to_qldate(theloan.issue_date), 
                        datestr_to_qldate(theloan.maturity), 
                        ql_period, 
                        ql.WeekendsOnly(), 
                        ql_business_day[setting.business_day],
                        ql_business_day[setting.terminate_business_day],
                        ql_date_generation[setting.date_gen],
                        setting.is_eom)
    
    # Create the loan rate structure which increase by 0.25%
    # info is used by ql.FixedRateLeg
    loan_rates = []
    rate_initial = 5.00
    step = 0.00
    step_size = 0.25
    for i in range(1, len(schedule)):
        loan_rates.append((rate_initial + step)/100)
        step += step_size

    # Setting the array of face values which increases by 200,000
    # info is used by ql.FixedRateLeg
    face_values = []
    fv_initial = 10_000_000.00
    step = 0.00
    fv_step_size = 200_000.00
    for i in range(1, len(schedule)):
        face_values.append(fv_initial + step)
        step += fv_step_size
    #print(face_values)
    interests = ql.FixedRateLeg(schedule, ql_day_count[setting.day_count], 
                face_values, loan_rates)

    cashflows = []
    no_of_cfs = len(face_values)
    fvflows = [-fv_step_size for i in range(no_of_cfs - 1)]
    #print(no_of_cfs)
    for i in range(no_of_cfs):
        if i == no_of_cfs - 1:
            cashflow = face_values[i] - sum(fvflows) +interests[i].amount()
            #print(interests[i].date(), face_values[i], sum(fvflows), interests[i].amount() )
        else:
            cashflow = fvflows[i] + interests[i].amount()
            #print(interests[i].date(), fvflows[i], interests[i].amount() )
        simple_cash_flow = ql.SimpleCashFlow(cashflow, interests[i].date())
        cashflows.append(simple_cash_flow)

    loanleg = ql.Leg(cashflows)

    return loanleg


def sample_floatingrate_structuredloan():
    theloan, setting  = sample_structuredloaninfo()
    ql_period = ql.Period(ql_freq_tenor[setting.frequency])
    schedule = ql.Schedule(datestr_to_qldate(theloan.issue_date), 
                        datestr_to_qldate(theloan.maturity), 
                        ql_period, 
                        ql.WeekendsOnly(), 
                        ql_business_day[setting.business_day],
                        ql_business_day[setting.terminate_business_day],
                        ql_date_generation[setting.date_gen],
                        setting.is_eom)
    
    
    # Setting the array of face values which increases by 200,000
    # info is used by ql.FixedRateLeg
    face_values = []
    fv_initial = 10_000_000.00
    step = 0.00
    fv_step_size = 200_000.00
    for i in range(1, len(schedule)):
        face_values.append(fv_initial + step)
        step += fv_step_size
    
    index, engine = sample_index(setting)
    loanleg = ql.IborLeg(face_values, 
                schedule, 
                index, 
                ql.Actual360(), 
                ql.ModifiedFollowing, 
                fixingDays=[0])

    return loanleg


def callabilityschedule(qlSchedule: ql.QuantLib.Schedule):
    
    callability_schedule = ql.CallabilitySchedule()
    call_price = 100.0
    no_of_dates = len(list(qlSchedule))
    start = int(no_of_dates/4)
    #print(start, no_of_dates)
    for i in range(start, no_of_dates):
        callability_price  = ql.CallabilityPrice(
            call_price, ql.CallabilityPrice.Clean)
        callability_schedule.append(
                ql.Callability(callability_price, 
                            ql.Callability.Call,
                            qlSchedule[i]))
        print(qlSchedule[i])
    return callability_schedule


def callable_bondinfo():
    bondsetting = {
        "frequency":Frequency.semi_annual,
        "start_basis": StartBasis.today,
        "day_count": DayCount.act_act_isma,
        "business_day": BusinessDay.no_adjustment,
        "terminate_business_day": BusinessDay.following,
        "date_gen": DateGeneration.backward,
        "is_eom":  True
        }

    setting = BondSetting(**bondsetting)

    bonddata = {"issue_date": "2021-08-18", 
                "maturity": "2031-08-18", 
                "settings": setting, 
                "coupon": 5.00,
                "face_value": 10_000_000
                }
    thebond = FixedRateBond(**bonddata)

    return thebond, setting
    

def convertibles_fixedratebond():
    thebond = sample_convertiblebondinfo()
    bond_dict = thebond.dict()
    bond_dict["redemption"] = 100.00
    bond_dict["conversion_price"] = 26.00
    bond_dict["conversion_ratio"] = 3.84615
    bond_dict["dividend_yield"] =   2
    bond_dict["stock_price"] = 29.04
    bond_dict["credit_spread"] = 3.0
    bond_dict["exercise_type"] = OptionExercise.european
    bond_dict["european_expiry"] = "2028-08-18"

    calendar =ql.WeekendsOnly()
    conv_bond = pymodels.ConvertibleFixedRate(**bond_dict)
    #Create schedule to create sample callability and puttable
    schedule = qlSchedule2(conv_bond, calendar)
    dates = list(schedule)
    no_of_dates = len(dates)
    call_start = int(no_of_dates/4)
    put_start = int(no_of_dates/2)

    calls = []
    for i in range(call_start, put_start ):
        calldict = {"price_type": BondPriceType.clean,
                    "price": 100.00,
                    "date": dates[i].ISO(),
                    "option_type":OptionType.calloption}
        callprices = CallabilityPrice(**calldict)
        calls.append(callprices)  
    conv_bond.call_list = calls
    
    puts = []
    for i in range(put_start + 1, no_of_dates):
        putdict = {"price_type": BondPriceType.clean,
                    "price": 100.00,
                    "date": dates[i].ISO(),
                    "option_type": OptionType.putoption}
        putprices = CallabilityPrice(**putdict)
        puts.append(putprices)
    conv_bond.put_list = puts

    conv_bond.structure = structure_from_qlSchedule(conv_bond, schedule )
    

    return conv_bond


def curve_with_spread(value_date: str):
    vdate = datestr_to_qldate(value_date) 
    calendar = ql.WeekendsOnly()
    rates, depo_setting, parrates, par_setting = sample_curveinfo()
    t_structure = curve_piecewise(value_date, 
                                depo_setting, 
                                rates,
                                par_setting, 
                                parrates)
    curve_handle = ql.YieldTermStructureHandle(t_structure)
    spreads = sample_spreadinfo()
    spread_handles = []
    spread_dates = []
    spread_quotes = []

    for spread in spreads:
        spread_quote = ql.SimpleQuote(spread.rate/100)
        spread_quotes.append(spread_quote)
        spread_handle = ql.QuoteHandle(spread_quote)
        spread_handles.append(spread_handle)
        maturity = calendar.advance(vdate, get_qlPeriod(spread.tenor))
        spread_dates.append(maturity)

    spread_curve = ql.SpreadedLinearZeroInterpolatedTermStructure(
                            curve_handle,
                            spread_handles,
                            spread_dates)
    spread_curve_handle = ql.YieldTermStructureHandle(spread_curve)
    return spread_curve_handle


def srmodel_info():
    callbond_model = {"name": "HullWhite",
                            "vas_r0": 0.05,
                            "vas_a": 0.1,
                            "vas_b": 0.05,
                            "vas_sigma": 0.01,
                            "vas_lambda": 0.00,
                            "bk_a": 0.1,
                            "bk_sigma": 0.1,
                            "hw_a": 0.1,
                            "hw_sigma": 0.01,
                            "gsr_step": None,
                            "gsr_sigma": None,
                            "gsr_reversion": None,
                            "g2_a": 0.1,
                            "g2_b": 0.1,
                            "g2_sigma": 0.01,
                            "g2_eta": 0.01,
                            "g2_rho": -0.75,
                        }
    return callbond_model


def data_EONIA():
    
    depo_sett = {
        "start_basis": StartBasis.spot, 
        "business_day": BusinessDay.following,
        "day_count": DayCount.act_act_act365,
        "eom": False
        }
    depos = [{'tenor':'O/N', 'rate': 0.04, 'start_basis': StartBasis.today},
            {'tenor':"T/N", 'rate': 0.04, 'start_basis': StartBasis.tom}, 
            {'tenor':"S/N", 'rate': 0.04, 'start_basis': StartBasis.spot}]
    depo_helper = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(depo['rate']/100)),
                                                ql.Period(1,ql.Days),
                                                depo['start_basis'],
                                                ql.TARGET(), 
                                                ql.Following,
                                                False,
                                                ql.Actual360()) 
                    for depo in depos]
    #>>>>>>>> NOT USED >>>>>>>>>>>>>
    depo_rates = []
    for depo in depos:
        rate = pymodels.Rate(**depo)
        depo_rates.append(rate)
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    index = ql.Eonia()
    ois = [{'tenor':"1W", 'rate': 0.07}, 
            {'tenor':"2W", 'rate': 0.069}, 
            {'tenor':"3W", 'rate': 0.078}]

    ois_helper = [ ql.OISRateHelper(2, ql.Period(datum['tenor']),
                                   ql.QuoteHandle(ql.SimpleQuote(datum['rate']/100)), index)
                                    for datum in ois] 
    #>>>>>>>> NOT USED >>>>>>>>>>>>>
    ois_rates = []
    for oi in ois:
        rate = pymodels.Rate(**oi)
        ois_rates.append(rate)
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    ois_fwds = [{'rate': 0.046, 'start_date': '2013-01-16', "end_date": '2013-02-13'},
            {'rate': 0.016, 'start_date': '2013-02-13', "end_date": '2013-03-13'}, 
            {'rate': -0.007, 'start_date': '2013-03-13', "end_date": '2013-04-10'},
            {'rate': -0.013, 'start_date': '2013-04-10', "end_date": '2013-05-08'}, 
            {'rate': -0.014, 'start_date': '2013-05-08', "end_date": '2013-06-12'}]
    ois_fwd_helper = [ql.DatedOISRateHelper(ql.Date(datum['start_date'], '%Y-%m-%d'), 
                                            ql.Date(datum['end_date'],  '%Y-%m-%d'),
                                            ql.QuoteHandle(ql.SimpleQuote(datum['rate']/100)), 
                                            index)
                        for datum in ois_fwds ]
    #>>>>>>>>>> NOT USED >>>>>>>>>>>>>>>>
    ##ois_frwd = []
    #for ois_fwd in ois_fwds:
    #    rate = pymodels.Rate(**ois_fwd)
    #    ois_frwd.append(rate)
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ois_swap = [ {'tenor':"15M", 'rate': 0.002}, 
                {'tenor':"18M", 'rate': 0.008},
                {'tenor':"21M", 'rate': 0.021},
                {'tenor':"2Y", 'rate': 0.036},
                {'tenor':"3Y", 'rate': 0.127},
                {'tenor':"4Y", 'rate': 0.274},
                {'tenor':"5Y", 'rate': 0.456},
                {'tenor':"6Y", 'rate': 0.647},
                {'tenor':"7Y", 'rate': 0.824},
                {'tenor':"8Y", 'rate': 0.996},
                {'tenor':"9Y", 'rate': 1.147},
                {'tenor':"10Y", 'rate': 1.280},
                {'tenor':"11Y", 'rate': 1.404},
                {'tenor':"12Y", 'rate': 1.516},
                {'tenor':"15Y", 'rate': 1.764},
                {'tenor':"20Y", 'rate': 1.939},
                {'tenor':"25Y", 'rate': 2.003},
                {'tenor':"30Y", 'rate': 2.038}
                ]
    ois_swap_helper = [ql.OISRateHelper(2, 
                                        ql.Period(datum['tenor']),
                                        ql.QuoteHandle(ql.SimpleQuote(datum['rate']/100)), index)
                        for datum in ois_swap]
    
    return depo_helper, ois_helper, ois_fwd_helper, ois_swap_helper


def depo_data():
    depo_rates = [
        {"tenor": "1M", "rate": 2.00},
        {"tenor": "2M", "rate": 2.05}, 
        {"tenor": "3M", "rate": 2.10},
        {"tenor": "6M", "rate": 2.20}
    ]

    rates = []
    for depo_rate in depo_rates:
        rate = Rate(**depo_rate)
        rates.append(rate)

    depo_sett = {
        "start_basis": StartBasis.today, 
        "business_day": BusinessDay.mod_following,
        "day_count": DayCount.act_act_act365,
        "eom": False
        }
    setting = DepoSetting(**depo_sett)
    return setting, rates


def parbond_data():
    par_rates = [
        {"tenor": "1Y", "rate": 2.30},
        {"tenor": "2Y", "rate": 2.40}, 
        {"tenor": "3Y", "rate": 2.50},
        {"tenor": "5Y", "rate": 2.70},
        {"tenor": "7Y", "rate": 2.80},
        {"tenor": "10Y", "rate": 2.90},
        {"tenor": "20Y", "rate": 3.00},
        {"tenor": "30Y", "rate": 3.10}
    ]
    rates = []
    for par_rate in par_rates:
        rate = Rate(**par_rate)
        rates.append(rate)

    par_sett = {
        "frequency": "Semi-Annual",
        "start_basis": 2,
        "day_count": "Actual/Actual (ISMA)",
        "business_day": "Modified Following",
        "terminate_business_day": "Modified Following",
        "date_gen": "Backward from maturity date",
        "is_eom":  False
    }
    setting = BondSetting(**par_sett)
    return setting, rates


def fra_data():
    fra_rates = [
        {"depo":{"tenor": "3M", "rate": 2.00, "start_basis": qle.StartBasis.spot}, "start_tenor": "1M"},
        {"depo":{"tenor": "3M", "rate": 2.05, "start_basis": qle.StartBasis.spot}, "start_tenor": "4M"},
        {"depo":{"tenor": "3M", "rate": 2.10, "start_basis": qle.StartBasis.spot}, "start_tenor": "7M"},
        {"depo":{"tenor": "3M", "rate": 2.20, "start_basis": qle.StartBasis.spot}, "start_tenor": "10M"},
        ]
    rates = []
    for fra_rate in fra_rates:
        rate = FRA(**fra_rate)
        rates.append(rate)
    
    return rates


def ois_data():
    ois = [{'tenor':"1W", 'rate': 2.00}, 
            {'tenor':"2W", 'rate': 2.05}, 
            {'tenor':"3W", 'rate': 2.1}]

    rates = []
    for oi in ois:
        rate = pymodels.Rate(**oi)
        rates.append(rate)

    return rates


def irs_data():
    irs = [{'tenor':"1W", 'rate': 2.00}, 
            {'tenor':"2W", 'rate': 2.05}, 
            {'tenor':"3W", 'rate': 2.1}]

    rates = []
    for ir in irs:
        rate = pymodels.Rate(**ir)
        rates.append(rate)

    return rates
