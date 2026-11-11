"""
THE HALCYON MERIDIAN
A text adventure aboard a city at sea.

Run:   python halcyon_meridian_game.py

Type the number of a choice. Other commands:
  i  inventory (items you can use are offered here)
  s  status
  p  people you have met
  q  quit
"""

import random
import textwrap

WIDTH = 78
VOYAGE_DAYS = 20
STACKABLE = {"ration_chit", "first_aid_kit"}
STANDING_NAMES = {"company": "the Company", "residents": "the Residents", "crew": "the Crew"}


# ---------------------------------------------------------------- output

def say(text=""):
    if not text:
        print()
        return
    for para in text.strip().split("\n\n"):
        print(textwrap.fill(" ".join(para.split()), WIDTH))
        print()


def read_line(prompt="> "):
    try:
        return input(prompt).strip().lower()
    except EOFError:
        raise SystemExit("\nThe signal drops. Game closed.")


# ---------------------------------------------------------------- items

ITEMS = {
    "torch": {"name": "Heavy torch",
              "desc": "A rubber-cased torch from the engineering stores. Good for dark tanks and dark corridors."},
    "family_photo": {"name": "Family photo",
                     "desc": "A creased print of your family on a beach in Lisbon, taken before the ship."},
    "harness": {"name": "Safety harness",
                "desc": "A sail-crew harness with a clip and a two-metre lanyard. Worn on the masts."},
    "access_pass": {"name": "Operations pass",
                    "desc": "A Hotel Directorate pass that opens most service doors, including the Water Vault gate. Every use is logged."},
    "ration_chit": {"name": "Commissary ration chit",
                    "desc": "A printed chit worth one hot meal. Restores a little health.",
                    "use": lambda g: g.change_health(8)},
    "first_aid_kit": {"name": "First-aid kit",
                      "desc": "Bandages, painkillers and a sachet of rehydration salts. Restores health.",
                      "use": lambda g: g.change_health(25)},
    "mallet": {"name": "Listener's mallet",
               "desc": "A rubber-headed mallet for tapping tank walls. The note tells you the level."},
    "walk_log": {"name": "Tank walk log",
                 "desc": "A damp notebook of tank readings in pencil. The last entry for Tank 17 says: hollow, low, near base."},
    "brass_watch": {"name": "Chronist's brass watch",
                    "desc": "A small brass watch on a chain. Chronists give them to people they trust with the rota."},
    "shore_clock": {"name": "Shore clock",
                    "desc": "A battery clock set to Lisbon time. Someone has written 'home' on the back in pen."},
    "sealed_letter": {"name": "Letter from Lisbon",
                      "desc": "A letter addressed to 'Mags Doucet, Harbour Terraces', with a Lisbon postmark."},
    "swap_ledger": {"name": "Berth broker's ledger page",
                    "desc": "A page listing cabins, grades and needs on Terraces 12 to 16, in a neat, careful hand."},
    "gait_card": {"name": "Gait coach's card",
                  "desc": "Four motion-walking exercises, stamped by Sunniva Lind."},
    "petition_sheet": {"name": "Petition sheet",
                       "desc": "A sheet of signatures against the water-price rise. It needs more names than it has."},
    "gazette_clipping": {"name": "Gazette clipping",
                         "desc": "A clipping about the 2071 microphone vote, with the Council's comments underlined."},
    "tally_chalk": {"name": "Tally chalk",
                    "desc": "A stub of white chalk for marking walls. The Hotel Directorate would prefer you didn't."},
    "lighter_tin_note": {"name": "Tide note",
                         "desc": "A folded note from a lighter crew's tin. You are not supposed to read it."},
    "ship_coin": {"name": "Lighter coin",
                  "desc": "A coin tucked under a lifting shackle by lighter folk on their first lift."},
    "grey_glove": {"name": "Grey glove",
                   "desc": "A damp woman's glove, found on a Deck 14 stair. The Hotel Directorate has no record of anyone losing it."},
}


# ---------------------------------------------------------------- people

PEOPLE = {
    "ansah": ("Captain Teodora Ansah",
              "The Master. Walks the Spine at six every morning and reads every incident report herself."),
    "vance": ("Gregor Vance",
              "Chief Operating Officer of Meridian Maritime Holdings. Speaks softly and thinks in quarters."),
    "malk": ("Iver Malk",
             "Chronist. Keeps the rota of the hour and wears a brass watch on a chain."),
    "nadia": ("Nadia Okonkwo-Reyes",
              "Tank listener. Taps the walls of the Water Vault and trusts her ears more than the sensors."),
    "brandt": ("Ilse Brandt",
               "Chief Engineer. Holds the reactor licence and has no patience for rumours."),
    "joon": ("Joon-ho Baek",
             "Batch clerk in the shift-change hall. Carries the letters nobody else will."),
    "pilar": ("Pilar Ferreira",
              "Berth broker. Knows every cabin on Terraces 10 to 16 and charges for knowing."),
    "dara": ("Sergeant Dara Quist",
             "Warden in the City Operations Centre. Blunt, fair and short of sleep."),
    "ilyas": ("Ilyas Karim",
              "Nineteen. Stowaway from a container of tinned fish loaded at Lisbon. Wanted to see the sea."),
    "oduya": ("Ben Oduya",
              "Council member for Ward 23. Harbour Alliance. Argues with a clipboard in his hand."),
    "castellanos": ("Mira Castellanos",
                    "Gazette reporter. Writes everything down, including what you didn't mean to say."),
    "lind": ("Sunniva Lind",
             "Gait coach, known on the Spine as 'Sway'. Walks as if the deck were always moving."),
    "yusuf": ("Yusuf Abdi",
              "Trader in the Central Hall. Sells first-aid kits at controlled prices and jokes about the rest."),
    "slack": ("Tomas Veiga, 'Slack'",
              "Lighter hand, Port Services. Knows the anchorage better than the charts do."),
    "haarsma": ("Ruud Haarsma",
                "Sail Master. Speaks in wind speeds and has never lost a man from the masts."),
    "adeyemi": ("Dr Ifeoma Adeyemi",
                "Senior physician at Meridian Central Hospital. Sees injuries before they become emergencies."),
    "mags": ("Marguerite 'Mags' Doucet",
             "Eighty-one. Lived aboard eleven years. Husband Henri died in the second year. Son Rui is in Lisbon."),
    "tavi": ("Tavi Osei",
             "Nine years old. Lives in the next cabin and knows every knock code on the terrace."),
    "tran": ("Rev. Samuel Tran",
             "Chaplain. Keeps the memorial board and the chapel open at all hours."),
    "hedda": ("Hedda Lund",
              "Chair of the Terrace 14 committee. Keeps the laundry rota and knows whose child is ill."),
    "chenmei": ("Chen Mei-ling",
                "Head cook at the Aft Hall. Runs the Galley Association's grill and never repeats a recipe."),
    "carvalho": ("Ines Carvalho",
                 "Company auditor. Samples one account in a hundred each quarter and never seems surprised."),
}


# ---------------------------------------------------------------- game state

class Game:
    def __init__(self, name):
        self.name = name
        self.day = 0
        self.health = 80
        self.credits = 150
        self.standing = {"company": 0, "residents": 0, "crew": 0}
        self.inventory = []
        self.flags = set()
        self.met = []
        self.seen = set()
        self.counts = {}

    def has(self, key):
        return key in self.inventory

    def flag(self, name):
        return name in self.flags

    def set_flag(self, name):
        self.flags.add(name)

    def add_item(self, key):
        if key in self.inventory and key not in STACKABLE:
            return
        self.inventory.append(key)
        say(f"[Received: {ITEMS[key]['name']}]")

    def remove_item(self, key):
        if key in self.inventory:
            self.inventory.remove(key)

    def change_health(self, n):
        self.health = max(0, min(100, self.health + n))
        if n:
            say(f"[Health {n:+d}]")

    def change_credits(self, n):
        self.credits = max(0, self.credits + n)
        if n:
            say(f"[Ledger {n:+d} LC]")

    def change_standing(self, who, n):
        self.standing[who] += n
        if n:
            say(f"[Standing with {STANDING_NAMES[who]} {n:+d}]")

    def meet(self, key):
        if key not in self.met:
            self.met.append(key)


