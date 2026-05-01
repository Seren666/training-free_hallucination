# COCO-CHAIR First-Logit Full Confirmation

> Date: 2026-05-02
> Status: full paired confirmation completed

## 1. Experiment Status

This run is complete.

- dataset: `COCO val2014`
- evaluated image count: `40504`
- caption model: `LLaVA-1.5-7B`
- evaluator: `Python3 adapted CHAIR-style evaluator`
- setting:
  - `faithful later-step first-logit adaptation`
  - not an official COCO-CHAIR reproduction script
  - not an official FLB COCO-CHAIR script
  - `The effect` not used
  - first generated token unchanged
  - fixed `gamma=0.3`
  - fixed `lambda=0.05`
  - fixed `cd_beta=0.1`
  - prompt unchanged:
    `Please describe the image.`
  - decoding unchanged:
    greedy / deterministic

## 2. Integrity Audit

The post-run consistency audit passes.

- `regular_caption_full.json` contains `40504` samples
- `first_logit_caption_full.json` contains `40504` samples
- both final json files have `40504` unique `image_id`s
- no duplicate `image_id`s were found in either final json
- no missing `image_id`s were found relative to the full COCO image list
- `regular` and `first_logit` use the same `image_id` set
- `regular` and `first_logit` also keep the same image order
- paired evaluation is therefore based on the same image list
- `metrics.csv` value `images=40504` is credible

### 40404 vs 40504

The `40404` count in the `*_full_resume.jsonl` files is expected and does not mean missing samples.

- bootstrap prefix:
  - the first `100` images came from `regular_caption_100.json` / `first_logit_caption_100.json`
- shared resumable work file:
  - the same `work/*.jsonl` file was reused across stage `500`, stage `1000`, and stage `full`
- cumulative logic:
  - stage `500` adds `400`
  - stage `1000` adds `500`
  - stage `full` adds `39504`
  - total in resume jsonl:
    `400 + 500 + 39504 = 40404`
- final full json merges:
  - bootstrap `100`
  - cumulative resume `40404`
  - final total:
    `40504`

This is also consistent with final metadata:

- `completed_before_run = 1000`
- `generated_this_run = 39504`

That metadata describes the `full` stage only, while the final `resume jsonl` is cumulative across earlier prefix stages plus the full stage.

## 3. Main Full Metrics

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 40504 | 0.2037 | 0.0655 | 49.6823 | 181268 | 11875 | 1.2956 |
| first_logit | 40504 | 0.1631 | 0.0513 | 50.9320 | 187440 | 9609 | 1.2897 |

Full delta vs regular:

- `CHAIRs`: `-0.0406`
- `CHAIRi`: `-0.0142`
- `Avg Caption Length`: `+1.2497`
- `Object Mentions`: `+6172`
- `Hallucinated Object Count`: `-2266`
- `s/sample`: `-0.0059`

## 4. 500 / 1000 / Full Trend

| Stage | Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count |
|---|---|---:|---:|---:|---:|---:|---:|
| 500 | regular | 500 | 0.1880 | 0.0561 | 49.8000 | 2280 | 128 |
| 500 | first_logit | 500 | 0.1440 | 0.0429 | 51.0380 | 2356 | 101 |
| 1000 | regular | 1000 | 0.2090 | 0.0657 | 49.6580 | 4522 | 297 |
| 1000 | first_logit | 1000 | 0.1610 | 0.0509 | 50.9190 | 4717 | 240 |
| full | regular | 40504 | 0.2037 | 0.0655 | 49.6823 | 181268 | 11875 |
| full | first_logit | 40504 | 0.1631 | 0.0513 | 50.9320 | 187440 | 9609 |

| Stage | CHAIRs delta | CHAIRi delta | Length delta | Object mentions delta | Hallucinated object delta |
|---|---:|---:|---:|---:|---:|
| 500 | -0.0440 | -0.0132 | +1.2380 | +76 | -27 |
| 1000 | -0.0480 | -0.0148 | +1.2610 | +195 | -57 |
| full | -0.0406 | -0.0142 | +1.2497 | +6172 | -2266 |

