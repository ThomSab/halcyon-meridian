# Communications and the Intranet Aboard the Halcyon Meridian

## The Basic Constraint

The ship is a long way from shore for most of its voyage. A typical crossing puts it more than 1,000 km from land for several days at a time, so communications depend on satellite links. The total capacity is about **8 Gbps**, shared across the whole ship (see `daily_life_and_routines.md`). This is a tiny amount per person, which shapes almost everything about how residents communicate.

## Satellite Links

The ship has three types of connection:

1. **Low-Earth-orbit (LEO) broadband**, which provides most of the bandwidth, with latency of 30 to 60 milliseconds.
2. **Medium-Earth-orbit (MEO) links**, which provide backup capacity and are used for safety services. Latency is higher.
3. **Maritime safety and distress channels**, which are always kept open and cannot be used for other traffic.

The LEO antennas are on the superstructure, with redundant terminals on both sides. The ship's communications officers monitor signal quality and switch traffic automatically if one link degrades.

## Traffic Priorities

Traffic is managed by a priority system:

| Priority | Traffic | Share of Bandwidth |
|---|---|---|
| 1 | Safety, navigation, and distress | Reserved, usually under 2% |
| 2 | Medical and telemedicine | About 8% |
| 3 | Company operations, ledger, and freight | About 25% |
| 4 | Board reporting and regulatory data | About 5% |
| 5 | Residents' messaging and news | About 40% |
| 6 | Streaming, media updates, and personal browsing | Remainder, rate-limited |

Residents' traffic is limited per person. Personal browsing is metered and priced in ledger credits (see `economics_and_trade.md`), and heavy use is throttled during busy hours.

## The Intranet

Most daily communication takes place on the **intranet**, a local network that runs on the ship's servers. It includes:

- Messaging, with text, voice, and short video, all stored locally
- The Halcyon Gazette and official notices (see `arts_media_and_entertainment.md`)
- Schoolwork, library catalogues, and course material (see `schools_and_education.md`)
- Medical appointments and records (see `hospital_and_medical_care.md`)
- Terrace notices, repair requests, and Council business
- Ship maps, muster information, and emergency alerts (see `emergency_response_and_evacuation.md`)

Most content is cached on the ship's servers, so the intranet works even when the satellite link is down. A full cache is updated at each port call, and in between, residents see only what has already been loaded.

## Messaging Behaviour

Because external bandwidth is scarce, residents communicate in predictable patterns:

- Messages are sent in batches, often at shift changes
- Voice notes are preferred to calls, because they use less data
- Video calls are restricted to scheduled slots, and are reserved for medical, legal, and family emergencies
- Families often send long letters or recorded messages, which are sent during off-peak times

The Demographic Office's research found that residents who have family ashore send about three times as many messages in the weeks before a port call (see `population_and_demographics.md`).

## Calls to Shore

Residents can make a limited number of calls to shore each month, funded from their allowance. Calls are routed through the satellite link and are charged at a fixed rate. Calls to emergency services are always free and always connected.

## Communications Staff

The Communications Department has about 300 staff, including network engineers, communications officers, and a team that runs the Gazette's technical systems. The department maintains the satellite terminals, the ship's internal network, and the radio systems used for navigation and safety.

## Cyber Security

The intranet and ship systems are protected by the Cyber Security Team (see `piracy_security_and_threats.md`). Critical systems, including the Bridge, power management, and the ledger, are kept on separate networks. Residents' devices are registered on the intranet and checked for malware when they connect.

## Outages and Fallbacks

When the satellite link fails, the ship falls back to:

- The local intranet, which continues to work normally
- Ship-to-ship radio for urgent messages
- Printed notices and public announcements on the Spine
- Paper ledgers for essential payments, held in the City Operations Centre

The longest outage in the ship's history was 19 hours, in 2071, during a satellite network failure. The Company later installed a second LEO terminal, which reduced the risk of a total outage.

## Devices

Residents receive a ship terminal when they arrive, which is used for the intranet, ledger, and messaging. The terminal is rugged, water-resistant, and has a battery that lasts about a day. Personal devices may be used on the intranet after registration.
