---
name: "ground-stations"
category: "space-tech"
version: "1.0.0"
tags: ["space-tech", "ground-stations", "antenna", "signal-processing"]
---

# Ground Stations Toolkit

## Overview

The Ground Stations module provides a complete computational framework for designing, operating, and analyzing satellite ground station systems. It covers antenna tracking geometry, signal processing chain modeling, telemetry and telecommand link analysis, Doppler compensation, rain fade mitigation, polarization tracking, and multi-station network coordination. The module serves both the design engineer who needs to size an antenna system and link budget, and the operations engineer who needs to schedule passes, predict signal quality, and coordinate handovers between stations in a global network.

The antenna tracking subsystem computes azimuth and elevation pointing angles, slew rate requirements, and tracking loop performance for various antenna mount types (az-el, X-Y, equatorial). It includes models for antenna gain patterns, sidelobe levels, and pointing loss as a function of off-axis angle. The signal processing chain models the complete receive and transmit signal path — from antenna through LNA, downconversion, digitization, demodulation, and decoding — with realistic noise figure and signal-to-noise ratio calculations at each stage.

The link analysis subsystem computes end-to-end link margins including free-space path loss, atmospheric absorption (ITU-R P.676), rain attenuation (ITU-R P.618), scintillation, multipath, and polarization mismatch. Doppler compensation models include both the geometric Doppler shift and the rate of change, enabling pre-compensation tables for receiver frequency tracking. The multi-station coordination module supports automatic handover scheduling, load balancing, and failover for continuous-contact missions.

## Core Capabilities

- **Antenna Tracking**: Az-el, X-Y, and equatorial mount geometry; tracking rate computation; pointing loss estimation; auto-tracking loop modeling; antenna pattern visualization
- **Signal Processing Chain**: Full transmit/receive chain modeling with noise figure cascade, SNR computation, bandwidth optimization, and dynamic range analysis
- **Telemetry Decoding**: PCM/FM, BPSK/QPSK/8PSK modulation modeling; bit error rate computation; coding gain for convolutional, Reed-Solomon, and LDPC codes; data throughput optimization
- **Doppler Compensation**: Geometric Doppler shift computation for LEO/GEO/MEO; Doppler rate estimation; pre-compensation table generation; two-way ranging Doppler correction
- **Link Margin Analysis**: End-to-end link budget with atmospheric, rain, scintillation, and multipath losses; availability computation for rain fade statistics
- **Ground Station Network**: Multi-station pass scheduling, automatic handover, load balancing, failover logic, and utilization optimization
- **Rain Fade Mitigation**: ITU-R P.618 rain attenuation model, site diversity gain computation, adaptive coding and modulation (ACM) thresholds
- **Polarization Tracking**: Faraday rotation compensation for linear polarization, circular polarization axial ratio analysis, polarization isolation assessment

## Usage Examples

### Antenna Tracking Geometry

```python
from ground_stations import AntennaTracker, AntennaMount, AntennaConfig

tracker = AntennaTracker(
    station_lat_deg=40.0,
    station_lon_deg=-75.0,
    station_alt_m=100.0,
    antenna=AntennaConfig(
        mount_type=AntennaMount.AZ_EL,
        aperture_m=7.0,
        frequency_ghz=8.0,
        gain_dbi=48.0,
        beamwidth_deg=0.35,
        max_slew_rate_deg_s=2.0,
    ),
)

# Satellite position in ECI (meters)
sat_eci = [1200000.0, -4500000.0, 4200000.0]
pointing = tracker.compute_pointing(sat_eci)
print(f"Azimuth:       {pointing.azimuth_deg:.2f}°")
print(f"Elevation:     {pointing.elevation_deg:.2f}°")
print(f"Slew rate:     {pointing.slew_rate_deg_s:.2f}°/s")
print(f"Pointing loss: {pointing.pointing_loss_db:.3f} dB")
print(f"Range:         {pointing.range_km:.1f} km")
```

### Signal Processing Chain

