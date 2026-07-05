#!/usr/bin/env python3
"""Quoti Live — original quote library generator.
Created By: iTechSmart Inc.

Generates 10,000 original aphorisms, exactly balanced: 20 categories x 500.
Deterministic (seeded) so rebuilds are reproducible.

Usage: python3 _build/gen_quotes.py
Writes: assets/data/quotes/index.json + assets/data/quotes/<slug>.json
"""
import json
import pathlib
import random
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "data" / "quotes"
PER_CATEGORY = 500

# ---------------------------------------------------------------- templates
# Slots: {a}/{b} abstract concepts · {o} obstacle · {m} metaphor (with article)
#        {p} person (with article) · {v} verb phrase (3rd person plural base)
#        {r} reward/outcome · {t} time word
TEMPLATES = [
    "{A} is the quiet decision to begin again after {o} has had its say.",
    "Where {o} builds walls, {a} builds doors.",
    "{A} whispers while {o} shouts — and still wins.",
    "Treat {a} like {m}: tend it daily and it will repay you for decades.",
    "The distance between you and {r} is measured in days of {a}, not moments of luck.",
    "{P} does not wait for permission to {v}.",
    "Feed your {a} in the morning and {o} will starve by evening.",
    "{A} is {m}: planted quietly today, harvested for a lifetime.",
    "No one drifts toward {r}; they are pulled there by {a}.",
    "When {o} knocks, send {a} to answer the door.",
    "{A} turns {o} into instruction and instruction into {r}.",
    "The smallest act of {a} outweighs the grandest intention.",
    "You cannot borrow {a}, but you can build it — one {t} at a time.",
    "{O} is loud, brief and hollow; {a} is quiet, long and full.",
    "Every {t} spent on {a} is a brick in the house of {r}.",
    "{P} measures progress in {a}, not applause.",
    "Let {a} be the habit and {r} will be the consequence.",
    "{A} is not the absence of {o}; it is the decision that {r} matters more.",
    "First you choose {a}; then {a} quietly chooses your future.",
    "The road to {r} is paved with one unglamorous {t} of {a} after another.",
    "{A} and {b} are the two hands that build {r}.",
    "Trade the comfort of {o} for the company of {a}.",
    "{A} begins where excuses end.",
    "What {o} takes in a moment, {a} rebuilds into something stronger.",
    "{P} plants {m} knowing someone else may enjoy the shade.",
    "Your {a} today is a gift to the person you are becoming.",
    "{O} asks what could go wrong; {a} asks what could go right — and acts.",
    "Guard your {a} the way you would guard {m}.",
    "{A} rarely roars. More often it {v}, again and again, until the walls give way.",
    "{R} arrives on foot after {a} has walked ahead for years.",
    "A life led by {a} needs no audience to feel like {r}.",
    "{A} is choosing the harder today for the easier decade.",
    "Do not confuse {o} with fate; {a} rewrites it daily.",
    "{P} carries {a} like a compass through every storm of {o}.",
    "Between stimulus and response sits {a} — spend it well.",
    "{A} is the interest rate on every promise you keep to yourself.",
    "When the map fails, {a} becomes the territory.",
    "{O} ends conversations; {a} starts them over.",
    "The world makes room for {p} who knows where their {a} points.",
    "{A} without {b} is a spark without kindling.",
    "Practice {a} until {o} forgets your address.",
    "{R} is rented, and the rent is due every {t} in {a}.",
    "Turn your wounds from {o} into wells of {a}.",
    "{A} is doing the next right thing when no one is keeping score.",
    "Even {m} began as something small that refused to stay small — so does {a}.",
    "Where attention goes, {a} grows; where {a} grows, {r} follows.",
    "{P} fails forward: every stumble a stone laid toward {r}.",
    "What you repeat, you become — so repeat {a}.",
    "{O} is a debt collector; {a} pays in advance.",
    "Some chase {r}; the wise raise {a} and let {r} come home on its own.",
]

