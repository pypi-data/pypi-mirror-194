---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.1
  kernelspec:
    display_name: Python 3 Quantify Env
    language: python
    name: qenv
---

# Qblox Quantify validation notebook

```{seealso}
Download the notebook: {download}`quantify-validate-qblox.md`
```


## Setup

```python
!pip show quantify-core quantify-scheduler
```

### Enable DeprecationWarnings

```python
import warnings

warnings.simplefilter("default")
```

### Connect to Cluster

```python
import pprint
import traceback

import numpy as np
from quantify_core.data import handling as dh
from quantify_core.measurement.control import MeasurementControl
from quantify_scheduler.helpers.mock_instruments import MockLocalOscillator
from quantify_scheduler.instrument_coordinator import InstrumentCoordinator
from quantify_scheduler.instrument_coordinator.components.qblox import ClusterComponent

from qblox_instruments import Cluster, ClusterType
from qcodes import Instrument
from qcodes.utils import validators

dh.set_datadir(dh.default_datadir())
```

```python
Instrument.close_all()
meas_ctrl = MeasurementControl("meas_ctrl")
ic = InstrumentCoordinator("ic")

try:
    cluster = Cluster("cluster", "192.168.0.2")
except:
    traceback.print_exc()
    print("Falling back to Dummy device")
    cluster = Cluster(
        "cluster",
        dummy_cfg={
            1: ClusterType.CLUSTER_QCM,
            2: ClusterType.CLUSTER_QRM,
            3: ClusterType.CLUSTER_QCM_RF,
            4: ClusterType.CLUSTER_QRM_RF,
        },
    )

ic_cluster = ClusterComponent(cluster)
ic.add_component(ic_cluster)

lo0 = MockLocalOscillator("lo0")
lo1 = MockLocalOscillator("lo1")

# Always picks the first module of a certain type, and ignores the others of same type!
qcm_rf, qrm_rf, qcm, qrm = [None] * 4
for module in cluster.modules:
    try:
        if module.is_rf_type:
            if module.is_qcm_type:
                if qcm_rf is None:
                    qcm_rf = module
            else:
                if qrm_rf is None:
                    qrm_rf = module
        else:
            if module.is_qcm_type:
                if qcm is None:
                    qcm = module
            else:
                if qrm is None:
                    qrm = module
    except KeyError:
        continue

pprint.pprint(ic_cluster.instrument.get_idn())
print()

print(f"qcm    => {qcm}\nqrm    => {qrm}\nqcm_rf => {qcm_rf}\nqrm_rf => {qrm_rf}")
```

<!-- #region tags=[] -->
### Device Configuration
<!-- #endregion -->

```python
from quantify_scheduler.device_under_test.quantum_device import QuantumDevice
from quantify_scheduler.device_under_test.transmon_element import BasicTransmonElement

quantum_device = QuantumDevice("quantum_device")
q0, q1 = BasicTransmonElement("q0"), BasicTransmonElement("q1")

quantum_device.add_element(q0)
quantum_device.add_element(q1)

quantum_device.instr_measurement_control(meas_ctrl.name)
quantum_device.instr_instrument_coordinator(ic.name)
```

```python
q0.clock_freqs.f01(7.3e9)
q0.clock_freqs.f12(7.0e9)
q0.clock_freqs.readout(1.9e9)  # Clock freq of the Measure readout pulse
q0.measure.acq_delay(100e-9)
q0.measure.acq_channel(0)
q0.measure.pulse_amp(0.2)

q1.clock_freqs.f01(7.25e9)
q1.clock_freqs.f12(6.89e9)
q1.clock_freqs.readout(8.3e9)
q1.measure.acq_delay(100e-9)
q1.measure.acq_channel(1)
q1.measure.pulse_amp(0.05)
```

### Hardware Configuration