Trend summary:

- the positive `CHAIRs` gain persists from `100` to `500`, `1000`, and `full`
- the positive `CHAIRi` gain also persists at all observed scales
- the gain does not disappear when moving from prefix evaluation to the full `40504` image set

## 5. Paired Behavior Summary

Full paired statistics:

- total paired images:
  - `40504`
- changed caption count:
  - `40499`
- unchanged caption count:
  - `5`
- exact unchanged caption ids:
  - `185292`, `193041`, `272728`, `484695`, `531327`
- first word changed count:
  - `0`
- improved image count:
  - `5066`
- worsened image count:
  - `3287`
- no-delta stable count:
  - `32151`
- regular hallucinated object count:
  - `11875`
- first_logit hallucinated object count:
  - `9609`
- hallucinated object delta:
  - `-2266`
- avg caption length delta:
  - `+1.2497`
- object mentions delta:
  - `+6172`

Per-image mention and length movement:

- images where object mentions decreased:
  - `11788`
- images where object mentions increased:
  - `15539`
- images where object mentions stayed the same:
  - `13177`
- images where caption got much shorter:
  - `22`
  - threshold used here:
    at least `10` whitespace tokens shorter
- images where caption got much longer:
  - `184`
  - threshold used here:
    at least `10` whitespace tokens longer

### Is the gain coming from shorter captions?

Current answer:

- no

Evidence:

- full average caption length increases by `+1.2497`
- only `22 / 40504` images become at least `10` tokens shorter
- `184 / 40504` images become at least `10` tokens longer
- among improved images:
  - `3178` got longer
  - `1288` got shorter
  - `600` had the same token length

So the full COCO-CHAIR improvement is not explained by caption shortening.

### Is the gain coming from fewer object mentions?

Current answer:

- not as a global suppression effect

Evidence:

- total object mentions increase by `+6172`
- more images increase object mentions (`15539`) than decrease them (`11788`)
- among improved images:
  - `3115` have fewer object mentions
  - `802` have more object mentions
  - `1149` stay equal
- among worsened images:
  - `2248` have more object mentions
  - `373` have fewer object mentions

Interpretation:

- many improved cases do remove some object mentions locally
- but the full-run gain is not explained by a blanket reduction in mention frequency
- the direction looks more like lexical reallocation / content steering than global suppression

### Does the first word stay unchanged?

Current answer:

- yes

Evidence:

- first word changed count:
  - `0 / 40504`

This is consistent with the intended later-step-only adaptation.

## 6. Hallucination Vocabulary Shift

Most frequent hallucinated objects in `regular`:

- `dining table` `1754`
- `person` `1145`
- `chair` `703`
- `car` `511`
- `bowl` `381`
- `sink` `343`
- `sports ball` `335`
- `bench` `292`
- `orange` `283`
- `cup` `273`

Most frequent hallucinated objects in `first_logit`:

- `dining table` `1626`
- `chair` `581`
- `person` `435`
- `couch` `390`
- `car` `370`
- `sink` `305`
- `bowl` `289`
- `sports ball` `288`
- `orange` `254`
- `refrigerator` `233`

Top reduced hallucinated objects:

- `person` `-915`
- `dining table` `-705`
- `chair` `-444`
- `car` `-339`
- `bowl` `-249`
- `cup` `-214`
- `sink` `-203`
- `bench` `-184`
- `backpack` `-184`
- `bottle` `-178`

Top newly introduced or expanded hallucinated objects:

- `dining table` `+577`
- `chair` `+322`
- `couch` `+218`
- `person` `+205`
- `car` `+198`
- `sink` `+165`
- `refrigerator` `+131`
- `cake` `+118`
- `tv` `+111`
- `spoon` `+105`

Interpretation:

- the method clearly reduces many existing hallucinations
- it also introduces new hallucinations in some categories
- the profile is therefore not purely conservative
- the strongest improvements seem concentrated on common over-mentioned categories such as `person`, `dining table`, `chair`, and `car`

## 7. Improved Examples

### Image 74

regular hallucinated objects:
`handbag`

first_logit hallucinated objects:
none

behavior:
removes the extra accessory mention without shortening the caption.

regular:
`The image features a white dog lying on a sidewalk, resting comfortably on the ground. The dog is positioned near a bicycle, which is leaning against a wall. The scene also includes several people walking by, with some of them carrying handbags. In the background, there`

first_logit:
`The image features a white dog lying on the sidewalk in a city street. The dog is resting on the sidewalk near a bicycle, which is parked on the left side of the scene. The street is lined with a variety of people walking in the background, creating a lively atmosphere.`

### Image 192

regular hallucinated objects:
`baseball glove`, `sports ball`

first_logit hallucinated objects:
`sports ball`

behavior:
reduces two baseball-related hallucinations down to one.

regular:
`The image captures a baseball game in progress, with a batter standing at home plate, holding a baseball bat and preparing to swing. The catcher and the umpire are also present, positioned behind the batter. The catcher is wearing a baseball glove, ready to catch the ball.`

first_logit:
`The image captures a baseball game in progress, with a baseball player in the middle of the scene, holding a baseball bat and preparing to swing at the ball. The baseball player is the main focus of the image, and the scene is set on a baseball field. In the scene, there are several`

### Image 241

regular hallucinated objects:
`chair`

first_logit hallucinated objects:
none

behavior:
removes the extra furniture mention and also reduces object mentions.

regular:
`The image depicts a group of people gathered in a living room, enjoying a video game session on a Nintendo Wii console. A man is standing in the center of the room, holding a Wii remote, while others are sitting on couches and chairs around him. There`

first_logit:
`The image depicts a group of people gathered in a living room, enjoying a video game session on a Nintendo Wii console. A man in a plaid shirt is standing in the center of the room, holding a Wii remote in his hand, while the others watch and engage in the`

### Image 257

regular hallucinated objects:
`car`

first_logit hallucinated objects:
none

behavior:
stays focused on the truck line and removes the extra vehicle mention.

regular:
`The image depicts a busy city street with a large group of people gathered around a food truck. The food truck is parked in front of a monument, and there are several other trucks and cars in the vicinity. The crowd of people is diverse, with some standing closer to the food`

first_logit:
`The image depicts a busy city street with a large group of people gathered around a food truck. The truck is parked in the middle of the scene, and the people are standing in a line, waiting to be served. The crowd is diverse, with people of various ages and genders.`

### Image 357

regular hallucinated objects:
`sports ball`

first_logit hallucinated objects:
none

behavior:
reframes the baseball scene around players and actions instead of a nonexistent ball.

regular:
`The image captures a baseball game in progress on a field. There are three baseball players in the scene, with one player holding a baseball bat, another player wearing a baseball glove, and the third player standing in the outfield. The batter is preparing to hit the ball, while the other two players`

first_logit:
`The image captures a baseball game in progress on a field. There are three baseball players in the scene, with one player in the infield, another in the outfield, and the third player in the outfield as well. The infield player is in the process of throwing the baseball to the outfield player`

### Image 428

regular hallucinated objects:
`dining table`

first_logit hallucinated objects:
none

behavior:
keeps the focus on the child and cake instead of inserting furniture.

regular:
`The image features a baby boy standing in front of a birthday cake, which is placed on a dining table. The baby is wearing a tie and appears to be enjoying the celebration. The cake is decorated with white frosting, and the baby is smiling and eating the`

first_logit:
`The image features a baby boy standing in front of a birthday cake, which is the center of attention in the scene. The baby is in the process of eating the cake, with a little bit of cake on his face. The baby is wearing a tie, adding a touch of formality`

### Image 536