```python
from ground_stations import SignalChain, ChainComponent

chain = SignalChain(frequency_ghz=8.15, bandwidth_mhz=50.0)
chain.add_component(ChainComponent("Antenna", gain_dbi=48.0, noise_temp_k=30.0))
chain.add_component(ChainComponent("Feeder", gain_db=-0.5, noise_figure_db=0.3))
chain.add_component(ChainComponent("LNA", gain_db=55.0, noise_figure_db=0.8))
chain.add_component(ChainComponent("Mixer", gain_db=-6.0, noise_figure_db=8.0))
chain.add_component(ChainComponent("IF Amp", gain_db=30.0, noise_figure_db=3.0))
chain.add_component(ChainComponent("Demodulator", gain_db=0.0, noise_figure_db=2.0))

result = chain.compute()
print(f"System noise temperature: {result.system_noise_temp_k:.1f} K")
print(f"System noise figure:      {result.system_noise_figure_db:.2f} dB")
print(f"G/T:                      {result.g_over_t_db:.2f} dB/K")
print(f"Total system gain:        {result.total_gain_db:.1f} dB")
print(f"Dynamic range:            {result.dynamic_range_db:.1f} dB")
```

### Doppler Compensation

```python
from ground_stations import DopplerCompensator, SatelliteState

doppler = DopplerCompensator(frequency_hz=8150e6)

sat_states = [
    SatelliteState(time_s=0,    position_eci=[7000000, 0, 0],       velocity_eci=[0, 7500, 0]),
    SatelliteState(time_s=10,   position_eci=[7000000, 75000, 0],  velocity_eci=[-100, 7500, 0]),
    SatelliteState(time_s=60,   position_eci=[7000000, 450000, 0], velocity_eci=[-500, 7300, 0]),
    SatelliteState(time_s=300,  position_eci=[7000000, 2250000, 0],velocity_eci=[-1000, 6500, 0]),
    SatelliteState(time_s=600,  position_eci=[6900000, 4500000, 0],velocity_eci=[-200, 5000, 0]),
]

table = doppler.generate_compensation_table(sat_states, ground_lat=40.0, ground_lon=-75.0)
for entry in table[:5]:
    print(f"T+{entry['time_s']:6.0f}s: "
          f"Δf={entry['doppler_shift_hz']:.1f} Hz, "
          f"rate={entry['doppler_rate_hz_s']:.2f} Hz/s, "
          f"range={entry['range_km']:.1f} km")
```

### Link Margin Analysis

```python
from ground_stations import LinkMarginAnalyzer, AtmosphereModel

analyzer = LinkMarginAnalyzer(
    frequency_ghz=8.15,
    data_rate_mbps=150.0,
    modulation="QPSK",
    coding_rate=0.75,
    satellite_eirp_dbw=20.0,
    satellite_antenna_gain_dbi=18.0,
    ground_antenna_gain_dbi=48.0,
    ground_noise_temp_k=50.0,
)

result = analyzer.compute_link_margin(
    range_km=900,
    elevation_deg=45.0,
    atmosphere=AtmosphereModel.ITUR_P676,
    rain_rate_mm_hr=12.0,
    pointing_loss_db=0.5,
    polarization_loss_db=0.3,
)

print(f"Total link margin: {result.margin_db:.2f} dB")
print(f"Available Eb/N0:   {result.eb_n0_db:.1f} dB")
print(f"Availability:      {result.availability_pct:.2f}%")
print(f"Required Eb/N0:    {result.required_eb_n0_db:.1f} dB")
print(f"Rain fade margin:  {result.rain_fade_db:.2f} dB")
```

### Multi-Station Network Coordination

```python
from ground_stations import GroundStationNetwork

network = GroundStationNetwork()
network.add_station("Kourou",    lat=5.2,   lon=-52.7,  min_elev=5.0, bandwidth_mhz=500)
network.add_station("Malindi",   lat=-2.99, lon=40.2,   min_elev=5.0, bandwidth_mhz=200)
network.add_station("Fairbanks", lat=64.85, lon=-147.7, min_elev=5.0, bandwidth_mhz=500)
network.add_station("Svalbard",  lat=78.23, lon=15.46,  min_elev=5.0, bandwidth_mhz=1000)

schedule = network.schedule_passes(
    satellite_tle="1 25544U ...",
    planning_window_days=7,
    data_volume_required_gb=50.0,
)

for contact in schedule:
    print(f"  {contact['station']}: {contact['start']} — {contact['end']}  "
          f"max_el={contact['max_elevation']:.1f}°  "
          f"data={contact['data_volume_gb']:.1f}GB")
```

