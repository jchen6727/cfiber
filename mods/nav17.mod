COMMENT

Human WT NaV1.7 Channel 
reproduced from 
Sheets Et. Al (2007)
and
Tigerholm Et. Al (2014)

ENDCOMMENT



UNITS {
    (mV) = (millivolt)
    (mA) = (milliamp)
    (S)  = (siemens)
}

NEURON {
    SUFFIX nav17
    USEION na READ ena WRITE ina
    RANGE gnabar, gna, ina
    RANGE malpha, mbeta, mtau, minf
    RANGE halpha, hbeta, htau, hinf
    RANGE salpha, sbeta, stau, sinf

    RANGE emut, rmut

    RANGE q10

}

PARAMETER{ 
    gnabar = 0.1066 (S/cm2)
    emut   = 0
    rmut   = 0.0
    q10    = 2.5
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

    mbeta
    hbeta
    sbeta

    mtau (ms) 
    htau (ms)
    stau (ms)

    minf
    hinf
    sinf

    tadj (1)

}

STATE{
    m h s
}

UNITSOFF

INITIAL{
    settables(v)
    tadj = q10 ^ ( ( celsius - 21) / 10 )
    m = minf
    h = hinf
    s = sinf
}

BREAKPOINT{
    SOLVE states METHOD cnexp
    
    gna = gnabar * m^3 * h * s
    ina = gna * ( (1-rmut) * (v - ena) + (rmut * (v-emut) ) )
}

DERIVATIVE states{
    settables(v)
    m' = (minf-m)/mtau
    h' = (hinf-h)/htau
    s' = (sinf-s)/stau
}


PROCEDURE settables(v (mV)){
:    TABLE minf, mtau, hinf, htau, sinf, stau
:    FROM -100 TO 100 WITH 200

    malpha = 15.5 / ( 1 + exp( (v-5   ) / -12.08 ) )
    mbeta  = 35.2 / ( 1 + exp( (v+72.7) /  16.7  ) )
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