```python tags=[]
hardware_cfg_baseband = {
    "backend": "quantify_scheduler.backends.qblox_backend.hardware_compile",
    "cluster": {
        "ref": "internal",
        "instrument_type": "Cluster",
    },
    "lo0": {"instrument_type": "LocalOscillator", "frequency": 1.7e9, "power": 17},
    "lo1": {"instrument_type": "LocalOscillator", "frequency": None, "power": 17},
}

if qcm is not None:
    hardware_cfg_baseband["cluster"][f"cluster_module{qcm.slot_idx}"] = {
        "instrument_type": "QCM",
        "complex_output_0": {
            "lo_name": "lo0",
            "dc_mixer_offset_I": 0.0,
            "dc_mixer_offset_Q": 0.0,
            "portclock_configs": [
                {
                    "mixer_amp_ratio": 0.9998,
                    "mixer_phase_error_deg": -4.1,
                    "port": "q0:mw",
                    "clock": "q0.01",
                    "interm_freq": None,
                }
            ],
        },
    }

if qrm is not None:
    hardware_cfg_baseband["cluster"][f"cluster_module{qrm.slot_idx}"] = {
        "instrument_type": "QRM",
        "complex_output_0": {
            "lo_name": "lo1",
            "dc_mixer_offset_I": 0.0,
            "dc_mixer_offset_Q": 0.0,
            "portclock_configs": [
                {
                    "mixer_amp_ratio": 0.9998,
                    "mixer_phase_error_deg": -4.1,
                    "port": "q0:res",
                    "clock": "q0.ro",
                    "interm_freq": 200e6,
                },
                {
                    "mixer_amp_ratio": 0.9998,
                    "mixer_phase_error_deg": -4.1,
                    "port": "q1:res",
                    "clock": "q1.ro",
                    "interm_freq": None,
                },
            ],
        },
    }

hardware_cfg_rf = {
    "backend": "quantify_scheduler.backends.qblox_backend.hardware_compile",
    "cluster": {
        "ref": "internal",
        "instrument_type": "Cluster",
    },
}

if qcm_rf is not None:
    hardware_cfg_rf["cluster"][f"cluster_module{qcm_rf.slot_idx}"] = {
        "instrument_type": "QCM_RF",
        "complex_output_0": {
            "lo_freq": 2.0e9,  # LO freq of RF modules: 2e9 <= x <= 18e9
            "dc_mixer_offset_I": 0.0,
            "dc_mixer_offset_Q": 0.0,
            "portclock_configs": [
                {
                    "mixer_amp_ratio": 0.9998,
                    "mixer_phase_error_deg": -4.1,
                    "port": "q0:mw",
                    "clock": "q0.01",
                    "interm_freq": None,
                }
            ],
        },
    }

if qrm_rf is not None:
    hardware_cfg_rf["cluster"][f"cluster_module{qrm_rf.slot_idx}"] = {
        "instrument_type": "QRM_RF",
        "complex_output_0": {
            "lo_freq": 2e9,
            "dc_mixer_offset_I": 0.0,
            "dc_mixer_offset_Q": 0.0,
            "portclock_configs": [
                {
                    "mixer_amp_ratio": 0.9998,
                    "mixer_phase_error_deg": -4.1,
                    "port": "q0:res",
                    "clock": "q0.ro",
                    "interm_freq": None,
                },
                {
                    "mixer_amp_ratio": 0.9998,
                    "mixer_phase_error_deg": -4.1,
                    "port": "q1:res",
                    "clock": "q1.ro",
                    "interm_freq": None,
                },
            ],
        },
    }
```

### Schedule: Simple Rabi