regular hallucinated objects:
`couch`

first_logit hallucinated objects:
none

behavior:
removes furniture hallucination while preserving a rich description.

regular:
`The image features three women dressed in elegant evening gowns, sitting together in a room. They are all wearing pearl necklaces, adding to their sophisticated appearance. Two of the women are sitting on a couch, while the third woman is sitting on a chair. Each woman`

first_logit:
`The image features three women dressed in elegant evening gowns, sitting in a room and talking on their cell phones. The women are positioned in the center of the scene, with one woman on the left, the second woman in the middle, and the third woman on the right. The three women are the`

### Image 692

regular hallucinated objects:
`sink`

first_logit hallucinated objects:
none

behavior:
removes the nonexistent sink without shortening the description.

regular:
`The image features a woman holding a baby in a bathroom. The woman is smiling and appears to be taking a picture of the baby using a digital camera. The baby is sitting on the woman's lap, and they are both positioned in front of a sink. In the background, there is`

first_logit:
`The image features a woman holding a baby in a bathroom. The woman is smiling and the baby is brushing its teeth with a toothbrush in its mouth. The woman is holding the baby in a loving and caring manner, showcasing the bond between the two. The scene is captured`

### Image 772

regular hallucinated objects:
`person`

first_logit hallucinated objects:
none

behavior:
keeps the caption centered on sheep and the fence rather than inventing a person.

regular:
`The image features two sheep standing in a grassy field, with one sheep positioned closer to the left side of the field and the other sheep standing more towards the right side. They appear to be looking at something, possibly a camera or a person. The sheep are standing behind a fence, which is visible in`

first_logit:
`The image features two sheep standing in a grassy field, with a fence in the background. The sheep are positioned close to the fence, and they appear to be looking in the same direction. The scene is set in a lush green field, providing a natural and serene environment for the sheep.`

### Image 999

regular hallucinated objects:
`sports ball`

first_logit hallucinated objects:
none

behavior:
removes a false ball mention even though the caption becomes slightly longer.

regular:
`The image features a baseball player wearing an orange shirt and white pants, kneeling on the ground in front of home plate. The player appears to be in a crouched position, possibly preparing to catch a ball or make a play. There are two other people in the scene,`

first_logit:
`The image features a baseball player in the middle of a game, kneeling on the baseball field with his head in his hands. The player is wearing a baseball glove, and the scene captures the intensity of the game. The baseball player is the main focus in the image, with the rest of the field`

## 8. Worsened Examples

### Image 139

regular hallucinated objects:
none

first_logit hallucinated objects:
`couch`

behavior:
introduces a new living-room furniture hallucination without any length reduction.

regular:
`The image depicts a spacious and well-lit living room with a dining area. A woman is standing in the dining area, which features a dining table surrounded by chairs. There are three chairs in total, with one on the left side of the table, one on the right`

first_logit:
`The image depicts a spacious and well-lit living room with a dining area. The dining table is surrounded by several chairs, and the room features a TV on the left side. The living room is furnished with a couch and a potted plant, and the space is bright`

### Image 164

regular hallucinated objects:
none

first_logit hallucinated objects:
`sink`

behavior:
adds kitchen fixtures that are not supported by the image.

regular:
`The image depicts a small, cluttered kitchen with a white refrigerator and a microwave oven. The kitchen is filled with various items, including numerous bottles, cups, and bowls. There are at least 13 bottles scattered throughout the kitchen, with some placed`

first_logit:
`The image depicts a small, cluttered kitchen with a white refrigerator and a microwave oven. The kitchen is filled with various items, including a dining table, a chair, and a sink. The table is set with a variety of dishes, cups, and a`

### Image 196

regular hallucinated objects:
none

first_logit hallucinated objects:
`knife`

behavior:
adds utensil detail and increases object mentions.

regular:
`The image features a wooden dining table filled with a variety of foods, including several pies, casseroles, and salads. There are multiple bowls placed on the table, containing different types of food. Some of the bowls are filled with salad, while others contain casseroles or other`