# --------------------------------------------------------- category lexicons
CATEGORIES = {
    "motivation": {
        "name": "Motivation", "emoji": "🔥",
        "a": ["motivation", "drive", "hunger", "momentum", "fire", "purpose", "ambition", "initiative", "energy", "willingness", "spark", "determination"],
        "o": ["procrastination", "doubt", "hesitation", "apathy", "comfort", "excuse-making", "inertia", "snooze-button thinking"],
        "m": ["a struck match", "a morning sunrise", "an engine warming", "a drumbeat", "a lit fuse", "a rising tide", "a first step", "a spark in dry grass"],
        "p": ["a self-starter", "the hungry", "a dreamer with a deadline", "the early riser", "a beginner with heart", "the one who shows up"],
        "v": ["takes the first step", "shows up early", "starts before it's ready", "moves anyway", "begins again", "lights the match"],
        "r": ["momentum", "a life in motion", "the finished work", "an unstoppable week", "real progress", "the breakthrough"],
        "t": ["morning", "day", "hour", "sunrise", "Monday", "minute"],
    },
    "success": {
        "name": "Success", "emoji": "🏆",
        "a": ["preparation", "consistency", "focus", "execution", "excellence", "follow-through", "craftsmanship", "persistence", "standards", "practice", "patience", "commitment"],
        "o": ["shortcuts", "overnight thinking", "comparison", "complacency", "hype", "luck-chasing", "half-effort", "applause-hunting"],
        "m": ["a cathedral built stone by stone", "a compound-interest account", "an iceberg", "a harvest", "a long staircase", "a masterpiece under a cloth", "a well-run kitchen", "a ship's keel"],
        "p": ["a craftsman", "the prepared", "a finisher", "the quietly excellent", "a professional", "the one who stayed"],
        "v": ["finishes what it starts", "raises the standard", "does the reps", "keeps the promise", "polishes the details", "outlasts the noise"],
        "r": ["mastery", "a reputation that precedes you", "the summit", "lasting achievement", "work that speaks for itself", "the win that endures"],
        "t": ["rep", "season", "year", "attempt", "draft", "practice"],
    },
    "wisdom": {
        "name": "Wisdom", "emoji": "🦉",
        "a": ["wisdom", "discernment", "perspective", "humility", "reflection", "patience", "understanding", "judgment", "curiosity", "listening", "self-knowledge", "clarity"],
        "o": ["certainty", "haste", "vanity", "noise", "assumption", "cleverness without depth", "borrowed opinion", "the rush to answer"],
        "m": ["an old oak", "a deep well", "a lantern in fog", "a river that has seen many stones", "a library at dusk", "a mountain that outwaits the weather", "a slow-brewed tea", "a polished mirror"],
        "p": ["an elder", "the patient student", "a good listener", "the humble learner", "a keeper of questions", "the quiet observer"],
        "v": ["asks one more question", "waits before speaking", "reads the silence", "weighs before it wants", "learns from every teacher", "studies its own reflection"],
        "r": ["understanding", "peace of mind", "sound judgment", "a well-lived life", "clear sight", "truth you can stand on"],
        "t": ["question", "pause", "season", "conversation", "mistake", "evening"],
    },
    "leadership": {
        "name": "Leadership", "emoji": "🧭",
        "a": ["leadership", "service", "example", "accountability", "vision", "trust", "listening", "clarity", "stewardship", "courage under pressure", "empathy", "conviction"],
        "o": ["ego", "micromanagement", "blame", "title-worship", "fear of hard conversations", "popularity-seeking", "credit-hoarding", "indecision"],
        "m": ["a lighthouse", "a compass", "a keel in rough water", "the first domino", "a bridge others cross", "a steady drumbeat", "a north star", "an open door"],
        "p": ["a servant leader", "the first to arrive", "a coach", "the calm in the room", "a standard-bearer", "the one who takes the blame and shares the credit"],
        "v": ["goes first", "listens loudest", "absorbs the pressure", "holds the standard", "clears the path", "keeps the promise public"],
        "r": ["a team that believes", "trust that compounds", "a culture worth joining", "people who grow", "a mission that outlives you", "followers who become leaders"],
        "t": ["decision", "meeting", "crisis", "quarter", "conversation", "example"],
    },
    "business": {
        "name": "Business", "emoji": "💼",
        "a": ["strategy", "systems", "customer obsession", "cash discipline", "clarity", "execution", "positioning", "reputation", "operational excellence", "focus", "resilience", "good bookkeeping"],
        "o": ["busywork", "vanity metrics", "debt-fueled haste", "shiny-object syndrome", "guesswork", "bloated overhead", "chaos", "untracked spending"],
        "m": ["a well-kept ledger", "a flywheel", "a deep moat", "a trusted brand", "a machine with oiled gears", "a storefront with clean windows", "a supply chain in rhythm", "a balance sheet at peace"],
        "p": ["a builder", "an owner who knows the numbers", "the operator", "a founder with focus", "the entrepreneur who plans", "a merchant of trust"],
        "v": ["knows its numbers", "serves the customer twice", "builds the system", "protects the margin", "keeps the books clean", "delivers before the deadline"],
        "r": ["a business that runs without you", "loyal customers", "healthy margins", "a fundable company", "an enterprise that endures", "freedom on your own terms"],
        "t": ["quarter", "invoice", "customer", "process", "review", "decision"],
    },
    "wealth": {
        "name": "Money & Wealth", "emoji": "💰",
        "a": ["saving", "patience", "budgeting", "investing", "financial literacy", "frugality", "stewardship", "delayed gratification", "ownership", "planning", "discipline with dollars", "generosity"],
        "o": ["impulse spending", "lifestyle inflation", "get-rich-quick schemes", "status-chasing", "untracked money", "consumer debt", "financial denial", "keeping up appearances"],
        "m": ["a seed vault", "compound interest", "an orchard planted young", "a dam that stores the river", "a quiet portfolio", "a well that refills", "an emergency fund at rest", "a deed in your name"],
        "p": ["a patient investor", "the quiet millionaire next door", "a saver", "the owner, not the owed", "a steward", "the one who pays themselves first"],
        "v": ["pays itself first", "buys assets, not applause", "tracks every dollar", "waits out the market", "lives below the means", "lets time do the lifting"],
        "r": ["financial freedom", "options money can buy", "a calm bank account", "generational stability", "wealth that whispers", "the power to say no"],
        "t": ["dollar", "paycheck", "month", "decade", "purchase", "deposit"],
    },
    "discipline": {
        "name": "Discipline", "emoji": "⚔️",
        "a": ["discipline", "routine", "self-control", "structure", "consistency", "the daily standard", "training", "order", "restraint", "practice", "punctuality", "commitment"],
        "o": ["mood-dependence", "impulse", "chaos", "the comfortable path", "someday-thinking", "distraction", "the snooze button", "negotiating with yourself"],
        "m": ["a sharpened blade", "a soldier's morning", "a metronome", "a well-worn path", "a trellis for the vine", "an anvil", "a locked gate", "a drill repeated a thousand times"],
        "p": ["a professional", "the trained", "an athlete in the off-season", "the one who keeps their word to themselves", "a monk of the mundane", "the early morning"],
        "v": ["shows up on schedule", "does it especially when it's hard", "repeats the boring rep", "keeps the appointment with itself", "closes the loop", "obeys the plan, not the mood"],
        "r": ["freedom", "self-respect", "a body and mind that answer", "days that compound", "an unshakeable routine", "the quiet pride of kept promises"],
        "t": ["rep", "morning", "session", "habit", "appointment", "standard"],
    },
    "courage": {
        "name": "Courage", "emoji": "🦁",
        "a": ["courage", "boldness", "honesty under pressure", "the willingness to be seen", "daring", "conviction", "backbone", "audacity", "moral bravery", "risk-taking", "speaking up", "the first move"],
        "o": ["fear", "the opinion of strangers", "perfectionism", "the safe seat", "silence", "what-if thinking", "the crowd's comfort", "hesitation"],
        "m": ["a first parachute jump", "a door opened in the dark", "a hand raised alone", "a small boat leaving harbor", "a voice that cracks but continues", "a match struck in wind", "a step onto new ice", "a flag planted"],
        "p": ["the brave", "a truth-teller", "the first volunteer", "a beginner in public", "the one who goes anyway", "a heart that trembles and tries"],
        "v": ["raises its hand", "speaks the unpopular truth", "leaves the harbor", "asks anyway", "stands back up", "walks toward the fear"],
        "r": ["a bigger life", "self-trust", "the story worth telling", "doors that only open from the inside", "freedom from the crowd", "the other side of fear"],
        "t": ["leap", "ask", "attempt", "moment", "risk", "yes"],
    },
    "resilience": {
        "name": "Resilience", "emoji": "🌊",
        "a": ["resilience", "grit", "endurance", "recovery", "adaptability", "toughness", "perseverance", "bouncing back", "steadiness", "stamina", "the long game", "getting up again"],
        "o": ["the setback", "rejection", "the storm", "failure's echo", "burnout", "bad luck", "the closed door", "the hard season"],
        "m": ["bamboo in a storm", "a river around rock", "a callus", "a lighthouse in weather", "an anvil that outlasts hammers", "a tree ringed by hard winters", "a tide that returns", "a bone healed stronger"],
        "p": ["a survivor", "the twice-rejected", "a comeback in progress", "the storm-tested", "one who rebuilds", "the last one standing"],
        "v": ["bends without breaking", "returns like the tide", "rebuilds on the same ground", "outlasts the weather", "takes the hit and stays", "turns the page"],
        "r": ["the comeback", "strength with scars", "a story of return", "unbreakable calm", "the finish line", "roots no storm can pull"],
        "t": ["storm", "setback", "round", "winter", "fall", "recovery"],
    },
    "growth": {
        "name": "Personal Growth", "emoji": "🌱",
        "a": ["growth", "learning", "self-improvement", "curiosity", "feedback", "stretching", "becoming", "practice", "unlearning", "evolution", "the beginner's mind", "reinvention"],
        "o": ["the comfort zone", "the fixed mindset", "old stories", "the fear of looking new", "stagnation", "yesterday's identity", "the plateau", "know-it-all thinking"],
        "m": ["a seedling through concrete", "a snake shedding skin", "a draft becoming a book", "a chrysalis", "rings inside a tree", "a staircase built while climbing", "a garden in spring", "a map redrawn"],
        "p": ["a lifelong student", "the work in progress", "a version two", "the one still learning", "an apprentice of life", "the becoming"],
        "v": ["outgrows its old skin", "asks better questions", "reads the feedback", "stretches past the edge", "starts as a beginner", "updates the map"],
        "r": ["the person you're becoming", "range", "new rooms in the mind", "capability", "a wider life", "the next version of you"],
        "t": ["lesson", "chapter", "iteration", "stretch", "season", "mistake"],
    },
    "happiness": {
        "name": "Happiness", "emoji": "☀️",
        "a": ["happiness", "contentment", "joy", "presence", "simplicity", "lightness", "savoring", "enough-ness", "play", "wonder", "cheerfulness", "inner sunshine"],
        "o": ["comparison", "the hedonic treadmill", "someday-thinking", "accumulation", "the highlight reel", "rushing", "grasping", "postponed living"],
        "m": ["a sunlit kitchen", "a child's laugh", "an ordinary Tuesday loved well", "a warm loaf shared", "a porch at golden hour", "a song you forgot you knew", "a small boat on calm water", "an open window in spring"],
        "p": ["the grateful", "a person fully here", "the easily delighted", "one who needs little", "a collector of small joys", "the present-tense heart"],
        "v": ["savors the ordinary", "laughs first", "wants what it has", "keeps the window open", "finds the sun in small rooms", "arrives fully"],
        "r": ["a light heart", "days that feel like enough", "quiet delight", "a life you don't need a vacation from", "sunlight from the inside", "the ordinary made golden"],
        "t": ["moment", "morning", "breath", "meal", "walk", "today"],
    },
    "love": {
        "name": "Love", "emoji": "❤️",
        "a": ["love", "tenderness", "devotion", "attention", "kindness", "affection", "loyalty", "presence", "forgiveness", "care", "the daily choosing", "openness"],
        "o": ["pride", "scorekeeping", "distraction", "the unsaid", "fear of being known", "resentment", "taking for granted", "the closed door"],
        "m": ["a fire tended nightly", "a garden kept by two", "a bridge rebuilt each morning", "a hand held in the dark", "an old song danced slowly", "a letter kept for years", "a lamp left on", "roots grown together"],
        "p": ["a devoted heart", "the one who stays", "a keeper of small promises", "the first to apologize", "a listener at midnight", "two people choosing again"],
        "v": ["chooses again each morning", "listens past the words", "shows up in the small hours", "forgives first", "remembers the little things", "leaves the light on"],
        "r": ["a love that ages well", "being fully known", "home in another person", "a thousand ordinary days made warm", "trust like bedrock", "the long romance of staying"],
        "t": ["morning", "gesture", "apology", "anniversary", "goodnight", "small act"],
    },
    "friendship": {
        "name": "Friendship", "emoji": "🤝",
        "a": ["friendship", "loyalty", "showing up", "honesty between friends", "laughter shared", "trust", "camaraderie", "kept confidence", "being there", "reciprocity", "warmth", "true company"],
        "o": ["convenience-only ties", "flattery", "fair-weather company", "the unreturned call", "envy", "gossip", "distance left untended", "score-keeping"],
        "m": ["an old front porch", "a worn path between two houses", "a rope tested by storms", "a standing Tuesday call", "an inside joke decades old", "a chair always saved", "a campfire circle", "a spare key trusted"],
        "p": ["a three-a.m. friend", "the one who remembers", "an honest mirror", "the friend who drives over", "a keeper of your secrets", "the same laugh across years"],
        "v": ["answers at midnight", "tells the loving truth", "saves you a seat", "celebrates your wins louder than you", "keeps the secret", "walks in when others walk out"],
        "r": ["a friend for the decades", "chosen family", "laughter that survives distance", "someone to call first", "an easier road shared", "wealth no bank can hold"],
        "t": ["call", "visit", "laugh", "favor", "year", "check-in"],
    },
    "family": {
        "name": "Family", "emoji": "🏡",
        "a": ["family", "belonging", "tradition", "patience at home", "presence at the table", "forgiveness among kin", "legacy", "roots", "togetherness", "home-making", "the passing down", "unconditional welcome"],
        "o": ["busyness", "the phone at dinner", "old grudges", "distance", "the unsaid apology", "work that eats the evenings", "comparison between children", "doors slammed"],
        "m": ["a long dinner table", "an old family recipe", "a tree with deep roots", "a photo album's spine", "a porch light left on", "hand-me-down stories", "a quilt of many hands", "the smell of a childhood kitchen"],
        "p": ["an elder telling stories", "the parent who listens", "a child watching everything", "the cousin who calls", "a grandmother's patience", "the one who hosts"],
        "v": ["keeps the table long", "passes the stories down", "leaves the porch light on", "shows up for the recital", "forgives at the threshold", "makes room for one more chair"],
        "r": ["a home worth returning to", "roots that hold", "stories that outlive us", "children who come back", "a name kept warm", "belonging that needs no invitation"],
        "t": ["dinner", "holiday", "story", "phone call", "Sunday", "bedtime"],
    },
    "health": {
        "name": "Health & Wellness", "emoji": "💪",
        "a": ["health", "movement", "rest", "nourishment", "sleep", "strength", "breath", "recovery", "hydration", "self-care", "the daily walk", "vitality"],
        "o": ["the sedentary week", "junk fuel", "sleep debt", "burnout", "the skipped meal", "stress left unspent", "screens past midnight", "someday-fitness"],
        "m": ["a well-tuned instrument", "a garden watered daily", "an engine given clean fuel", "a river kept flowing", "a house with strong beams", "a battery honored with charge", "a temple swept each morning", "a knife kept sharp"],
        "p": ["a body listened to", "the one who trains for old age", "an athlete of the everyday", "the early walker", "a guardian of their sleep", "the future eighty-year-old you"],
        "v": ["moves a little every day", "sleeps like it matters", "eats for the afternoon, not the moment", "takes the stairs", "stretches before it must", "rests on purpose"],
        "r": ["energy that lasts all day", "a body that says yes", "strong years, not just long ones", "a clear mind in a strong frame", "mobility at ninety", "health as quiet wealth"],
        "t": ["walk", "meal", "night's sleep", "workout", "breath", "glass of water"],
    },
    "mindfulness": {
        "name": "Mindfulness & Peace", "emoji": "🧘",
        "a": ["stillness", "presence", "breath", "attention", "calm", "acceptance", "silence", "awareness", "letting go", "groundedness", "the pause", "inner quiet"],
        "o": ["the racing mind", "notification noise", "rumination", "hurry", "the replayed argument", "tomorrow's imagined storm", "mental clutter", "the scroll"],
        "m": ["a still lake at dawn", "a single candle flame", "an unhurried cup of tea", "a slow deep breath", "a bell fading into silence", "a mountain unbothered by clouds", "a swept stone garden", "moonlight on water"],
        "p": ["a quiet mind", "the observer of thoughts", "one breath at a time", "the unhurried", "a student of the present", "stillness practiced daily"],
        "v": ["returns to the breath", "lets the thought pass like weather", "sits with what is", "notices without grabbing", "slows the moment down", "puts the phone face-down"],
        "r": ["peace that travels with you", "a spacious mind", "calm in the middle of noise", "the present moment, fully lived", "quiet beneath the storm", "room to respond instead of react"],
        "t": ["breath", "pause", "sit", "moment", "morning silence", "exhale"],
    },
    "creativity": {
        "name": "Creativity", "emoji": "🎨",
        "a": ["creativity", "imagination", "craft", "play", "originality", "curiosity", "the daily page", "experimentation", "voice", "vision", "making", "wonder"],
        "o": ["the blank-page fear", "perfectionism", "the inner critic", "imitation without digestion", "waiting for inspiration", "the unstarted draft", "comparison to masters", "the precious idea never tested"],
        "m": ["a sketchbook full of wrong turns", "clay on a wheel", "a jazz solo finding itself", "a messy studio at midnight", "a first draft written badly on purpose", "a child's crayon certainty", "a darkroom photo emerging", "an unfinished song hummed anyway"],
        "p": ["a maker", "the one who ships the draft", "an artist of the ordinary", "the curious hand", "a beginner unafraid of bad work", "the voice only you have"],
        "v": ["makes bad first drafts bravely", "shows the work", "follows the strange idea", "plays past the fear", "finishes the ugly version", "creates before it critiques"],
        "r": ["work only you could make", "a voice that carries", "the finished piece", "ideas that breed ideas", "a body of work", "the joy of making"],
        "t": ["draft", "sketch", "session", "experiment", "page", "idea"],
    },
    "time": {
        "name": "Time & Priorities", "emoji": "⏳",
        "a": ["time", "focus", "priority", "presence", "the calendar you keep", "attention", "the essential", "single-tasking", "saying no", "deep work", "the hour protected", "intention"],
        "o": ["the scattered day", "everyone else's urgent", "the meeting that should be an email", "multitasking", "the leaking hour", "yes to everything", "the someday list", "hurry without direction"],
        "m": ["an hourglass you cannot flip twice", "a garden bed with limited rows", "one candle burning at both ends", "a jar filled with big rocks first", "a river that never returns upstream", "a blank calendar page", "the last slice of daylight", "a ticket used once"],
        "p": ["a guardian of the calendar", "the one who says no kindly", "a deep worker", "the essentialist", "someone counting sunsets honestly", "the unhurried but unstoppable"],
        "v": ["puts the big rocks in first", "says no to say yes", "guards the morning", "spends attention like money", "does one thing wholly", "leaves margins on purpose"],
        "r": ["a life aimed on purpose", "hours that count double", "the important done first", "days with room to breathe", "time for what you love", "a calendar that matches your values"],
        "t": ["hour", "morning", "no", "block", "sunset", "week"],
    },
    "change": {
        "name": "Change & New Beginnings", "emoji": "🦋",
        "a": ["change", "reinvention", "the fresh start", "letting go", "adaptation", "the pivot", "renewal", "beginning again", "the open door", "transformation", "the next chapter", "release"],
        "o": ["the sunk cost", "nostalgia's grip", "the familiar cage", "fear of the blank page", "old labels", "the way it's always been", "waiting for perfect timing", "the closed fist"],
        "m": ["a snake's shed skin", "spring after a long winter", "a train leaving the station", "a page turned", "a door closing so another opens", "a river changing course", "new paint on old walls", "dawn after the longest night"],
        "p": ["a beginner again", "the one who turned the page", "a life mid-pivot", "the newly brave", "someone unpacking in a new city", "the reinvented"],
        "v": ["packs light", "turns the page", "closes the door gently and walks", "plants in new soil", "answers when the new thing knocks", "lets the old name go"],
        "r": ["the next chapter", "a life re-chosen", "room for the new", "becoming who you're meant to be", "the fresh start earned", "a story with a better second act"],
        "t": ["chapter", "season", "step", "goodbye", "first day", "threshold"],
    },
    "gratitude": {
        "name": "Gratitude", "emoji": "🙏",
        "a": ["gratitude", "thankfulness", "appreciation", "counting blessings", "noticing", "the grateful eye", "acknowledgment", "wonder at the ordinary", "saying thank you", "cherishing", "the full heart", "reverence for small things"],
        "o": ["entitlement", "the taken-for-granted", "wanting the next thing", "the unnoticed gift", "complaint", "scarcity thinking", "the unsent thank-you", "blindness to enough"],
        "m": ["a jar of written blessings", "bread warm from someone's oven", "rain after drought", "a borrowed coat in winter", "the first cup of morning coffee", "a letter of thanks sent late but sent", "sunlight through a kitchen window", "a full table"],
        "p": ["a grateful heart", "the one who writes thank-you notes", "a counter of small blessings", "the person who noticed", "an appreciator of Tuesdays", "the rich-in-enough"],
        "v": ["counts what remains", "says thank you out loud", "notices the unnoticed", "writes the note today", "finds the gift inside the ordinary", "blesses the meal and the hands that made it"],
        "r": ["a heart at peace", "enough that feels like plenty", "joy hiding in plain sight", "wealth already owned", "days lit from within", "the antidote to wanting"],
        "t": ["thank-you", "blessing", "morning", "meal", "note", "breath"],
    },
}