```python
from quantify_scheduler import Schedule
from quantify_scheduler.operations.gate_library import Measure, Reset
from quantify_scheduler.operations.pulse_library import DRAGPulse
from quantify_scheduler.resources import ClockResource

rabi_pulse_amps = np.linspace(0, 0.25, 10)  # Trigger level: 15-20 mV


def rabi_sched(
    qrm_only: bool,
    repetitions: int,
    pulse_amps: np.ndarray = rabi_pulse_amps,
    clock_freq: float = 1.8e9,  # Below 2e9 to be able to visualize on oscilliscope
) -> Schedule:
    sched = Schedule("Simple Rabi experiment", repetitions)

    port = "q0:mw"
    clock = "q0.01"
    if qrm_only:
        port = "q0:res"
        clock = "q0.ro"

    sched.add_resources([ClockResource(clock, clock_freq)])

    for acq_idx, amp in enumerate(pulse_amps):
        sched.add(Reset("q0"))
        sched.add(
            DRAGPulse(
                G_amp=amp,
                D_amp=0,
                phase=0,
                duration=160e-9,
                port=port,
                clock=clock,
            )
        )
        sched.add(Measure("q0", acq_index=acq_idx))

    return sched


sched = rabi_sched
print(f"sched: {sched}")
```

### Schedule: Simple Trace

```python
from quantify_scheduler import Schedule
from quantify_scheduler.operations.gate_library import Measure, Reset
from quantify_scheduler.operations.pulse_library import DRAGPulse
from quantify_scheduler.resources import ClockResource


def simple_trace_sched(
    qrm_only: bool,
    repetitions: int,
    pulse_amp: float = 0.2,
    clock_freq: float = 1.8e9,  # Below 2e9 to be able to visualize on oscilliscope
) -> Schedule:
    sched = Schedule("Simple trace schedule", repetitions)

    port = "q0:mw"
    clock = "q0.01"
    if qrm_only:
        port = "q0:res"
        clock = "q0.ro"

    sched.add_resources([ClockResource(clock, clock_freq)])

    sched.add(Reset("q0"))
    sched.add(Measure("q0", acq_index=0, acq_protocol="Trace"))
    sched.add(
        DRAGPulse(
            G_amp=pulse_amp,
            D_amp=0,
            phase=0,
            duration=160e-9,
            port=port,
            clock=clock,
        )
    )

    return sched


sched = simple_trace_sched
print(f"sched: {sched}")
```

## Prepare validation


### Prep baseband validation (QRM + QCM)

scope C1 <- QCM O1 (QCM optional)  
scope C2 <- QRM O1, set trigger to C2 (trigger level: see schedule)

For testing Trace acquisition:  
QRM I2 <- QRM 02  
keep trigger on C2

```python
cluster.reset()

hardware_cfg = hardware_cfg_baseband

qrm_only = qcm is None
```

### Prep RF validation (QRM-RF + QCM-RF)

scope C1 <- QCM-RF O1 (QCM-RF optional)   
scope C2 <- QRM-RF O1, set trigger to C2 (trigger level: see schedule)

For testing Trace acquisition:  
QRM-RF I1 <- QRM-RF O1  
if QCM-RF present, set trigger to C1 (trigger level: see schedule)

```python
cluster.reset()

hardware_cfg = hardware_cfg_rf

qrm_only = qcm_rf is None
```

## Run validation

```python
quantum_device.hardware_config(hardware_cfg)

label = f'Validating {"baseband" if hardware_cfg is hardware_cfg_baseband else "RF" if hardware_cfg is hardware_cfg_rf else "<not set>"}'
print(f"===> {label} <===")
```

### Run using MeasurementControl


#### Simple Rabi

|  QRM only (no QCM) | QRM-RF + QCM-RF | QRM-RF only (no QCM-RF) |
|--------------------|-----------------|-------------------------|
|![](images/QRM_only_-_Rabi.JPEG)|![](images/QRM-RF+QCM-RF_-_Rabi.JPEG)|![](images/QRM-RF_only_-_Rabi.JPEG)|

