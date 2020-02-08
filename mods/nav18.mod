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

}

PARAMETER{ 
    gnabar = 0.1066 (S/cm2)

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
    m = minf
    h = hinf
    s = sinf
    u = uinf
}

BREAKPOINT{
    SOLVE states METHOD cnexp
    
    gna = gnabar * m^3 * h * s * u
    ina = gna * (v - ena)
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

    tadj = 2.5 ^ ( ( celsius - 21) / 10 )
    malpha = 2.85 - 2.839 / ( 1 + exp( (v-1.159 ) / 13.95  ) )
    mbeta  = 7.6205       / ( 1 + exp( (v+46.463) / 8.8289 ) )
    mtau   = 1 / (malpha + mbeta) / tadj
    minf   = malpha / (malpha + mbeta)

    halpha =  0.38685           / ( 1 + exp( (v + 122.35) /  15.29   ))
    hbeta  = -0.00283 + 2.00283 / ( 1 + exp( (v + 5.5266) / -12.70195))
    htau   = 1 / (halpha + hbeta) / tadj
    hinf   = halpha / (halpha + hbeta)

    salpha = 0.00003 + 0.00092 / ( 1 + exp( (v + 93.9 ) / 16.6))
    sbeta  = 132.05  - 132.05  / ( 1 + exp( (v - 384.9) / 28.5))
    stau   = 1 / (salpha + sbeta) / tadj
    sinf   = salpha / (salpha + sbeta)
}

UNITSON