# ---------------------------------------------------------------- effect and condition helpers

def fx(*steps):
    def run(g):
        for step in steps:
            step(g)
    return run


def give(key):
    return lambda g: g.add_item(key)


def take(key):
    return lambda g: g.remove_item(key)


def flag(name):
    return lambda g: g.set_flag(name)


def heal(n):
    return lambda g: g.change_health(n)


def hurt(n):
    return lambda g: g.change_health(-n)


def earn(n):
    return lambda g: g.change_credits(n)


def pay(n):
    return lambda g: g.change_credits(-n)


def stand(who, n):
    return lambda g: g.change_standing(who, n)


def meet(key):
    return lambda g: g.meet(key)


def chance(p, yes, no=None):
    def run(g):
        if random.random() < p:
            yes(g)
        elif no:
            no(g)
    return run


def has(key):
    return lambda g: g.has(key)


def not_has(key):
    return lambda g: not g.has(key)


def flag_is(name):
    return lambda g: g.flag(name)


def not_flag(name):
    return lambda g: not g.flag(name)


def stand_at_least(who, n):
    return lambda g: g.standing[who] >= n


def can_pay(n):
    return lambda g: g.credits >= n


def health_below(n):
    return lambda g: g.health < n


def all_of(*conds):
    return lambda g: all(c(g) for c in conds)


def any_of(*conds):
    return lambda g: any(c(g) for c in conds)


def ch(label, to, when=None, do=None):
    return {"label": label, "to": to, "when": when, "do": do}


NODES = {}


def node(name, text, choices, enter=None):
    NODES[name] = {"text": text, "choices": choices, "enter": enter}


LEAVE = ch("Head back out to the Spine", "spine")
CARRY_ON = ch("Carry on up the Spine", "spine_menu")


# ---------------------------------------------------------------- special effects

def deliver_letter(g):
    g.remove_item("sealed_letter")
    g.set_flag("letter_delivered")
    g.meet("mags")
    if g.flag("read_letter"):
        say("She sees the torn corner and the creases. 'You read it,' she says. 'Well. At least you brought it.' She is quiet for a long time, then she thanks you anyway.")
        g.change_standing("residents", 1)
    else:
        say("She holds the envelope against her chest and does not open it for a long time. 'Rui,' she says, and nothing else.")
        g.change_standing("residents", 2)
    say("Before you go she presses a small battery clock into your hand. It is set to Lisbon time, and on the back someone has written 'home' in pen. 'Henri's,' she says. 'Keep it going for me.'")
    g.add_item("shore_clock")


def read_letter(g):
    g.set_flag("read_letter")
    say("You slip a finger under the flap. Inside, in careful handwriting: 'Mae, the house is sold. I am sorry I did not come for Pai. I will bring the photographs when the ship reaches Bridgetown.' You fold it closed again. The seal has torn at one corner, and you cannot pretend it hasn't.")
    g.add_item("sealed_letter")


def sleeping_man_story(g):
    g.set_flag("heard_sleeping_man")
    say("Somewhere in the Water Vault, the old story goes, there is a man who sleeps in the cold, dark water. When the fresh water falls below a certain line he wakes, and the tanks knock in the night. Henri used to say the knocking was the Sleeping Man turning over. When it stopped, you knew he had dropped off again and the pumps could run.")


def sound_tank(g):
    if g.flag("tank_confirmed"):
        say("You tap the wall again. The note is the same: flat and hollow near the base, where the rest of the tank should ring full.")
        return
    g.set_flag("tank_confirmed")
    g.meet("nadia")
    say("You tap the wall of Tank 17 with the mallet, low down by the base. The note is wrong: a flat, hollow ring where the tank should sound full. You kneel and put your ear to the steel. Under the pump noise there is a faint second slosh, as if water is moving behind something it shouldn't. Nadia's hand settles on your shoulder. 'Baffle,' she says. 'Cracked through. The sensor sits on the wrong side of it.'")
    g.change_standing("crew", 1)


def sail_training(g):
    if g.has("harness"):
        say("Your harness clips to the mast ladder. Ruud's crew check every link before you climb, and the wind up there is the strongest thing you have ever stood in.")
    else:
        say("Without a harness you are tied to the ladder with a borrowed line. Halfway up a gust slams you against the mast, and a rung splits your palm.")
        g.change_health(-10)
    g.set_flag("mast_trained")
    g.change_standing("crew", 2)
    g.meet("haarsma")


def escape_stowaway(g):
    g.change_credits(-60)
    g.set_flag("helped_escape")
    g.change_standing("company", -2)
    g.meet("ilyas")
    say("You pay the corridor porter sixty credits. He looks at the wall while you lead Ilyas through the service door. At the threshold Ilyas stops. 'Thank you,' he says. 'I didn't think anyone would.' Then he is gone into the grey service light, and you don't know where he will end up.")


# ---------------------------------------------------------------- shared menu of places on the Spine

bridge_open = any_of(stand_at_least("company", 1), has("access_pass"), flag_is("captain_ally"))
vault_open = any_of(has("access_pass"), flag_is("nadia_trust"))

MENU = [
    ch("Central Market Hall", "market"),
    ch("Your cabin, Terrace 14 (west tower)", "terrace"),
    ch("The Solarium", "solarium"),
    ch("Aft Hall (galley and restaurants, Deck 9 aft)", "aft_hall"),
    ch("Harbour Care Complex (Deck 11)", "care"),
    ch("Meridian Central Hospital", "clinic"),
    ch("Shift-change hall (message halls)", "shift_hall"),
    ch("Ship Time Office", "time_office"),
    ch("Chapel (multi-faith, Deck 11)", "chapel"),
    ch("Council office (Solarium)", "council"),
    ch("City Operations Centre", "coc"),
    ch("Engineering, Deck 6", "engineering"),
    ch("The Bridge", "bridge", when=bridge_open),
    ch("Sail Control, mast bases", "sail"),
    ch("Cargo yard and lighter dock", "cargo"),
    ch("Water Vault (double bottom)", "water_vault", when=vault_open),
    ch("Detention block", "detention", when=flag_is("ev_stowaway_seen")),
    ch("Stay on the Spine and watch the crowd", "spine"),
]


# ---------------------------------------------------------------- the Spine

SCHEDULE = {
    2: "ev_letter",
    4: "ev_tank_note",
    6: "ev_broker",
    8: "ev_stowaway",
    10: "ev_storm_warning",
    11: "storm",
    13: "ev_petition",
    15: "ev_election",
    17: "ev_vance",
    14: "ev_audit",
    19: "ev_landfall",
}

RANDOM_ENCOUNTERS = [
    "rnd_seasick", "rnd_wallet", "rnd_knock", "rnd_rumour",
    "rnd_tally", "rnd_rail", "rnd_blackmarket", "rnd_recipe",
    "rnd_ghost", "rnd_lostchild", "rnd_fight", "rnd_gait",
]


def weather(day):
    if day <= 4:
        return "The trade wind holds steady and the sails draw well."
    if day <= 9:
        return "A long swell lifts the ship and lets it down, slow as breathing."
    if day == 10:
        return "The barometer on the Spine screens is falling fast."
    if day <= 14:
        return "Rough seas. The sails are feathered and the Spine rocks underfoot."
    return "A warm, flat sea. Bridgetown is a few days off."


def spine_text(g):
    return ("The Spine runs the length of the ship, forty metres wide, and at this hour it is full: "
            "clerks in batch tabards, children on the Spine Run, rail cars humming down the centre. "
            "Where do you go?")


def spine_enter(g):
    g.day += 1
    if g.day > VOYAGE_DAYS:
        g.counts["ending"] = pick_ending(g)
        return "ending"
    say(f"--- Day {g.day} of {VOYAGE_DAYS}. {weather(g.day)} ---")
    if g.day in SCHEDULE:
        return SCHEDULE[g.day]
    if random.random() < 0.6:
        pool = [r for r in RANDOM_ENCOUNTERS if r not in g.seen]
        if pool:
            pick = random.choice(pool)
            g.seen.add(pick)
            return pick
    return None