first_logit:
`The image features a wooden dining table filled with a variety of food dishes, including a large assortment of pies and casseroles. The table is set with a variety of bowls, plates, and utensils, including forks, knives, and spoons. The table is`

### Image 294

regular hallucinated objects:
none

first_logit hallucinated objects:
`toaster`, `sink`

behavior:
broadens the kitchen inventory too aggressively and creates two false objects.

regular:
`The image features a man standing in a kitchen, holding a frying pan in his hand. He is positioned in front of a wall with various pots and pans hanging on it. There are at least six pots and pans visible, with some of them being larger and others smaller.`

first_logit:
`The image features a man standing in a kitchen, holding a frying pan in his hand. The kitchen is well-equipped with a variety of utensils and cooking tools, including a microwave, a toaster, and a sink. The man is in the center of the scene, with`

### Image 338

regular hallucinated objects:
none

first_logit hallucinated objects:
`sink`

behavior:
changes scene framing and inserts an unsupported sink mention.

regular:
`The image depicts a kitchen scene with two people standing in front of a refrigerator. One person is an older man, and the other is an older woman. They are both holding clipboards, possibly taking notes or looking at recipes. The kitchen is well-equipped with various`

first_logit:
`The image depicts a kitchen scene with two people standing in the middle of the room. The kitchen is well-equipped with a refrigerator, a sink, and an oven. The two people in the kitchen are engaged in a conversation, possibly discussing the contents of the refrigerator`

### Image 395

regular hallucinated objects:
none

first_logit hallucinated objects:
`orange`

behavior:
injects a color-object mention that becomes a CHAIR error.

regular:
`The image depicts a busy city street with a man wearing a red jacket and a black hat, talking on his cell phone. He is surrounded by a crowd of people, some of whom are also engaged in conversations on their phones. The scene captures the hustle and bustle`

first_logit:
`The image depicts a busy city street with a man in an orange jacket standing in the middle of the scene, talking on his cell phone. The man is wearing a hat and appears to be the main focus of the scene. The street is bustling with people, as there are at least`

### Image 486

regular hallucinated objects:
`sink`

first_logit hallucinated objects:
`spoon`, `fork`

behavior:
replaces one hallucinated kitchen item with two different utensil hallucinations.

regular:
`The image depicts a large, well-equipped kitchen with a wooden countertop and various appliances. There is a refrigerator on the right side of the kitchen, and an oven is located on the left side. A sink can be seen in the middle of the kitchen, and a`

first_logit:
`The image depicts a large, well-equipped kitchen with a wooden counter and a stainless steel refrigerator. The kitchen is filled with various utensils and kitchenware, including a large bowl, a spoon, and a fork. The counter is lined with a variety of`

### Image 589

regular hallucinated objects:
`baseball bat`, `sports ball`

first_logit hallucinated objects:
`baseball bat`, `sports ball`, `sports ball`

behavior:
amplifies an already hallucinated baseball scene instead of correcting it.

regular:
`The image captures a man in a white shirt and khaki shorts playing baseball in a field at night. He is holding a baseball bat and appears to be in the middle of a swing, possibly attempting to hit a sports ball that is visible in the scene. The field is surrounded by a forest,`

first_logit:
`The image features a man standing in a grassy field at night, holding a baseball bat and preparing to swing at a sports ball in the air. The scene is set in a dark night, with the man being the main focus of the image. The sports ball is in the air, close to the man,`

### Image 775

regular hallucinated objects:
none

first_logit hallucinated objects:
`person`

behavior:
adds a reflected person not supported by the image.

regular:
`The image features a motorcycle parked on the side of a street, with its rearview mirror reflecting a large advertisement. The motorcycle is positioned next to a tree, and the mirror's reflection captures the attention of the viewer. In the background, there is a b`

