"""Write the English (TOEFL ITP-style) tests E4-E6 to site/data/english-4..6.json.

  E4 Structure            20 sentence completions
  E5 Written Expression   20 error-identification sentences, 4 underlined parts A-D, exactly one wrong
  E6 Reading              3 passages (science, history, social science), 7 + 7 + 6 questions

All content is original, written for this site. E1-E3 were hand-written JSON; these tests keep the same
schema but live here so a question can be fixed and the JSON rebuilt. Their timers are in site/js/data.js
(ENGLISH_MINUTES), not in the JSON.

Error-identification sentences mark each underlined part as {A|text}; the site draws it underlined with
its letter beneath, and the option texts are taken from the marks.

Sentence-completion and reading options are listed correct first; the correct option is then moved to a
seeded letter so each test uses A-D exactly five times. Run: python tools/gen_english.py
"""
import json
import random
import re
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "site" / "data"
LETTERS = "ABCD"
MARK = re.compile(r"\{([A-D])\|([^}]*)\}")
DIFFICULTY = {"easy": 6, "medium": 10, "hard": 4}  # per test: 30% / 50% / 20%

# ---------------------------------------------------------------- E4 Structure
# (topic, difficulty, sentence, [correct, wrong, wrong, wrong], explanation)
E4 = [
    ("subject-verb agreement", "easy",
     "The migration patterns of the monarch butterfly ______ scientists for more than a century.",
     ["have fascinated", "has fascinated", "fascinating", "to fascinate"],
     "The subject is \"patterns\" (plural), so the verb is \"have fascinated\". \"Has fascinated\" is tempting "
     "because the nearest noun, \"butterfly\", is singular, but a prepositional phrase never changes the subject."),
    ("appositive", "easy",
     "______, the largest planet in the solar system, has dozens of known moons.",
     ["Jupiter", "It is Jupiter", "Jupiter is", "Because Jupiter"],
     "The sentence already has its verb (\"has\"); the blank needs only the subject, which the appositive "
     "\"the largest planet…\" then renames. \"Jupiter is\" adds a second verb, leaving \"has\" with no subject."),
    ("reduced clause", "medium",
     "______ in 1869, the transcontinental railroad cut the journey across the United States from months to about a week.",
     ["Completed", "Completing", "It was completed", "Having completed"],
     "A reduced passive clause (\"[It was] completed in 1869\") describes the subject, the railroad, which was "
     "completed by others. \"Having completed\" is active: it would mean the railroad completed something."),
    ("inversion", "medium",
     "Rarely ______ a comet bright enough to be seen in daylight.",
     ["do astronomers observe", "astronomers observe", "astronomers do observe", "observe astronomers"],
     "A negative adverb such as \"rarely\" at the start of a sentence requires question word order: auxiliary + "
     "subject + verb. \"Astronomers observe\" keeps normal order, which formal English doesn't allow after \"Rarely\"."),
    ("parallelism", "easy",
     "Coral reefs protect coastlines, provide habitat for fish, and ______ millions of visitors each year.",
     ["attract", "attracting", "they attract", "the attraction of"],
     "The three verbs in the list share the subject \"coral reefs\" and must have the same form: protect, provide, "
     "attract. \"Attracting\" breaks the parallel series."),
    ("conditional", "medium",
     "If the Earth's axis were not tilted, the planet ______ distinct seasons.",
     ["would not have", "will not have", "had not had", "does not have"],
     "\"If … were not\" is an unreal present condition, so the result clause takes \"would\" + base verb. "
     "\"Will not have\" belongs to a real (first) conditional with a present-tense if-clause."),
    ("noun clause", "medium",
     "______ the dinosaurs died out remains a subject of scientific debate.",
     ["Why", "Because", "Since", "For"],
     "The blank starts a noun clause that is the subject of \"remains\"; \"Why the dinosaurs died out\" is such a "
     "clause. \"Because\" starts an adverb clause, which can't be the subject of a verb."),
    ("comparative", "medium",
     "The deeper a diver descends, ______ the water pressure becomes.",
     ["the greater", "greater", "the greatest", "it is greater"],
     "The double comparative is \"the + comparative …, the + comparative …\": \"The deeper …, the greater …\". "
     "\"Greater\" without \"the\" breaks the pattern, and \"the greatest\" is a superlative."),
    ("subject-verb agreement", "medium",
     "The number of languages spoken worldwide ______ to be about seven thousand.",
     ["is estimated", "are estimated", "estimate", "estimating"],
     "\"The number of …\" is singular (it is one number), so the verb is \"is estimated\". \"Are estimated\" "
     "would suit \"A number of languages\", which means \"many languages\"."),
    ("reduced clause", "hard",
     "Most of the solar energy ______ the Earth's surface arrives as visible light or infrared radiation.",
     ["reaching", "reaches", "is reached", "that reach"],
     "The main verb is \"arrives\", so the blank must be a reduced relative clause: \"energy reaching\" = \"energy "
     "that reaches\". \"That reach\" is tempting but disagrees with \"energy\", which is uncountable (singular); "
     "\"reaches\" would give the sentence two main verbs."),
    ("appositive", "easy",
     "Marie Curie, ______ research on radioactivity earned her two Nobel Prizes, was born in Warsaw.",
     ["whose", "who", "which", "her"],
     "The clause needs a possessive relative pronoun before the noun \"research\": \"whose research\". \"Who "
     "research\" and \"her research\" are ungrammatical here (\"her\" would create a run-on)."),
    ("inversion", "hard",
     "______ the Moon closer to Earth, ocean tides would be much stronger.",
     ["Were", "If", "Was", "Had"],
     "This is an inverted unreal condition: \"Were the Moon closer\" = \"If the Moon were closer\". Formal English "
     "uses \"were\" for every subject here, so \"Was\" is wrong; \"If\" leaves the clause without a verb."),
    ("parallelism", "easy",
     "The new vaccine is effective not only in adults ______ in young children.",
     ["but also", "and also", "as well", "or else"],
     "The paired conjunction is \"not only … but also\". \"And also\" can't complete \"not only\"."),
    ("noun clause", "easy",
     "The study found ______ honeybees can learn to recognize human faces.",
     ["that", "what", "which", "about"],
     "\"Found\" takes a noun clause as its object, introduced by \"that\". \"What\" would need a gap in the clause "
     "(\"found what bees recognize\"), but \"honeybees can learn to recognize human faces\" is already complete."),
    ("comparative", "medium",
     "The heart of a blue whale is roughly ______ a small car.",
     ["as large as", "as large than", "larger as", "so large that"],
     "An equal comparison is \"as + adjective + as\". \"As large than\" and \"larger as\" mix the two comparison "
     "patterns (as … as / -er … than)."),
    ("reduced clause", "medium",
     "While ______ the Galápagos Islands, Charles Darwin collected specimens of finches and tortoises.",
     ["exploring", "he exploring", "was exploring", "explored"],
     "\"While exploring\" is a reduced adverb clause (\"While he was exploring\"); the subject is dropped along with "
     "\"was\". \"Explored\" is passive in meaning here: Darwin was the explorer, not the thing explored."),
    ("subject-verb agreement", "hard",
     "Among the oldest surviving written texts ______ the Epic of Gilgamesh.",
     ["is", "are", "being", "have been"],
     "The sentence is inverted: the real subject comes after the verb, and it is \"the Epic of Gilgamesh\" "
     "(singular). \"Are\" is tempting because it follows the plural \"texts\", but that noun is inside the "
     "introductory prepositional phrase."),
    ("conditional", "medium",
     "If current trends ______, the glacier will disappear within fifty years.",
     ["continue", "continued", "would continue", "had continued"],
     "A real (first) conditional has a present-tense if-clause and \"will\" in the result: \"If current trends "
     "continue, … will disappear\". \"Continued\" would need \"would disappear\"."),
    ("appositive", "medium",
     "The platypus, ______, is one of the few mammals that lay eggs.",
     ["a native of eastern Australia", "is native to eastern Australia", "which native to eastern Australia",
      "it is native to eastern Australia"],
     "Between the commas the sentence needs an appositive (a noun phrase renaming \"the platypus\"), since the verb "
     "\"is\" comes later. \"Which native to…\" is a relative clause with no verb; the others add a second main verb."),
    ("comparative", "hard",
     "Sound travels about four times ______ in water as in air.",
     ["as fast", "faster", "as faster", "so fast"],
     "The sentence continues with \"as in air\", so it needs \"as fast … as\": \"four times as fast in water as in "
     "air\". \"Faster\" would need \"than\" (\"four times faster than in air\"), not \"as\"."),
]