node("spine", spine_text, MENU, enter=spine_enter)
node("spine_menu", "You are back on the Spine. The crowd closes around you again.", MENU)


# ---------------------------------------------------------------- places

node("market",
     "The Central Hall is loud at this hour. Yusuf Abdi sells first-aid kits and ration chits from a stall with a faded canvas roof. "
     "'Prices are controlled, friend,' he says. 'Only the lies are free.'",
     [
         ch("Buy a first-aid kit (25 LC)", "here",
            when=all_of(can_pay(25), not_has("first_aid_kit")),
            do=fx(pay(25), give("first_aid_kit"), meet("yusuf"))),
         ch("Buy a ration chit (5 LC)", "here", when=can_pay(5),
            do=fx(pay(5), give("ration_chit"))),
         ch("Ask what people are saying about the water price", "here",
            do=fx(flag("heard_water_price"), meet("yusuf"))),
         ch("Dig through the Hand-me-Down bins", "here",
            do=chance(0.5, give("tally_chalk"),
                      lambda g: say("Two odd socks, a tin of boot polish and no chalk."))),
         LEAVE,
     ])

node("terrace",
     "Cabin 14-07 is nine square metres: a sway-compensated bunk, a fold-down desk and a tally wall you have marked in pencil for a month. "
     "Through the partition comes a knock, one, a pause, then one. Tavi Osei, nine, from the next cabin. The walls carry sound both ways.",
     [
         ch("Lie down and rest (+15 health)", "here", do=heal(15)),
         ch("Knock back through the wall (+5 health)", "here",
            do=fx(flag("knock_friend"), heal(5), meet("tavi"))),
         ch("Mark your tally wall with the chalk", "here", when=has("tally_chalk"),
            do=flag("marked_wall")),
         ch("Talk with the neighbours on the terrace garden", "here",
            do=fx(stand("residents", 1), meet("tavi"))),
         ch("Join the terrace committee (+1 Residents)", "here",
            when=not_flag("committee_member"),
            do=fx(flag("committee_member"), stand("residents", 1), meet("hedda"))),
         LEAVE,
     ])

node("solarium",
     "The translucent panels over the Solarium turn the sky to pale gold on the lawns. Sunniva Lind, the gait coach, walks a line of children along the edge of the grass, knees soft and shoulders loose. "
     "Mira Castellanos of the Halcyon Gazette sits on a bench with a notebook on her knee.",
     [
         ch("Train with Sunniva Lind (10 LC)", "here",
            when=all_of(can_pay(10), not_flag("gait_trained")),
            do=fx(pay(10), give("gait_card"), flag("gait_trained"), heal(5), meet("lind"))),
         ch("Interview with Mira: speak frankly about the water price", "here",
            when=not_flag("interviewed"),
            do=fx(flag("interviewed"), flag("frank_interview"), stand("residents", 1),
                  stand("company", -1), give("gazette_clipping"), meet("castellanos"))),
         ch("Interview with Mira: speak carefully, for the Company", "here",
            when=not_flag("interviewed"),
            do=fx(flag("interviewed"), stand("company", 1), stand("residents", -1),
                  give("gazette_clipping"), meet("castellanos"))),
         ch("Lie on the lawn in the sun (+8 health)", "here", do=heal(8)),
         LEAVE,
     ])


def care_text(g):
    text = ("The Harbour Care Complex smells of soap and oranges. Marguerite 'Mags' Doucet, eighty-one, sits by the window "
            "with a blanket over her knees. Her husband Henri died in the second year you were aboard, or the year before; "
            "she can't always say which. Her son Rui is in Lisbon and has not come to a single port call.")
    if g.has("sealed_letter") and not g.flag("letter_delivered"):
        text += " You have something in your pocket addressed to her."
    if g.flag("letter_delivered"):
        text += " She looks more rested than she did, and she waves when she sees you."
    return text


node("care", care_text,
     [
         ch("Give Mags the letter", "here",
            when=all_of(has("sealed_letter"), not_flag("letter_delivered")),
            do=deliver_letter),
         ch("Listen to her story of the Sleeping Man", "here",
            when=not_flag("heard_sleeping_man"),
            do=fx(sleeping_man_story, meet("mags"))),
         ch("Sit with her while she dozes (+5 health, +1 Residents)", "here",
            do=fx(heal(5), stand("residents", 1), meet("mags"))),
         LEAVE,
     ])

node("clinic",
     "The Meridian Central Hospital has a bright ward full of bunks and a smell of antiseptic. Dr Ifeoma Adeyemi is reading a chart at the desk. "
     "'Everyone thinks the roll is harmless,' she says without looking up. 'Then they fall over in the Spine.'",
     [
         ch("Have your fatigue and bruises looked at (+20 health)", "here",
            when=health_below(80), do=fx(heal(20), meet("adeyemi"))),
         ch("Ask about the Quarantine Ward and norovirus rules", "here",
            do=fx(flag("knows_quarantine"), meet("adeyemi"))),
         ch("Volunteer for the morning ward round (-3 health, +1 Crew, +1 Residents)", "here",
            do=fx(hurt(3), stand("crew", 1), stand("residents", 1), meet("adeyemi"))),
         LEAVE,
     ])

node("shift_hall",
     "The shift-change hall is packed with people holding terminals, letters and small parcels. Joon-ho Baek works the queue desk, "
     "stamping batch slips with the speed of long practice. The batch clock on the wall says the next send is in forty minutes.",
     [
         ch("Send a message home (5 LC, +3 health)", "here",
            when=can_pay(5), do=fx(pay(5), heal(3), flag("sent_message"), meet("joon"))),
         ch("Volunteer as a batch runner for the afternoon (-2 health, +1 Crew, +1 Residents)", "here",
            do=fx(hurt(2), stand("crew", 1), stand("residents", 1), meet("joon"))),
         ch("Ask when the next batch leaves the ship", "here",
            do=fx(flag("knows_batch"), meet("joon"))),
         LEAVE,
     ])


def clock_text(g):
    if g.has("brass_watch"):
        return ("Iver Malk is at his desk with the rota of the hour spread out, pencil in hand, marking minutes. "
                "He nods at the brass watch on your chain as if he has been expecting it.")
    return ("Iver Malk looks up from the rota of the hour, which is covered in small pencilled times. "
            "'Every clock change is a negotiation,' he says. 'The reactors want one minute, the Commissary wants another. Want to help?'")


node("time_office", clock_text,
     [
         ch("Study the rota of the hour", "here",
            when=any_of(has("brass_watch"), stand_at_least("crew", 1)),
            do=fx(flag("knows_rota"), stand("crew", 1), meet("malk"))),
         ch("Ask whether the Captain's schedule can be moved for the storm", "here",
            when=flag_is("knows_rota"),
            do=fx(flag("knows_captain_schedule"), stand("company", 1), meet("malk"))),
         ch("Offer to help with tonight's clock change", "here",
            when=not_has("brass_watch"),
            do=fx(stand("crew", 1), give("brass_watch"), flag("chronist_trust"), meet("malk"))),
         ch("Ask about shore clocks and home time", "here",
            do=fx(flag("discussed_clocks"), meet("malk"))),
         LEAVE,
     ])

node("chapel",
     "The chapel is quiet. The memorial board by the door carries a long list of names, some with small pencilled birds beside them. "
     "Chaplain Samuel Tran is sitting in the second row with his hands folded.",
     [
         ch("Add a line to the memorial board (+4 health)", "here",
            do=fx(heal(4), flag("memorial"), meet("tran"))),
         ch("Leave a bread offering for the Sleeping Man", "here",
            do=fx(stand("residents", 1), flag("left_offering"), meet("tran"))),
         ch("Ask the chaplain about the Sleeping Man", "here",
            when=flag_is("heard_sleeping_man"),
            do=fx(flag("understood_tank"), heal(2), meet("tran"))),
         LEAVE,
     ])