first_logit:
`The image features a motorcycle parked on the side of the road, with a mirror reflecting the scene around it. The mirror captures the reflection of a bicycle parked in the background, as well as a person standing near the bicycle. The scene also includes a tree in the background,`

### Image 1268

regular hallucinated objects:
`bench`

first_logit hallucinated objects:
`bench`, `bench`

behavior:
duplicates an already wrong object category and worsens the hallucination count.

regular:
`The image features a man sitting on a bench near a body of water, possibly a river or a lake. He is looking at a bird that is standing on the ground nearby. The man appears to be enjoying the view of the bird and the water. There are a few other people in the scene`

first_logit:
`The image features a man sitting on a bench near a body of water, possibly a river or a lake. The man is wearing a red shirt and appears to be enjoying the view. A woman is standing nearby, taking a picture of the scene with a camera. The man on the bench is`

## 9. No-Delta Stable Examples

### Image 42

regular hallucinated objects:
none

first_logit hallucinated objects:
none

behavior:
description style changes, CHAIR outcome unchanged.

regular:
`The image features a dog lying on a shelf, surrounded by various shoes. The dog is curled up and appears to be sleeping or resting comfortably. The shoes are placed in different positions around the dog, with some on the floor and others on the shelf. The scene creates a co`

first_logit:
`The image features a dog lying on a shelf, surrounded by various shoes. The dog is in the center of the scene, with the shoes placed in a pile around it. The shoes are in different sizes and colors, and some are placed on the floor in the foreground, while others are`

### Image 73

regular hallucinated objects:
none

first_logit hallucinated objects:
none

behavior:
same object grounding, different phrasing.

regular:
`The image features an old-fashioned motorcycle parked on a street. The motorcycle is positioned in the center of the scene, with its front wheel prominently visible. The motorcycle has a vintage appearance, and it appears to be a classic model. In the background,`

first_logit:
`The image features an old-fashioned motorcycle parked on the side of the road. The motorcycle is the main focus of the scene, and it is parked in the foreground. The motorcycle is an antique, and the vintage design is evident in the black and silver color scheme`

### Image 133

regular hallucinated objects:
none

first_logit hallucinated objects:
none

behavior:
becomes more repetitive but does not create object hallucination.

regular:
`The image features a bedroom with a neatly made bed, positioned against the wall. The bed is covered with a white sheet and has a wooden headboard. A dresser is located next to the bed, with a drawer open, revealing its contents. In the room, there is`

first_logit:
`The image features a bedroom with a neatly made bed, positioned in the corner of the room. The bed is the main focus of the scene, and it is the only bed in the room. The bed is situated in the middle of the room, with the bed frame and the mattress visible.`

### Image 136

regular hallucinated objects:
none

first_logit hallucinated objects:
none

behavior:
changes feeding description without changing CHAIR result.

regular:
`The image features two giraffes in a zoo enclosure, standing next to each other and eating hay. One giraffe is positioned on the left side of the enclosure, while the other is on the right side. They are both focused on eating the hay provided for them.`

first_logit:
`The image features two giraffes in a zoo enclosure, standing next to each other and eating from a feeder. The giraffes are positioned in the center of the scene, with one giraffe on the left and the other on the right. The enclosure is a dirt`

### Image 143

regular hallucinated objects:
none

first_logit hallucinated objects:
none

behavior:
changes counting/style language but remains hallucination-free.

regular:
`The image features a group of birds perched on a tree branch in a snowy environment. There are nine birds in total, with some of them sitting closer to the top of the branch and others near the bottom. The birds are of various sizes and are spread out across the branch, creating a sense of depth in`

first_logit:
`The image features a group of birds perched on the branches of a tree in the snow. There are a total of 11 birds in the scene, with some birds sitting on the top of the tree and others on the branches. The birds are of various sizes and are scattered throughout the tree, creating a l`

### Image 208

regular hallucinated objects:
none

first_logit hallucinated objects:
none

behavior:
changes the toy animal description but not the CHAIR outcome.

