v 20130925 2
T 55700 36100 9 10 1 0 0 0 1
Time-Lock Switch Controller
T 55600 35800 9 10 1 0 0 0 1
ckt-timelock.sch
T 55600 35500 9 10 1 0 0 0 1
1
T 57100 35500 9 10 1 0 0 0 1
1
T 59500 35500 9 10 1 0 0 0 1
Nathan D. Holmes
T 56100 37000 9 10 1 0 0 0 3
Notes:
1) All unpolarized capacitors are ceramic (X7R/X5R) unless otherwise noted.
2) All capacitors and resistors are 0805 unless otherwise noted.
C 42500 44400 1 0 1 avrprog-1.sym
{
T 42500 46000 5 10 0 1 0 6 1
device=AVRPROG
T 41900 44100 5 10 1 1 0 6 1
refdes=J5
T 42500 44400 5 10 0 0 0 0 1
footprint=TC2030-NL
}
N 40800 45000 41100 45000 4
{
T 40700 45000 5 10 1 1 0 7 1
netname=MOSI
}
C 41000 44300 1 0 0 gnd-1.sym
N 41100 45400 41100 46000 4
N 47300 50000 47300 49800 4
C 44800 49800 1 90 1 Cap_H-2.sym
{
T 44500 50500 5 10 1 1 180 6 1
refdes=C2
T 43300 49800 5 10 0 0 270 2 1
device=Capacitor
T 44900 50300 5 10 1 1 0 8 1
value=68uF
T 44500 49900 5 10 1 1 0 0 1
description=25V
T 44800 49800 5 10 0 0 0 0 1
footprint=cap-elec-Panasonic-FK--D6.30-H5.80-mm
}
C 39500 35200 0 0 0 title-bordered-A2.sym
C 43800 49800 1 270 0 capacitor-1.sym
{
T 44500 49600 5 10 0 1 270 0 1
device=CAPACITOR
T 43800 50300 5 10 1 1 0 0 1
refdes=C1
T 44700 49600 5 10 0 0 270 0 1
symversion=0.1
T 43800 50100 5 10 1 1 0 0 1
value=1uF
T 43800 49800 5 10 0 0 0 0 1
footprint=0805
T 43800 49900 5 10 1 1 0 0 1
description=25V
}
C 45900 48600 1 0 0 gnd-1.sym
N 43100 48900 47600 48900 4
N 42200 49800 41500 49800 4
N 43100 49800 45500 49800 4
C 48800 48800 1 270 1 led-3.sym
{
T 50050 48950 5 10 1 1 0 6 1
device=GREEN
T 49650 49250 5 10 1 1 0 6 1
refdes=D2
T 48800 48800 5 10 0 0 270 0 1
footprint=0805
}
C 48900 47600 1 0 0 gnd-1.sym
C 45500 49200 1 0 0 78l05-1.sym
{
T 47100 50500 5 10 0 0 0 0 1
device=7805
T 46900 50200 5 10 1 1 0 6 1
refdes=U1
T 45500 49200 5 10 0 0 0 0 1
footprint=SOT89
}
N 46300 48900 46300 49200 4
C 56400 43300 1 0 0 switch-dip5-1.sym
{
T 57400 45275 5 8 1 1 0 0 1
device=CT2195MST
T 56700 45250 5 10 1 1 0 0 1
refdes=SW1
T 56400 43300 5 10 0 0 0 0 1
footprint=DIPSW10
}
C 57600 43400 1 0 0 gnd-1.sym
N 57700 43700 57700 44900 4
C 47100 50000 1 0 0 5V-plus-1.sym
N 47100 49800 53200 49800 4
N 49000 49800 49000 49700 4
C 47400 49800 1 270 0 capacitor-1.sym
{
T 48100 49600 5 10 0 1 270 0 1
device=CAPACITOR
T 47800 49500 5 10 1 1 0 0 1
refdes=C3
T 48300 49600 5 10 0 0 270 0 1
symversion=0.1
T 47800 49100 5 10 1 1 0 0 1
value=1uF
T 47400 49800 5 10 0 0 0 0 1
footprint=0805
T 47800 48900 5 10 1 1 0 0 1
description=16V
}
C 41500 48800 1 0 1 termblk3-1.sym
{
T 40500 49450 5 10 0 0 0 6 1
device=HEADER3
T 41100 50100 5 10 1 1 0 6 1
refdes=J1
T 41500 48800 5 10 0 0 0 0 1
footprint=TERMBLK3_3p5MM
}
N 41500 49400 43100 49400 4
N 43100 49400 43100 48900 4
N 41500 49000 42200 49000 4
T 40700 49700 9 10 1 0 0 6 1
12V
T 40700 49300 9 10 1 0 0 6 1
GND
T 40700 48900 9 10 1 0 0 6 1
CNTL IN
C 40900 46000 1 0 0 5V-plus-1.sym
C 55100 39500 1 180 0 resistor-1.sym
{
T 54800 39100 5 10 0 0 180 0 1
device=RESISTOR
T 54800 39700 5 10 1 1 180 0 1
refdes=R3
T 54800 39100 5 10 1 1 180 0 1
value=330
T 55100 39500 5 10 0 0 180 0 1
footprint=0805
}
N 55100 39400 56800 39400 4
C 56300 39500 1 0 0 gnd-1.sym
N 56400 39800 56800 39800 4
C 54500 41500 1 270 0 resistor-1.sym
{
T 54900 41200 5 10 0 0 270 0 1
device=RESISTOR
T 54800 41000 5 10 1 1 0 0 1
refdes=R4
T 54800 40800 5 10 1 1 0 0 1
value=10k
T 54500 41500 5 10 0 0 270 0 1
footprint=0805
}
N 54000 40200 56800 40200 4
C 54400 42500 1 0 0 5V-plus-1.sym
T 58000 39700 9 10 1 0 0 6 1
GND
T 57600 39300 9 10 1 0 0 0 1
LED
T 57600 40100 9 10 1 0 0 0 1
LOCK
N 54600 40200 54600 40600 4
N 53000 39400 54200 39400 4
{
T 52900 39400 5 10 1 1 0 7 1
netname=TL_LAMP
}
T 51400 40500 9 10 1 0 0 0 1
TRK SHUNT A
T 51400 40100 9 10 1 0 0 0 1
TRK SHUNT B
T 59000 49300 9 10 1 0 0 0 1
SLO-MO DRIVE A
T 59000 48900 9 10 1 0 0 0 1
SLO-MO DRIVE B
T 40400 48400 9 10 1 0 0 0 1
In From Control
C 43200 46500 1 0 0 mmbz52xxblt1g-1.sym
{
T 44000 47450 5 10 1 1 0 0 1
refdes=Z1
T 43400 48900 5 10 0 0 0 0 1
footprint=SOT23
T 45400 47250 5 10 1 1 0 6 1
device=MMBZ5230BLT1G
}
C 47300 41700 1 0 0 ATtiny44-SO14.sym
{
T 51900 45500 5 10 1 1 0 0 1
refdes=U2
T 49200 45500 5 10 1 1 0 6 1
device=ATtiny44
T 53395 42895 5 10 1 1 0 8 1
footprint=SO14
}
C 50600 46900 1 0 0 5V-plus-1.sym
N 50800 46900 50800 45700 4
C 50700 42400 1 0 0 gnd-1.sym
N 42800 45000 42500 45000 4
{
T 42900 45000 5 10 1 1 0 1 1
netname=SCK
}
N 42800 45400 42500 45400 4
{
T 42900 45400 5 10 1 1 0 1 1
netname=MISO
}
N 47000 43400 47600 43400 4
{
T 46900 43400 5 10 1 1 0 7 1
netname=MOSI
}
N 54400 43400 53800 43400 4
{
T 54500 43400 5 10 1 1 0 1 1
netname=MISO
}
N 53800 44900 56400 44900 4
N 56400 44600 53800 44600 4
N 53800 44300 56400 44300 4
N 56400 44000 53800 44000 4
N 55400 43400 55700 43400 4
{
T 55800 43400 5 10 1 1 0 1 1
netname=SCK
}
N 53800 43700 56400 43700 4
N 55400 43400 55400 43700 4
N 47300 44900 47600 44900 4
{
T 47200 44900 5 10 1 1 0 7 1
netname=TL_LAMP
}
N 53200 49000 52700 49000 4
{
T 52600 49000 5 10 1 1 0 7 1
netname=SWM_DRV_F
}
N 47600 44600 47300 44600 4
{
T 47200 44600 5 10 1 1 0 7 1
netname=SWM_DRV_F
}
N 42200 47800 42200 49000 4
N 43400 47800 45100 47800 4
{
T 45300 47800 5 10 1 1 0 1 1
netname=CTRL_IN
}
N 43700 47800 43700 47700 4
C 43600 46500 1 0 0 gnd-1.sym
C 50500 40000 1 0 0 termblk2-1.sym
{
T 51500 40650 5 10 0 0 0 0 1
device=TERMBLK2
T 50900 40900 5 10 1 1 0 0 1
refdes=J3
T 50500 40000 5 10 0 0 0 6 1
footprint=TERMBLK2_200MIL
}
C 50300 40300 1 180 0 resistor-1.sym
{
T 50000 39900 5 10 0 0 180 0 1
device=RESISTOR
T 50300 40300 5 10 0 0 180 0 1
footprint=1206
T 50000 40500 5 10 1 1 180 0 1
refdes=R5
T 50000 40000 5 10 1 1 180 0 1
value=750
}
N 50300 40200 50500 40200 4
N 49200 40200 49400 40200 4
C 47400 39800 1 0 0 cpc1017n-1.sym
{
T 47500 42700 5 8 0 0 0 0 1
symversion=1.0
T 47800 39600 5 10 1 1 0 0 1
refdes=U4
T 47800 39400 5 10 1 1 0 0 1
value=CPC1017N
T 47500 41300 5 8 0 1 0 0 1
footprint=LTV352-1
}
N 49200 41000 50500 41000 4
N 50500 41000 50500 40600 4
C 47400 37700 1 0 0 gnd-1.sym
N 47500 38000 47500 38500 4
N 46500 38300 47500 38300 4
N 46500 38500 46500 38300 4
N 46500 40100 46500 39400 4
N 45500 41000 47500 41000 4
N 42500 47800 42200 47800 4
N 47400 43100 47100 43100 4
{
T 47000 43100 5 10 1 1 0 7 1
netname=CTRL_IN
}
N 47400 43100 47400 43400 4
N 54000 40200 54000 43400 4
C 53200 47900 1 0 0 zxbm5210-1.sym
{
T 53700 50250 5 10 1 1 0 6 1
refdes=U3
T 53995 48100 5 10 0 1 0 0 1
footprint=SO8
T 53995 48100 5 10 1 1 0 0 1
device=ZXBM5210
}
N 53200 49400 52800 49400 4
N 52800 49400 52800 49800 4
N 45200 49800 45200 50700 4
N 45200 50700 55500 50700 4
N 55500 50700 55500 49800 4
N 55500 49800 55200 49800 4
N 55200 49400 58200 49400 4
N 58200 49000 55200 49000 4
C 55400 48300 1 0 0 gnd-1.sym
N 55200 48600 55500 48600 4
N 47600 44000 47300 44000 4
{
T 47200 44000 5 10 1 1 0 7 1
netname=SWM_DRV_R
}
N 53200 48600 52900 48600 4
{
T 52800 48600 5 10 1 1 0 7 1
netname=SWM_DRV_R
}
C 56700 47500 1 0 0 led-3.sym
{
T 56450 47450 5 10 1 1 0 0 1
device=BLUE
T 57050 47250 5 10 1 1 0 0 1
refdes=D3
T 56700 47500 5 10 0 0 0 6 1
footprint=0805
}
C 57600 46600 1 0 1 led-3.sym
{
T 56950 46950 5 10 1 1 0 6 1
device=AMBER
T 57250 46350 5 10 1 1 0 6 1
refdes=D4
T 57600 46600 5 10 0 0 0 0 1
footprint=0805
}
C 56000 48700 1 270 0 resistor-1.sym
{
T 56400 48400 5 10 0 0 270 0 1
device=RESISTOR
T 56400 48300 5 10 1 1 0 0 1
refdes=R2
T 56400 48000 5 10 1 1 0 0 1
value=2k
T 56000 48700 5 10 0 0 270 0 1
footprint=0805
}
N 56100 46800 56100 47800 4
N 56100 47700 56700 47700 4
N 56100 46800 56700 46800 4
N 56100 48700 56100 49400 4
N 57600 49000 57600 46800 4
N 47600 44300 43100 44300 4
N 43100 44000 43100 44600 4
N 43100 44600 42500 44600 4
C 42900 44000 1 270 0 capacitor-1.sym
{
T 43600 43800 5 10 0 1 270 0 1
device=CAPACITOR
T 43200 43700 5 10 1 1 0 0 1
refdes=C4
T 43800 43800 5 10 0 0 270 0 1
symversion=0.1
T 43400 43300 5 10 1 1 0 0 1
value=1uF
T 42900 44000 5 10 0 0 0 0 1
footprint=0805
T 43400 43100 5 10 1 1 0 0 1
description=16V
}
C 43000 42800 1 0 0 gnd-1.sym
C 48900 49200 1 270 0 res-pack4-1.sym
{
T 48900 49200 5 10 0 0 270 0 1
slot=2
T 49300 48400 5 10 1 1 0 0 1
refdes=R1
T 49300 48100 5 10 1 1 0 0 1
value=1k
T 48900 49200 5 10 0 0 180 0 1
footprint=RPACK4-1206
}
C 46300 40100 1 270 1 led-3.sym
{
T 45750 40450 5 10 1 1 0 0 1
device=RED
T 45750 40650 5 10 1 1 0 0 1
refdes=D5
T 46300 40100 5 10 0 0 270 0 1
footprint=0805
}
C 46400 39800 1 270 0 res-pack4-1.sym
{
T 46400 39800 5 10 0 0 270 0 1
slot=3
T 46800 39000 5 10 1 1 0 0 1
refdes=R1
T 46800 38700 5 10 1 1 0 0 1
value=1k
T 46400 39800 5 10 0 0 180 0 1
footprint=RPACK4-1206
}
C 47400 39800 1 270 0 res-pack4-1.sym
{
T 47400 39800 5 10 0 0 270 0 1
slot=4
T 47800 39000 5 10 1 1 0 0 1
refdes=R1
T 47800 38700 5 10 1 1 0 0 1
value=1k
T 47400 39800 5 10 0 0 180 0 1
footprint=RPACK4-1206
}
N 47500 39400 47500 40200 4
C 40200 35800 1 0 0 hole-1.sym
{
T 40200 35800 5 10 0 1 0 0 1
device=HOLE
T 40200 35800 5 10 0 0 0 0 1
footprint=STANDOFF_HEX_n4
T 40400 36400 5 10 1 1 0 4 1
refdes=H1
}
C 41700 35800 1 0 0 hole-1.sym
{
T 41700 35800 5 10 0 1 0 0 1
device=HOLE
T 41700 35800 5 10 0 0 0 0 1
footprint=STANDOFF_HEX_n4
T 41900 36400 5 10 1 1 0 4 1
refdes=H4
}
C 41200 35800 1 0 0 hole-1.sym
{
T 41200 35800 5 10 0 1 0 0 1
device=HOLE
T 41200 35800 5 10 0 0 0 0 1
footprint=STANDOFF_HEX_n4
T 41400 36400 5 10 1 1 0 4 1
refdes=H3
}
C 40700 35800 1 0 0 hole-1.sym
{
T 40700 35800 5 10 0 1 0 0 1
device=HOLE
T 40700 35800 5 10 0 0 0 0 1
footprint=STANDOFF_HEX_n4
T 40900 36400 5 10 1 1 0 4 1
refdes=H2
}
N 47600 43700 45500 43700 4
N 45500 43700 45500 41000 4
C 42200 49500 1 0 0 schottky-diode-1.sym
{
T 42200 50100 5 10 1 1 0 0 1
device=CDBM140G
T 42500 50400 5 10 1 1 0 0 1
refdes=D1
T 42200 49500 5 10 0 0 0 0 1
footprint=SOD123T
}
C 58200 49600 1 180 1 termblk2-1.sym
{
T 59200 48950 5 10 0 0 180 6 1
device=TERMBLK2
T 58600 48700 5 10 1 1 180 6 1
refdes=J2
T 58200 49600 5 10 0 0 180 0 1
footprint=TERMBLK2_200MIL
}
C 42100 47900 1 180 1 res-pack4-1.sym
{
T 42100 47900 5 10 0 0 180 6 1
slot=1
T 43100 47600 5 10 1 1 180 6 1
refdes=R1
T 42600 47600 5 10 1 1 180 6 1
value=1k
T 42100 47900 5 10 0 0 90 2 1
footprint=RPACK4-1206
}
C 53400 39100 1 270 0 resistor-1.sym
{
T 53800 38800 5 10 0 0 270 0 1
device=RESISTOR
T 53700 38800 5 10 1 1 0 0 1
refdes=R6
T 53700 38500 5 10 1 1 0 0 1
value=1k
T 53400 39100 5 10 0 0 270 0 1
footprint=0805
}
N 53500 39400 53500 39100 4
C 53300 37300 1 270 1 led-3.sym
{
T 52550 37650 5 10 1 1 0 0 1
device=WHITE
T 52750 37850 5 10 1 1 0 0 1
refdes=D6
T 53300 37300 5 10 0 0 270 0 1
footprint=0805
}
C 53400 37000 1 0 0 gnd-1.sym
C 56800 40400 1 180 1 termblk3-1.sym
{
T 57800 39750 5 10 0 0 180 6 1
device=HEADER3
T 57200 39100 5 10 1 1 180 6 1
refdes=J4
T 56800 40400 5 10 0 0 180 6 1
footprint=TERMBLK3_3p5MM
}
C 57600 40700 1 0 1 qwiic-1.sym
{
T 56600 41350 5 10 0 0 0 6 1
device=QWIIC
T 57300 42550 5 10 1 1 0 3 1
refdes=J4A
T 56800 42900 5 10 0 1 0 6 1
footprint=SM04B-SRSS
}
N 54600 42500 54600 41500 4
N 56300 42300 56700 42300 4
C 56200 42000 1 0 0 gnd-1.sym
N 56700 41500 55500 41500 4
N 55500 41500 55500 40200 4
N 56700 41100 55900 41100 4
N 55900 41100 55900 39400 4
T 57800 41500 9 10 1 0 0 0 2
This is *not* Qwiic-compatible,
it just uses the same connectors
N 56700 41900 55900 41900 4
{
T 55700 41900 5 10 1 1 0 7 1
netname=CTRL_IN
}
