import numpy as np
import lf.txrx as txrx
import lf.utils as utils
import cmath
import math

def to_r_phi(amp_ns,amp_ew,phase_ns,phase_ew,tx,rx):
#Convert field from NS/EW to phi/r coordinates
#Parameters:
#	amp_ns : float
#		B field narrowband amplitude in N/S direction
#	amp_ew : float
#		B field narrowband amplitude in E/W direction
#	phase_ns: float
#		B field narrowband phase (radians) in N/S direction
#	phase_ew: float
#		B field narrowband phase (radians) in E/W direction
#	tx: str
#		Transmitter call sign
#	rx: str
#		Receiver abbreviation
#Returns:
#	amp_r : float
#		B field amplitude in radial direction
#	amp_phi : float
#		B field amplitude in transverse (phi) direction
#	phase_r : float
#		B field phase in r direction
#	phase_phi : float
#		B field phase in phi direction
    azimuth = math.radians(utils.get_azimuth(rx,tx))
    #Convert fields to complex form
    B_ns = amp_ns*cmath.exp(1j*phase_ns)
    B_ew = -1*amp_ew*cmath.exp(1j*phase_ew)
    #Perform rotation
    B_r = cmath.cos(azimuth+math.pi/2)*B_ns
    B_r += cmath.sin(azimuth+math.pi/2)*B_ew
    B_phi = -1*cmath.sin(azimuth+math.pi/2)*B_ns
    B_phi += cmath.cos(azimuth+math.pi/2)*B_ew
    amp_r = abs(B_r)
    phase_r = cmath.phase(B_r)
    amp_phi = abs(B_phi)
    phase_phi = cmath.phase(B_phi)
    return amp_r,amp_phi,phase_r,phase_phi

def to_ellipse(amp_r,amp_phi,phase_r,phase_phi):
#Generates converts r/phi fields to polarization ellipse
#Calculation method from Gross (2018)
#Parameters:
#	amp_r : float
#		B field amplitude in radial direction
#	amp_phi : float
#		B field amplitude in transverse (phi) direction
#	phase_r : float
#		B field phase in r direction
#	phase_phi : float
#		B field phase in phi direction
#Returns:
#	amp_maj : float
#		B field component along ellipse semimajor axis
#	amp_min : float
#		B field component along ellipse minor axis
#	tilt_angle : float
#		Tilt angle of the ellipse with respect to r/phi axis
#	start_phase :float
#		Phase value when B(t) = B_maj
    B_r = amp_r*cmath.exp(1j*phase_r)
    B_phi = amp_phi*cmath.exp(1j*phase_phi)
    #Calculate tilt angle
    psi_0 = cmath.phase(-B_r/B_phi)
    gamma = amp_r/amp_phi
    tilt_angle = (1/2)*math.atan((2*gamma/(1-gamma**2))*math.cos(psi_0))
    B_min = math.cos(tilt_angle)*B_r -math.sin(tilt_angle)*B_phi
    B_maj = math.sin(tilt_angle)*B_r +math.cos(tilt_angle)*B_phi
    start_phase = -1*cmath.phase(B_maj)
    amp_maj = abs(B_maj)
    amp_min = abs(B_min)
    return amp_maj,amp_min,tilt_angle,start_phase