node("council",
     "The Council office on the Solarium has two desks, a wall of ward maps and a kettle that never quite boils. "
     "Ben Oduya is on the phone to someone at the Hotel Directorate. He waves you to a chair.",
     [
         ch("Ask about the water-price referendum", "here",
            do=fx(flag("knows_referendum"), meet("oduya"))),
         ch("Offer to help with the ward tally (+1 Residents)", "here",
            do=fx(stand("residents", 1), flag("ward_help"), meet("oduya"))),
         ch("Ask how a candidate gets on the ballot", "here",
            do=fx(flag("knows_ballot"), meet("oduya"))),
         LEAVE,
     ])

node("coc",
     "The City Operations Centre is a wall of screens: power, water, air, the rail lines and the terraces. "
     "Sergeant Dara Quist is at the centre console with two radios and a cold cup of tea.",
     [
         ch("Ask Sergeant Quist for the storm plan", "here",
            do=fx(flag("knows_storm"), meet("dara"))),
         ch("Ask to see the detention block", "detention",
            when=flag_is("ev_stowaway_seen"), do=meet("dara")),
         ch("Report a leaking ventilation duct on Terrace 16 (+1 Crew, +1 Residents)", "here",
            do=fx(stand("crew", 1), stand("residents", 1), meet("dara"))),
         LEAVE,
     ])

node("engineering",
     "Engineering on Deck 6 is a maze of gauges, valves and handrails painted in safety yellow. Chief Engineer Ilse Brandt is "
     "standing over a wall-mounted pressure log with her arms folded.",
     [
         ch("Report the Tank 17 note to Ilse Brandt", "here",
            when=all_of(flag_is("heard_tank"), not_flag("tank_reported")),
            do=fx(flag("tank_reported"), stand("crew", 1), meet("brandt"))),
         ch("Ask for a tour of the reactor citadel gallery (+1 Crew)", "here",
            do=fx(stand("crew", 1), flag("toured"), meet("brandt"))),
         ch("Ask about the 2072 power dip", "here",
            do=fx(flag("heard_blackout"), meet("brandt"))),
         LEAVE,
     ])

node("bridge",
     "The Bridge is glass, screens and low voices. Captain Ansah stands at the forward window with her hands behind her back, "
     "watching the swell roll in under the bow.",
     [
         ch("Ask the Captain how she plans for storms", "here",
            do=fx(flag("knows_storm"), meet("ansah"))),
         ch("Tell the Captain about Tank 17", "here",
            when=flag_is("tank_confirmed"),
            do=fx(flag("captain_ally"), stand("crew", 2), stand("company", 1), meet("ansah"))),
         ch("Mention the Tank 17 rumour", "here",
            when=all_of(flag_is("heard_tank"), not_flag("tank_confirmed")),
            do=fx(stand("crew", 1), meet("ansah"))),
         LEAVE,
     ])

node("sail",
     "The mast bases are loud with wind and the creak of composite under load. Ruud Haarsma, the Sail Master, is checking a line "
     "with his thumb. 'Wind is twenty-two metres a second up top,' he says. 'Beautiful, and I hate it.'",
     [
         ch("Climb a mast for a training shift", "here",
            do=sail_training),
         ch("Ask Ruud about the wind data", "here",
            do=fx(flag("sail_intel"), meet("haarsma"))),
         LEAVE,
     ])

node("cargo",
     "The cargo yard is stacked with containers under floodlights. Lighter boats rock alongside the ship's side, and their crews are "
     "shouting in a dialect you only half follow. Tomas Veiga, 'Slack', sits on a bollard with a cup of tea.",
     [
         ch("Ask Slack about a parcel run ashore (+60 LC)", "here",
            when=not_flag("smuggler"),
            do=fx(flag("smuggler"), earn(60), meet("slack"))),
         ch("Drink tea with the crew from a lighter tin (+3 health)", "here",
            do=fx(give("lighter_tin_note"), heal(3), meet("slack"))),
         ch("Ask about your first lift", "here",
            when=not_has("ship_coin"),
            do=fx(give("ship_coin"), stand("crew", 1), meet("slack"))),
         LEAVE,
     ])


def vault_text(g):
    base = ("The double bottom is cold and loud when the pumps run. The Water Vault is forty tanks in rows, "
            "each one a steel cylinder taller than a terrace. Tank 17 is the third from the aft wall.")
    if g.flag("tank_confirmed"):
        base += " The mallet's note from Tank 17 still rings in your head."
    return base


node("water_vault", vault_text,
     [
         ch("Sound the walls of Tank 17 with the mallet", "here",
            when=has("mallet"), do=sound_tank),
         ch("Take Nadia's walk log for Tank 17", "here",
            when=all_of(flag_is("nadia_trust"), not_has("walk_log")),
            do=fx(give("walk_log"), meet("nadia"))),
         ch("Read the sensor gauge (it says 91 percent)", "here",
            do=fx(flag("saw_gauge"), meet("nadia"))),
         LEAVE,
     ])


node("detention",
     "The detention block is small and clean. Ilyas Karim, nineteen, sits on the bunk with his knees pulled up. "
     "He has a grey blanket over his shoulders and the fixed look of someone who has been asked the same questions all day.",
     [
         ch("Ask why he came aboard", "here",
            do=fx(flag("ilyas_story"), stand("residents", 1), meet("ilyas"))),
         ch("Pay the porter to help him out through the service corridor (60 LC)", "spine",
            when=can_pay(60), do=fx(escape_stowaway)),
         ch("Tell Sergeant Quist he is a risk to the ship (+2 Company, -1 Residents)", "spine",
            do=fx(stand("company", 2), stand("residents", -1), flag("reported_stowaway"), meet("ilyas"))),
         LEAVE,
     ])


node("ev_letter",
     "Joon-ho Baek, the batch clerk, catches your sleeve on the Spine. He holds a sealed envelope with a Lisbon postmark. "
     "'It came in the last batch. It's for a Margarida Doucet at the Harbour Care Complex. The address field says Mags. "
     "She's on a list of people nobody writes to. I'm not supposed to take letters out of the hall. I'm asking you.'",
     [
         ch("Take the letter to Mags", "spine_menu",
            do=fx(give("sealed_letter"), flag("letter_taken"), meet("joon"))),
         ch("Open it first to check it isn't urgent", "spine_menu",
            do=fx(read_letter, meet("joon"))),
         ch("Tell him it's not your business (-1 Crew)", "spine_menu",
            do=fx(stand("crew", -1), flag("letter_refused"), meet("joon"))),
     ])

node("ev_tank_note",
     "Nadia Okonkwo-Reyes, the tank listener, is waiting at the rail with her hands black from the Water Vault. "
     "'Tank 17,' she says. 'The gauge says ninety-one percent. My mallet says it's wrong. The note near the base is hollow, like a drum with a crack in it. "
     "I've logged it twice, and twice the Water Department has told me the sensor is right.'",
     [
         ch("Go down with her to the Water Vault (she gives you her mallet)", "spine_menu",
            do=fx(flag("nadia_trust"), flag("heard_tank"), give("mallet"), meet("nadia"))),
         ch("Pass her note to Chief Engineer Brandt (+1 Crew)", "spine_menu",
            do=fx(flag("heard_tank"), flag("tank_reported"), stand("crew", 1), meet("nadia"))),
         ch("Tell her the sensor is more reliable than a drum (+1 Company, -1 Crew)", "spine_menu",
            do=fx(flag("heard_tank"), flag("tank_ignored"), stand("company", 1), stand("crew", -1), meet("nadia"))),
     ])

node("ev_broker",
     "Pilar Ferreira, the berth broker, leans on the rail beside you with a cup of coffee she isn't drinking. "
     "'There's a family on Terrace 12 with two children and one lower-deck cabin. You have a Grade 2 single that suits a couple. "
     "I have a page of cabins, and I won't pretend I'm doing this for free. Forty credits and you can have a Grade 1 by Thursday.'",
     [
         ch("Accept the swap (40 LC)", "spine_menu",
            when=can_pay(40),
            do=fx(pay(40), give("swap_ledger"), flag("swapped"), stand("residents", 1), meet("pilar"))),
         ch("Ask her to do it for nothing and look after the family", "spine_menu",
            do=fx(flag("swapped"), stand("residents", 2), give("swap_ledger"), meet("pilar"))),
         ch("Decline and keep your cabin", "spine_menu",
            do=fx(flag("refused_swap"), meet("pilar"))),
     ])

