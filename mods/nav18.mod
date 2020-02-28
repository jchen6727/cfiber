COMMENT

NaV1.8 Channel (from unknown)
reproduced from 
Sheets et al. (2007)
Maingret et al. (2008)
and
Tigerholm Et. Al (2014)

ENDCOMMENT

UNITS {
    (mV) = (millivolt)
    (mA) = (milliamp)
    (S)  = (siemens)
}

NEURON {
    SUFFIX nav18
    USEION na READ ena WRITE ina
    RANGE gnabar, gna, ina
    RANGE malpha, mbeta, mtau, minf
    RANGE halpha, hbeta, htau, hinf
    RANGE salpha, sbeta, stau, sinf
    RANGE ualpha, ubeta, utau, uinf

    RANGE emut, rmut

    RANGE q10, tadj

}

PARAMETER{ 
    gnabar = 0.1066 (S/cm2)
    q10    = 2.5
    emut   = 0
    rmut   = 0

}

ASSIGNED {

	celsius (degC)
	v (mV)
    ina (mA/cm2)
    ena (mV)
:Nernst at 37 degC at [na]o / [na]i => 140/10
:0.227404 * (celsius + 273.15) => ena
    gna (S/cm2)

    malpha
    halpha
    salpha
    ualpha

    mbeta
    hbeta
    sbeta
    ubeta

    mtau (ms) 
    htau (ms)
    stau (ms)
    utau (ms)

    minf
    hinf
    sinf
    uinf

    tadj

}

STATE{
    m h s u
}

UNITSOFF

INITIAL{
    settables(v)
    tadj = q10 ^ ( ( celsius - 21) / 10 )
    m = minf
    h = hinf
    s = sinf
    u = uinf
}

BREAKPOINT{
    SOLVE states METHOD cnexp
    
    gna = gnabar * m^3 * h * s * u
    ina = gna * ( (1-rmut) * (v - ena) + ( rmut * (v-emut) ) )
}

DERIVATIVE states{
    settables(v)
    m' = (minf-m)/mtau
    h' = (hinf-h)/htau
    s' = (sinf-s)/stau
    u' = (uinf-u)/utau
}


PROCEDURE settables(v (mV)){
:    TABLE minf, mtau, hinf, htau, sinf, stau
:    FROM -100 TO 100 WITH 200

    malpha = 2.85 - 2.839 / ( 1 + exp( (v-1.159 ) / 13.95  ) )
    mbeta  = 7.6205       / ( 1 + exp( (v+46.463) / 8.8289 ) )
    mtau   = 1 / (malpha + mbeta) / tadj
    minf   = malpha / (malpha + mbeta)

:    halpha =  0.38685           / ( 1 + exp( (v + 122.35) /  15.29   ))
:    hbeta  = -0.00283 + 2.00283 / ( 1 + exp( (v + 5.5266) / -12.70195))
    htau   = ( 1.218 + 42.043 * exp( - ( (v+38.1)^2 / (2 * 15.19^2) ) ) ) / tadj
    hinf   = 1 / ( 1 + exp((v + 32.2)/4) )

    salpha = 0.001 * 5.4203/(1 + exp((v + 79.816)/16.269))
    sbeta  = 0.001 * 5.0757/(1 + exp( - ( v+15.968 )/11.542 ))
    stau   = 1 / (salpha + sbeta) / tadj
    sinf   = 1 / ( 1 + exp((v + 45)/8) )

    ualpha = 0.0002 * 2.0434/(1 + exp((v + 67.499)/19.51))
    ubeta  = 0.0002 * 1.9952/(1 + exp( - (v + 30.963)/14.792))
    utau   = 1 / (ualpha + ubeta) / tadj
    uinf   = 1 / ( 1 + exp((v + 51)/8))
}

UNITSON
