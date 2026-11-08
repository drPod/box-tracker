# Build the trainer box (about 30 minutes, household stuff only)

You are building a cardboard "belly" with 3 holes. Sticks poked through the holes are your
instruments. A Raspberry Pi camera above the box watches coloured bands on the sticks and
moves the virtual instruments in the headset. Inside the box, a sponge and a water bag give
you something to touch.

All distances are in centimetres. "Right/left" and "near/far" are as seen standing at
the side of the box where you will work (the **near edge**).

## What to grab

- A cardboard box with a lid (or flaps you can tape flat). The lid must be **at least 26 × 21 cm**,
  and the box at least **14 cm deep**. A boot box or a small delivery box works.
- **3 sticks, about 30 cm long**: long cooking chopsticks, or wooden kebab skewers with the
  sharp point snipped off and taped over, or two pencils taped end to end (overlap 3 cm).
  Normal chopsticks (23 cm) work too, but you will get less depth (see step 4).
- Markers or coloured tape in **3 strong colours: blue, green and red** (pink or orange can
  stand in for red). Avoid yellow, brown and skin-like colours. Wide marker or tape is best.
- A sheet of plain white paper (or two) and tape.
- A ruler, a pen, a craft knife or scissors, a pencil to poke holes.
- Inside the box: a kitchen sponge (the liver), a small ziploc bag or balloon half filled with
  water (the gallbladder), 2 drinking straws (the ducts), and cling film (the fat).
- To hold the camera: a mug or a stack of books, and tape (masking tape or sticky tape).
- Optional: a USB keyboard plugged into the Pi, put on the floor (foot pedal for cautery).

## Steps

### The lid

1. **Cover the lid with white paper.** Tape a sheet of plain white paper over the top of the lid
   so the camera sees a clean white background. Brown cardboard and print confuse the colours.
2. **Draw the centre cross.** Find the middle of the lid. Draw a line through it from left to
   right (as you stand at the near edge) and a second line from near to far. Where they cross is
   the **centre**.
3. **Mark the 4 points.** From the centre, measure along the left/right line first, then towards
   the far edge (positive) or the near edge (negative):

   | Mark | What it is | Left/right from centre | Far/near from centre |
   |---|---|---|---|
   | **U** | camera port, just a dot (no hole) | 1 cm **left** | 8 cm **near** |
   | **R** | hole for your **left** hand (blue stick) | 9.5 cm **left** | 7.5 cm **far** |
   | **L** | hole for your **right** hand (green stick) | 6.5 cm **right** | 4.5 cm **near** |
   | **A** | assistant hole (red stick) | 10 cm **right** | 6.5 cm **far** |

   Write the letters next to the marks, big and clear. Colour the **U** dot black (thumb-nail size).
   (The letters R and L are the simulator's names for those ports. The simulator draws the R tool
   on the left of the screen, so you hold it with your left hand. That is on purpose.)
4. **Make the holes.** At R, L and A, poke a hole with a pencil, then widen it so the stick slides
   and pivots easily but does not flop. About 1 cm across is right. Poking with a pencil instead of
   cutting keeps the edge snug, like a real trocar.

### The sticks

5. **Mark the sticks.** Measure from the **top end** (the end you hold). Each band goes all the
   way round the stick and is **1.5 cm tall**. Use tape wrapped 2 or 3 times, or colour it solid
   with marker.

   | Band | From the top end | What it does |
   |---|---|---|
   | **Jaw band** | 0 to 1.5 cm, and colour the flat top end too | thumb on it = jaws close |
   | (grip here) | 1.5 to 7 cm, leave bare | where your fingers go |
   | **Band 1** | 8 to 9.5 cm | tracking |
   | **Band 2** | 13 to 14.5 cm | tracking |

   Stick colours: **blue** stick goes in hole R, **green** in hole L, **red** in hole A.
   The two tracking bands must be exactly **5 cm apart** (centre to centre). Keep the bottom
   part plain. Measure your stick's total length and write it down; calibration asks for it.
   If your sticks are only 23 cm, make the same bands. You can then go only about 8 cm into the
   box, so raise the sponge (step 8) until you can reach it.
6. **How to hold a stick:** like a syringe. Fingers on the bare grip zone, thumb resting on top.
   **Press your thumb on the top end to close the jaws**, lift it off to open them. Keep your
   fingers off the two tracking bands.

### Inside the box (touch only; the headset shows the real anatomy)

Measure positions on the **underside of the lid** using the same centre cross, then measure down.

7. **Liver = sponge.** Put the sponge under the left half of the lid. Its middle should sit
   about 3 cm left of centre and 3 cm far, and its top surface **10 cm below the lid**. Prop it up on
   books, cups or folded cardboard to get the height right. A big sponge is good: the virtual liver
   is about 16 cm wide and 15 cm deep.
8. **Gallbladder = water bag.** Tape the half-filled ziploc or balloon on top of the sponge,
   with its centre right under the lid centre and 4 cm far. It runs about 9 cm from near to far
   (narrow end, the neck, towards the near edge). Its top should be about **9.5 cm below the lid**.
9. **Ducts = straws.** Lay one straw from the gallbladder's near end diagonally towards near-left
   (about 4 cm long), and a second straw from 6 cm left and 3.5 cm far down to 3 cm left and
   8 cm near, both about 12 cm below the lid, resting on the sponge.
10. **Fat = cling film.** Lay a loose layer of cling film over the straws and the gallbladder neck.
11. Close the lid and tape it so it does not shift. Stick each stick through its hole.

### The camera

12. **Place the camera on the far side of the box** (opposite you), looking down at the lid from
    about **45 cm above the lid**, set back about **15 to 20 cm** past the far edge. Tape the camera
    board flat against a mug sitting on a stack of books, or tape it to the end of a ruler that
    sticks out from the top of a book stack. The Pi sits on the books next to it.
    Point it so the **whole lid fills most of the picture** and the sticks stand up against the
    white lid, not against the room. The debug page (step 14) shows what it sees.
13. Light: room lights on, no direct sun on the box, no strong shadow across the lid.

### Calibrate (5 minutes, guided on screen)

14. On a laptop or phone on the same network, open **http://<pi-address>:8080** (the debug page).
    On the Pi, run `boxtracker calibrate` (or press **Calibrate** on the page) and follow the steps:
    1. *Focus*: hold still, press **Focus**.
    2. *Lens (optional)*: open `http://<pi-address>:8080/checker` on a phone, set brightness to full,
       and slowly wave the phone around in front of the camera until the counter reaches 15.
       You can skip this, the built-in lens values are good enough to start.
    3. *Lid*: click the **U, R, L, A** marks on the camera picture, in that order.
    4. *Colours*: put all 3 sticks in their holes, then click band 1 and band 2 of the
       **blue**, **green**, then **red** stick.
    5. *Jaw*: hold each stick with your thumb off, press **Open**, then thumb on, press **Closed**.
15. Done. The tracker now streams to the simulator by itself, and also every time the Pi boots.
    Cautery: press **F** on the Pi's keyboard (put it on the floor and press with your foot) or on
    the debug page.