def sentence_case(s):
    s = re.sub(r"\s+", " ", s).strip()
    return s[0].upper() + s[1:]


def fill(template, lex, rng):
    a = rng.choice(lex["a"])
    b = rng.choice([x for x in lex["a"] if x != a])
    o = rng.choice(lex["o"])
    m = rng.choice(lex["m"])
    p = rng.choice(lex["p"])
    v = rng.choice(lex["v"])
    r = rng.choice(lex["r"])
    t = rng.choice(lex["t"])
    out = (template
           .replace("{A}", sentence_case(a)).replace("{a}", a)
           .replace("{B}", sentence_case(b)).replace("{b}", b)
           .replace("{O}", sentence_case(o)).replace("{o}", o)
           .replace("{M}", sentence_case(m)).replace("{m}", m)
           .replace("{P}", sentence_case(p)).replace("{p}", p)
           .replace("{V}", sentence_case(v)).replace("{v}", v)
           .replace("{R}", sentence_case(r)).replace("{r}", r)
           .replace("{T}", sentence_case(t)).replace("{t}", t))
    return sentence_case(out)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20260705)
    seen_global = set()
    index = []
    total = 0
    for slug, lex in CATEGORIES.items():
        quotes = []
        seen = set()
        attempts = 0
        while len(quotes) < PER_CATEGORY:
            attempts += 1
            if attempts > 200000:
                raise SystemExit(f"lexicon too small for {slug}")
            q = fill(rng.choice(TEMPLATES), lex, rng)
            key = q.lower()
            if key in seen or key in seen_global or len(q) > 190:
                continue
            seen.add(key)
            seen_global.add(key)
            quotes.append(q)
        (OUT / f"{slug}.json").write_text(json.dumps(quotes, ensure_ascii=False))
        index.append({"slug": slug, "name": lex["name"], "emoji": lex["emoji"], "count": len(quotes)})
        total += len(quotes)
        print(f"{lex['name']:24s} {len(quotes)}")
    (OUT / "index.json").write_text(json.dumps({
        "total": total,
        "note": "Original aphorisms by Quoti Live. Created By: iTechSmart Inc.",
        "categories": index,
    }, ensure_ascii=False, indent=1))
    print("TOTAL", total)


if __name__ == "__main__":
    build()
