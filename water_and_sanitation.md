# Water and Sanitation Aboard the Halcyon Meridian

## Water Demand

The ship's population uses roughly 30,000 cubic metres of fresh water per day in total. This breaks down approximately as:

| Use | Share | Approximate Volume |
|---|---|---|
| Residential (drinking, cooking, washing) | ~55% | 16,500 m³/day |
| Greenhouses and aquaculture | ~25% | 7,500 m³/day |
| Industry and cooling | ~12% | 3,600 m³/day |
| Commissary and medical | ~8% | 2,400 m³/day |

Residents receive a free allowance of **60 litres per person per day**. Water above that allowance is charged at 0.4 ledger credits per 100 litres (see `economics_and_trade.md`).

## Desalination

Fresh water is produced by **reverse osmosis (RO)**. Seawater is drawn through twelve intakes on the hull, located below the waterline at about 18 m depth, where water is cleaner and less affected by surface waves.

The treatment chain is:

1. **Screening.** Coarse filters remove debris and marine life.
2. **Pretreatment.** Ultrafiltration membranes remove suspended solids. Antiscalant chemicals are added to prevent mineral deposits on membranes.
3. **Reverse osmosis.** Six RO trains, each producing about 5,000 m³ per day, push water through semi-permeable membranes at around 60 bar. Salt and most dissolved ions are rejected.
4. **Post-treatment.** Calcium and magnesium are added back to prevent corrosion in pipes and to improve taste. Chlorine is dosed to maintain residual disinfectant in the distribution network. Ultraviolet lamps provide an additional barrier.

The RO plant consumes about **3.5 kWh per cubic metre**, or roughly 105 MWh per day. Averaged over 24 hours, this is about 4.4 MW of continuous electrical load.

## Brine Discharge

Reverse osmosis produces concentrated brine, roughly twice as salty as seawater, at a rate of about 1.6 times the fresh water output. This is discharged through diffusers at about 35 m depth, behind the ship, where it spreads into the wake and dilutes rapidly.

Discharge is regulated under IMO guidelines and the Company's environmental permit. The ship monitors salinity and temperature in its wake continuously. Brine is not discharged at anchor in shallow or enclosed water.

## Storage

The ship stores about **220,000 cubic metres** of fresh water in forty tanks, most of them in the double bottom and known collectively as the **Water Vault**. This is roughly seven days of total demand, sized to cover:
- Loss of the RO plant during a storm, when intakes can aerate or pick up sediment and must be shut down
- Equipment failure
- Contamination events that require shutting down a tank for testing

Storage tanks are coated with epoxy linings. Water in storage is circulated continuously to prevent stagnation. Temperature and conductivity are logged in each tank.

## Water Quality

Water quality is held to WHO drinking-water guidelines. The Medical Office and the Water Department run continuous sensors for:
- Total organic carbon
- Electrical conductivity (a proxy for dissolved salts)
- Chlorine residual
- *E. coli* and coliform bacteria, through periodic sampling

Results are reported to the City Operations Centre in real time. A sample failure triggers an immediate isolation of the affected distribution zone and a boil-water advisory.

## Greywater and Recycling

About 90 percent of water used on the ship is recycled. Greywater from showers, sinks, and laundry is treated in **membrane bioreactors (MBRs)**, which combine biological treatment with ultrafiltration. The recycled water is used for toilet flushing, greenhouse irrigation, and industrial cooling.

Blackwater from toilets is sent to anaerobic digesters, where bacteria break down solids and produce methane-rich biogas. The biogas is burned in boilers to produce heat and a small amount of electricity, about 0.5 MW.

## Toilets and Sanitation

The ship uses **vacuum toilets**, the same design used in aircraft and some cruise ships. A flush uses about 1 litre, compared with 6 litres for a conventional toilet. Vacuum systems are less likely to leak and reduce the volume of blackwater.

Hot water is circulated at 60 degrees Celsius in a continuous loop to prevent *Legionella* growth. Hot-water outlets are tested weekly. Cold-water systems are kept below 20 degrees Celsius.

Public showers and laundries are located on the residential terraces. Each person is entitled to one shower per day within the free allowance.

## Storm Conditions

In heavy seas, the intake pumps may trip automatically because of excessive pitch, roll, or aeration. When this happens, the Water Department draws on the Water Vault while the RO plant is offline. Storage is sized to handle a 72-hour storm event.

## Waste Management

Solid waste is sorted at source into organic, recyclable, and residual categories. Organic waste goes to the composting and insect-rearing halls (see `food_and_agriculture.md`). Recyclables are baled and stored for port disposal. Residual waste is incinerated in boilers that also supply heat to the residential decks.

Hazardous waste, including medical waste, batteries, and used chemicals, is stored in sealed containers and offloaded at port.

## Disease Control

Norovirus and other waterborne illnesses are the main public-health risks. When a cluster of cases is detected, the Medical Office:
- Isolates affected residents in the Quarantine Ward
- Chlorinates the implicated water zone and increases residual chlorine
- Restricts shared facilities such as laundries and public showers until testing is complete

Outbreaks are reported to the Chief Medical Officer and the Master.