node("ev_stowaway",
     "Sergeant Dara Quist is at the rail with a notebook. 'We have a stowaway in detention. He came aboard in a container of tinned fish at Lisbon. "
     "The medic says he needs someone who speaks Portuguese to explain the rules. I'm told you do. Come and talk to him, and then decide whether you're useful to me.'",
     [
         ch("Go to the detention block with her", "detention",
            do=fx(flag("ev_stowaway_seen"), meet("dara"))),
         ch("Tell her you're busy (-1 Company)", "spine_menu",
            do=stand("company", -1)),
     ])

node("ev_storm_warning",
     "The Spine screens show the barometer falling through the night. At the noon briefing Ruud Haarsma, the Sail Master, puts it plainly. "
     "'Storm Law from tomorrow at nine. Sails feathered, decks closed. Anyone who wants to help on the masts, I need you now, not when it's blowing.'",
     [
         ch("Volunteer for the masts (+2 Crew)", "spine_menu",
            do=fx(flag("mast_volunteer"), stand("crew", 2), meet("haarsma"))),
         ch("Stock up on ration chits (10 LC)", "spine_menu",
            when=can_pay(10), do=fx(pay(10), give("ration_chit"), give("ration_chit"))),
         ch("Stay in your cabin and sleep early (+10 health)", "spine_menu",
            do=heal(10)),
     ])


def storm_mast_enter(g):
    safe = (g.flag("mast_volunteer") or g.flag("mast_trained")
            or g.has("harness") or g.flag("gait_trained"))
    amount = 6 if safe else 22
    if not safe and random.random() < 0.5:
        amount = 0
    g.counts["mast_hurt"] = amount
    if amount:
        g.change_health(-amount)


def storm_mast_text(g):
    hurt_amount = g.counts.get("mast_hurt", 0)
    if hurt_amount >= 20:
        return ("A gust lifts the platform and throws you into the mast. Ruud's hand catches your harness and holds. "
                "Below you the sea is a grey field of white. Your ribs ache and you cannot stop shaking.")
    if hurt_amount:
        return "A gust knocks you against a rung. The crew hauls you back to the platform, bruised but on your feet."
    return "You clip on, check your lanyard and climb into the roar of the wind. The gusts come in long pulses, and you learn to ride them."


node("storm", "Storm Law is in force from nine. The Spine's lights drop to amber. The wind on the masts is thirty metres a second, and the ship moves more than you have ever felt it move. "
     "Everyone on the Spine is heading for a shelter or a station.",
     [
         ch("Go up to the masts with Ruud's crew", "storm_mast"),
         ch("Go to the City Operations Centre and help coordinate", "storm_coc"),
         ch("Go to the Bridge with the Captain", "storm_bridge", when=bridge_open),
         ch("Stay in your cabin", "storm_home"),
     ])

node("storm_mast", storm_mast_text,
     [
         ch("Hold the lines through the night (+2 Crew)", "storm_end",
            do=fx(flag("storm_hero"), stand("crew", 2))),
         ch("Help bring the crew down to the galley (+1 Crew)", "storm_end",
            do=stand("crew", 1)),
         ch("Go back to the cabin", "storm_end"),
     ], enter=storm_mast_enter)

node("storm_coc",
     "Sergeant Quist hands you a radio and a list of names. 'Terraces 12 to 16 first. Old, sick, the ones who don't answer.'",
     [
         ch("Check on the Harbour Care Complex (+2 Residents)", "storm_end",
            do=fx(stand("residents", 2), flag("checked_on_mags"), meet("mags"))),
         ch("Run messages between the terraces (+1 Residents)", "storm_end",
            do=stand("residents", 1)),
         ch("Stay at the console and log the alarms (+1 Company)", "storm_end",
            do=stand("company", 1)),
     ])

node("storm_bridge",
     "The Bridge is dark except for the instrument glow. Captain Ansah does not turn around. 'Good. Stand there and don't touch anything.'",
     [
         ch("Ask about the storm plan", "storm_end",
            do=fx(flag("knows_storm"), meet("ansah"))),
         ch("Tell her about the Tank 17 note", "storm_end",
            when=flag_is("heard_tank"),
            do=fx(flag("captain_ally"), stand("company", 1), stand("crew", 1), meet("ansah"))),
         ch("Hold the rail and watch the sea (+1 Crew)", "storm_end",
            do=stand("crew", 1)),
     ])

node("storm_home",
     "The terrace is loud with the wind. Through the partition, Tavi's knocks come in a new pattern: a game, and then a question. Are you still there?",
     [
         ch("Knock back until the wind drops (+8 health)", "storm_end",
            do=fx(heal(8), flag("knock_friend"), meet("tavi"))),
         ch("Sleep through it (+12 health)", "storm_end",
            do=heal(12)),
     ])

node("storm_end",
     "By morning the wind has dropped to eighteen metres a second. Storm Law is lifted at noon. The Spine is strewn with lost hats "
     "and a few broken tiles, and somewhere a choir is singing over a broken rail car.",
     [ch("Go out to the Spine", "spine_menu")])


node("ev_petition",
     "Ben Oduya, Council member for Ward 23, finds you at the rail with a clipboard. 'The Board wants water above the sixty-litre allowance billed at a higher rate. "
     "It's in next month's budget. We need a referendum, and a referendum needs names. Sign, stand for the Council, or stay out of it. Your call.'",
     [
         ch("Sign the petition (+1 Residents, -1 Company)", "spine_menu",
            do=fx(give("petition_sheet"), flag("petition_signed"), stand("residents", 1),
                  stand("company", -1), meet("oduya"))),
         ch("Stand as a candidate for the Council (+1 Residents)", "spine_menu",
            do=fx(flag("candidate"), stand("residents", 1), meet("oduya"))),
         ch("Stay out of it (+1 Company)", "spine_menu",
            do=fx(stand("company", 1))),
     ])


def election_enter(g):
    if not g.flag("candidate"):
        g.counts["election"] = "none"
        return None
    score = (g.standing["residents"] + (2 if g.flag("petition_signed") else 0)
             + (1 if g.flag("committee_member") else 0) + random.randint(-2, 2))
    if score >= 3:
        g.counts["election"] = "won"
        g.set_flag("council_seat")
    else:
        g.counts["election"] = "lost"
    return None


def election_text(g):
    result = g.counts.get("election", "none")
    if result == "won":
        return ("Polling runs three days on the intranet, with paper ballots in every terrace common room. "
                "The count comes in at midnight: you have won a seat on the Residents' Council for Ward 23. "
                "Ben Oduya shakes your hand in the common room and says, 'Don't look so surprised.'")
    if result == "lost":
        return ("The count comes in at midnight. You lost by a handful of votes. Ben Oduya is already on the phone to the "
                "terraces, calling the people who did vote for you and asking them to try again next time.")
    return ("Polling day. The ward board on the Spine lists the candidates for the Residents' Council. "
            "You didn't stand, so you watch the queues at the terrace common rooms and wonder who got your neighbours' votes.")


node("ev_election", election_text,
     [
         ch("Make a short speech to the terrace (+1 Residents)", "spine_menu",
            when=flag_is("candidate"), do=stand("residents", 1)),
         ch("Go out to the Spine", "spine_menu"),
     ], enter=election_enter)