```python
from quantify_scheduler.gettables import ScheduleGettable

from qcodes.instrument.parameter import ManualParameter

# Configure the settable
rabi_pulse_amp = ManualParameter(
    "rabi_pulse_amp", label="Rabi pulse amplitude", unit="Hz"
)
rabi_pulse_amp.batched = True

quantum_device.cfg_sched_repetitions(2)

# Configure the gettable
rabi_gettable = ScheduleGettable(
    quantum_device=quantum_device,
    schedule_function=rabi_sched,
    schedule_kwargs={"qrm_only": qrm_only, "pulse_amps": rabi_pulse_amp},
    real_imag=True,
    batched=True,
)

# Configure measurement control
meas_ctrl.settables(rabi_pulse_amp)
meas_ctrl.setpoints(rabi_pulse_amps)
meas_ctrl.gettables(rabi_gettable)

# Run!
dataset = meas_ctrl.run(f"{label} on Simple Rabi")

compiled_schedule = rabi_gettable.compiled_schedule
```

```python
dataset
```

```python
pprint.pprint(quantum_device.hardware_config())
```

<!-- #region tags=[] -->
#### Simple Trace
<!-- #endregion -->

```python
## TODO: remove section
##
## Still here to
## - document the assert (len(vals)) == 1 error
## - as well as the qcodes validated param + batched not working

from quantify_scheduler.gettables import ScheduleGettable

# Configure the gettable
trace_gettable = ScheduleGettable(
    quantum_device=quantum_device,
    schedule_function=simple_trace_sched,
    schedule_kwargs={"qrm_only": qrm_only},
)

# Configure measurement control
meas_ctrl.settables(q0.measure.pulse_amp)
meas_ctrl.setpoints(np.linspace(0, 0.25, 10))
meas_ctrl.gettables(trace_gettable)

# Run!
dataset = meas_ctrl.run(f"{label} on Simple Trace")

compiled_schedule = trace_gettable.compiled_schedule
```

### Run using InstrumentCoordinator

```python
sched = sched(qrm_only=qrm_only, repetitions=1)
```

```python
from quantify_scheduler.backends.graph_compilation import SerialCompiler

device_compile = SerialCompiler(name="Device compile")
compiled_schedule = device_compile.compile(
    schedule=sched, config=quantum_device.generate_compilation_config()
)

compiled_schedule
```

```python
ic.prepare(compiled_schedule)
```

```python
ic.start()
```

#### Simple Trace

|  QRM only (no QCM) | QRM-RF + QCM-RF | QRM-RF only (no QCM-RF) |
|--------------------|-----------------|-------------------------|
|![](images/QRM_only_-_Trace.JPEG)|![](images/QRM-RF+QCM-RF_-_Trace.JPEG)|![](images/QRM-RF_only_-_Trace.JPEG)|

```python
acquisitions = ic.retrieve_acquisition()
acquisitions
```

```python
qrm.get_acquisitions(0)
```

```python
qrm_rf.get_acquisitions(0)
```

### Recalibrate ADC 
For removing ADC discretization noise; done automatically on cluster boot and after running 20 min to account for temperature change

```python
# QRM
cluster.start_adc_calib(qrm.slot_idx)
```

```python
# QRM-RF
cluster.start_adc_calib(qrm_rf.slot_idx)
```

## Plots

<!-- #region tags=[] -->
### Circuit diagram
<!-- #endregion -->

```python
_, ax = sched.plot_circuit_diagram()
ax.set_xlim(-0.5, 9.5)
for t in ax.texts:
    if t.get_position()[0] > 9.5:
        t.set_visible(False)
```

### Pulse diagram

```python tags=[]
compiled_schedule.plot_pulse_diagram(plot_backend="plotly")
```

### Trace plot

|  QRM only (no QCM) | QRM-RF + QCM-RF | QRM-RF only (no QCM-RF) |
|--------------------|-----------------|-------------------------|
|![](images/QRM_only_-_Trace_plot.png)|![](images/QRM-RF+QCM-RF_-_Trace_plot.png)|![](images/QRM-RF_only_-_Trace_plot.png)|

