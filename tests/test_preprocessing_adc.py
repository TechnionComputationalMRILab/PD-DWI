import numpy as np

from pd_dwi.preprocessing.adc import ADCMap


def test_adc_fit():
    slice_shape = (2, 2)
    b_values = (0, 100, 200, 400)

    syntehtic_s0 = np.array(np.random.randint(500, 2000, slice_shape), dtype=np.float64)
    syntentic_adc = np.random.randint(1, 10, slice_shape) / 1000

    S = np.stack([syntehtic_s0] + [_adc_formula(syntehtic_s0, syntentic_adc, b) for b in b_values[1:]])
    assert S.shape == (len(b_values),) + slice_shape

    adc = ADCMap(b_values)
    out_S0, out_ADC = adc._fit_slice(S)

    assert np.all(np.isclose(out_S0, syntehtic_s0))
    assert np.all(np.isclose(out_ADC, syntentic_adc))

def _adc_formula(s0, adc_model, b_value):
    return s0 * np.exp(-b_value * adc_model)