node("ev_vance",
     lambda g: ("Gregor Vance, the Company's Chief Operating Officer, has taken the table nearest the Solarium cafe. "
                "He wears a navy blazer with a Company pin. 'I've read the Water Department report,' he says. 'The sensor is calibrated. "
                "Whatever's in Tank 17 is a sensor problem, and I'd like the Atlantic committee to hear that the ship has no problem with it. "
                "Three hundred credits and a seat at the table. Think of it as a thank-you for keeping the schedule.'")
     if g.flag("tank_confirmed") else
     ("Gregor Vance, the Company's Chief Operating Officer, has taken the table nearest the Solarium cafe. "
      "'The petition is a nuisance,' he says. 'The water rise is a budget matter, not a referendum matter. "
      "I'd be glad to see it go quiet. One hundred and fifty credits, and I'll remember your name on the Atlantic committee.'"),
     [
         ch("Take the money and call Tank 17 a sensor fault (+300 LC, +4 Company, -3 Crew)", "spine_menu",
            when=flag_is("tank_confirmed"),
            do=fx(flag("bought_silence"), earn(300), stand("company", 4), stand("crew", -3), meet("vance"))),
         ch("Refuse, and put the tank in the Gazette (-3 Company, +2 Residents)", "spine_menu",
            when=flag_is("tank_confirmed"),
            do=fx(flag("resisted_company"), stand("company", -3), stand("residents", 2), meet("vance"))),
         ch("Ask for the committee seat in exchange for an open inspection (+100 LC)", "spine_menu",
            when=flag_is("tank_confirmed"),
            do=fx(earn(100), stand("company", 1), flag("bargained"), meet("vance"))),
         ch("Take the money and drop the petition (+150 LC, +2 Company, -2 Residents)", "spine_menu",
            when=not_flag("tank_confirmed"),
            do=fx(flag("bought_petition"), earn(150), stand("company", 2), stand("residents", -2), meet("vance"))),
         ch("Refuse and keep the petition alive (+2 Residents, -2 Company)", "spine_menu",
            when=not_flag("tank_confirmed"),
            do=fx(stand("residents", 2), stand("company", -2), meet("vance"))),
         ch("Walk away without answering (-1 Company)", "spine_menu",
            do=stand("company", -1)),
     ])


node("ev_landfall",
     "Tomorrow the ship anchors off Bridgetown, and the lighter crews are already testing their lines. Tomas Veiga, 'Slack', leans over the rail. "
     "'Parcel run tomorrow. Fresh fruit from the anchorage market, no Commissary stamp. I'll pay you sixty to carry it down to the lighter. No questions.'",
     [
         ch("Carry the parcel for Slack (+60 LC, -1 Company)", "spine_menu",
            when=not_flag("smuggler"),
            do=fx(flag("smuggler"), earn(60), stand("company", -1), meet("slack"))),
         ch("Leave a tip for the lighter crew (-20 LC, +1 Crew)", "spine_menu",
            when=can_pay(20), do=fx(pay(20), stand("crew", 1))),
         ch("Decline and go out to the Spine", "spine_menu"),
     ])


# ---------------------------------------------------------------- random encounters

node("rnd_seasick",
     "A young man in a Deck 9 maintenance jacket holds onto a rail with both hands. His face is grey. "
     "'Don't tell me it's the roll,' he says. 'Everyone keeps telling me it's the roll.'",
     [
         ch("Help him to a bench and sit with him (+1 Residents)", "spine_menu",
            do=stand("residents", 1)),
         ch("Give him a ration chit (+1 Residents)", "spine_menu",
            when=has("ration_chit"), do=fx(take("ration_chit"), stand("residents", 1))),
         CARRY_ON,
     ])

node("rnd_wallet",
     "Beside the rail platform a leather wallet lies half under a bench. Inside: a Hotel Directorate card, a photo of a dog, and forty ledger credits in a clip.",
     [
         ch("Take it to the Hotel Directorate desk (+1 Residents)", "spine_menu",
            do=fx(stand("residents", 1), flag("returned_wallet"))),
         ch("Keep the forty credits (-1 Residents)", "spine_menu",
            do=fx(earn(40), stand("residents", -1))),
         ch("Hand it to the Wardens (+1 Company)", "spine_menu",
            do=stand("company", 1)),
     ])

node("rnd_knock",
     "Late in the rest period a knock comes through a wall you share with a cabin you have never seen anyone enter. Five quick knocks, then nothing. "
     "Every child on the terrace learns that pattern in their first week. It means: I need help.",
     [
         ch("Knock back and go to the door (+2 Residents)", "spine_menu",
            do=fx(flag("helped_neighbour"), stand("residents", 2))),
         ch("Call the terrace alarm from the nearest panel (+1 Crew)", "spine_menu",
            do=stand("crew", 1)),
         ch("Stay in your cabin and turn over (-1 Residents)", "spine_menu",
            do=stand("residents", -1)),
     ])

node("rnd_rumour",
     "Two girls on the Spine are telling a story loud enough for everyone to hear. The Sleeping Man in the Water Vault has woken up, "
     "and the tanks are knocking because he is hungry for the Atlantic.",
     [
         ch("Ask them to tell it properly", "spine_menu",
            do=sleeping_man_story),
         ch("Tell them the knocking is a pump valve (+1 Crew, -1 Residents)", "spine_menu",
            do=fx(stand("crew", 1), stand("residents", -1))),
         CARRY_ON,
     ])

node("rnd_tally",
     "A child is chalking a countdown on the Spine wall: seven strokes, a diagonal, three more. The port is seven days away. "
     "The child looks up. 'Do you want to add one? You get to choose the mark.'",
     [
         ch("Add a mark of your own (+1 Residents)", "spine_menu",
            do=fx(stand("residents", 1), flag("chalked_spine"))),
         ch("Correct the count: it's six days (+1 Crew)", "spine_menu",
            do=stand("crew", 1)),
         CARRY_ON,
     ])

node("rnd_rail",
     "The rail car stops between stations and the lights drop to amber. Somewhere in the next car a baby is crying. "
     "An announcement says: power interlock, twenty minutes.",
     [
         ch("Talk to the people around you (+1 Residents)", "spine_menu",
            do=stand("residents", 1)),
         ch("Use the intercom to ask for a status report (+1 Crew)", "spine_menu",
            do=fx(stand("crew", 1), flag("asked_rail"))),
         ch("Sit quietly and wait (+2 health)", "spine_menu",
            do=heal(2)),
     ])

node("rnd_blackmarket",
     "A man in a dark coat has a net bag of oranges. Port fruit, not Commissary. 'Thirty credits,' he says. "
     "'Don't ask where they came from. Don't ask where they're going.'",
     [
         ch("Buy the oranges (30 LC, +8 health, -1 Company)", "spine_menu",
            when=can_pay(30), do=fx(pay(30), heal(8), stand("company", -1))),
         ch("Report him to the Wardens (+1 Company)", "spine_menu",
            do=stand("company", 1)),
         CARRY_ON,
     ])

node("rnd_recipe",
     "A stall in the Aft Hall is handing out samples of fermented vegetables on a wooden board. The taste is sour, sharp and unexpectedly good. "
     "The stallholder is watching to see what you think.",
     [
         ch("Eat a second piece (+4 health)", "spine_menu",
            do=heal(4)),
         ch("Ask for the recipe (+1 Residents)", "spine_menu",
            do=fx(stand("residents", 1), flag("asked_recipe"))),
         CARRY_ON,
     ])


node("aft_hall",
     "The Aft Hall is the busiest kitchen on the ship, a long room of steam and clatter. Chen Mei-ling runs the grill for the Galley Association "
     "and does not look up. 'You're standing in my light,' she says. 'Ask or move.'",
     [
         ch("Buy a hot meal (8 LC, +10 health)", "here",
            when=can_pay(8), do=fx(pay(8), heal(10), meet("chenmei"))),
         ch("Work the grill for a shift (-4 health, +2 Crew)", "here",
            do=fx(hurt(4), stand("crew", 2), flag("worked_grill"), meet("chenmei"))),
         ch("Ask for the recipe for the fermented vegetables (+1 Residents)", "here",
            when=not_flag("asked_recipe"),
            do=fx(stand("residents", 1), flag("asked_recipe"), meet("chenmei"))),
         ch("Sit with the night shift and listen to the gossip (+1 Crew)", "here",
            do=fx(flag("heard_listeners_moved"), stand("crew", 1), meet("chenmei"))),
         LEAVE,
     ])