```python
import matplotlib.pyplot as plt

for _, trace in acquisitions.items():
    i_trace, q_trace = trace

plt.plot(i_trace[:1400], label="I")
plt.plot(q_trace[:1400], label="Q")
plt.xlabel("Time (ns)")
plt.ylabel("Complex Amplitude")
plt.legend()
```

<!-- #region -->
In case of ADC discretization noise, **[Recalibrate ADC](#Recalibrate-ADC)** and re-run


|  QRM only (no QCM) | QRM-RF only (no QCM-RF) |
|--------------------|-------------------------|
|![](images/QRM_only_-_Trace_plot_ADC_noise.png)|![](images/QRM-RF_only_-_Trace_plot_ADC_noise.png)|
<!-- #endregion -->

## Inspect


### Frequency settings

```python
def assert_clock_LO_IF(clock, LO, IF, magn=1e9):
    eq_str = f"clock:{clock/magn} == LO:{LO/magn} + IF:{IF/magn}"
    assert clock == LO + IF, eq_str
    print(eq_str)
```

```python
if qcm is not None:
    print("QCM:")
    assert_clock_LO_IF(
        clock=compiled_schedule.data["resource_dict"]["q0.01"].data["freq"],
        LO=lo0.frequency(),
        IF=qcm.sequencer0.nco_freq(),
    )

if qrm is not None:
    print("QRM:")
    assert_clock_LO_IF(
        clock=q0.clock_freqs.readout(),
        LO=lo1.frequency(),
        IF=qrm.sequencer0.nco_freq(),
    )
```

```python
if qcm_rf is not None:
    print("QCM_RF:")
    assert_clock_LO_IF(
        clock=compiled_schedule.data["resource_dict"]["q0.01"].data["freq"],
        LO=qcm_rf.out0_lo_freq(),
        IF=qcm_rf.sequencer0.nco_freq(),
    )

if qrm_rf is not None:
    print("QRM_RF:")
    assert_clock_LO_IF(
        clock=q0.clock_freqs.readout(),
        LO=qrm_rf.out0_in0_lo_freq(),
        IF=qrm_rf.sequencer0.nco_freq(),
    )
```

<!-- #region jp-MarkdownHeadingCollapsed=true tags=[] -->
### Inspect compiled instructions
<!-- #endregion -->

```python
compiled_schedule.compiled_instructions
```

```python
module = qrm

seq_fn = compiled_schedule.data["compiled_instructions"][cluster.name][module.name][
    "seq0"
]["seq_fn"]

import json

with open(seq_fn) as json_file:
    seq = json.load(json_file)

pprint.pprint(seq["program"])
```

## Stop, print status


### Stop sequencers

```python
qcm.stop_sequencer()
qrm.stop_sequencer()

qcm_rf.stop_sequencer()
qrm_rf.stop_sequencer()
```

### Stop cluster

```python
ic_cluster.stop()
```

### Optional reset

```python
cluster.reset()
```

### Print status of sequencers

```python
print(f"QCM get_sequencer_state: {qcm.get_sequencer_state(0)}")
print(f"QRM get_sequencer_state: {qrm.get_sequencer_state(0)}")
```

```python
print(f"QCM-RF get_sequencer_state: {qcm_rf.get_sequencer_state(0)}")
print(f"QRM-RF get_sequencer_state: {qrm_rf.get_sequencer_state(0)}")
```

### Print overview of instrument parameters

```python
print("QCM snapshot:")
qcm.print_readable_snapshot(update=True)
```

```python
print("QRM snapshot:")
qrm.print_readable_snapshot(update=True)
```

```python
print("QCM-RF snapshot:")
qcm_rf.print_readable_snapshot(update=True)
```

```python
print("QRM-RF snapshot:")
qrm_rf.print_readable_snapshot(update=True)
```
