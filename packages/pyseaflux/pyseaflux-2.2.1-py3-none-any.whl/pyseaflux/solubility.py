"""
CO2 solubility in seawater
--------------------------
"""


def solubility_weiss1974(salt, temp_K, press_atm=1, checks=True):
    """Calculates the solubility of CO2 in sea water

    Used in the calculation of air-sea CO2 fluxes. We use the formulation by
    Weiss (1974) summarised in Wanninkhof (2014).

    Args:
        salt (array): salinity in PSU
        temp_K (array): temperature in deg Kelvin
        press_atm (array): pressure in atmospheres. Used in the solubility
            correction for water vapour pressure. If not given, assumed
            that press_atm is 1atm

    Returns:
        array: solubility of CO2 in seawater (:math:`K_0`) in mol/L/atm

    Examples:
        from Weiss (1974) Table 2 but with pH2O correction

        >>> solubility_weiss1974(35, 299.15)
        0.029285284543519093
    """

    from numpy import exp, log, nanmedian
    from xarray import DataArray

    from . import vapour_pressure as vapress

    if checks:
        if nanmedian(temp_K) < 270:
            raise ValueError("Temperature is not in Kelvin")

    T = temp_K
    S = salt
    P = press_atm

    # from table in Wanninkhof 2014
    a1 = -58.0931
    a2 = +90.5069
    a3 = +22.2940
    b1 = +0.027766
    b2 = -0.025888
    b3 = +0.0050578

    T100 = T / 100
    K0 = exp(
        a1 + a2 * (100 / T) + a3 * log(T100) + S * (b1 + b2 * T100 + b3 * T100 ** 2)
    )

    pH2O = vapress.weiss1980(S, T)
    K0 = K0 / (P - pH2O)

    # mol / L / atm --> mol / m3 / uatm
    # mol . L-1 . atm-1 * (L . m-3) * (atm . uatm-1)
    #                       1000    *   1e-6

    if isinstance(K0, DataArray):
        K0 = K0.assign_attrs(
            units="mol/L/atm",
            description=(
                "solubility based on Weiss (1974), with a correction for "
                "vapour pressure (Weiss, 1980)"
            ),
        )

    return K0  # units mol/L/atm
