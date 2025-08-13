import numpy as np
def jy_per_sr_to_jy_per_beam(jy_per_sr, beam_maj_arcsec, beam_min_arcsec):
    # Constants
    arcsec_to_rad = np.pi/(180*3600)
    factor = np.pi / (4 * np.log(2))
    # Convert arcsec to radians
    beam_maj_rad = beam_maj_arcsec * arcsec_to_rad
    beam_min_rad = beam_min_arcsec * arcsec_to_rad
    # Beam solid angle in steradians
    omega_beam_sr = factor * beam_maj_rad * beam_min_rad
    # Convert
    jy_per_beam = jy_per_sr * omega_beam_sr
    return jy_per_beam