regular:
`The image features a bathroom sink with a toy alligator figurine sitting on the edge of the sink. The alligator is positioned near the faucet, giving the impression that it is drinking water from the faucet. The sink is surrounded by a tan countertop, and there`

first_logit:
`The image features a bathroom sink with a toy crocodile figurine sitting on the edge of the sink. The toy is positioned in a way that it appears to be brushing its teeth, with the toothbrush in the crocodile's mouth. The sink is located in the`

### Image 283

regular hallucinated objects:
none

first_logit hallucinated objects:
none

behavior:
stylistic rewrite only, with a slight drop in object mentions.

regular:
`The image features a glass of red wine placed on a glass table, accompanied by a bottle of wine. The wine glass is positioned in the center of the table, while the bottle is located to the left side. A chair is situated near the table, inviting someone to sit and enjoy the wine.`

first_logit:
`The image features a glass of wine placed on a glass table, accompanied by a bottle of wine. The glass is positioned in the center of the table, and the bottle is located on the left side of the table. The scene is set in a dining area, with a chair placed on the right`

### Image 285

regular hallucinated objects:
none

first_logit hallucinated objects:
none

behavior:
keeps the same grounded object set while changing wording.

regular:
`The image features a large brown bear sitting on a grassy field. The bear appears to be relaxed and enjoying the outdoor environment. The bear is positioned in the center of the scene, with its body occupying a significant portion of the image. The grassy field provides a natural backdrop for the`

first_logit:
`The image features a large brown bear sitting in a grassy field. The bear is the main focus of the scene, occupying a significant portion of the image. The bear appears to be in a relaxed and comfortable position, possibly enjoying the sunshine in the outdoor environment. The grassy field provides`

### Image 328

regular hallucinated objects:
none

first_logit hallucinated objects:
none

behavior:
keeps the scene grounded and adds one extra mention without changing CHAIR.

regular:
`The image features three men dressed in military uniforms, sitting on a bench and reading books. They are all wearing ties, which adds to their formal appearance. The men are positioned in a row, with one man on the left, another in the middle, and the third on the right side of`

first_logit:
`The image features three young men dressed in military uniforms, sitting on a bench and reading a book together. The men are positioned in a row, with the first man on the left, the second in the middle, and the third on the right. The book is placed in the middle of the three men`

### Image 359

regular hallucinated objects:
none

first_logit hallucinated objects:
none

behavior:
swaps from cars to traffic lights but remains hallucination-free under the evaluator.

regular:
`The image captures a city street scene with a tall building in the background. The street is bustling with traffic, as there are multiple cars visible in the scene. One car is located on the left side of the image, another car is in the middle, and a third car is on the right side.`

first_logit:
`The image captures a city street scene with a tall building in the background. The street is lined with buildings on both sides, and the sky is cloudy, creating a somewhat gloomy atmosphere. The street is also equipped with traffic lights, with one on the left side and another on the right side of`

## 10. Final Judgment

What is supported by this full run:

- `first_logit` keeps a stable positive effect on full COCO-CHAIR
- the gain persists from `500` to `1000` to `40504`
- the gain is not explained by shorter captions
- the gain is not explained by lower overall object mention counts
- the first generated token remains unchanged
- the direction is therefore worth continuing as a serious caption-side baseline

What is not yet supported:

- this is not yet a final paper-ready method claim
- this is not yet official evaluator alignment with every external implementation detail
- the mechanism is still not selective in a strict sense because `40499 / 40504` captions changed
- there are still `3287` worsened images and new hallucination categories introduced

## 11. Recommended Next Step

Recommended next steps after this completed full confirmation:

1. do evaluator alignment and careful result presentation cleanup
2. do mechanism analysis on why later-step anchoring reduces some hallucinated categories and introduces others
3. return to `one-forward signal audit` as the analysis track
4. avoid immediate parameter sweep
5. avoid over-claiming this as the final method before mechanism and robustness checks