# ---------------------------------------------------------------- E5 Written Expression
# (topic, difficulty, sentence with {X|underlined part}, wrong letter, explanation)
E5 = [
    ("word form", "easy",
     "The {A|ancient} Egyptians {B|developed} a calendar {C|base} on the {D|annual} flooding of the Nile.",
     "C",
     "\"Base\" must be the past participle \"based\": a calendar (that was) based on the flooding. \"Ancient\" and "
     "\"annual\" are adjectives correctly placed before nouns."),
    ("singular/plural", "easy",
     "Many {A|specie} of frogs {B|are} sensitive to small {C|changes} in {D|water quality}.",
     "A",
     "After \"many\" the noun must be plural: \"species\" (the same form for singular and plural). \"Are\" is correct "
     "because the subject is plural."),
    ("verb tense", "medium",
     "In 1928, Alexander Fleming {A|noticed} that a mold {B|has killed} the bacteria {C|growing} in one of {D|his} culture dishes.",
     "B",
     "The killing happened before Fleming noticed it in the past, so it needs the past perfect \"had killed\". "
     "\"Growing\" is a correct reduced clause (\"that were growing\")."),
    ("pronoun agreement", "medium",
     "A young kangaroo {A|remains} in {B|its} mother's pouch {C|until} {D|they are} about eight months old.",
     "D",
     "The pronoun refers to \"a young kangaroo\", an animal in the singular, so it must be \"it is\". \"Its\" in B "
     "shows the correct pronoun for the same noun."),
    ("preposition", "medium",
     "The success of the experiment {A|depends} largely {B|in} the {C|accuracy} {D|of} the initial measurements.",
     "B",
     "The verb \"depend\" takes the preposition \"on\": \"depends largely on the accuracy\". \"Of\" in D is correct "
     "(\"the accuracy of the measurements\")."),
    ("article", "easy",
     "{A|An} unusual feature of {B|the} octopus is that it {C|has} three hearts and {D|a} blue blood.",
     "D",
     "\"Blood\" is an uncountable noun, so it takes no \"a\": \"three hearts and blue blood\". \"The octopus\" (B) "
     "is correct: \"the\" + singular noun can name a whole species."),
    ("parallel structure", "medium",
     "The study of volcanoes helps scientists {A|predict} eruptions, {B|protect} nearby communities, and {C|understanding} how the Earth's interior {D|works}.",
     "C",
     "The three items after \"helps scientists\" must be parallel base verbs: predict, protect, understand. "
     "\"Works\" (D) is correct; it agrees with \"the Earth's interior\"."),
    ("word form", "medium",
     "The {A|economy} growth of the Roman Empire {B|depended} heavily on trade routes {C|that} stretched {D|across} the Mediterranean.",
     "A",
     "Before the noun \"growth\" we need the adjective \"economic\", not the noun \"economy\". \"Depended\" (B) "
     "correctly takes \"on\", which follows it."),
    ("verb tense", "hard",
     "Scientists {A|have been studying} the Antarctic ice sheet {B|since} the 1950s, and last year they {C|have recorded} {D|its} fastest rate of melting.",
     "C",
     "A finished past time such as \"last year\" takes the simple past: \"recorded\", not the present perfect. "
     "\"Have been studying … since the 1950s\" (A) is correct because that action continues to now."),
    ("singular/plural", "easy",
     "The human skeleton {A|is made up} of more than two hundred {B|bone}, {C|which} support the body and {D|protect} its organs.",
     "B",
     "After a number greater than one the noun must be plural: \"two hundred bones\". \"Support\" and \"protect\" "
     "are plural because \"which\" refers to the bones."),
    ("pronoun agreement", "easy",
     "A mature oak tree {A|can absorb} large amounts of carbon dioxide {B|through} {C|their} leaves {D|each} year.",
     "C",
     "The pronoun refers to \"a mature oak tree\" (singular, not a person), so it must be \"its leaves\". \"Can "
     "absorb\" (A) is a correct modal + base verb."),
    ("preposition", "medium",
     "{A|Contrary of} popular belief, bats are not blind; many species {B|can see} quite well and {C|rely on} echolocation mainly {D|to hunt} in darkness.",
     "A",
     "The fixed expression is \"contrary to\": \"Contrary to popular belief\". \"Rely on\" (C) is the correct "
     "preposition for \"rely\"."),
    ("article", "medium",
     "The Sahara is {A|a} largest hot desert in {B|the} world, {C|covering} {D|much} of North Africa.",
     "A",
     "A superlative (\"largest\") takes \"the\": \"the largest hot desert\". \"The world\" (B) is correct because "
     "there is only one."),
    ("parallel structure", "medium",
     "Archaeologists study ancient cultures by examining tools, {A|analyzing} bones, and {B|they reconstruct} {C|buildings} {D|from} ruins.",
     "B",
     "All three items after \"by\" must be -ing forms: examining, analyzing, reconstructing. \"They reconstruct\" "
     "breaks the series with a full clause."),
    ("word form", "medium",
     "The population of the city {A|grew} {B|rapidly} during the nineteenth century, and its streets became {C|increasingly} {D|crowd}.",
     "D",
     "After the linking verb \"became\" we need an adjective: \"crowded\". \"Rapidly\" (B) is correct: an adverb "
     "describing the verb \"grew\"."),
    ("singular/plural", "hard",
     "Auroras are among the most {A|beautiful} natural {B|phenomenon}, {C|appearing} as bands of colored light {D|near} the poles.",
     "B",
     "\"Among the most beautiful …\" needs a plural noun, and the plural of \"phenomenon\" is \"phenomena\". "
     "\"Appearing\" (C) is a correct reduced clause describing the auroras."),
    ("verb tense", "hard",
     "By the end of the Ice Age, many large mammals {A|had disappeared} from North America, {B|probably} because of climate change and hunting {C|by} humans who {D|arrive} only recently.",
     "D",
     "The humans' arrival happened before a past point (the end of the Ice Age), so it needs the past perfect "
     "\"had arrived\"; the present tense \"arrive\" doesn't fit a past narrative. \"Had disappeared\" (A) is the "
     "correct past perfect for the same reason."),
    ("word form", "medium",
     "The {A|discover} of oxygen in the 1770s {B|is} usually {C|credited} {D|to both} Joseph Priestley and Carl Scheele.",
     "A",
     "The subject needs the noun \"discovery\", not the verb \"discover\". \"Credited to both\" (D) is correct "
     "(\"credit something to someone\")."),
    ("comparison", "hard",
     "The Nile, {A|which} flows {B|northward}, is longer than {C|any} river in Africa and {D|provides} water to eleven countries.",
     "C",
     "The Nile is itself a river in Africa, so the comparison must exclude it: \"longer than any other river in "
     "Africa\". Without \"other\" the sentence says the Nile is longer than itself. \"Provides\" (D) agrees with "
     "\"the Nile\"."),
    ("word form", "easy",
     "Glass is {A|made} by heating sand {B|to} a very high temperature and then {C|cooling} it {D|rapid}.",
     "D",
     "\"Rapid\" describes how the glass is cooled, so it must be the adverb \"rapidly\". \"Cooling\" (C) is correct: "
     "it is parallel with \"heating\" after \"by\"."),
]