node("ev_audit",
     "Ines Carvalho, a Company auditor with a slim tablet, stops you at the rail. 'Routine. The Hotel Directorate gives me one account in a hundred each quarter. "
     "Yours came up this morning.' She looks at your balance, then at you.",
     [
         ch("Show her everything (+1 Company)", "spine_menu",
            do=fx(stand("company", 1), flag("audited_clean"), meet("carvalho"))),
         ch("Tell her the swap ledger is a personal note", "spine_menu",
            when=has("swap_ledger"),
            do=fx(flag("audit_lie"), meet("carvalho"))),
         ch("Offer her a cup of tea and say nothing (15 LC, +2 Company)", "spine_menu",
            when=can_pay(15),
            do=fx(pay(15), stand("company", 2), flag("bribed_auditor"), meet("carvalho"))),
         ch("Walk away without answering (-1 Company)", "spine_menu",
            do=stand("company", -1)),
     ])

node("rnd_ghost",
     "On Deck 14 a draught lifts the curtains of an empty cabin and lets them fall. At the end of the corridor a woman in a grey coat walks away from you towards the stairwell. "
     "The Hotel Directorate has an old report about her and a ventilation fault that was 'fixed' in 2071.",
     [
         ch("Follow her down the stairwell", "spine_menu",
            do=fx(flag("followed_grey_coat"), give("grey_glove"))),
         ch("Report it to the Hotel Directorate (+1 Residents)", "spine_menu",
            do=stand("residents", 1)),
         CARRY_ON,
     ])

node("rnd_lostchild",
     "A girl of about six stands by the rail platform holding a shore clock set three hours wrong. 'My mum said wait here,' she says. "
     "Her mother is nowhere in sight.",
     [
         ch("Walk her to the shift-change hall to find her mother (+2 Residents)", "spine_menu",
            do=fx(stand("residents", 2), flag("helped_child"))),
         ch("Call the Wardens (+1 Company)", "spine_menu",
            do=stand("company", 1)),
         ch("Keep her company until her mother comes (+2 health)", "spine_menu",
            do=heal(2)),
     ])

node("rnd_fight",
     "Outside the Harbour Hall two lighter hands are shouting over a crate with a Commissary seal that has been cut open. "
     "One of them is bleeding from the lip, and the other has a tin in his fist.",
     [
         ch("Step between them (-3 health, +2 Crew)", "spine_menu",
            do=fx(hurt(3), stand("crew", 2))),
         ch("Go and find a Warden (+1 Company)", "spine_menu",
            do=stand("company", 1)),
         ch("Pocket a tin from the crate while they're shouting (+15 LC, -2 Residents)", "spine_menu",
            do=fx(earn(15), stand("residents", -2), flag("took_crate"))),
     ])

node("rnd_gait",
     "An old man on the stairs of Terrace 16 slips on a wet step, and a woman with a shopping net is about to go down with him.",
     [
         ch("Catch the woman (+2 Residents, -3 health)", "spine_menu",
            do=fx(hurt(3), stand("residents", 2))),
         ch("Call for the gait coaches (+1 Residents)", "spine_menu",
            do=fx(stand("residents", 1), meet("lind"))),
         ch("Step past them (-1 Residents)", "spine_menu",
            do=stand("residents", -1)),
     ])


# ---------------------------------------------------------------- endings

def pick_ending(g):
    if g.flag("helped_escape") and not g.flag("captain_ally"):
        return "handover"
    if g.flag("council_seat"):
        return "council_chair"
    if g.flag("bought_silence") and g.standing["company"] >= 4:
        return "company_man"
    if g.flag("tank_confirmed") and g.flag("tank_reported") and not g.flag("bought_silence"):
        return "sleeping_man_wakes"
    if g.flag("storm_hero") and g.standing["crew"] >= 3:
        return "storm_hero"
    if g.flag("swapped") and g.credits >= 250:
        return "broker_ledger"
    if g.has("shore_clock") and g.flag("letter_delivered"):
        return "shore_clock"
    if g.flag("smuggler"):
        return "shore_runner"
    if g.flag("committee_member") and g.standing["residents"] >= 4:
        return "terrace_chair"
    if g.flag("followed_grey_coat"):
        return "grey_coat"
    if g.flag("resisted_company") and not any(g.flag(f) for f in ("smuggler", "bribed_auditor", "audit_lie")):
        return "clean_hands"
    if g.standing["residents"] >= 3:
        return "good_neighbour"
    return "crossing_complete"


ENDINGS = {
    "handover": ("Handover",
                 "The Wardens take the stowaway's escape seriously. When the ship anchors off Bridgetown, a port police launch comes alongside, "
                 "and the Master files her report within the Articles' twenty-four hours. You are held until the port takes custody. "
                 "You spend the last days of the voyage on the wrong side of a door you once helped open."),
    "council_chair": ("Member for Ward 23",
                      "You take your seat in the Solarium council office on the morning of the anchorage. The first item on the agenda is the water-price referendum, "
                      "and the petition sheets are stacked on your desk. Ben Oduya brings you a cup of tea that has never been near a kettle that boils. "
                      "The Residents' Council is yours to argue with now, and for the next three years it will be."),
    "company_man": ("The Atlantic Committee",
                    "Gregor Vance's committee meets for the first time in the Company boardroom, and you are the youngest member at the table. "
                    "The Tank 17 report is marked 'closed'. Your name is on the minutes, and so is the sum of money that went with it. "
                    "You will be offered more, and you know that you will take it."),
    "sleeping_man_wakes": ("The Sleeping Man Wakes",
                           "The Water Department opens Tank 17 during the Bridgetown call and finds the baffle cracked through. "
                           "Nadia Okonkwo-Reyes's note goes into the Company's report, with your name beside it. The tank is repaired in port. "
                           "Children on the terraces say the Sleeping Man is awake, and for once the Engineering crews do not joke about it."),
    "storm_hero": ("Lines in the Storm",
                   "On the night of the storm you stayed on the lines when the wind wanted you off them. Ruud Haarsma enters your name in the Sail Department's roll of honour, "
                   "and the crew who held the masts with you buy you a drink in the Galley Association hall. The mast crews will remember that night for the rest of their lives."),
    "broker_ledger": ("The Broker's Ledger",
                      "Pilar Ferreira's swap went through. You have a bank balance that could buy a Grade 0 suite, and a page of cabins that the Hotel Directorate would very much like to see. "
                      "At Bridgetown you sit with her on the quay and you start a list of your own. You have learned that housing is the one thing aboard that money can actually buy."),
    "shore_clock": ("Shore Clock",
                    "Mags Doucet's clock ticks on your desk, set to Lisbon, and you keep it right at every port call. At Bridgetown you walk to the post office and "
                    "write a letter to Rui in Lisbon, telling him that his mother is well, that the house can wait, and that she is waiting to see him."),
    "shore_runner": ("Shore Runner",
                     "Slack's parcel is delivered to a stall on the quay, and the money is in your pocket before the lighter pulls away. "
                     "Nobody at the anchorage looks twice at a resident walking the harbour road with empty hands and a full purse. "
                     "You are not sure you are proud of it, but you are sure you will do it again."),
    "good_neighbour": ("A Good Neighbour",
                       "The terraces know your name. Tavi knocks through the wall at the end of the voyage, a pattern you have learned to answer. "
                       "On the last night the terrace common room is full of people eating, telling stories and comparing the marks on their walls."),
    "crossing_complete": ("Crossing Complete",
                          "The lighters carry you to the quay at Bridgetown, and the ground does not move. You stand there for a long time, waiting for it to stop. "
                          "Behind you the Halcyon Meridian waits at anchor with her sails furled, ready for the next crossing and the next set of names on the batch slips."),
    "terrace_chair": ("Chair of Terrace 14",
                      "The terrace gives you its chair in the spring vote, and with it a key to the garden shed, the laundry rota and the names of every child who is ill. "
                      "You meet the Residents' Council liaison once a week and make sure the water rise is explained to people before it arrives on their bills. "
                      "It is not glamorous work. It is the work that keeps the terraces talking to each other."),
    "grey_coat": ("The Woman on Deck 14",
                  "You follow the grey coat down the stairwell, and at the bottom she is gone. The glove in your pocket is damp, though no sea has been near Deck 14 in years. "
                  "The Hotel Directorate files your report under 'ventilation', and the terrace children add your name to their stories about the woman who walks the corridors at night. "
                  "Sometimes, when the ship rolls, you think you hear footsteps behind you on the stairs."),
    "clean_hands": ("Clean Hands",
                    "When the Company offered you a price for silence, you refused, and you meant it. The Gazette runs your interview under a headline you did not write, "
                    "but every word in it is yours. At the anchorage the auditors leave your ledger alone, and for the first time in the voyage you sleep the whole night through."),
    "burial": ("Burial at Sea",
               "You do not reach the anchorage. The Master reads your name at the next evening's muster, and the Chaplaincy lays a bird on your place on the memorial board. "
               "The sea takes the weight of your passing without a sound, the way it takes everything aboard the ship."),
}


