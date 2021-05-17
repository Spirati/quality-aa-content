import random
import re
from PIL.Image import Image
from typing import Union, Dict, List

quotes = {
"""
{0}: Look {1}
{0}: Everything the light touches
{0}: Is too tall for you to reach
""":2,
"""
{0}: I may be gay, but even I know how to please a woman. You buy her a dress with pockets.
{1}: ...
{2}: I mean, they're not wrong
{3}: *frantically taking notes*
""":4,
"""
{0}: Good morning.
{1}: Good morning.
{2}: Good morning.
{3}: You all sound like robots, try spicing it up a bit.
{4}: MORNING MOTHERFUCKERS
""":5,
"""
{0}, texting: Is your new girlfried a blonde?
{0}: Grilfied
{0}: Girlfien
{0}: FEMALE COMPANION
{1}: My boyfriend is
""":2,
"""
{0}: hey what do you want for dinner
{1}: the souls of the innocent
{2}: a bagel
{1}: No!
{2}: ... two bagels
""":3,
"""
{0}: You call it a near death experience, I call it a vibe check from god
""":1,
"""
{0}: Are you okay?
{1}: NO I'M NOT, I'M HAVING FEELINGS AND IT'S {2}'S FAULT
""":3,
"""
Judge: The defense may now begin its cross-examination.
{0}: Heh. You should take this one, {1}. You're always cross.
{1}: Somebody get them some more feet. They're going to need them!
{0}: Ow, my other foot!!!
{1}: You’ll run out eventually!
{0}: I won’t *run* anywhere if you keep STEPPING ON MY FEET!
""":2,
"""
{0}, over text: The wind is screaming over here
{1}, sends a pic of {2}: Same here. I can almost here it sometimes
{2}: Fuck you
""":3,
"""
{0}: You're scamming them?
{1}: I was thinking more like flat-out stealing from them.
{0}: What? No way.
{1}: Why not? We already stole a kid.
{2}: Hey guys.
{0}: No, we didn't. {2}'s almost an adult. They can do what they want.
{2}: I wanna steal.
""":3,
"""
{0}: Only the true king could remove the sword from the stone... no one else could... they didn't have... arthurization.
{1}: THAT PUN IS BAD AND YOU SHOULD FEEL BAD!
""":2,
"""
{0}, biking with {1}: I know how you feel about {2}. I'm not blind
{1}: Well you must be if you don't see that goose
{0}: Huh?
Goose, slams into their head: HONK
""":3,
"""
{0}: {1}, I have bad news.
{1} (compeletly done with the world): There is no good news or bad news, only news.
{0}: {2}'s missing.
{1}: That is bad news.
""":3,
"""
{0}: There is a friday 13th this month!
{1}: When?
{0}:
{0}, visibly confused: ... on friday?
""":2,
"""
{0}, from the defense bench: You idiot!
{1}, from the prosecution bench: FOOL!
{2}, from the witness bench: I'm sure you're both right, but why?
""":3,
"""
{0}, to {1}: What'cha doin in that box?
{2}: They're plotting to take over the world
{0}: You really think they can take over the world when they failed to arson us?
""":3,
"""
{0}: I will not be mocked in such a manor!!
{1}: Well how would you like me to mock you? I take requests
""":2,
"""
{0}: Do you ever want to talk about your emotions, {1}?
{1}: No.
{2}: I do!
{0}: I know, {2}.
{2}: I’m sad. 
{0}: I know, {2}.
""":3,
"""
{0}: " Sometimes people ask me how I manage my friends so easily. The secret is that I don't. I have no control over them whatsoever."
{0}: "Earlier, {1} called for me and when I showed up to see what was going on, {2} shot me in the throat with a nerf gun."
""":3,
"""
{0}: I sort of did something and I need some advice, but I don't want a lot of judgment and criticism.
{1}: And you came to me?
""":2,
"""
{0}: It is very safe. Go on. Walk in through the door.
{1}, crying: I'm not sure I trust you enough.
{0}: Go in through the fucking door, {1}.
""":2,
"""
Robber: *points gun at {0} and {1}* Give me your money if you want to live!
{0}: Bold of you to assume I want to live
{1}: Bold of you to assume I have money
{2}, getting shot: Guys, this is not the time-
""":3,
"""
Judge: While reopening a trial at this point is illegal and grossly unconstitutional...
Judge, looking at {0}: I just can't say "no" to kids.
""":1,
"""
({0}, {1}, and {2} get caught on a stealth mission)

{0}, pulling out a bottle and smashing it on the ground: SCATTER
""":3,
"""
{0}, pointing to {1}: Thirteen-year-olds are the meanest people in the world.
""":2
}

mulaney = [
"{0}: And I replied, \"Hey, you want me to kill that guy for you?\"",
"{0}: You have the moral backbone of a chocolate éclair.",   
"{0}: I am very small. And I have no money, so you can imagine the kind of stress that I am under.",
"{0}: Woah, that tall child looks terrible! Get some rest, tall child! You can't keep burning the candle at both ends!",
"{0}: Shut up! You're all gonna die. Street smarts!",
"{0}: You know those days when you're like, \"this might as well happen?\"",
"{0}: And I'm like \"No! That's the thing I'm sensitive about!\"",
"{0}: Could be a nursery.",
"{0}: I need everyone to like me so much. It's exhausting.",
"{0}: I was just shiny and dumb and easy to trick.",
"{0}: Hey, you could pour soup in my lap and I'll probably apologize to you.",
"{0}: I'll keep all my emotions right here, and then I'll die.",
"{0}: Adult life is already so goddamn weird.",
"{0}: You know how I'm filled with rage?",
"{0}: My dad loved us. He just didn't care much about our general happiness or self-esteem.",
"{0}: \"2029?\" That's not a real year.",
"{0}: I will pepper in the fact that I am gay,",
"{0}: Well, here goes nothing. You ever seen a ghost?",
"{0}: I yelled, \"Fuck the police!\"",
"{0}: I just wanna sit here and feed my birds.",
"{0}: And I said \"no\"... You know, like a liar.",
"{0}: First off, get out of here with your facts.",
"{0}: I also don't want me to be doing what I'm doing.",
"{0}: That's what I thought you'd say, you dumb fucking horse.",
"{0}: And I said, \"I think Emily Dickinson's a lesbian,\" and they're like, \"Partial credit.\" And that's a whole thing.",
"{0}: I always thought that quicksand was gonna be a much bigger problem than it turned out to be."
]

templates = {
    "quotes": quotes,
    "mulaney": mulaney
}

def random_template(category: str, character_list: Dict[str, List[str]]) -> Union[str, Image]:
    if category not in templates:
        category = "quotes"
    if type(templates[category]) == dict:
        source = random.choice(list(templates[category].keys()))
    elif type(templates[category]) == list:
        source = random.choice(templates[category])

    if category in ("quotes","mulaney"):
        
        template_text = source.strip()

        if category == "quotes":
            num_characters = templates[category][source]
        else:
            num_characters = 1

        character_names = [random.choice(list(character_list.keys())) for _ in range(num_characters)]

        return template_text.format(*character_names).replace("\n","<br/>")
    