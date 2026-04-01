# Speech Script: MIN-E-630 Final Presentation

**Presenter:** Jinpeng Zhu  
**Duration:** 15 minutes  
**Course:** Underground Mining and Bulk Materials Handling (MIN-E 630)  
**Instructor:** Professor Wei Victor Liu

---

## Opening [~2 min]

Good morning/afternoon, everyone.

My name is Jinpeng Zhu. I'm a graduate student in Civil and Environmental Engineering at the University of Alberta.

Today, I will present my term paper on **sensing technologies for cementitious ground support in underground mining**.

This course is called "Underground Mining and Bulk Materials Handling," taught by Professor Wei Victor Liu.

---

## Agenda [~1 min]

I will cover three main parts:

**First**, my term paper — the motivation, key findings, and takeaways.

**Second**, what I learned from writing this paper and from this course.

**Third**, insights and gains from my learning experience.

Let's begin with the background.

---

## Part 1: Background & Motivation [~3 min]

### Why did I choose this topic?

When mines go deeper, they face three big problems:

1. **High stress** — The rock pushes hard from all sides.
2. **High temperature** — It gets hot underground.
3. **Complex water** — Groundwater flows in and causes damage.

Under these conditions, the ground support — the things that keep tunnels safe — becomes very important.

### What is cementitious support?

These are materials made with cement:

1. **Shotcrete** — Concrete sprayed onto tunnel walls. Like painting with concrete using a machine.
2. **Cast-in-place linings** — Concrete poured into forms to build walls and shafts.
3. **Cemented backfill** — A mixture of tailings (waste rock) and cement. Fills empty spaces to support walls.
4. **Grouted bolts** — Long bolts held in place by cement grout. They anchor the rock together.

These four types are used everywhere in underground mining. They are the backbone of safety.

### The challenge

Cementitious support changes over time:

- At first, it's soft like soup (fresh state)
- Then it hardens (hardening)
- Later, it ages, cracks, and degrades (aging)

We can't see inside the rock to check if everything is okay. That's why we need sensors.

---

## Part 2: Key Message [~2 min]

**My paper does three things:**

1. **Frames the problem** — Organized cementitious support monitoring into **five lifecycle phases**. Each phase asks different questions and needs different answers.

2. **Links variables to decisions** — Connected what we measure (temperature, strain, cracking) to what we decide (can we re-enter? should we reinforce? is it safe?).

3. **Identifies the bottleneck** — The hardest part is not the sensors. It's making all the data work together. Communication, data fusion, analysis, and decision-making — that's where we need more work.

---

## Part 3: Five Lifecycle Phases [~4 min]

### Phase I — Hours to Days (Placement and Early Age)

**Questions:** When can workers go back in? Did we place it well? Is the thickness correct?

**We measure:** Temperature → estimate strength (maturity method)

*Simple example: Like baking bread — it's done when it reaches a certain temperature.*

---

### Phase II — Days to Weeks (Early Service)

**Questions:** Is it carrying the load? Are we seeing early cracks?

**We measure:** Strain and stress

*Simple example: When you lean on a table, it bends a little. Strain sensors tell us how much the support is bending.*

---

### Phase III — Months to Years (Long-term Degradation)

**Questions:** Is it creeping? Is it corroding? When should we maintain or reinforce?

**We measure:** Deformation over time, corrosion indicators

*Simple example: Like a bridge that slowly sags over decades. We track this over time.*

---

### Phase IV — Dynamic Events (Blasting and Seismic)

**Questions:** What happened during the event? Did it cause damage?

**We measure:** High-frequency signals (acoustic emission, microseismic)

*Simple example: Like a car crash. The impact happens in milliseconds. Regular sensors are too slow.*

---

### Phase V — Post-event Assessment

**Questions:** What changed? Should we repair, reinforce, or abandon?

**We measure:** Geometry, cracks, internal defects (LiDAR, photogrammetry, radar)