# ---------------------------------------------------------------- E6 Reading
PASSAGES = {
    "p1": ("Passage 1 of 3",
           "Most plants open the tiny pores on their leaves, called stomata, during the day. Through these openings "
           "they take in the carbon dioxide they need for photosynthesis, the process that uses the energy of "
           "sunlight to turn carbon dioxide and water into sugar. The arrangement works well in mild climates, but it "
           "carries a cost: every time the stomata open, water vapor escapes. In a hot desert, a plant that kept its "
           "pores open through the afternoon could lose more water in a single day than its roots are able to "
           "collect in a week.\n\n"
           "Many cacti, agaves and other succulents avoid this problem with a method known as crassulacean acid "
           "metabolism, or CAM, named after the stonecrop family of plants, in which it was first studied. CAM "
           "plants reverse the usual schedule. They open their stomata at night, when the air is cooler and more "
           "humid, and absorb carbon dioxide while little water is lost. Because photosynthesis cannot take place "
           "without light, the plant cannot use this carbon dioxide at once. Instead, it stores the gas in the form "
           "of an acid, which builds up inside its cells until morning. When the sun rises, the stomata close "
           "tightly, and the stored acid is broken down to release carbon dioxide inside the leaf, where it is used "
           "to make sugar throughout the day.\n\n"
           "The strategy is remarkably economical. Studies of CAM plants have found that they may lose as little as "
           "one-fifth as much water as ordinary plants for each gram of carbon they take in. Yet the method has "
           "drawbacks. A plant can store only a limited amount of acid overnight, so its daily supply of carbon is "
           "restricted, and most CAM species grow slowly as a result. This trade-off helps explain why CAM plants "
           "are common in deserts but rarely compete successfully in wetter regions, where faster-growing plants "
           "can shade them out."),
    "p2": ("Passage 2 of 3",
           "For most of human history, time was a local matter. Each town set its clocks by the sun, declaring noon "
           "at the moment the sun stood highest in its own sky. Because the sun appears to move westward, noon in "
           "one town arrived a few minutes earlier or later than in a town some distance to the east or west. As "
           "long as people traveled on foot or by horse, these small differences caused little trouble; no one "
           "could move fast enough to notice them.\n\n"
           "The railway changed that. By the middle of the nineteenth century, trains were carrying passengers "
           "hundreds of kilometers in a single day, and each railway company tended to run its trains by the time "
           "of its home city. A traveler changing trains might find that the timetable followed a different clock "
           "from the one on the station wall. In the United States alone, railroads used dozens of separate times, "
           "and the confusion contributed to missed connections and, on lines with a single track, to dangerous "
           "collisions.\n\n"
           "British railways were among the first to respond. During the 1840s, many lines adopted the time kept "
           "at Greenwich, near London, and within a few decades most public clocks in Britain followed it. In North "
           "America, the railroad companies acted on their own: on 18 November 1883, they replaced their many local "
           "times with a small number of standard time zones, each one hour apart. The following year, delegates "
           "from twenty-five nations met in Washington and chose the meridian passing through Greenwich as the "
           "starting point for measuring longitude and time around the world.\n\n"
           "Standard time was not welcomed everywhere. Some newspapers complained that the railroads had no right to "
           "alter the sun, and several cities kept their own local time for years. In the United States, the zones "
           "did not become law until 1918, thirty-five years after the railroads first adopted them."),
    "p3": ("Passage 3 of 3",
           "In 1968, the ecologist Garrett Hardin published an essay describing what he called \"the tragedy of the "
           "commons.\" Hardin asked readers to imagine a pasture open to every herder in a village. Each herder gains "
           "the full benefit of adding one more animal to the pasture, while the cost of the extra grazing is shared "
           "by everyone. Acting sensibly in their own interest, the herders keep adding animals until the grass is "
           "destroyed. Hardin concluded that shared resources would be ruined unless they were divided into private "
           "property or placed under strict government control.\n\n"
           "The political scientist Elinor Ostrom doubted that these were the only two choices. Over several "
           "decades, she and her colleagues gathered evidence from communities that had managed shared resources "
           "for generations: mountain pastures in Switzerland, forests in Japan, irrigation systems in Spain and "
           "fisheries on the coast of Maine. Many of these arrangements had lasted for centuries without private "
           "ownership or direction from a distant government.\n\n"
           "Ostrom found that successful communities tended to share certain features. They defined clearly who was "
           "allowed to use the resource. They created their own rules, suited to local conditions, and chose members "
           "to watch for people who broke them. Penalties usually started small, such as a modest fine for a first "
           "offense, and grew only if the behavior was repeated. Finally, the communities had cheap and quick ways "
           "to settle disputes among users.\n\n"
           "Ostrom did not claim that shared management always works. Where users are strangers to one another, or "
           "where a resource is too large to be watched, cooperation may break down just as Hardin predicted. Her "
           "point was that the outcome depends on the rules people build, not simply on who owns the resource. In "
           "2009 she became the first woman to receive the Nobel Prize in economics."),
}

# (passage, topic, difficulty, question, [correct, wrong, wrong, wrong], explanation)
E6 = [
    ("p1", "main idea", "easy", "What is the passage mainly about?",
     ["How desert plants take in carbon dioxide without losing much water",
      "Why cacti and agaves grow faster than most other plants in the desert",
      "How the stonecrop family of plants was first discovered",
      "Why photosynthesis in all plants takes place mainly at night"],
     "Paragraph 1 sets up the problem (open stomata lose water), paragraph 2 describes the CAM solution and "
     "paragraph 3 weighs its benefit and cost. \"Grow faster\" contradicts paragraph 3 (\"most CAM species grow slowly\")."),
    ("p1", "detail", "easy", "According to the passage, when do CAM plants open their stomata?",
     ["At night", "In the early morning", "Throughout the afternoon", "Only after it rains"],
     "Paragraph 2: \"They open their stomata at night, when the air is cooler and more humid.\" In the morning the "
     "stomata \"close tightly\", so \"In the early morning\" is wrong."),
    ("p1", "vocabulary", "medium", "The word \"economical\" in paragraph 3 is closest in meaning to",
     ["efficient", "profitable", "expensive", "complicated"],
     "The next sentence explains it: CAM plants lose far less water for each gram of carbon, i.e. they use "
     "water efficiently. \"Profitable\" is about making money, which doesn't fit a plant's use of water."),
    ("p1", "reference", "hard",
     "In paragraph 2, the word \"it\" in \"where it is used to make sugar throughout the day\" refers to",
     ["carbon dioxide", "the stored acid", "the leaf", "the sun"],
     "The acid \"is broken down to release carbon dioxide inside the leaf, where it is used to make sugar\": the "
     "carbon dioxide is what photosynthesis turns into sugar (paragraph 1). The acid is tempting but it is the "
     "store that is broken down, not what is made into sugar."),
    ("p1", "inference", "medium",
     "It can be inferred from the passage that CAM plants growing in a wet region would most likely",
     ["be shaded out by plants that grow faster", "grow faster than they would in a desert",
      "switch to opening their stomata by day", "store more acid than desert CAM plants"],
     "Paragraph 3: CAM plants \"rarely compete successfully in wetter regions, where faster-growing plants can "
     "shade them out.\" The passage never says CAM plants change their schedule, so \"switch to opening their "
     "stomata by day\" has no support."),
    ("p1", "author's purpose", "medium",
     "Why does the author mention that a desert plant could lose more water in a day than its roots collect in a week?",
     ["To show how costly the usual schedule would be in a desert",
      "To explain why the roots of desert plants are unusually short",
      "To compare how quickly CAM plants and other plants grow",
      "To suggest that desert plants rarely take in carbon dioxide"],
     "The example follows \"it carries a cost: every time the stomata open, water vapor escapes\" and sets up the "
     "problem that CAM solves. Growth rates are compared only in paragraph 3, not in this example."),
    ("p1", "detail", "hard", "According to the passage, why do most CAM species grow slowly?",
     ["They can store only a little acid each night.",
      "They lose too much water through their stomata.",
      "Their stomata stay open throughout the day.",
      "They cannot carry out photosynthesis in sunlight."],
     "Paragraph 3: \"A plant can store only a limited amount of acid overnight, so its daily supply of carbon is "
     "restricted, and most CAM species grow slowly as a result.\" Losing too much water is the problem CAM avoids, "
     "not the cause of slow growth."),

    ("p2", "main idea", "easy", "Which of the following would be the best title for the passage?",
     ["How the Railways Led to Standard Time", "Travel by Horse in the Nineteenth Century",
      "Why the Sun Appears to Move Westward", "The First Railway Lines in Britain"],
     "The passage moves from local sun time, to the confusion trains caused, to the adoption of standard time. "
     "British railways are only one step in that story (paragraph 3)."),
    ("p2", "detail", "easy", "According to the passage, how did a town decide when it was noon before standard time?",
     ["By the sun's highest point in its own sky", "By the official clock kept at Greenwich",
      "By the timetable of the nearest railway", "By agreement with the other towns nearby"],
     "Paragraph 1: each town declared \"noon at the moment the sun stood highest in its own sky.\" Greenwich time "
     "came later, with the railways (paragraph 3)."),
    ("p2", "vocabulary", "easy", "The word \"alter\" in paragraph 4 is closest in meaning to",
     ["change", "follow", "measure", "admire"],
     "The newspapers complained that the railroads had no right to change the sun, i.e. the time the sun set. "
     "\"Follow\" is the opposite of the complaint: local sun time was what people had followed before."),
    ("p2", "reference", "medium",
     "In paragraph 1, the word \"them\" in \"no one could move fast enough to notice them\" refers to",
     ["the differences in local time", "the towns to the east or west", "people who traveled on foot",
      "the horses people traveled by"],
     "The sentence reads \"these small differences caused little trouble; no one could move fast enough to notice "
     "them\": travelers were too slow to notice the few minutes between towns. Towns can be noticed at any speed."),
    ("p2", "inference", "hard", "It can be inferred from the passage that standard time zones in the United States were",
     ["set up by companies years before they became law",
      "first proposed by delegates at the meeting in Washington",
      "rejected by most railroad companies when they first appeared",
      "based on the local time of each railway's home city"],
     "Paragraph 3: \"the railroad companies acted on their own\" in 1883; paragraph 4: the zones \"did not become "
     "law until 1918.\" The Washington meeting was the following year (1884) and chose the Greenwich meridian, "
     "so the zones already existed."),
    ("p2", "author's purpose", "medium", "Why does the author mention \"dangerous collisions\" in paragraph 2?",
     ["To show that the confusion over time had serious consequences",
      "To explain why British railways adopted standard time first",
      "To argue that lines with a single track should be closed",
      "To show that trains in the United States were badly built"],
     "Collisions are listed as a result of \"the confusion\" over dozens of separate times. The passage never "
     "links them to Britain; paragraph 2 is about the United States."),
    ("p2", "detail", "medium", "According to the passage, what was decided at the meeting in Washington?",
     ["Longitude and time would be measured from Greenwich.",
      "Every city in the United States had to adopt railway time.",
      "Standard time zones would become law in the United States.",
      "Neighboring time zones would be exactly two hours apart."],
     "Paragraph 3: the delegates \"chose the meridian passing through Greenwich as the starting point for "
     "measuring longitude and time.\" The zones became U.S. law only in 1918, by a separate step."),

    ("p3", "main idea", "medium", "What is the passage mainly about?",
     ["Evidence that communities can manage shared resources on their own",
      "The reasons that herders in Swiss villages lost their mountain pastures",
      "How Hardin's essay led to new laws for fisheries on the coast of Maine",
      "Why Elinor Ostrom was awarded the Nobel Prize in economics in 2009"],
     "Paragraphs 2–4 present Ostrom's evidence against Hardin's claim that only private property or government "
     "control can save a shared resource. The Nobel Prize is mentioned only in the last sentence."),
    ("p3", "detail", "easy", "According to Hardin's example, why do the herders keep adding animals to the pasture?",
     ["Each herder keeps the gain from an extra animal but shares its cost.",
      "The village pays each herder a fee for every animal on the pasture.",
      "The grass on the pasture grows back faster than the animals eat it.",
      "The herders have agreed on rules for sharing the pasture."],
     "Paragraph 1: \"Each herder gains the full benefit of adding one more animal … while the cost of the extra "
     "grazing is shared by everyone.\" Agreed rules are Ostrom's answer to the problem, not part of Hardin's example."),
    ("p3", "vocabulary", "medium", "The word \"modest\" in paragraph 3 is closest in meaning to",
     ["small", "humble", "fair", "secret"],
     "\"Penalties usually started small, such as a modest fine\": a modest fine is a small one. \"Humble\" is "
     "another meaning of \"modest\", but it describes people, not amounts."),
    ("p3", "reference", "medium",
     "In paragraph 3, the word \"them\" in \"to watch for people who broke them\" refers to",
     ["the rules", "the members", "local conditions", "the communities"],
     "\"They created their own rules … and chose members to watch for people who broke them\": what people break "
     "is the rules. \"Local conditions\" is also plural, but conditions can't be broken."),
    ("p3", "inference", "hard",
     "Based on the passage, Ostrom would most likely say that a fishery used by thousands of people who do not know one another",
     ["may be overused, as Hardin predicted", "will be managed well because no one owns it",
      "must be placed under government control", "cannot be affected by the rules its users make"],
     "Paragraph 4: \"Where users are strangers to one another, or where a resource is too large to be watched, "
     "cooperation may break down just as Hardin predicted.\" \"Must be placed under government control\" goes "
     "further than the passage: Ostrom's point is that rules matter, not that the state must take over."),
    ("p3", "author's purpose", "medium",
     "Why does the author mention mountain pastures in Switzerland, forests in Japan and irrigation systems in Spain?",
     ["To give examples of resources managed well for centuries",
      "To show the places where Hardin carried out his own research",
      "To list resources that were ruined by too many users",
      "To compare the ways different governments control resources"],
     "Paragraph 2 calls them \"communities that had managed shared resources for generations\" and says many "
     "lasted \"for centuries\" without private or government control. They are Ostrom's evidence, not Hardin's."),
]


def check_difficulty(name, questions):
    counts = {d: sum(q["difficulty"] == d for q in questions) for d in DIFFICULTY}
    assert counts == DIFFICULTY, (name, counts)


def placed(rng, items):
    """Letters for the correct options: each of A-D five times, in a seeded order."""
    pool = [letter for letter in LETTERS for _ in range(len(items) // 4)]
    rng.shuffle(pool)
    return pool


def options_with(correct, wrong, letter):
    slots = list(wrong)
    slots.insert(LETTERS.index(letter), correct)
    return dict(zip(LETTERS, slots))


def build_structure(rng):
    questions = []
    for n, ((topic, diff, text, (correct, *wrong), why), letter) in enumerate(zip(E4, placed(rng, E4)), 1):
        questions.append({"id": f"E4-Q{n:02d}", "skill": "structure", "topic": topic, "difficulty": diff,
                          "text": text, "options": options_with(correct, wrong, letter), "answer": letter,
                          "explanation": why, "source": "generated", "flag": None})
    return {"title": "English – Test 4: Structure", "questions": questions}


def build_written(_rng):
    questions = []
    for n, (topic, diff, text, wrong_letter, why) in enumerate(E5, 1):
        marks = MARK.findall(text)
        assert [m[0] for m in marks] == list(LETTERS), f"E5 #{n}: marks must be A, B, C, D in order"
        questions.append({"id": f"E5-Q{n:02d}", "skill": "written expression", "topic": topic, "difficulty": diff,
                          "text": text, "options": dict(marks), "answer": wrong_letter,
                          "explanation": why, "source": "generated", "flag": None})
    return {"title": "English – Test 5: Written Expression", "questions": questions}


def build_reading(rng):
    questions = []
    for n, ((passage, topic, diff, text, (correct, *wrong), why), letter) in enumerate(zip(E6, placed(rng, E6)), 1):
        questions.append({"id": f"E6-Q{n:02d}", "skill": "reading", "topic": topic, "difficulty": diff,
                          "passage": passage, "text": text, "options": options_with(correct, wrong, letter),
                          "answer": letter, "explanation": why, "source": "generated", "flag": None})
    passages = {key: {"title": title, "text": text, "truncated": False} for key, (title, text) in PASSAGES.items()}
    for key, (_, text) in PASSAGES.items():
        words = len(text.split())
        assert 250 <= words <= 350, f"{key}: {words} words"
    return {"title": "English – Test 6: Reading", "passages": passages, "questions": questions}


def main():
    rng = random.Random(2026)
    for number, build in ((4, build_structure), (5, build_written), (6, build_reading)):
        body = build(rng)
        qs = body["questions"]
        assert len(qs) == 20
        check_difficulty(f"E{number}", qs)
        counts = {letter: sum(q["answer"] == letter for q in qs) for letter in LETTERS}
        assert set(counts.values()) == {5}, (number, counts)
        test = {"id": f"E{number}", "section": "english", "test": number, "title": body.pop("title"),
                "source": "generated", **body}
        path = DATA / f"english-{number}.json"
        path.write_text(json.dumps(test, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{path.name}: {len(qs)} questions, answers {counts}")
    for key, (_, text) in PASSAGES.items():
        print(f"passage {key}: {len(text.split())} words")


if __name__ == "__main__":
    main()