def ending_text(g):
    key = g.counts.get("ending", "crossing_complete")
    title, body = ENDINGS[key]
    summary = (f"Days aboard: {min(g.day, VOYAGE_DAYS)}. Health {g.health}. Ledger {g.credits} LC. "
               f"Standing: Company {g.standing['company']:+d}, Residents {g.standing['residents']:+d}, "
               f"Crew {g.standing['crew']:+d}. Things carried: {len(g.inventory)}.")
    return (f"ENDING: {title}\n\n{body}\n\n{summary}\n\n"
            f"This voyage has {len(ENDINGS)} possible endings. Play again to find the others.")


node("ending", ending_text, [ch("Close the logbook", None)])


# ---------------------------------------------------------------- engine

def show_inventory(g):
    """Stays open until the player presses Enter, so item numbers never reach the place menu."""
    while True:
        if not g.inventory:
            say("Your pockets are empty.")
            return
        print("\nINVENTORY")
        for i, key in enumerate(g.inventory, 1):
            print(f"  {i}. {ITEMS[key]['name']}: {ITEMS[key]['desc']}")
        raw = read_line("Enter an item number to use it, or press Enter to go back: ")
        if not raw:
            print()
            return
        if raw.isdigit() and 1 <= int(raw) <= len(g.inventory):
            key = g.inventory[int(raw) - 1]
            use = ITEMS[key].get("use")
            if use:
                use(g)
                g.remove_item(key)
                say(f"You use the {ITEMS[key]['name'].lower()}.")
                print()
                return
            say(f"You turn the {ITEMS[key]['name'].lower()} over in your hands and put it back. It has no use here.")
        else:
            say("No item has that number.")


def show_status(g):
    s = g.standing
    print(f"\nDay {g.day} of {VOYAGE_DAYS}   Health {g.health}/100   Ledger {g.credits} LC")
    print(f"Standing: Company {s['company']:+d}   Residents {s['residents']:+d}   Crew {s['crew']:+d}\n")


def show_people(g):
    if not g.met:
        say("You haven't been introduced to anyone yet.")
        return
    print()
    for key in g.met:
        name, role = PEOPLE[key]
        print(f"  {name}: {role}")
    print()


def show_options(options):
    for i, c in enumerate(options, 1):
        print(f"  {i}. {c['label']}")
    print("  [i] inventory   [s] status   [p] people   [q] quit")


def ask(g, options):
    print()
    show_options(options)
    while True:
        raw = read_line("> ")
        if raw == "i":
            show_inventory(g)
            show_options(options)
        elif raw == "s":
            show_status(g)
            show_options(options)
        elif raw == "p":
            show_people(g)
            show_options(options)
        elif raw == "q":
            if read_line("Quit the game? (y/n) ") == "y":
                raise SystemExit("\nYou close the logbook. The ship sails on without you.")
            show_options(options)
        elif raw.isdigit() and 1 <= int(raw) <= len(options):
            print()
            return options[int(raw) - 1]
        else:
            print("  Type the number of one of the choices above.")


def play(g):
    """Runs the game loop.

    Choices marked "here" are interactions: they stay in the current place, and each one
    can only be taken once per visit. Any other choice leaves the place. Only leaving
    the place (or going to an event) moves on to the next node and the next day.
    """
    current = "spine"
    used = set()          # interactions already taken during this visit
    show_text = True      # redraw the place's description only when arriving
    while current:
        nd = NODES[current]
        if nd["enter"]:
            override = nd["enter"](g)
            if isinstance(override, str):
                current = override
                used, show_text = set(), True
                continue
        if g.health <= 0 and current != "ending":
            g.counts["ending"] = "burial"
            current = "ending"
            used, show_text = set(), True
            continue
        if show_text:
            text = nd["text"](g) if callable(nd["text"]) else nd["text"]
            say(text)
        options = [c for c in nd["choices"]
                   if (c["when"] is None or c["when"](g))
                   and not (c["to"] == "here" and c["label"] in used)]
        if not options:
            say("There is nothing more to do here. You head back to the Spine.")
            current = "spine_menu"
            used, show_text = set(), True
            continue
        choice = ask(g, options)
        if choice["do"]:
            choice["do"](g)
        if choice["to"] == "here":
            used.add(choice["label"])
            show_text = False
            continue
        used, show_text = set(), True
        target = choice["to"]
        current = target(g) if callable(target) else target


# ---------------------------------------------------------------- setup

BACKGROUNDS = [
    {"name": "Engineering apprentice, Deck 6",
     "text": "You learned valves before you learned to drive. Chief Engineer Brandt's team took you on at seventeen, and you still smell of machine oil on your days off.",
     "items": ["torch"], "standing": {"crew": 1}, "credits": 120},
    {"name": "Terrace family, Tower West",
     "text": "Your family of four shares fifty square metres on Terrace 14. Your mother works in the laundries and your father is a carer at the Harbour Care Complex.",
     "items": ["family_photo"], "standing": {"residents": 1}, "credits": 160},
    {"name": "Sail crew, orange jacket",
     "text": "You climb the masts for a living. Your fear of heights was cured in your first month, and now the wind is the only thing you trust.",
     "items": ["harness"], "standing": {"crew": 1}, "credits": 130},
    {"name": "Hotel Directorate clerk",
     "text": "You keep the housing ledger for Terraces 10 to 16. You know who is behind on rent and who is about to get a better cabin, and you have never told anyone.",
     "items": ["access_pass"], "standing": {"company": 1}, "credits": 220},
]

INTRO = (
    "You are one of 300,000 people aboard the Halcyon Meridian, a wind-assisted ship a kilometre and a half long. "
    "She is crossing from Lisbon to Bridgetown, about twenty days of open Atlantic. Your choices over the voyage will decide "
    "where you stand with the Company, the Residents and the crew, and what you carry when the anchor goes down at the end."
)


def choose_background():
    print("Who are you aboard?")
    for i, b in enumerate(BACKGROUNDS, 1):
        print(f"  {i}. {b['name']}")
    while True:
        raw = read_line("> ")
        if raw.isdigit() and 1 <= int(raw) <= len(BACKGROUNDS):
            return BACKGROUNDS[int(raw) - 1]
        print("Type the number of a background.")


def new_game():
    try:
        name = input("Your name: ").strip() or "Passenger"
    except EOFError:
        raise SystemExit("\nGame closed.")
    bg = choose_background()
    g = Game(name)
    g.credits = bg["credits"]
    for who, n in bg["standing"].items():
        g.standing[who] += n
    g.inventory = list(bg["items"])
    say(INTRO)
    say(f"{name}: {bg['text']}")
    return g


def main():
    print("=" * WIDTH)
    print("THE HALCYON MERIDIAN".center(WIDTH))
    print("=" * WIDTH)
    print()
    g = new_game()
    while True:
        play(g)
        again = read_line("Play again? (y/n) ")
        if again != "y":
            break
        g = new_game()
    print("Fair winds.")


if __name__ == "__main__":
    main()