*Simple example: Like a doctor using an X-ray to see inside.*

---

## Part 4: Technology Selection [~3 min]

### Six Main Technology Groups

| Technology | What it measures | Example |
|------------|------------------|---------|
| Thermal/Maturity | Temperature → strength | Thermocouples |
| Mechanical | Stress, strain | Strain gauges |
| Deformation | Movement, displacement | Extensometers |
| Wave-based | Cracks, damage | Acoustic emission |
| Durability | Corrosion, chemistry | Resistivity sensors |
| Geometry | Shape, size | LiDAR scanning |

**No single technology can do everything.** We must combine them based on the phase and the question.

### Selection Process

1. Define goals — What do we want to know?
2. Assess constraints — What's the environment like?
3. Screen technologies — Which sensors match our needs?
4. Pilot test — Try it on-site before full deployment.

---

## Part 5: System Integration [~3 min]

### Key Point

**The sensors are not the hard part. Integration is the hard part.**

### Why integration is difficult

1. **Constrained communications**
   - No GPS underground
   - Complex tunnel geometry
   - Metal and water block signals

2. **Heterogeneous data**
   - Point sensors give single numbers
   - Distributed sensors give lines of data
   - Visual sensors give images
   - Acoustic sensors give sound data

3. **Complex analysis**
   - Decision-making needs comprehensive understanding
   - We need to look at the big picture, not just one sensor

*Simple example: Your car shows "low tire pressure" and "engine hot." These might be related, but one sensor can't tell you that. You need a system that connects the dots.*

---

## Part 6: Challenges & Future [~3 min]

### Challenge 1: Sensor Longevity

Sensors must survive:
- Water and humidity
- Blasting vibration
- Installation damage
- Chemical attack from groundwater

In underground mining, the support lasts for years. But sensors often fail after months. This is a major problem.

### Challenge 2: From Monitoring to Control

Most mines collect data but don't use it for decisions. They rely on experience and habit.

We need smarter models that connect sensing data to actions:
- IF (strain > threshold) THEN (trigger alert)

But the rules are not clear. The industry also lacks motivation — they only do what regulations require.

### Challenge 3: Self-Assessment and Self-Decision

In the future, systems should check themselves and make basic decisions without human help:

1. Detects abnormal strain
2. Runs a quick analysis
3. Sends an alert to the right person
4. Logs the event for future reference

This is possible with AI and automation. It's the direction of the future.

---

## Part 7: Learning from This Course [~3 min]

### Six Lessons I Learned

1. **Writing is not easy** — Good writing needs good ideas. Input first, output second.

2. **Support matters** — Professor Liu and the university provided resources. Use them. Ask questions.

3. **Knowledge comes from many places** — Important knowledge comes from discussions, from reading papers, from talking to others.

4. **Industry practice is not always right** — Understand the theory behind the practice. Then make your own judgment.

5. **Challenge the status quo** — Question things that don't make sense. Don't accept just because everyone else does.

6. **Focus on the target, not the engine** — Don't upgrade for the sake of upgrading. Know your goal. Know your environment. Then choose the right tool.

---

## Closing [~30 sec]

**Thank you for your attention.**

To summarize:

- Sensing technologies are essential for underground mining safety.
- No single sensor works for all situations.
- The real challenge is system integration — making data useful for decisions.
- The future is automation and self-assessment.

I welcome your questions.

---

## Timing Guide

| Section | Time |
|---------|------|
| Opening | 2 min |
| Agenda | 1 min |
| Background & Motivation | 3 min |
| Key Message | 2 min |
| Five Lifecycle Phases | 4 min |
| Technology Selection | 3 min |
| System Integration | 3 min |
| Challenges & Future | 3 min |
| Learning from Course | 3 min |
| Closing | 30 sec |
| **Total** | **~15 min** |

---

## Notes

Use this space for your personal notes:







