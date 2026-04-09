from enum import IntEnum

class ModbusRegs(IntEnum):
    
    M1_SETPOINT     = 0
    M1_SENTIDO      = 1
    M1_VELOCIDAD_H  = 2
    M1_VELOCIDAD_L  = 3
    M1_CORRIENTE_H  = 4
    M1_CORRIENTE_L  = 5
    
    M2_SETPOINT     = 6
    M2_SENTIDO      = 7
    M2_VELOCIDAD_H  = 8
    M2_VELOCIDAD_L  = 9
    M2_CORRIENTE_H  = 10
    M2_CORRIENTE_L  = 11
    
    M3_SETPOINT     = 12
    M3_SENTIDO      = 13
    M3_VELOCIDAD_H  = 14
    M3_VELOCIDAD_L  = 15
    M3_CORRIENTE_H  = 16
    M3_CORRIENTE_L  = 17

    M4_SETPOINT     = 18
    M4_SENTIDO      = 19
    M4_VELOCIDAD_H  = 20
    M4_VELOCIDAD_L  = 21
    M4_CORRIENTE_H  = 22
    M4_CORRIENTE_L  = 23
    
    BATERIA_H       = 26
    BATERIA_L       = 27
    ARMADO_SISTEMA  = 28