## Best Practices

1. **Always include atmospheric absorption in link budgets for frequencies above 4 GHz.** At X-band and above, atmospheric attenuation can exceed 1 dB at low elevation angles — ignoring this produces optimistic link margins that fail in operations.
2. **Doppler compensation tables should be generated with at least 1-second resolution for LEO passes.** The Doppler rate at L-band for a 500 km altitude pass can exceed 500 Hz/s — coarser resolution produces noticeable tracking errors during the high-rate portions of the pass.
3. **When sizing ground station antennas, always include the pointing loss budget in the gain requirement.** A 7-meter antenna at X-band has a 0.35° beamwidth — even a well-designed tracking system introduces 0.2–0.5 dB of pointing loss that must be accounted for.
4. **Rain fade mitigation should use the local ITU-R P.837 rainfall statistics, not a single rain rate value.** The link availability requirement (e.g., 99.5%) must be matched to the correct percentile of the local rain rate distribution.
5. **For ground station network operations, implement automatic failover with a maximum handover time of 30 seconds.** Longer handover times result in data loss that may exceed the retransmission buffer capacity of the spacecraft.
6. **Signal processing chain design should target at least 3 dB of implementation margin** beyond the theoretical SNR requirement. Component aging, temperature drift, and cable degradation all erode the noise figure over the station lifetime.
7. **Polarization isolation between co-located antennas should be verified with measured cross-polarization discrimination (XPD) values**, not just the theoretical feed pattern. Structural scattering and feed misalignment typically reduce XPD by 5–10 dB from the ideal.
8. **Ground station automation should include real-time signal quality monitoring with automatic data rate adaptation.** When rain fade reduces the link margin below the ACM switching threshold, the system should autonomously reduce the data rate rather than lose the link entirely.

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `coordinate_frame` | `str` | `"ITRF"` | Reference frame: `ITRF`, `J2000`, or `TEME` |
| `atmosphere_model` | `str` | `"ITUR_P676"` | Atmospheric attenuation model |
| `rain_model` | `str` | `"ITUR_P618"` | Rain attenuation model |
| `tracking_loop_bw_hz` | `float` | `2.0` | Auto-tracking servo bandwidth |
| `doppler_resolution_s` | `float` | `1.0` | Time resolution for Doppler compensation tables |
| `min_pass_elevation_deg` | `float` | `5.0` | Minimum elevation for usable pass contact |

## Key Formulas

- **Free Space Path Loss**: `FSPL(dB) = 20·log₁₀(4π·d·f/c)` where d = range, f = frequency, c = speed of light
- **System Noise Temperature**: `T_sys = T_ant + T_rec + T_background` (sum of antenna, receiver, and background noise)
- **G/T Ratio**: `G/T(dB/K) = G_ant(dBi) - 10·log₁₀(T_sys)` — figure of merit for receive sensitivity
- **Link Margin**: `M = EIRP + G_rx - FSPL - L_atm - L_rain - L_point - L_pol - N₀ - R - SNR_req` (all in dB)
- **Doppler Shift**: `Δf = f₀ · (v_r / c)` where v_r = relative radial velocity between satellite and ground station
- **Rain Attenuation (ITU-R P.618)**: `A_rain = k · R^α · d_eff` where R = rain rate (mm/hr), k and α are frequency/polarization coefficients, d_eff = effective path length through rain
- **Antenna Pointing Loss**: `L_point = 12·(θ_off / θ_3dB)² dB` for θ_off < θ_3dB (parabolic antenna approximation)

## Integration Patterns

The ground station toolkit integrates with satellite-systems for pass prediction and link budget coordination, with mission-planning for contact scheduling and resource allocation, and with space-data for real-time space weather inputs that affect link availability calculations.

## Related Modules

- [aerospace-engineering](../aerospace-engineering/GROK.md) — Propulsion, orbital mechanics, aerodynamics
- [satellite-systems](../satellite-systems/GROK.md) — ADCS, constellation design, link budgets
- [mission-planning](../mission-planning/GROK.md) — Scheduling, launch windows, resource allocation
- [space-data](../space-data/GROK.md) — Space weather, telemetry data analysis
